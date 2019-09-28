import cv2
import numpy
capture = cv2.VideoCapture(0)
while True:
    ret, capturing = capture.read()
    var = cv2.resize(capturing, None,fx=.5 ,fy=.5,  interpolation=cv2.INTER_AREA)
    cv2.imshow("",var)
    c = cv2.waitKey(1)
    if c == 27:
        break
capture.release()
cv2.destroyAllWindows()
