import cv2


resim_1 = cv2.imread('../Resimler/the_100.jpg')


cv2.imshow("Orijinal Resim", resim_1)

#resim_1[:,:, 1] = 255
resim_1[100:200,100:200,2] = 255

cv2.imshow("Renklendirilmis Resim", resim_1)

cv2.waitKey(0)
cv2.destroyAllWindows()