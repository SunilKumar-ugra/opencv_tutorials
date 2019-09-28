import cv2
import numpy as np
import mahotas
import imutils

img = cv2.imread('11.png',0)
kernel = np.ones((3,3),np.uint8)

dilation = cv2.dilate(img,kernel,iterations = 5)
erosion = cv2.erode(dilation,kernel,iterations = 5)

img2 = cv2.imread('LOL.png')

gray =cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#ret, thresh = cv2.threshold(gray, 70, 255,0)

T = mahotas.thresholding.otsu(gray)
thresh = gray.copy()
thresh[thresh > T] = 255


thresh[thresh < 255] = 0

(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)

con = img2.copy()


for (i, c) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)
    coin = thresh[y:y + h, x:x + w]

    mask = np.zeros(thresh.shape[:2], dtype = "uint8")


    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius),
    255, -1)
    mask = mask[y:y + h, x:x + w]
    cv2.imshow("Masked Coin", cv2.bitwise_and(coin, coin, mask =
    mask))
    cv2.waitKey(0)
    resized = imutils.resize( cv2.bitwise_and(coin, coin, mask =mask),width=50,height=50)
    cv2.imwrite("image_contours/"+str(i)+".png",resized)

(_, cnts, _) = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)

con = erosion.copy()

for (i, c) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)
    coin = erosion[y:y + h, x:x + w]

    mask = np.zeros(erosion.shape[:2], dtype = "uint8")


    ((centerX, centerY), radius) = cv2.minEnclosingCircle(c)
    cv2.circle(mask, (int(centerX), int(centerY)), int(radius),
    255, -1)
    mask = mask[y:y + h, x:x + w]
    cv2.imshow("Masked Coin", cv2.bitwise_and(coin, coin, mask =
    mask))
    cv2.waitKey(0)
    resized = imutils.resize( cv2.bitwise_and(coin, coin, mask =mask),width=50)
    cv2.imwrite("arena_contours/"+str(i)+".png",resized)


###########################################################################################################################################################################

import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),0)
        if img is not None:
            images.append(img)
    return images

image_contours= load_images_from_folder("image_contours")
arena_contours= load_images_from_folder("arena_contours")
matches={}
for (i,iimage) in enumerate(image_contours):
    least=0.5
    least_img=None
    for (a,aimage) in enumerate(arena_contours):
        for angle in range(0,360):
            rotated = imutils.rotate_bound(aimage,angle)
            _,contours,hierarchy = cv2.findContours(iimage,2,1)
            cnt1 = contours[0]
            _,contours,hierarchy = cv2.findContours(rotated,2,1)
            cnt2 = contours[0]
            ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
            if ret < least:
                least=ret
                matches[i]=(a,angle,ret)

print matches
        



