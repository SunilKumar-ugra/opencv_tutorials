import cv2
import imutils

cam = cv2.VideoCapture(0)
cam.set(3,768)  #width
cam.set(4,1024)   #height
cam.set(10, 100)  #brightness
cam.set(12, 255)  #saturation

while True:
    ret,frame = cam.read()
    print (ret)
    cv2.imshow('frame',frame)

    rotated = imutils.rotate(frame, 180)
    cv2.imshow("Rotated by 180 Degrees", rotated)
    #cv2.waitKey(0)


    if  cv2.waitKey(10) & 0xFF ==  ord('q'):
        break
        #Frame.cam.set(3,1024)  #width
        #Frame.cam.set(4,768)   #height



