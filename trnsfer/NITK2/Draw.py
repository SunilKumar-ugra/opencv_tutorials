import cv2
from ImageProcess import Frame
from Utils import Utils
from Point import Point
import numpy as np

class Draw(object):
    @staticmethod
    def path(listOfTuples):
        if listOfTuples == None:
            return
        i = 0
        distance = 0
        while(i < (len(listOfTuples) - 1)):
            cv2.arrowedLine(Frame.pathplan, listOfTuples[i],listOfTuples[i + 1],(0,255,255),1,8,0,0.1)
            distance += Utils.distance(Point(listOfTuples[i][0], listOfTuples[i][1]), Point(listOfTuples[i + 1][0], listOfTuples[i + 1][1]))
            i += 1
        return distance
    @staticmethod
    def path2src(listOfTuples):
        if listOfTuples == None:
            return
        i = 0
        distance = 0
        # print(listOfTuples[0])
        while(i < (len(listOfTuples) - 1)):
            cv2.arrowedLine(Frame.src, listOfTuples[i].get_coordinate(),listOfTuples[i + 1].get_coordinate(),(0,255,255),3,8,0,0.1)
            #distance += Utils.distance(Point(listOfTuples[i][0], listOfTuples[i][1]), Point(listOfTuples[i + 1][0], listOfTuples[i + 1][1]))
            i += 1
        return 0
    @staticmethod
    def circle(listOfTuples):
        if listOfTuples != None:
            for point in listOfTuples:
                cv2.circle(Frame.pathplan, point.get_coordinate(),5,(0,0,255),2,4)
    @staticmethod
    def line(box,remap = False):
        if remap:
            for point in box:
                point = Utils.remapPoint(Point(point[0],point[1])).get_coordinate()
        cv2.arrowedLine(Frame.pathplan,box[0],box[1],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.pathplan,box[2],box[3],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.pathplan,box[0],box[2],(255,255,25), 1,0,0,0.1)
        cv2.arrowedLine(Frame.pathplan,box[1],box[3],(255,255,25), 1,0,0,0.1)
    
    @staticmethod
    def boundingBox(boundingBoxList,remap = True,color = (255,255,255)): #[ (TUPLE,TUPLE), .... ]
        for point in boundingBoxList:
            if remap:
                point = (Utils.remapPoint(Point(point[0][0],point[0][1])).get_coordinate(),Utils.remapPoint(Point(point[1][0],point[1][1])).get_coordinate())
            cv2.arrowedLine(Frame.pathplan,point[0],point[1],color, 1,1,0,0.1)
if __name__ == "__main__":
    path = []
    path.append((0,0))
    path.append((3,4))
    path.append((0,0))
    print Draw.path(path)
