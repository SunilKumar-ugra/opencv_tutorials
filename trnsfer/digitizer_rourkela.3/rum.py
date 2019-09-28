import cv2
import imutils
import numpy as np

def nothing(x):
    pass

def getCrop():

    cap = cv2.VideoCapture(0)
    #cap.set(3,1024)
    #cap.set(4,768)

    #cv2.namedWindow('image')
    ret, resized = cap.read()

    #resized=cv2.imread("cropped.png")

    cv2.namedWindow('image')
    cv2.createTrackbar('x1','image',0,resized.shape[1],nothing)
    cv2.createTrackbar('y1','image',0,resized.shape[0],nothing)
    cv2.createTrackbar('x2','image',0,resized.shape[1],nothing)
    cv2.createTrackbar('y2','image',0,resized.shape[0],nothing)

    x1,y1=0,0
    (x2,y2)=resized.shape[:2]
    rot=0

    while(True):
        # Capture frame-by-frame
        ret, resized = cap.read()
        #resized=cv2.imread("cropped.png")

        #to know which part we are extracting from original image lets draw a rectangle
        black = (0, 0, 0)

        x1 = cv2.getTrackbarPos('x1','image')
        y1 = cv2.getTrackbarPos('y1','image')
        x2= cv2.getTrackbarPos('x2','image')
        y2 = cv2.getTrackbarPos('y2','image')

        cv2.rectangle(resized,  (x1,y1), (x2, y2), black,2)
        cv2.imshow('mask',resized)
        black = (0, 0, 0)
        cv2.rectangle(resized,  (x1,y1), (x2, y2), black,10)
        if x2>x1 and y2>y1:
            cropped = resized[y1:y2 , x1:x2]
            cv2.imshow('cropped',cropped)
        p=open( "crop.txt","w")
        p.write(str(y1)+','+str(y2)+','+str(x1)+','+str(x2)+','+str(rot))
        p.close()
        #here we extracta rectangular region of the image, starting at (150, 113) and ending at (200, 200).
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print "crop done"
            cv2.destroyAllWindows()
            break
    return y1,y2,x1,x2


y1,y2,x1,x2=getCrop()

import numpy as np

image = cv2.imread('boruto.jpg')

mask = np.zeros(image.shape[:2], dtype = "uint8")
(cX, cY) = (image.shape[1] // 2, image.shape[0] // 2)
cv2.rectangle(mask, (cX - 75, cY - 75), (cX + 75 , cY + 75), 255,-1)
cv2.imshow("Mask", mask)

masked = cv2.bitwise_and(image, image, mask = mask)
cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)





# When everything done, release the video capture object
#cap.release()

# Closes all the frames
#cv2.destroyAllWindows()


