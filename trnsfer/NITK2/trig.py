import cv2
import rearea as a
from Checkpoint import Checkpoint, CheckpointType, CheckpointShape
from Point import Point
from ImageProcess import Frame

def findgrid():
    Frame.capture_frame()
    src = Frame.resized
    src = cv2.resize(src,(500,500))
    green=(0, 255, 0)

    height,width= src.shape[:2]
    GRID_SIZE =35
    new_y=0
    #ector<Rect> mCells
    CheckpointType("Resource", "white",(0,255,255))
    CheckpointType("Obstacle", "white",(0,255,255))
    CheckpointType("Checkpoint", "white",(0,255,255))
    CheckpointType("Safe", "white",(0,255,255))

    Resource_List = []
    Obstacle_List = []
    checkPoint_List = []
    Safe_List = []

    for y in range(0,height,GRID_SIZE):  #(y = 0; y < height - GRID_SIZE; y += GRID_SIZE):
        for x in range(0,width,GRID_SIZE): #(x = 0; x < width - GRID_SIZE; x += GRID_SIZE):
            # k = x*y + x
            new_x=x+GRID_SIZE
            new_y=y+GRID_SIZE
            grid_rect=(x,y),(new_x,new_y)
            #print grid_rect
            piece=src[y:new_y,x:new_x]
            point = Point()
            point.x =(x+new_x)/2
            point.y =(y+new_y)/2
            center=((x+new_x)/2,(y+new_y)/2)
            str=a.setarea(piece.copy(),src,center)
            if(str=="Resource"):
                Resource_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
            elif(str=="Obstacle"):
                Obstacle_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
            elif(str=="Checkpoint"):
                checkPoint_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
                # if len(checkPoint_List) == 0:
                #     checkPoint_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
                # else:
                #     for chkpt in  checkPoint_List:
                #         if not Point.chkptinRange(point, chkpt.center):
                #             checkPoint_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
                #             cv2.putText(src,"chkpt",center,cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,255))
                #             break
                #         else:
                #             print "skipped " + point.toString()
                        #    Safe_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
            elif(str=="Safe"):
                Safe_List.append(Checkpoint(0, point, 0, 0, CheckpointShape.SQUARE))
            # cv2.imshow("PART", piece)
            # cv2.waitKey(0)

            cv2.rectangle(src, (x,y),(new_x,new_y), green , 1)

            #cv2.imshow("src", src)


            # cv2.imshow(format("grid%d",k), src(grid_rect))
            # cv2.waitKey(0)
    cv2.imshow("src", src)
    #cv2.waitKey(0)
    Frame.src = src
    return Resource_List,Obstacle_List,checkPoint_List,Safe_List



# 00 5050
# 500 100100
# 1000 200200
