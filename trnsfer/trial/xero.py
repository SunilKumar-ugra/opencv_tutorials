import cv2
import numpy as np

img = cv2.imread('mon.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy= cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print M

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

area = cv2.contourArea(cnt)

perimeter = cv2.arcLength(cnt,True)

epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

#hull = cv2.convexHull(points[, hull[, clockwise[, returnPoints]]

#hull = cv2.convexHull(cnt)

#k = cv2.isContourConvex(cnt)

rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(im,[box],0,(0,0,255),2)

cv2.imshow("om",im)
cv2.waitKey(0)
