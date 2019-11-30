import socket
from PIL import Image
import cv2
import io
import numpy as np
import matplotlib.pyplot as plt

UDP_IP = "127.0.0.1"
UDP_PORT = 5557

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def byte_array_to_cv2_image(byte_array):
    image = Image.open(io.BytesIO(byte_array))
    #image.save("aaaaa.png")
    opencv_img = np.array(image)
    opencv_img = opencv_img[:, :, ::-1].copy()  
    return opencv_img

def canny(resim):
    resim_gray = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    resim_blur = cv2.GaussianBlur(resim_gray, (5, 5), 0)
    resim_canny = cv2.Canny(resim_blur, 50, 150)
    return resim_canny

def bolge_secimi(resim):
    yukseklik = resim.shape[0]
    genislik  = resim.shape[1]
    polygons = np.array([[(0, yukseklik - 30), (128, 40), (genislik, yukseklik - 30)]])
    maske = np.zeros_like(resim)
    cv2.fillPoly(maske, polygons, 255)

    maskelenmis_resim = cv2.bitwise_and(resim, maske)
    return maskelenmis_resim

def line_goruntule(resim, lines):
    line_image = np.zeros_like(resim)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def make_coordinates(resim, line_parameters):
    slope, intercept = line_parameters

    y1 = resim.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(resim, lines):
    left_fit  = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    if len(left_fit) == 0:
        left_fit.append((-0.0001, 1))
    if len(right_fit) == 0:
        right_fit.append((0.0001, 1))

    left_fit_average  = np.average(left_fit,  axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(resim, left_fit_average)
    right_line = make_coordinates(resim, right_fit_average)
    return np.array([left_line, right_line])


#starting
print("Server started")
while True:
    try:
        data, addr = sock.recvfrom(200000) # buffer size is 200k bytes
        frame = byte_array_to_cv2_image(data)
        #cv2.imshow('Normal', frame)
        canny_image = canny(frame)
        cv2.imshow('Canny', canny_image)
        
        secilen_bolge = bolge_secimi(canny_image)
        #cv2.imshow('Bolge', secilen_bolge)
        
        lines = cv2.HoughLinesP(secilen_bolge, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
        averaged_lines = average_slope_intercept(frame, lines)
        
        line_image = line_goruntule(frame, averaged_lines)
        #cv2.imshow('Line Resim', line_image)
        
        combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        cv2.imshow('Arac On Kamera', combo_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("hata")
cv2.destroyAllWindows()
