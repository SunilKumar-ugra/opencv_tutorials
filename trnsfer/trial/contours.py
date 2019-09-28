import cv2
import numpy as np
vid=cv2.VideoCapture(0)
if vid.isOpened():
        #for frame
        ret,img=vid.read()
else:
    ret=False
while ret:
    #img = cv2.imread('mon.jpg')
    ret,img=vid.read()
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    im,contours,hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    for c in contours:
        cv2.drawContours(img, [c], -1, (0, 255, 255), 2)
        cv2.imshow("bol",img)
# img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
# cv2.imshow("bol",img)
    if cv2.waitKey(1) & 0xFF == ord('e'):
            break

vid.release()
cv2.destroyAllWindows()
