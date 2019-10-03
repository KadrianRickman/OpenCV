import cv2
import numpy as np


def main():
    resim_bgr = cv2.imread("../Resimler/test_resim.jpg")
    resim_bgr_kopya = np.copy(resim_bgr)
    resim_gray  = cv2.cvtColor(resim_bgr_kopya, cv2.COLOR_BGR2GRAY)
    resim_blur  = cv2.GaussianBlur(resim_gray, (5, 5), 0)
    resim_canny = cv2.Canny(resim_gray, 50, 150)

    cv2.imshow("BGR Resim", resim_bgr)
    cv2.imshow("Gray Resim", resim_gray)
    cv2.imshow("Blur Resim", resim_blur)
    cv2.imshow("Canny Resim", resim_canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()