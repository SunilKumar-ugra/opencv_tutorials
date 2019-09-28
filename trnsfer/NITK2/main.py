
# DO NOT CHANGE CODE UNLESS IT IS NECESSARY!!!!! 
# CALL ME IF YOU HAVE ANY DOUBTS!! PHONE no 992075227 :)
# ALL CONFIGURATION OPTIONS ARE AVAILABLE IN Config.py.

# I have not tried updated sorting algorithms!!!!
# If you think this program works, cool. If it doesn't work, that's too bad
# ALL THE BEST :)

import math
from time import sleep
import cv2
from Area import Area
from AStar import *
from BluetoothController import BluetoothController
from BotController import Bot
from Checkpoint import Checkpoint, CheckpointType
from ImageProcess import Frame
from Point import Point
import trig


#
# connect Bluetooth
BluetoothController.connect()
Bot.Stop()
#sleep(1)
Bot.setBotSpeed(50)
sleep(1)

Frame.connect(1)
Bot.resource = CheckpointType("Resource", "white",(0,255,255))
Bot.obstacle = CheckpointType("Obstacle", "red",(255,0,0))
Bot.botFront = CheckpointType('botFront', 'yellow',(0,255,0))
Bot.botBack = CheckpointType('botBack', 'pink',(0,0,255))

# Bot.position.x = (Bot.botBack.center.x + Bot.botFront.center.x) / 2
# Bot.position.y = (Bot.botBack.center.y + Bot.botFront.center.y) / 2
# print Bot.position.x,Bot.position.y

# raw_input("Start ?????? Press Enter to continue.... : ")





Frame.capture_frame()
Frame.townHall = Checkpoint(0,Point(315,315),0,0,0)
#(315,315)

#initially find center of townhall by finding bot center
Resource_List,Obstacle_List,checkPoint_List,Safe_List=trig.findgrid()
sleep(2)

Bot.UpdateProperties()


print "finish"

obstacle_checkPoints = Obstacle_List
Config.obstacleList = obstacle_checkPoints

Config.obstacleCount = len(obstacle_checkPoints)
print(Config.obstacleCount)
#do Astar Search in the beggining

resource_checkPoints = Resource_List
Config.resourceList = resource_checkPoints
Config.resourceCount = len(resource_checkPoints)
print(Config.resourceCount )

Frame.show_frame()

endResource=None
max_distance=0
cv2.waitKey(0)
# raw_input("Start ?????? Press Enter to continue 2.... : ")
previous_res=Frame.townHall.center
print "obstacle count:" + str(Config.obstacleCount)
if(Config.obstacleCount > 0):
    for resource in resource_checkPoints:
        print("From " +Utils.mapPoint(Frame.townHall.center).toString() )
        print("to " +Utils.mapPoint(resource.center).toString() )
        cv2.circle(Frame.pathplan,Utils.mapPoint(Frame.townHall.center).get_coordinate(),5,(0,0,255),2,4)#Config.mappedWidth Config.mappedHeight
        optimizedAStarPath = AStar.search(Utils.mapPoint(previous_res).get_coordinate(), Utils.mapPoint(resource.center).get_coordinate(), Config.mappedHeight, Config.mappedWidth, obstacle_checkPoints)
        if optimizedAStarPath== None:
            print "failed to find optimized path"
            continue
        print "Found Path"
        distance = Draw.path(optimizedAStarPath)
        finalPath, noOfSkips = Utils.generatePath(previous_res, resource.center,optimizedAStarPath)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips
        resource.distance = distance
        print "resource distance " + str(distance)
        if distance>max_distance:
            max_distance=distance
            endResource=resource
        #previous_res= resource.center
        Frame.show_frame()
        #cv2.waitKey(0)
    #now sort the resources withrespect to the updated distance
    resource_checkPoints.sort()
    #>>>> Call your updated sorting HERE (LEVEL 2)!!!!! Do not change if you dont want to try new algos. 
    # >>>> HERE <<<<<<<      Utils.arena_two_sort(resource_checkPoints)
    #save sorted list
    Config.resourceList = resource_checkPoints
else:
    for resource in resource_checkPoints:
        finalPath, noOfSkips = Utils.generatePath(Frame.townHall.center, resource.center)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips

#for chkpt in checkPoint_List:
all_chkpt=Grid.find_chkpt(checkPoint_List,0)
Draw.boundingBox(Config.chkptBoundingPointList,color=(0,0,255))



    #>>>> Call your updated sorting HERE (LEVEL 1)!!!!!
    # >>>> HERE <<<<<<<      Utils.arena_one_sort(resource_checkPoints)

Draw.path2src(endResource.path)
Frame.show_frame()
cv2.waitKey(0)

print "Finished Astar"
## Remove this~!  Only for testing!!!
#sleep(5)

Bot.currentTarget = Checkpoint(0, Point(0, 0), 0, 0, 0)

#initial Run.. covers all resources once (considering only distance)
Bot.Traverse([endResource],obstacle_checkPoints,checkPoint_List)  #checkPoint_List

#call Traverse again with the new sorted resource list

#if you want to travel to Triangles first then squares then use the following sorted
#shape_sorted_resource_checkPoints = Utils.prioritySort(resource_checkPoints) # modified prioritySort. please check Source
#if you want to sort using arena_one_sort
#shape_sorted_resource_checkPoints = Utils.arena_one_sort(resource_checkPoints)
#Bot.Traverse(shape_sorted_resource_checkPoints,obstacle_checkPoints)
