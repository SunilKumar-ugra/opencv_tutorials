import numpy as np
import cv2
import ImageProcess
from ImageProcess import Frame

# blue=
# bgr=cv2.cvtColor(blue,cv2.COLOR_HSV2BGR)
# print bgr

# src = cv2.imread("nitk2.jpg")
Frame.capture_frame()
src = Frame.resized
src = cv2.resize(src,(500,500))
green=(0, 255, 0)

height,width= src.shape[:2]
print src.shape
GRID_SIZE =35


for y in range(0,height,GRID_SIZE):  #(y = 0; y < height - GRID_SIZE; y += GRID_SIZE):
    for x in range(0,width,GRID_SIZE): #(x = 0; x < width - GRID_SIZE; x += GRID_SIZE):
            # k = x*y + x
        new_x=x+GRID_SIZE
        new_y=y+GRID_SIZE
        cv2.rectangle(src, (x,y),(new_x,new_y), green , 1)

cv2.imshow("src", src)
cv2.waitKey(0)
