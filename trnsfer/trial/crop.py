import cv2
import imutils

img = cv2.imread("red.jpg")
cv2.imshow("lol",img)
cv2.waitKey(0)

resized = imutils.resize(img, height = 500)

cv2.imshow("Resized via Function", resized)
cv2.waitKey(0)

cropped = img[30:120 , 240:335]
cv2.imshow("T-Rex Face", cropped)
cv2.waitKey(0)
