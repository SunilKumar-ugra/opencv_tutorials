import cv2
import numpy as np


image = cv2.imread('image_3.jpg')
cv2.imshow("original", image)
cv2.waitKey(0)


#flipping vertical
flip = cv2.flip(image, 0)
cv2.imshow("horizontal", flip)
cv2.waitKey(0)


#flipping horizotal

flip1 = cv2.flip(image, 1)
cv2.imshow("vertical", flip1)
cv2.waitKey(0)

flip2 = cv2.flip(image, -1)
cv2.imshow("horizontal and vertical", flip2)
cv2.waitKey(0)
cv2.destroyAllWindows()
