# OpenCV Bazı Fonksiyonlar

    cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
Resmi gri hale getiriyor.

    cv2.Canny(img, dusuk_esik_degeri, yuksek_esik_degeri)
Verilen esik değerlerine göre resim üzerinde kenarları bulmaya yarıyor.

    cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
Gereksiz ayrıntıların da kenar gibi görünmemesi için resmi bulanıklaştırıyor.

    cv2.bitwise_and(img, mask)
Pikseller karşılaştırılarak maskelenmiş kısımda resmin görünmesini sağlıyor.
