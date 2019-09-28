import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import urllib2
import sys
from Color import Color
import calibrate_arena as ca


def eachcolour(x,colorName):
    # colorName = open( color + ".txt","r")
    upperColor = Color(colorName,1)
    lowerColor = Color(colorName,0)


    # res, i = cap.read(1)
    # i=i[y1:y2 , x1:x2]
    # resized=imutils.rotate_bound(i,rot)
    # # resized = imutils.resize(i, width=690)
    ratio = x.shape[0] / float(x.shape[0])

    hsv = cv2.cvtColor(x, cv2.COLOR_BGR2HSV)

    #t = cv2.getTrackbarPos('t','img')

    mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

    res = cv2.bitwise_and(x,x, mask= mask)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    b = cv2.threshold(gray, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]
    #thresh = cv2.threshold(b, 80, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(b,0,255)
    cnts = cv2.findContours(b.copy(), cv2.RETR_LIST,
                cv2.CHAIN_APPROX_NONE)
    # cv2.imshow("blurred",edges)

    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd=ShapeDetector
    area=0
    max_area=10000
    cX=0
    cY=0
    maxCnt = []
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
        #print area
        if area > max_area:
            max_area = area
            maxCnt = c
    #if len(maxCnt) != 0:
    #cv2.drawContours(x,maxCnt , -1, (255,0,0), 2)
    # cv2.putText(x,str(max_area),(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,0))
    # cv2.imshow("op",x)
    # cv2.waitKey(0)
    return max_area
            # if area > 310:
            #     cv2.drawContours(res, [c], -1, (255,0,0), 2)
            #
            #     cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
            #     if area > max_area:
            #         max_area = area
            #     elif area < min_area:
            #         min_area=area

        #print min_area

        #print max_area
        # cv2.imshow('frame',edges)
        # cv2.imshow('mask',mask)
        # cv2.imshow('resized',res)

        #cv2.imshow("original",resized)
        # k = cv2.waitKey(5) & 0xFF
        # if k == 27:
        #     break
    cv2.destroyAllWindows()

def setarea(x,src,center):
    x = cv2.resize(x,(500,500))
    blue_area=eachcolour(x,"blue")
    white_area=eachcolour(x,"white")
    red_area=eachcolour(x,"red")
    green_area=eachcolour(x,"green")
    pink_area=eachcolour(x,"pink")
    yellow_area=eachcolour(x,"yellow")
    black_area=eachcolour(x,"black")
    # dgreen_area=eachcolour(x,"dgreen")
    safe_area=red_area+white_area+blue_area+green_area+yellow_area+pink_area
    other=red_area+blue_area+green_area
    list = [red_area,white_area,blue_area,green_area,black_area]
    if white_area>200000:
        cv2.putText(src,"res",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
        return "Resource"
    elif white_area>30000:
        if (white_area>70000 and other>30000) :
            cv2.putText(src,"chkpt",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
            return "Checkpoint"
        else:#cv2.putText(src,"chkpt",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
            cv2.putText(src,"safe",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
            return "Safe"
    elif safe_area>150000:
        cv2.putText(src,"safe",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255))
        return "Safe"
    # elif blue_area>30000:
    #     cv2.putText(src,"blue",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255))
    # elif red_area>30000:
    #     cv2.putText(src,"red",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255))
    # elif green_area>30000:
    #     cv2.putText(src,"green",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255))
    # elif safe_area<30000 and safe_area>10000:
    #     cv2.putText(src,"obs",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255))
    else:
        cv2.putText(src,"?",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
        return "Obstacle"
        # largest=white_area
        # index=1
    # else:
        # largest=max(list)
        # index=list.index(max(list))


    # print largest
    # print index
