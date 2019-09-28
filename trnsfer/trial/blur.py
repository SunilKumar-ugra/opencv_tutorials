import numpy as np
import cv2

image = cv2.imread('mon.jpg')

#averaging
blurred = np.hstack([
cv2.blur(image, (3, 3)),
cv2.blur(image, (5, 5)),+++
cv2.blur(image, (7, 7))])
cv2.imshow("Averaged", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()

blurred = np.hstack([
cv2.GaussianBlur(image, (3, 3), 0),
cv2.GaussianBlur(image, (5, 5), 0),
cv2.GaussianBlur(image, (7, 7), 0)])
cv2.imshow("Gaussian", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()

# blurred = np.hstack([
# cv2.bilateralFilter(image, 5, 31, 31),
# cv2.bilateralFilter(image, 7, 51, 51),
# cv2.bilateralFilter(image, 9, 71, 71)])
# cv2.imshow("Bilateral", blurred)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
