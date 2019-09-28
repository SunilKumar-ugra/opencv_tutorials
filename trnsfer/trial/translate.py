import numpy as np
import cv2
import imutils


img = cv2.imread("red.jpg")

cv2.imshow("lol",img)
cv2.waitKey(0)

#COMPLICTED METHOD NOT USING IMUTILS
#M = np.float32([[1, 0, 25], [0, 1, 50]])
#shifted = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))

#cv2.imshow("Shifted Down and Right", shifted)
#cv2.waitKey(0)

shifted = imutils.translate(img, 50, 100)
cv2.imshow("Shifted Down and right", shifted)
cv2.waitKey(0)

