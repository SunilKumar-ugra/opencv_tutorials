import cv2
import imutils
import numpy as np

img = cv2.imread("red.jpg")
cv2.imshow("lol",img)
cv2.waitKey(0)

#r = 50.0 / img.shape[0]
#dim = (int(img.shape[1] * r), 50)

#resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
#cv2.imshow("Resized (Height)", resized)
#cv2.waitKey(0)

#ASK IF RESIZING USING HEIGHT AUTOMATICALLY MULTIPIES THE ASPECT RATIO TO WIDTH
resized = imutils.resize(img, height = 100)

cv2.imshow("Resized via Function", resized)
cv2.waitKey(0)
