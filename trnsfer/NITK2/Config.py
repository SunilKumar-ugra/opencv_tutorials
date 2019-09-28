class Config(object):
    
    
    #grid size > devide the arena into given value. Higher the value slower path finding and more resolution (Not required!! )
    gridSize = 14 #CHANGE THIS for new AREANA (3m X 3m) may be 35?

    #path optimizer value
    pathTolerance = 1.3
    # boundry of obtstacle
    obstacleRange =  1 #may be 4? for 3X3 arena | Reduce this if you get came_from[target] error!
    chkptRange =  10
    #max speed 255
    # reduce for 200 RPM Motors!!!!!!
    moveSpeed = 40
    moveSpeedNear = moveSpeed - 10 #When bot is closer to the target
    turnSpeed = 35
    reduceSpeedAt = 20
    # + or - angle for target
    targetAngleRange = 8

    goToResourceTwice = False   #if True Bot will go to resource twice

    resourcePositionRange = 25  # within 25X25, looks fine for current arena
    
    
    mapRatio = 1
    FrameWidth = 500 * mapRatio
    FrameHeight = 500

    #static DO NOT CHANGE !!!
    mappedWidth = 30 #FrameWidth * mapRatio
    mappedHeight = 30 #FrameWidth
    findPathOnce = True
    obstacleCount = 0
    obstacleList = None
    resourceList = None
    obstacleBoundingPointList = []
    chkptBoundingPointList = []
    startTime = None
    endTime = None

