import cv2
import imutils

img = cv2.imread("red.jpg")

cv2.imshow("lol",img)
cv2.waitKey(0)

rotated = imutils.rotate(img, 45)
cv2.imshow("Rotated by 180 Degrees", rotated)
cv2.waitKey(0)
