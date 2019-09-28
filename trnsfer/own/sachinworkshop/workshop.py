import cv2
import numpy as np
import random
 


def draw_something(event,x,y,flag,param):
    if event== cv2.EVENT_LBUTTONDOWN:
        color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
        cv2.circle(img,(x,y),50,color,-1)
        cv2.imshow("Image",img)
    if event== cv2.EVENT_RBUTTONDOWN:
        color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
        cv2.line(img,(x,y),(x+50,y+50),color,10)
        cv2.imshow("Image",img)
 
cv2.namedWindow("Image",cv2.WINDOW_AUTOSIZE)
img= np.zeros((512,512,3), dtype="uint8")
cv2.setMouseCallback("Image",draw_something)


cv2.imshow("Image",img)
cv2.waitKey(0