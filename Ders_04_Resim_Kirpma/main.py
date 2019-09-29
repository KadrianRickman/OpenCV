import cv2

resim = cv2.imread('../Resimler/the_100.jpg')

#y1:y2,x1:x2
resim = resim[20:200, 50:200]

cv2.imshow('The 100 Resmi', resim)
cv2.waitKey(0)
cv2.destroyAllWindows()