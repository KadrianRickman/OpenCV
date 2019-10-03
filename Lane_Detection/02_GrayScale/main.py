import cv2
import numpy as np

def main():
    resim_bgr = cv2.imread("../Resimler/test_resim.jpg")
    resim_bgr_kopya = np.copy(resim_bgr)
    resim_gray = cv2.cvtColor(resim_bgr_kopya, cv2.COLOR_BGR2GRAY)

    cv2.imshow("BGR Resim", resim_bgr)
    cv2.imshow("Gray Resim", resim_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()