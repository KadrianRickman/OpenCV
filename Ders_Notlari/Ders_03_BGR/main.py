import cv2

resim = cv2.imread('../Resimler/the_100.png', 0)

#Resmin 100'e 100'üncü pikselindeki BGR degerleri.
print(resim.item((100, 100), 0))
print(resim.item((100, 100), 1))
print(resim.item((100, 100), 2))

#Resmin boyutu(Kac piksel oldugu)
print(resim.size)


#resim ozelligi: (a,b,c) sırasıyla yuseklik, genislik, kanal
print(resim.shape)

#Resmin verilen pikselindeki degeri
print(resim[50, 50])