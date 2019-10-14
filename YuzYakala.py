from PIL import Image, ImageFilter
from tkinter import filedialog
from tkinter import *
import numpy as np
import cv2
import pickle

input("""Yazılım herhangi bir görüntü kaynağındaki yüzleri algılayarak 
    dataset dizinine kaydedecektir.

    Devam etmek için enter (giriş) tuşuna basınız. """)
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")


labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

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
    kok.dosyaYolu =  filedialog.askopenfilename(initialdir = "/", 
    title = "Yüzlerin algılanacağı video dosyasını seçiniz", 
    filetypes = [("mp4 dosyaları","*.mp4"), ("avi dosyaları", "*.avi"), 
    ("diğer video dosyaları", "*.flv *.vmw *.mkv"), ("tüm dosyalar","*.*")])
    print ("seçilen dosyanın yolu= ", kok.dosyaYolu)
    cap = cv2.VideoCapture(kok.dosyaYolu)
cv2.waitKey(120)
sayac=0;
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
    	#print(x,y,w,h)
    	roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
    	roi_color = frame[y:y+h, x:x+w]

    	# recognize? deep learned model predict keras tensorflow pytorch scikit 
    	alan=w*h
    	if alan>6560:
    		id_, conf = recognizer.predict(roi_gray)
    		temp=sayac
    		img_item = "dataset/" + str(temp) + ".png"
    		sayac=sayac+1
    		cv2.imwrite(img_item, roi_color)
    		color = (0, 255, 255) #BGR 0-255 
    		stroke = 2
    		end_cord_x = x + w
    		end_cord_y = y + h
    		cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    	#subitems = smile_cascade.detectMultiScale(roi_gray)
    	#for (ex,ey,ew,eh) in subitems:
    	#	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # Display the resulting frame

    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

input("""Tüm yüzler dataset dizinine kaydedilmiştir

    devam etmek için enter (giriş) tuşuna basınız. """)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



