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
    return maske

resim_bgr = cv2.imread("../Resimler/test_resim.jpg")
resim_bgr_kopya = np.copy(resim_bgr)
canny = canny(resim_bgr_kopya)
secilen_bolge = bolge_secimi(canny)


cv2.imshow("Resim Canny", canny)
cv2.imshow("Resim Ucgen", secilen_bolge)

cv2.waitKey(0)
cv2.destroyAllWindows()