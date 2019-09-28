import cv2


img=cv2.imread("mon.jpg")
height,width=img.shape[:2]
print height,width

# vid= cv2.VideoCapture(0)
#
# while 1:
#     ret,frame=vid.read()
#     height,width=frame.shape[:2]
#     print height,width
#     cv2.imshow("pkdk",frame)
