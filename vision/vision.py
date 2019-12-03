from time import sleep
import cv2
import numpy as np
import sys
import argparse


cascPath = "haarcascade_frontalface_default.xml"
#face_cascade &lt;span class="pl-k"&gt;=&lt;/span&gt;


face_cascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture(0)

while(True):
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1,
        minNeighbors = 5,
        minSize = (30,30)
 
        )
 
    print("The number of faces found = ", len(faces))
 
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+h, y+h), (0, 255, 0), 2)
    
    cv2.imshow('image', gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
                                    break

cap.release()
cv2.destroyAllWindows()
