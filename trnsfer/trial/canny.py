import numpy as np
import cv2

image = cv2.imread('mon.jpg',0)
image2 = cv2.imread('red.jpg')

blurred = cv2.GaussianBlur(image, (3, 3), 0)
blurred2 = cv2.GaussianBlur(image2, (13, 13), 0)

(T, thresh) = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)
cv2.imshow("Threshold Binary", thresh)

thresh = cv2.adaptiveThreshold(blurred, 255,
cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 3)
cv2.imshow("Gaussian Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

edged = cv2.Canny(blurred2, 30, 150)
cv2.imshow("Edges", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image2, cnts, -1, (255, 255, 0), 2)
cv2.imshow("Contours", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()
