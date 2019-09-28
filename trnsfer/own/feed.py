import cv2
import numpy as np
import imutils
import mahotas
import aliencaliberation as ac

def HSV(colour):
    H=0
    S=0
    V=0
    h=0
    s=0
    v=0

    # f=open(colour + ".txt","r")
    # data=f.read().split(',')
    # H=int(data[0])
    # S=int(data[1])
    # V=int(data[2])
    # h=int(data[3])
    # s=int(data[4])
    # v=int(data[5])
    # f.close()

    vc = cv2.VideoCapture(0)

    cv2.namedWindow("bars")

    cv2.createTrackbar("H","bars",H,255,nothing)
    cv2.createTrackbar("S","bars",S,255,nothing)
    cv2.createTrackbar("V","bars",V,255,nothing)
    cv2.createTrackbar("h","bars",h,255,nothing)
    cv2.createTrackbar("s","bars",s,255,nothing)
    cv2.createTrackbar("v","bars",v,255,nothing)

    if vc.isOpened():
        #for frame
        rval,i = vc.read()
    else:
        rval = False

    while rval:

        rval,i = vc.read()
        i=i[y1:y2 , x1:x2]
        resized=imutils.rotate_bound(i,rot)
        #ratio = resized.shape[0] / (float(resized.shape[0]))
        blurred = cv2.GaussianBlur(resized, (5, 5), 0)
        cng = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        H = cv2.getTrackbarPos("H","bars")
        S = cv2.getTrackbarPos("S","bars")
        V = cv2.getTrackbarPos("V","bars")
        h = cv2.getTrackbarPos("h","bars")
        s = cv2.getTrackbarPos("s","bars")
        v = cv2.getTrackbarPos("v","bars")
        higher = np.array([H, S, V])
        lower = np.array([h, s, v])
        mask = cv2.inRange(cng, lower, higher)
        res = cv2.bitwise_and(resized,resized, mask=mask)
        blurredm = cv2.GaussianBlur(mask, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)

        p=open( colour + ".txt","w")
        p.write(str(H)+","+str(S)+","+str(V)+","+str(h)+","+str(s)+","+str(v))
        p.close()

        T = mahotas.thresholding.rc(blurredm)
        thresh = blurredm.copy()
        thresh[thresh > T] = 255
        thresh[thresh < 255] = 0
        thresh = cv2.bitwise_not(thresh)
        dilation = cv2.dilate(blurredm, kernel, iterations=1)
        #dilation = cv2.dilate(mask, kernel, iterations=1)
        erosion = cv2.erode(dilation, kernel, iterations=1)

        _, contours, _ = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        #cv2.drawContours(blurredm, contours, -1, (0, 255, 0), 3)

        def detectShape(cnt):
                shape = 'unknown'
                peri = cv2.arcLength(c, True)
                vertices = cv2.approxPolyDP(c, 0.04 * peri, True)

                # for triangle
                if len(vertices) == 3:
                    shape = 'triangle'


                elif len(vertices) == 4:
                    # for square ya rect

                    x, y, width, height = cv2.boundingRect(vertices)
                    aspectRatio = float(width) / height
                    if aspectRatio >= 0.80 and aspectRatio <= 1.20:
                        shape = "square"
                    else:
                        shape = "rectangle"

                elif len(vertices) == 5:
                    shape = "pentagon"

                else:
                    shape = "circle"

                return shape



        for c in contours:
            M = cv2.moments(c)
            # for centroid
            cX = int(M['m10'] /( M['m00']+0.000001))
            cY = int(M['m01'] /( M['m00']+0.000001))
            #cX = int(25)
            #cY = int(25)
            shape = detectShape(c)

            cv2.drawContours(res, [c], -1, (0, 0, 255), 2)
            cv2.putText(res, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)


        cv2.imshow('Mask', erosion)
        # cv2.imshow('img', frame)
        cv2.imshow('the ultimate window', res)
        #cv2.imshow("Image", mask)
        #cv2.imshow('bleh', thresh)


        key = cv2.waitKey(10)
        if key == 27:
            if (colour=="white" or colour=="blue"):
                file= open("visit.txt","a")
                file.write(shape+","+str(cX)+","+str(cY))
                file.close()
            elif (colour=="red" or colour=="yellow"):
                file= open("avoid.txt","a")
                file.write(shape+","+str(cX)+","+str(cY))
                file.close()
            elif (colour=="green"):
                file= open("start.txt","w")
                file.write(shape+","+str(cX)+","+str(cY))
                file.close()
            elif (colour=="brown"):
                file= open("stop.txt","w")
                file.write(shape+","+str(cX)+","+str(cY))
                file.close()
            else:
                pass
            break
    #means for break press esc++

    cv2.destroyWindow('the ultimate window')
    cv2.destroyWindow('Mask')
    cv2.destroyWindow("bars")
    vc.release()

   #cv2.drawContours(res, [c], -1, (0, 0, 255), 2)  #for red


def nothing(x):
    pass




colour=raw_input("which colour? :")
if str(colour)=="crop":
    y1,y2,x1,x2,rot= ac.crop()
    colour=raw_input("which colour? :")


fil=open("crop.txt","r")
data=fil.read().split(',')
y1=int(data[0])
y2=int(data[1])
x1=int(data[2])
x2=int(data[3])
rot=int(data[4])
fil.close()

while (str(colour)!="done"):
    HSV(colour)
    colour=raw_input("which colour? :")


