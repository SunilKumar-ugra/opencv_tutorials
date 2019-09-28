import cv2

img=cv2.imread("try.JPG",cv2.IMREAD_COLOR)
res_img=cv2.resize(img,(619,621))
cv2.imshow("hola",res_img)
cv2.waitKey(0)

gray = cv2.cvtColor(res_img, cv2.COLOR_BGR2GRAY)
ret,thresh=cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
cv2.imshow("hols",thresh)
cv2.waitKey(0)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow("hole",blurred)
cv2.waitKey(0)
