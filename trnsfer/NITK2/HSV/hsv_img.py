import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import urllib2
import sys
from Color import Color
import calibrate_arena as ca

colorName =raw_input("Enter the color : ")
upperColor = Color(colorName,1)
lowerColor = Color(colorName,0)

cap=cv2.imread("nitk2.jpg")

# cap=cv2.VideoCapture(0)
# cap.set(5, 18)  #frame rate
# cap.set(10, 50)  #brightness
# cap.set(12, 255)  #saturation

def HSVProcess(x):

    upperColor.H = cv2.getTrackbarPos('H','img')
    upperColor.S = cv2.getTrackbarPos('S','img')
    upperColor.V = cv2.getTrackbarPos('V','img')

    lowerColor.H = cv2.getTrackbarPos('h','img')
    lowerColor.S = cv2.getTrackbarPos('s','img')
    lowerColor.V = cv2.getTrackbarPos('v','img')
    lowerColor.T = cv2.getTrackbarPos('t','img')
    sh =cv2.getTrackbarPos('sh','img')
    #cap.set(13,sh)#contrast
    #cap.set(12,sh)#saturation
    #t = cv2.getTrackbarPos('t','img')
    p=open(  colorName + ".txt","w")
    p.write(upperColor.toString() + "," + lowerColor.toString() + "," + str(lowerColor.T) + "," + str(min_area) + "," + str(max_area))

cv2.namedWindow('img',cv2.WINDOW_NORMAL)
# cap.set(5,18) #frame rate
# cap.set(10,0.1)#brightness
# cap.set(12,255)#saturation


cv2.createTrackbar('H', 'img', int(upperColor.H),255,HSVProcess)
cv2.createTrackbar('S','img',int(upperColor.S),255,HSVProcess)
cv2.createTrackbar('V','img',int(upperColor.V),255,HSVProcess)
cv2.createTrackbar('h','img',int(lowerColor.H),255,HSVProcess)
cv2.createTrackbar('s','img',int(lowerColor.S),255,HSVProcess)
cv2.createTrackbar('v','img',int(lowerColor.V),255,HSVProcess)
cv2.createTrackbar('t','img',int(lowerColor.T),255,HSVProcess)
cv2.createTrackbar('sh','img',0,1000,HSVProcess)
max_area = 0
min_area = 10000
while(1):

        # res, i = cap.read(1)
        # i=i[y1:y2 , x1:x2]
        # resized=imutils.rotate_bound(i,rot)
        # # resized = imutils.resize(i, width=690)
        ratio = cap.shape[0] / float(cap.shape[0])

        hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

        #t = cv2.getTrackbarPos('t','img')

        mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

        res = cv2.bitwise_and(cap,cap, mask= mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        b = cv2.threshold(blurred, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]
        #thresh = cv2.threshold(b, 80, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(b,0,0)
        cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        sd=ShapeDetector
        area=0
        cX=0
        cY=0
        for c in cnts:
            M = cv2.moments(c)
            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                #shape = sd.detect(c)
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                if area > 310:
                    cv2.drawContours(res, [c], -1, (255,0,0), 2)

                    cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                    if area > max_area:
                        max_area = area
                    elif area < min_area:
                        min_area=area

        #print min_area

        #print max_area
        cv2.imshow('frame',edges)
        cv2.imshow('mask',mask)
        cv2.imshow('resized',res)

        #cv2.imshow("original",resized)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

cv2.destroyAllWindows()
