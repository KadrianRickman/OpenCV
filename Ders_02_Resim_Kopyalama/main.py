import cv2


resim_1 = cv2.imread('../Resimler/the_100.jpg')
resim_2 = cv2.imwrite('../Resimler/yeni_resim.png', resim_1)

cv2.imshow('The 100 Resmi', resim_1)
cv2.waitKey(0)
cv2.destroyAllWindows()