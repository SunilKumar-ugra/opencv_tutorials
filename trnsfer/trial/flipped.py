import cv2
import imutils

img = cv2.imread("red.jpg")
cv2.imshow("lol",img)

flipped = cv2.flip(img, 1)
cv2.imshow("Flipped Horizontally", flipped)

flipped = cv2.flip(img, 0)
cv2.imshow("Flipped Vertically", flipped)

flipped = cv2.flip(img, -1)
cv2.imshow("Flipped Horizontally & Vertically", flipped)
cv2.waitKey(0)
