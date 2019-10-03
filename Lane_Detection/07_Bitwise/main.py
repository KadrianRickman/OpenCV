import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(resim):
    resim_gray = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    resim_blur = cv2.GaussianBlur(resim_gray, (5, 5), 0)
    resim_canny = cv2.Canny(resim_blur, 50, 150)
    return resim_canny

def bolge_secimi(resim):
    yukseklik = resim.shape[0]
    polygons = np.array([[(200, yukseklik), (1100, yukseklik), (550, 250)]])
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
    print(line_parameters)
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
        print(parameters)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average  = np.average(left_fit,  axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(resim, left_fit_average)
    right_line = make_coordinates(resim, right_fit_average)
    return np.array([left_line, right_line])

"""
resim_bgr = cv2.imread("../Resimler/test_resim.jpg")
resim_bgr_kopya = np.copy(resim_bgr)
canny = canny(resim_bgr_kopya)
secilen_bolge = bolge_secimi(canny)
lines = cv2.HoughLinesP(secilen_bolge, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average_slope_intercept(resim_bgr_kopya, lines)
line_image = line_goruntule(resim_bgr_kopya, averaged_lines)
combo_image = cv2.addWeighted(resim_bgr_kopya, 0.8, line_image, 1, 1)

cv2.imshow("Resim Ucgen", combo_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""

kamera = cv2.VideoCapture("../Videolar/test_video.mp4")
while kamera.isOpened():
    ret, frame = kamera.read()

    canny_image = canny(frame)
    secilen_bolge = bolge_secimi(canny_image)
    lines = cv2.HoughLinesP(secilen_bolge, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = line_goruntule(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("Frame", combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
kamera.release()
cv2.destroyAllWindows()







