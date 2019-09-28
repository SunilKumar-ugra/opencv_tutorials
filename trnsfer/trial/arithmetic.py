# open cv sets a maximum and minimum value and clips the output
# numpy has awraparound feature
import cv2
import numpy as np


img = cv2.imread("red.jpg")
cv2.imshow("lol",img)

M = np.ones(img.shape, dtype = "uint8") * 100
added = cv2.add(img, M)
cv2.imshow("Added", added)

M = np.ones(img.shape, dtype = "uint8") * 50
subtracted = cv2.subtract(img, M)
cv2.imshow("Subtracted", subtracted)
cv2.waitKey(0)
