import socket
from PIL import Image
import cv2
import io
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread
import json


class ImageProcessing:
    def __init__(self, image = ''):
        self.image = image

    def setImage(self, image):
        self.image = image
    
    def getImage(self):
        return self.image

    def canny(self):
        grayImage  = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurImage  = cv2.GaussianBlur(grayImage, (5, 5), 0)
        cannyImage = cv2.Canny(blurImage, 50, 150)
        return cannyImage
    
    def regionOfInterest(self, image):
        height = image.shape[0]
        width  = image.shape[1]
        #polygons = np.array([[(0, height - 10), (width // 2, 60), (width, height - 10)]])
        polygons = np.array([[(0, height), (0, height - 30), (width // 2 - 40, height // 2 - 40), (width, height - 40), (width, height)]])
        mask = np.zeros_like(image)
        cv2.fillPoly(mask, polygons, 255)
        maskedImage = cv2.bitwise_and(image, mask)
        return maskedImage

    def showLines(self, lines):
        lineImage = np.zeros_like(self.image)
        height = self.image.shape[0]
        width  = self.image.shape[1]
        diff = 0
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                cv2.line(lineImage, (x1, y1), (x2, y2), (255, 0, 0), 6)
            if len(lines) == 2:
                line1X2 = lines[0][2]
                line2X2 = lines[1][2]
                x = (line1X2 + line2X2) // 2
                if x > width:
                    x = width // 2 + 15
                elif x < 0:
                    x = width // 2 - 15
                diff = x - width // 2
                cv2.line(lineImage, (x, height - 40), (x, height - 30), (0, 255, 0), 4)
                cv2.line(lineImage, (width // 2, height - 30), (x, height - 30), (0, 255, 0), 4)
        cv2.line(lineImage, (width // 2, height - 30), (width // 2, height), (0, 255, 0), 4)
        return lineImage, diff
    
    def makeCoordinates(self, line_parameters):
        slope, intercept = line_parameters  
        y1 = self.image.shape[0]
        y2 = int(y1 * (3 / 5))
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        return np.array([x1, y1, x2, y2])

    def averageSlopeIntercept(self, lines):
        leftFit  = []
        rightFit = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                leftFit.append((slope, intercept))
            else:
                rightFit.append((slope, intercept))
        if len(leftFit) == 0:
            leftFit.append((-0.01, 1))
        if len(rightFit) == 0:
            rightFit.append((0.01, 1))

        leftFitAverage  = np.average(leftFit,  axis = 0)
        rightFitAverage = np.average(rightFit, axis = 0)
        leftLine  = self.makeCoordinates(leftFitAverage)
        rightLine = self.makeCoordinates(rightFitAverage)
        return np.array([leftLine, rightLine])

    def scaledImage(self, scale, img):
        width  = int(img.shape[1] * scale / 100)
        height = int(img.shape[0] * scale / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        return resized

class ControlDecision:
    
    def __init__(self, transmitData):
        self.transmitData = transmitData
    
    def laneTrackingDecision(self, diff):
        if diff > 4:
            self.transmitData["direction"] = "r"
        elif diff < -4:
            self.transmitData["direction"] = "l"
        else:
            self.transmitData["direction"] = "d"
        diff = abs(int(diff))
        if diff > 12:
            self.transmitData["steeringAngle"] = 20
        else:
            self.transmitData["steeringAngle"] = diff * 2

        if diff > 14:
            self.transmitData["motorForce"] = 90
        if diff > 10:
            self.transmitData["motorForce"] = 50
        elif diff > 5:
            self.transmitData["motorForce"] = 80
        else:
            self.transmitData["motorForce"] = 120
        return self.jsonToByteArray(self.dictToJson(self.transmitData))

    def dictToJson(self, dict_object):
        return json.dumps(dict_object)

    def jsonToByteArray(self, json_data):
        return json_data.encode()