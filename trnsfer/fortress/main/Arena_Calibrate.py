import numpy as np
import cv2
import imutils
import os
from Color import Color
import calibrate_arena as ca
import mahotas

import ast
import getpath as gp

import graphing as grph
import pandas as pd
minArea = 0
maxArea = 100000

flag =0.01#0.035847
fil=open("crop.txt","r")
data=fil.read().split(',')
y1=int(data[0])
y2=int(data[1])
x1=int(data[2])
x2=int(data[3])
rot=int(data[4])
fil.close()

info = []

colorName =raw_input("Enter the objects : ")
if str(colorName) == "crop":
    y1,y2,x1,x2,rot=ca.getCrop()
    colorName =raw_input("Enter the objects : ")
print "reading obj"
upperColor = Color(colorName,1)
lowerColor = Color(colorName,0)


cap=cv2.VideoCapture(1)


cap.set(5, 18)  #frame rate 
cap.set(10, 130)  #brightness
cap.set(12, 255)  #saturation


#cap.set(3,1024) #width
#cap.set(4,768) #height
print "done setting the cam"

##print "using demo image"
def draw_arrow(image, p, q, color, arrow_magnitude=9, thickness=2, line_type=8, shift=0):
        # adapted from http://mlikihazar.blogspot.com.au/2013/02/draw-arrow-opencv.html

    # draw arrow tail
    cv2.line(image, p, q, color, thickness)
    # calc angle of the arrow
    angle = np.arctan2(p[1]-q[1], p[0]-q[0])
    # starting point of first line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle + np.pi/4)),
    int(q[1] + arrow_magnitude * np.sin(angle + np.pi/4)))
    # draw first half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)
    # starting point of second line of arrow head
    p = (int(q[0] + arrow_magnitude * np.cos(angle - np.pi/4)),
    int(q[1] + arrow_magnitude * np.sin(angle - np.pi/4)))
    # draw second half of arrow head
    cv2.line(image, p, q, color, thickness, line_type, shift)

def load_images_from_folder(folder):
    images = []
    image_names=[]
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),0)
        if img is not None:
            images.append(img)
            image_names.append(filename)
    return images,image_names

def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff

def list_duplicates(seq):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  return list( seen_twice )

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

ret,i = cap.read(1)

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
while(1):
        info=[]
        ret,i = cap.read(1)
        #cv2.imwrite("lol.png",i)
        #i=cv2.imread("arena.png")
        i=i[y1:y2 , x1:x2]
        resized=imutils.rotate_bound(i,rot)
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
        gry = cv2.dilate(b, kernel, iterations=4)
        gry = cv2.erode(gry, kernel, iterations=5)



        (_,cnts,_) = cv2.findContours(gry.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for (i, c) in enumerate(cnts):
            epsilon1 = flag*cv2.arcLength(c,True)

            approx1= cv2.approxPolyDP(c,epsilon1,True)

            cv2.drawContours(res, [approx1] ,-1, (255, 255, 255), 1)



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
            (_,cnts,_) = cv2.findContours(gry.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for (i, c) in enumerate(cnts):
                epsilon1 = flag*cv2.arcLength(c,True)

                approx1= cv2.approxPolyDP(c,epsilon1,True)

                cv2.drawContours(res, [approx1] ,-1, (255, 255, 255), -1)
                M = cv2.moments(c)
                if M["m00"] > 0:
                    cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                    cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    (x, y, w, h) = cv2.boundingRect(c)
                    coin = gry[y:y + h, x:x + w]
                    info.append([i,(cX,cY),(x, y, w, h)])
                    HSVProcess(info)
                    area=cv2.contourArea(c)
                if colorName == "res" and area>100:
                    #constant= cv2.copyMakeBorder(coin,50,50,50,50,cv2.BORDER_CONSTANT,value=[0,0,0])
                    resized = imutils.resize(coin,width=150,height=150)
                    cv2.imwrite("arena_contours/"+str(i)+".png",resized)
            break
        
cv2.destroyAllWindows()
if str(colorName) == 'res':
    colorSequence =raw_input("Enter the order of rgby: ")
    colorSequence=str(colorSequence).split(',')
    image_contours,image_names= load_images_from_folder("image_contours")
    arena_contours,names= load_images_from_folder("arena_contours")
    df = pd.DataFrame(index=np.arange(0, (len(image_contours)*len(arena_contours))),columns=['color','image','coeff'])
    matches={}
    match_error  = {}
    list_error=[]
    for (i,iimage) in enumerate(image_contours):
        least=1
        list_error=[]
        for (a,aimage) in enumerate(arena_contours):
            for angle in range(0,360):
                rotated = imutils.rotate_bound(aimage,angle)
                _,contours,hierarchy = cv2.findContours(iimage,2,1)
                cnt1 = contours[0]
                epsilon1 = flag*cv2.arcLength(cnt1,True)
                approx1 = cv2.approxPolyDP(cnt1,epsilon1,True)
                _,contours,hierarchy = cv2.findContours(rotated,2,1)
                cnt2 = contours[0]
                epsilon2 = flag*cv2.arcLength(cnt2,True)
                approx2 = cv2.approxPolyDP(cnt2,epsilon2,True)
                ret = cv2.matchShapes(approx1,approx2,1,0)
                if ret < least:
                    least=ret
                    matches[image_names[i][:-4]]=a
            list_error.append([a,least])
            df.loc[len(arena_contours)*i+a]= pd.Series({'color':image_names[i][:-4], 'image':a, 'coeff':ret})
        match_error[image_names[i][:-4]]=list_error

    df = df.sort_values('coeff', ascending=True)
    df = df.reset_index()
    del df['index']
    for x in range(0,4):
        c = df['color'][0]
        i = df['image'][0]
        df = df[df.color != c]
        df = df[df.image != i]
        matches[c]=i
        df = df.reset_index()
        del df['index']

    print matches


    fil=open("final_resources.txt","w")
    fil.write(str(matches))
    fil.close()


    fil=open("res.txt","r")
    data=ast.literal_eval(fil.read())[7]
    fil.close()

    obstacles=[]

    for d in data:
            if d[0] not in matches.values():
                    obstacles.append(d)
                    
            for v,k in zip(matches.values(),matches.keys()):
                    if v==d[0]:
                            matches[k]=d

    ret,i = cap.read(1)
    #i=cv2.imread("arena.png")
    i=i[y1:y2 , x1:x2]
    resized=imutils.rotate_bound(i,rot)						

    res,path=gp.get_path(matches,obstacles,i,colorSequence)

    print res
    print path

    #img = cv2.imread("arena.png")

    for i,point in zip(range(0,len(path)-1),path):
        draw_arrow(resized,(point[0],point[1]),(path[i+1][0],path[i+1][1]),((i*20),(i*30),0),)

    list_of_gridpoints,map_dict,rmapd=grph.grid(resized,20)

    for point in list_of_gridpoints:
        cv2.circle(resized,point,1,(255,0,0))

    print obstacles
    list_of_obs = []
    k=15
    for obs in obstacles:
		for j in range(int(obs[2][1])-k,int(obs[2][1])+int(obs[2][3])+k):
			for i in range(int(obs[2][0])-k,int(obs[2][0])+int(obs[2][2])+k):
				list_of_obs.append((i,j))

    for point in list_of_obs:
        cv2.circle(resized,point,1,(255,0,255))

    cv2.imshow("s",resized)
    cv2.waitKey(0)

cv2.destroyAllWindows()
cap.release()
if colorName == 'res':
    fil=open("path.txt","w")
    fil.write(str([res,path]))
    fil.close()
