import cv2
import numpy as np
import mahotas
def nothing(x):
    pass

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

cv2.namedWindow("bars")

cv2.createTrackbar("H","bars",0,255,nothing)
cv2.createTrackbar("S","bars",0,255,nothing)
cv2.createTrackbar("V","bars",0,255,nothing)
cv2.createTrackbar("h","bars",0,255,nothing)
cv2.createTrackbar("s","bars",0,255,nothing)
cv2.createTrackbar("v","bars",0,255,nothing)

img = cv2.imread('mon.jpg')
blurred = cv2.GaussianBlur(img, (5, 5), 0)
cng = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
while True:
    H = cv2.getTrackbarPos("H","bars")
    S = cv2.getTrackbarPos("S","bars")
    V = cv2.getTrackbarPos("V","bars")
    h = cv2.getTrackbarPos("h","bars")
    s = cv2.getTrackbarPos("s","bars")
    v = cv2.getTrackbarPos("v","bars")
    higher = np.array([H, S, V])
    lower = np.array([h, s, v])
    mask = cv2.inRange(cng, lower, higher)
    res = cv2.bitwise_and(img,img, mask=mask)
    blurredm = cv2.GaussianBlur(mask, (5, 5), 0)
    kernel = np.ones((5, 5), np.uint8)

    T = mahotas.thresholding.rc(blurredm)
    thresh = blurredm.copy()
    thresh[thresh > T] = 255
    thresh[thresh < 255] = 0
    thresh = cv2.bitwise_not(thresh)
    dilation = cv2.dilate(blurredm, kernel, iterations=1)
    #dilation = cv2.dilate(mask, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    contours, _ = cv2.findContours(erosion, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     #cv2.drawContours(blurredm, contours, -1, (0, 255, 0), 3)

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


    #cv2.imshow('Mask', erosion)
    # cv2.imshow('img', frame)
    cv2.imshow('the ultimate window', res)
    #cv2.imshow("Image", mask)
    #cv2.imshow('bleh', thresh)

    key = cv2.waitKey(10)
    if key == 27:
        break
cv2.destroyAllWindows()
# img = cv2.imread('mon.jpg')
# imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
# #im,contours,hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# for c in contours:
#     cv2.drawContours(img, [c], -1, (0, 0, 255), 2)
#     cv2.imshow("bol",img)
colour = input("which colour? :")
file= open(colour+".txt", "w")
file.write(str(H)+","+str(S)+","+str(V)+","+str(h)+","+str(s)+","+str(v))
file.close()
cv2.waitKey(0)

