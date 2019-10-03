import cv2


def main():
    resim = cv2.imread("../Resimler/test_resim.jpg")
    cv2.imshow("Resim Başlığı", resim)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()