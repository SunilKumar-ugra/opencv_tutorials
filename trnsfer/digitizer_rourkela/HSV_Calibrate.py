import numpy as np
import cv2
import argparse
import imutils
import urllib2
import sys
from Color import Color
import calibrate_arena as ca
import mahotas
from Frame import Frame

minArea = 0
maxArea = 100000

fil=open("crop.txt","r")
data=fil.read().split(',')
y1=int(data[0])
y2=int(data[1])
x1=int(data[2])
x2=int(data[3])
rot=int(data[4])
fil.close()

colorPoints = []

colorName =raw_input("Enter the color : ")
if str(colorName) == "crop":
	y1,y2,x1,x2,rot=ca.getCrop()
	colorName =raw_input("Enter the color : ")
print "reading colors"
upperColor = Color(colorName,1)
lowerColor = Color(colorName,0)

'''
cap=cv2.VideoCapture(1)
cap.set(5, 18)  #frame rate
cap.set(10, 130)  #brightness
cap.set(12, 255)  #saturation
#cap.set(3,1024) #width
#cap.set(4,768) #height
print "done setting the cam"
'''
print "using demo image"

def detect(c):
    # initialize the shape name and approximate the contour
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    # if the shape is a triangle, it will have 3 vertices
    if len(approx) == 3:
        shape = "triangle"

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(approx) == 4:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)

        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "square"

    # if the shape is a pentagon, it will have 5 vertices


    # return the name of the shape
    return shape


def HSVProcess(colorPoints):

	upperColor.H = cv2.getTrackbarPos('H','img')
	upperColor.S = cv2.getTrackbarPos('S','img')
	upperColor.V = cv2.getTrackbarPos('V','img')
	
	lowerColor.H = cv2.getTrackbarPos('h','img')
	lowerColor.S = cv2.getTrackbarPos('s','img')
	lowerColor.V = cv2.getTrackbarPos('v','img')
	lowerColor.T = cv2.getTrackbarPos('t','img')
	minArea = cv2.getTrackbarPos('minArea','img')
	maxArea = cv2.getTrackbarPos('maxArea','img')    
	sh =cv2.getTrackbarPos('sh','img')
	#cap.set(13,sh)#contrast
	#cap.set(12,sh)#saturation
	#t = cv2.getTrackbarPos('t','img')
	p=open(  colorName + ".txt","w")
	p.write(upperColor.toString() + "," + lowerColor.toString() + "," + str(lowerColor.T) + "," + str(min_area) + "," + str(max_area)+"," + str(colorPoints))

cv2.namedWindow('img',cv2.WINDOW_NORMAL)


cv2.createTrackbar('H', 'img', int(upperColor.H),255,HSVProcess)
cv2.createTrackbar('S','img',int(upperColor.S),255,HSVProcess)
cv2.createTrackbar('V','img',int(upperColor.V),255,HSVProcess)
cv2.createTrackbar('h','img',int(lowerColor.H),255,HSVProcess)
cv2.createTrackbar('s','img',int(lowerColor.S),255,HSVProcess)
cv2.createTrackbar('v','img',int(lowerColor.V),255,HSVProcess)
cv2.createTrackbar('t','img',int(lowerColor.T),255,HSVProcess)
cv2.createTrackbar('minArea','img',minArea,100000,HSVProcess)
cv2.createTrackbar('maxArea','img',int(lowerColor.T),100000,HSVProcess)

max_area = 0
min_area = 0

x,y,w,h=0,0,0,0

if colorName == "green" or colorName =="brown":
	ans=raw_input("What is this color?")

while(1):

		#ret,i = cap.read(1)
		i=Frame.demo_image

		if colorName=="yellow":
			list_of_res=[]
		elif colorName=="white":
			list_of_xy_obstacles=[]

		i=i[y1:y2 , x1:x2]
		resized=imutils.rotate_bound(i,rot)
		ratio = resized.shape[0] / (float(resized.shape[0]))

		hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

		#t = cv2.getTrackbarPos('t','img')

		mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

		res = cv2.bitwise_and(resized,resized, mask= mask)
		gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)

		T=mahotas.thresholding.otsu(blurred)
		b=blurred.copy()
		b[b>T]=255
		b[b<255]=0
		#b = cv2.threshold(blurred, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]
		kernel = np.ones((3, 3), np.uint8)
		gry = cv2.erode(b, kernel, iterations=1)
		gry = cv2.dilate(b, kernel, iterations=1)

		#thresh = cv2.threshold(b, 80, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(gry.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE) 
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		area=0
		cX=0
		cY=0
		for c in cnts:
			M = cv2.moments(c)
			if M["m00"] > 0:
				cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
				cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
				shape = detect(c)
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				area=cv2.contourArea(c)





				if (colorName == "yellow"):
					cv2.drawContours(res, [c], -1, (255,0,0), 2)
					cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
					if area > max_area:
						max_area = area
						HSVProcess(colorPoints)
					elif area < min_area:
						min_area=area 
						HSVProcess(colorPoints)
					input_str = shape+','+str(cX)+','+str(cY)+','
					list_of_res.append(input_str)

					HSVProcess(colorPoints)





				elif (colorName == "white"):
					cv2.drawContours(res, [c], -1, (255,0,0), 2)
					x,y,w,h = cv2.boundingRect(c)
					cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
					cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
					if area > max_area:
						max_area = area
						HSVProcess(colorPoints)
					elif area < min_area:
						min_area=area 
						HSVProcess(colorPoints)
					input_str = str(x)+','+str(y)+','+str(x+w)+','+str(y+h)
					list_of_xy_obstacles.append(input_str)

					HSVProcess(colorPoints)








				elif(colorName=="green" or colorName=="brown"):
					cv2.drawContours(res, [c], -1, (255,0,0), 2)
					cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
					if area > max_area:
						max_area = area
						HSVProcess(colorPoints)
					elif area < min_area:
						min_area=area 
						HSVProcess(colorPoints)
					f=open(  ans + ".txt","w")
					f.write(str(cX)+','+str(cY))
					f.close()

						


						




				elif area>300:
					cv2.drawContours(res, [c], -1, (255,0,0), 2)
					x,y,w,h = cv2.boundingRect(c)
					cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
					
					cv2.putText(res, str(area) , (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
					if area > max_area:
						max_area = area
						HSVProcess(colorPoints)
					elif area < min_area:
						min_area=area 
						HSVProcess(colorPoints)



                    

		cv2.imshow('mask',mask)
		cv2.imshow('resized',res)
		#cv2.imshow("original",resized)
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			colorPoints =[(x+w,y),(x,y),(x,y+h),(x+w,y+h)]
			print colorPoints
			HSVProcess(colorPoints)
			if colorName=="yellow":
				f=open( "resources.txt","w")
				f.write(str(list_of_res))
				f.close()
			if colorName=="white":
				f=open( "obstacles.txt","w")
				f.write(str(list_of_xy_obstacles))
				f.close()
			break


cv2.destroyAllWindows()
#cap.release()
colorPoints=[]
