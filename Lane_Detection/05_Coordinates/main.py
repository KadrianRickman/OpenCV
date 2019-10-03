import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    resim_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resim_blur = cv2.GaussianBlur(resim_gray, (5, 5), 0)
    resim_canny = cv2.Canny(resim_blur, 50, 150)
    return resim_canny

resim_bgr = cv2.imread("../Resimler/test_resim.jpg")
resim_bgr_kopya = np.copy(resim_bgr)
canny = canny(resim_bgr_kopya)

plt.imshow(canny)
plt.show()