import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import os
import sys
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory Created")
else:
    print("Name already exists")

time.sleep(5)
count = 1
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if count > 30:
        break
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    for (x, y, w, h) in faces:
        roiGray = gray[y:y+h, x:x+w]
        fileName = dirName + "/" + name + str(count) + ".jpg"
        cv2.imwrite(fileName, roiGray)
        cv2.imshow("face", roiGray)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        count += 1

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    rawCapture.truncate(0)

    if key == 27:
        break

cv2.destroyAllWindows()

