import numpy as np
import cv2
import imutils
import sys
from Color import Color
import mahotas
from Frame import Frame


info = []

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
##print "using demo image"




def HSVProcess(info):

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
	p.write(upperColor.toString() + "," + lowerColor.toString() + "," + str(lowerColor.T)+','+str(info))

cv2.namedWindow('img',cv2.WINDOW_NORMAL)


cv2.createTrackbar('H', 'img', int(upperColor.H),255,HSVProcess)
cv2.createTrackbar('S','img',int(upperColor.S),255,HSVProcess)
cv2.createTrackbar('V','img',int(upperColor.V),255,HSVProcess)
cv2.createTrackbar('h','img',int(lowerColor.H),255,HSVProcess)
cv2.createTrackbar('s','img',int(lowerColor.S),255,HSVProcess)
cv2.createTrackbar('v','img',int(lowerColor.V),255,HSVProcess)



x,y,w,h=0,0,0,0
while(1):
		i=cv2.imread("HP.jpg")

		resized=i
		ratio = resized.shape[0] / (float(resized.shape[0]))

		hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

		mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

		res = cv2.bitwise_and(resized,resized, mask= mask)
		gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)

		T=mahotas.thresholding.otsu(blurred)
		b=blurred.copy()
		b[b>T]=255
		b[b<255]=0

		kernel = np.ones((3, 3), np.uint8)
		gry = cv2.erode(b, kernel, iterations=1)
		gry = cv2.dilate(b, kernel, iterations=1)

		(_,cnts,_) = cv2.findContours(gry.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
		cv2.drawContours(res, cnts, 0, (0, 255, 0), 2)
		for (i, c) in enumerate(cnts):
			M = cv2.moments(c)
			if M["m00"] > 0:
				cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
				cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				(x, y, w, h) = cv2.boundingRect(c)
				coin = gry[y:y + h, x:x + w]
				info=[(cX,cY),(x, y, w, h)]
				HSVProcess(info)
				#constant= cv2.copyMakeBorder(coin,50,50,50,50,cv2.BORDER_CONSTANT,value=[0,0,0])
				resized = imutils.resize(coin,width=150,height=150)
				cv2.imwrite("image_contours/"+str(colorName)+".png",resized)
				
		cv2.imshow("lol",res)

		#cv2.imshow("original",resized)
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			'''
			if colorName=="yellow":
				f=open( "resources.txt","w")
				f.write(str(list_of_res))
				f.close()
			'''
			break


cv2.destroyAllWindows()
#cap.release()

