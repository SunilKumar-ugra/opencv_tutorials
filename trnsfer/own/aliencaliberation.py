import cv2
import numpy as nm

def crop():
    import imutils

    def nothing():
        pass

    cv2.namedWindow("real_image")
    cv2.namedWindow("track")
    cap=cv2.VideoCapture(0)
    if cap.isOpened():
        flag,frame=cap.read()
    else:
        flag=False

    x1=0
    y1=0
    (x2,y2)=frame.shape[:2]
    rot=0

    cv2.createTrackbar('y1','track',0,frame.shape[0],nothing)
    cv2.createTrackbar('y2', 'track',0,frame.shape[0], nothing)
    cv2.createTrackbar('x1', 'track', 0,frame.shape[1], nothing)
    cv2.createTrackbar('x2', 'track', 0,frame.shape[1], nothing)
    cv2.createTrackbar('rot', 'track', 0,360, nothing)


    while flag:
        cv2.imshow("real_image",frame)
        flag,frame=cap.read()


        y1=cv2.getTrackbarPos('y1','track')
        y2=cv2.getTrackbarPos('y2','track')
        x1=cv2.getTrackbarPos('x1','track')
        x2=cv2.getTrackbarPos('x2','track')


        blue=(255,0,0)
        cv2.rectangle(frame,(x1,y1),(x2,y2),blue,3)

        cv2.imshow('real_image',frame)
        red=(0,0,255)


        cv2.rectangle(frame, (x1, y1), (x2, y2),red,3)
        if x2 > x1 and y2 > y1:
            cropped = frame[y1:y2, x1:x2]
            cv2.imshow('cropped', cropped)
        #p=open( "crop.txt","w")
        #p.write(str(y1)+','+str(y2)+','+str(x1)+','+str(x2)+','+str(rot))
        #p.close()

        if cv2.waitKey(1)& 0xFF == ord('e'):
            break

    cv2.destroyWindow("real_image")



#cv2.namedWindow("rotated")
    while 1:
        cv2.imshow("real_image", frame)
        flag, frame = cap.read()

        rot = cv2.getTrackbarPos('rot', 'track')

        cropped=frame[y1:y2, x1:x2]
        rotated=imutils.rotate(cropped,rot)
        cv2.imshow("After_rotation",rotated)
        p=open( "crop.txt","w")
        p.write(str(y1)+','+str(y2)+','+str(x1)+','+str(x2)+','+str(rot))
        p.close()
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break



    cap.release()
    cv2.destroyAllWindows()
    return y1,y2,x1,x2,rot








