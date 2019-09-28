#top box colour
import cv2
import imutils

img = cv2.imread("red.JPG",1)
imge=cv2.resize(img,(600,612))
cv2.imshow("lol",imge)
cv2.waitKey(0)

cv2.imwrite("pkd.png",img)

corner = img[0:100, 0:100]
mid= img[150:300,250:500]
cv2.imshow("Corner", corner)
cv2.waitKey(0)

img[0:100, 0:100] = (0, 255, 255)
img[150:300,250:500] =(255,0,255)
cv2.imshow("Updated", img)
cv2.waitKey(0)

# fourcc=cv2.cv.CV_FOURCC(*'XVID')
# out = cv2.VedioWriter("output.avi",fourcc,20.0,(680,480))
