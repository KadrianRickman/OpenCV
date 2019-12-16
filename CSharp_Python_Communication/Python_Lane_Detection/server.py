import socket
from PIL import Image
import cv2
import io
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread
import json
from laneProcessing import ImageProcessing, ControlDecision


UDP_IP = "127.0.0.1"
UDP_PORT = 5557
CONTROL_UDP_PORT = 5559

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

controlSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
controlSocket.bind((UDP_IP, 5553))

transmitData = {
    "steeringAngle": 30,
    "direction": 0,
    "motorForce": 400,
    "verticalValue": 1
}

imageProcessing = ImageProcessing()
controlDecision = ControlDecision(transmitData)
   
def sendControlMessage(message):
    controlSocket.sendto(message, (UDP_IP, CONTROL_UDP_PORT))


def byteArrayToCv2Image(byteArray):
    image = Image.open(io.BytesIO(byteArray))
    #image.save("aaaaa.png")
    opencvImg = np.array(image)
    opencvImg = opencvImg[:, :, ::-1].copy()  
    return opencvImg



#starting
print("Server started")
while True:
    try:
        data, addr = sock.recvfrom(65535)
        frame = byteArrayToCv2Image(data)

        imageProcessing.setImage(frame)
        cannyImage = imageProcessing.canny()
        roi = imageProcessing.regionOfInterest(cannyImage)
        lines = cv2.HoughLinesP(roi, 1, np.pi / 180, 60, None, 10, 10)
        averagedLines = imageProcessing.averageSlopeIntercept(lines)
        lineImage, diff = imageProcessing.showLines(averagedLines)
        comboImage = cv2.addWeighted(frame, 0.7, lineImage, 0.3, 1)
        
        cv2.imshow('Region of Interest', roi)
        cv2.imshow('Combo Image', comboImage)

        data = controlDecision.laneTrackingDecision(diff)
        print("data:", data)
        sendControlMessage(data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  
    except:
        print("Error")

cv2.destroyAllWindows()
