import math
from time import sleep
from BluetoothController import BluetoothController
import cv2
from Color import Color
from math import *
from Frame import Frame
import numpy as np
import imutils
import mahotas
import time
import ast
class Bot:

    currentBotPos = (0,0)
    currentBotfront= (0,0)
    nextCheckpointPos = (0,0)
    nextCheckpointAngle = 0
    currentCheckpointPos = (0,0)
    currentBotAngle = 0
    direction = 'forward'
    updateProperties = True
    @staticmethod
    def get_direction(bot_angle,target_angle):

        quad1=range(0,91)
        quad2=range(46,91)
        quad3=range(91,136)
        quad4=range(136,181)
        quad5=range(181,226)
        quad6=range(226,271)
        quad7=range(271,316)
        quad8=range(316,361)

        flag=0
        if bot_angle in quad1 and target_angle in quad1:
            flag=1
        elif bot_angle in quad2 and target_angle in quad2:
            flag=1
        elif bot_angle in quad3 and target_angle in quad3:
            flag=1
        elif bot_angle in quad4 and target_angle in quad4:
            flag=1
        elif bot_angle in quad5 and target_angle in quad5:
            flag=1
        elif bot_angle in quad6 and target_angle in quad6:
            flag=1
        elif bot_angle in quad7 and target_angle in quad7:
            flag=1
        elif bot_angle in quad8 and target_angle in quad8:
            flag=1

        if flag==1:
            return 'F'
        elif bot_angle in quad1 and target_angle in quad2:
            return 'I'
        elif bot_angle in quad2 and target_angle in quad3:
            return 'I'
        elif bot_angle in quad3 and target_angle in quad4:
            return 'I'
        elif bot_angle in quad4 and target_angle in quad5:
            return 'I'
        elif bot_angle in quad5 and target_angle in quad6:
            return 'I'
        elif bot_angle in quad6 and target_angle in quad7:
            return 'I'
        elif bot_angle in quad7 and target_angle in quad8:
            return 'I'
        elif bot_angle in quad8 and target_angle in quad1:
            return 'I'
        else:
            return  'G'


    @staticmethod
    def checkForResource(listOfResources, point):
        for x in listOfResources:
            i=x.real_point
            if (i[0], i[1]) == point:
                return x.shape

    @staticmethod
    def check_quad(val):
        if val in range(0,46):
            return 1
        elif val in range(46,91):
            return 2
        elif val in range(91,136):
            return 3
        elif val in range(136,181):
            return 4
        elif val in range(181,226):
            return 5
        elif val in range(226,271):
            return 6
        elif val in range(271,316):
            return 7
        elif val in range(316,361):
            return 8

    @staticmethod
    def kgp_traverse(pathList):
        for i, point in enumerate(pathList):
            bot_center,bot_back,bot_front = Bot.currentPos()
            bot_angle = Bot.angleBetweenPoints(bot_back, bot_front)
            target_angle = Bot.angleBetweenPoints(bot_center, point)
            direction = 'G'
            while Bot.distance(bot_center,point)>5:
                bot_center,bot_back,bot_front = Bot.currentPos()
                bot_angle = Bot.angleBetweenPoints(bot_back, bot_front)
                target_angle = Bot.angleBetweenPoints(bot_center, point)
                direction = 'G'
                print bot_angle,target_angle
                while Bot.check_quad(bot_angle) != Bot.check_quad(target_angle):
                    print bot_angle,target_angle
                    bot_center,bot_back,bot_front = Bot.currentPos()
                    bot_angle = Bot.angleBetweenPoints(bot_back, bot_front)
                    # target_angle = Bot.angleBetweenPoints(bot_center, point)
                    direction = 'G'
                    BluetoothController.send_command(direction)
                BluetoothController.send_command('FFFF')
            Bot.Stop()



    @staticmethod
    def traversePath(pathList):
        lastPoint = len(pathList) - 1
        for point in pathList:
            print point
            Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
            while Bot.distance(Bot.currentBotPos, point) >  17:
                print Bot.distance(Bot.currentBotPos, point)
                Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
                while abs(Bot.angleBetweenPoints(Bot.currentBotPos,Bot.currentBotfront)-Bot.angleBetweenPoints(Bot.currentBotPos, point)) >30:
                    print Bot.angleBetweenPoints(Bot.currentBotPos,Bot.currentBotfront),Bot.angleBetweenPoints(Bot.currentBotPos, point)
                    Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
                    print point
                    if Bot.angleBetweenPoints(Bot.currentBotPos, point) in range (225,315):
                        Bot.moveDirection('left', True,point)
                    elif Bot.angleBetweenPoints(Bot.currentBotPos,Bot.currentBotfront)-Bot.angleBetweenPoints(Bot.currentBotPos, point)<0:
                        Bot.moveDirection('left', True,point)
                        Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
                    else:
                        Bot.moveDirection('right', True,point)
                        Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
                Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()

                Bot.moveDirection('forward', True,point)

                #Bot.moveDirection('forward', True,point)
                Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()

            Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()


    @staticmethod
    def Blink(color):
        BluetoothController.send_command(color)
    @staticmethod
    def Stop():
        BluetoothController.send_command("S")

    @staticmethod
    def get_HW():
        fil=open("crop.txt","r")
        data=fil.read().split(',')
        y1=int(data[0])
        y2=int(data[1])
        x1=int(data[2])
        x2=int(data[3])
        rot=int(data[4])
        width = x2-x1
        height = y2-y1
        fil.close()
        return(width,height)

    @staticmethod
    def inRange(point1, point2):
        x,y = Bot.get_HW()
        k=16
        if point1[0] in range(point2[0] - x/k, point2[0] + x/k) and point1[1] in range(point2[1] - y/k, point2[1] + y/k):
            return True
        else:
            return False



    @staticmethod
    def distance(point1, point2):
        distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        return distance

    @staticmethod
    def traverse_new(res,path):
        flag=0
        bot_center,bot_back,bot_front = Bot.currentPos()
        path = [bot_center] + path
        for i,point in zip(range(0,len(path)-1),path):
            target_point = path[i+1]
            bot_center,bot_back,bot_front = Bot.currentPos()
            bot_center,Bot_angle= Bot.UpdateProperties()
            target_angle= Bot.angleBetweenPoints(bot_center,target_point)
            while not Bot.inRange(bot_center,target_point):
                target_angle= Bot.angleBetweenPoints(bot_center,target_point)
                print bot_center,target_point
                bot_center,Bot_angle= Bot.UpdateProperties()
                BluetoothController.send_command('G')
                bot_center,Bot_angle= Bot.UpdateProperties()
                if int(target_angle) in range(340,361)+range(0,40):
                    while( int(Bot_angle) not in range(((target_angle+40)%360),0,-1) + range((target_angle-40)%360,361)):
                        print "S1"
                        BluetoothController.send_command('G')
                        bot_center,Bot_angle= Bot.UpdateProperties()
                        BluetoothController.send_command('S')
                else:
                    while int(Bot_angle) not in range((((target_angle-40)%360)),((target_angle+40)%360)):
                        bot_center,Bot_angle = Bot.UpdateProperties()
                        if Bot_angle<41 and Bot_angle>340 and target_angle<41 and target_angle>340:
                            BluetoothController.send_command('F')
                        elif Bot_angle>((target_angle+30)%360) and ((target_angle+30)%360) < 226:
                            print Bot_angle,target_angle
                            print "S2"
                            BluetoothController.send_command('F')
                            BluetoothController.send_command('G')
                        else:
                            BluetoothController.send_command('G')
                        target_angle= Bot.angleBetweenPoints(bot_center,target_point)
                        bot_center,Bot_angle= Bot.UpdateProperties()
                target_angle= Bot.angleBetweenPoints(bot_center,target_point)
                BluetoothController.send_command('F')
                BluetoothController.send_command('F')
                bot_center,Bot_angle= Bot.UpdateProperties()
            Bot.Stop()
            if(target_point in res):
                print "point as res:"+str(target_point)
                flag = flag +1
                for n in range(0,flag):
                    BluetoothController.send_command('V')
                    BluetoothController.send_command('W')
                    sleep(0.4)
                    BluetoothController.send_command('v')
                    BluetoothController.send_command('w')


    @staticmethod
    def midPoint(point1, point2):
        midPoint = (((point1[0] + point2[0]) / 2), ((point1[1] + point2[1]) / 2))
        return midPoint

    @staticmethod
    def angleBetweenPoints(origin, position):
        '''
        param-origin [Type-Point], position [Type-Point]
        returns-angleInDegrees [Type-float], dist [Type-float]
        Uses simple tan inverse function to find the angle then maps it to a proper angle between 0 to 360.
        '''

        deltaY = position[1] - origin[1]
        deltaX = position[0] - origin[0]
        angleInDegrees = round(atan2(deltaY, deltaX) * float(180) / 3.14)
        if angleInDegrees < 0:
            # angle is in I and II Quad, ie between 0 to -180, so map it to 0,180
            angleInDegrees = Bot.map(angleInDegrees, 0, -180, 0, 180)
        else:
            # angle is in III and IV Quad, ie between 0 to -180, so map it to 360,180
            angleInDegrees = Bot.map(angleInDegrees, 0, 180, 360, 180)
        return angleInDegrees

    @staticmethod
    def map(value, in_min, in_max, out_min, out_max):
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    @staticmethod
    def moveDirection(direction, updateProperties=True,point=None):
        '''
        param-direction [Type-str] - pass direction of the bot, updateProperties [Type-bool, default = True]
        returns-None
        Also, if the bot is not in the camera range, the updateProperties parameter is False so that the position is not
        updated again. Based on the direction that the bot had to run, it sends the command to move in that direction. Usually forward
        or any other direction
        '''
        # Bot.setBotSpeed(Config.moveSpeed)

        if direction == 'forward':
            BluetoothController.send_command('F')
        elif direction == 'right':
            BluetoothController.send_command('G')
        elif direction == 'left':
            BluetoothController.send_command('I')
        else:
            BluetoothController.send_command(Bot.direction, "direction: " + Bot.direction)
        if updateProperties == True:
            Bot.UpdateProperties(point)

    @staticmethod
    def get_bot_front():
        max_area = 0
        min_area = 10000

        colour = "pink"

        f=open(colour + ".txt","r")
        data=f.read().split(',')
        H=int(data[0])
        S=int(data[1])
        V=int(data[2])
        h=int(data[3])
        s=int(data[4])
        v=int(data[5])
        f.close()

        higher = np.array([H, S, V])
        lower = np.array([h, s, v])
        list_of_points = []
        Frame.capture_frame()
        resized = Frame.cut
        ratio = 1


        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        #t = cv2.getTrackbarPos('t','img')

        mask = cv2.inRange(hsv, lower, higher)

        res = cv2.bitwise_and(resized,resized, mask= mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        T=mahotas.thresholding.otsu(blurred)
        b=blurred.copy()
        b[b>T]=255
        b[b<255]=0

        cnts = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        area = 0
        cX = 0
        cY = 0
        for c in cnts:
            M = cv2.moments(c)
            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"] + 1e-7) * ratio)
                cY = int((M["m01"] / M["m00"] + 1e-7) * ratio)
                #shape = sd.detect(c)
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area = cv2.contourArea(c)
                #rad = getRadFromArea(area)
                if area>300:
                    #cv2.drawContours(resized, [c], -1, (255,0,0), 2)
                    list_of_points.append((cX, cY))


        if len(list_of_points)>0:
            bot_front = list_of_points[0]
            return bot_front
        else:
            return Bot.get_bot_front()
    @staticmethod
    def get_bot_back():
        max_area = 0
        min_area = 10000

        colour = "lgreen"
        f=open(colour + ".txt","r")
        data=f.read().split(',')
        H=int(data[0])
        S=int(data[1])
        V=int(data[2])
        h=int(data[3])
        s=int(data[4])
        v=int(data[5])
        f.close()

        higher = np.array([H, S, V])
        lower = np.array([h, s, v])

        list_of_points = []
        Frame.capture_frame()
        resized = Frame.cut
        ratio = 1

        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        #t = cv2.getTrackbarPos('t','img')

        mask = cv2.inRange(hsv, lower, higher)

        res = cv2.bitwise_and(resized,resized, mask= mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        T=mahotas.thresholding.otsu(blurred)
        b=blurred.copy()
        b[b>T]=255
        b[b<255]=0

        cnts = cv2.findContours(b, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        area = 0
        cX = 0
        cY = 0
        for c in cnts:
            M = cv2.moments(c)
            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"] + 1e-7) * ratio)
                cY = int((M["m01"] / M["m00"] + 1e-7) * ratio)
                #shape = sd.detect(c)
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area = cv2.contourArea(c)
                #rad = getRadFromArea(area)
                if area>300:
                    #cv2.drawContours(resized, [c], -1, (255,0,0), 2)
                    list_of_points.append((cX, cY))
                    if area > max_area:
                        max_area = area
                    elif area < min_area:
                        if __name__ == '__main__':
                            min_area = area

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        if len(list_of_points)>0:
            bot_back = list_of_points[0]
            return bot_back
        else:
            return Bot.get_bot_back()
    @staticmethod
    def currentPos():
        bot_front = Bot.get_bot_front()

        bot_back = Bot.get_bot_back()
        bot_center = Bot.midPoint(bot_front,bot_back)
        return bot_center,bot_back,bot_front
    @staticmethod
    def UpdateProperties():
        Bot.currentBotPos,_,Bot.currentBotfront = Bot.currentPos()
        botAngle = Bot.angleBetweenPoints(Bot.currentBotPos, Bot.currentBotfront)
        return Bot.currentBotPos, botAngle
