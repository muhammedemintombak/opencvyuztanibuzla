import numpy as np
import cv2

secim_kaynak= input("""

    Görüntü Kaynakları:

    1. Dahili webcam veya tabletlerdeki arka veya ana kamera
    2. Harici webcam veya tabletlerdeki ön veya ikincil kamera
    3. IP Kamera
    4. Video Dosyası

    İşlem yapmak istediğiniz görüntü kaynağını seçiniz: """)
if int(secim_kaynak)==1:
    cap=cv2.VideoCapture(0)
elif int(secim_kaynak)==2:
    cap=cv2.VideoCapture(1)
elif int(secim_kaynak)==3:
    ip_kamera_adresi=input("IP kameranın url'sini giriniz: ")
    cap=cv2.VideoCapture(ip_kamera_adresi)
elif int(secim_kaynak)==4:
    print('İşlem yapılacak video dosyasını seçiniz')
    kok = Tk()
    kok.dosyaYolu =  filedialog.askopenfilename(initialdir = "/", title = "Buzlanacak video dosyasını seçiniz", 
    filetypes = [("mp4 dosyaları","*.mp4"), ("avi dosyaları", "*.avi"), 
    ("diğer video dosyaları", "*.flv *.vmw *.mkv"), ("tüm dosyalar","*.*")])
    print ("seçilen dosyanın yolu= ", kok.dosyaYolu)
    cap = cv2.VideoCapture(kok.dosyaYolu)
cv2.waitKey(120)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()