import cv2

"""
-imread: dosyadan resim okumak icin kullanilir.
-ilk parametre okunacak resmin yolu(path)
"""
resim = cv2.imread('../Resimler/the_100.jpg')
#resim = cv2.imread('../Resimler/the_100.jpg', 0)

cv2.imshow('The 100 Resmi', resim)
cv2.waitKey(0)
cv2.destroyAllWindows()