import cv2
import numpy as np

facedetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eyesdetect = cv2.CascadeClassifier('haarcascade_eye.xml')
noisedetect = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')


if facedetect.empty():
        raise IOError('Unable to haarcascade_frontalface_alt.xml file')
if eyesdetect.empty():
	raise IOError('Unable to load haarcascade_eye.xml file')
if noisedetect.empty():
        raise IOError('Unable to load haarcascade_mcs_nose.xml file')

capture = cv2.VideoCapture(0)
while True:
        ret, capturing = capture.read()
	resize_frame = cv2.resize(capturing, None,fx=.5 ,fy=.5,  interpolation=cv2.INTER_AREA)
	gray = cv2.cvtColor(resize_frame, cv2.COLOR_BGR2GRAY)
	face_detection = facedetect.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in face_detection:
		cv2.rectangle(resize_frame, (x,y), (x+w,y+h), (0,0,255), 2)
	cv2.imshow("",resize_frame)
	c = cv2.waitKey(1)
	if c == 27:
		break
capture.release()
cv2.destroyAllWindows()
