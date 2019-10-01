import cv2


resim_1 = cv2.imread('../Resimler/the_100.jpg')

cv2.rectangle(resim_1, (80, 200), (150, 20), [0, 0, 255], 2)
cv2.rectangle(resim_1, (320, 200), (420, 50), [0, 0, 255], 2)

cv2.imshow('The 100 Resmi', resim_1)
cv2.waitKey(0)
cv2.destroyAllWindows()