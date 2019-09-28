import cv2
import numpy as np

img = cv2.imread('IMAGE.png',0)
kernel = np.ones((3,3),np.uint8)

dilation = cv2.dilate(img,kernel,iterations = 5)
erosion = cv2.erode(dilation,kernel,iterations = 5)

cv2.imshow("d",dilation)
cv2.imshow("e",erosion)
cv2.waitKey(0)