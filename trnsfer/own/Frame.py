import cv2
import imutils

class Frame(object):
    width = None
    height = None

    cam = None
    image = None
    res = None
    ratio = None
    cut = None
    contour = None

    botPosition = None

    @staticmethod
    def connect(cameraID):
        Frame.cam = cv2.VideoCapture(cameraID)

        Frame.cam.set(5, 18)  #frame rate
        Frame.cam.set(10, 130)  #brightness
        Frame.cam.set(12, 255)  #saturation
        '''
        Frame.cam.set(3,1024)
        Frame.cam.set(4,768)
        '''
    @staticmethod
    def capture_frame():
        Frame.res, Frame.image = Frame.cam.read(1)
        '''        cv2.imshow("fr",Frame.image)
        cv2.waitKey(0)'''

        Frame.find_cut()
    
    @staticmethod
    def show_frame():#
        hsv = cv2.cvtColor(Frame.resized, cv2.COLOR_BGR2HSV)
        res = cv2.bitwise_and(Frame.resized,Frame.resized)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #cv2.imwrite("frame.jpg", Frame.resized)
        cv2.imshow("frame", Frame.resized)
        cv2.waitKey(5) & 0xFF
    @staticmethod
    def find_cut():
        fil=open("crop.txt","r")
        data=fil.read().split(',')
        y1=int(data[0])
        y2=int(data[1])
        x1=int(data[2])
        x2=int(data[3])
        rot=int(data[4])
        fil.close()
        Frame.cut = Frame.image[y1:y2, x1:x2]
        Frame.cut = imutils.rotate_bound(Frame.cut, rot)

        Frame.ratio = 1
        Frame.width = Frame.cut.shape[1]
        Frame.height = Frame.cut.shape[0]
        return Frame.image, Frame.cut, Frame.ratio

    @staticmethod
    def disconnect():
        Frame.cam.release()
