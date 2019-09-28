def getCrop():
    
    #cap = cv2.
    #cap.set(3,1024)
    #cap.set(4,768)

    #cv2.namedWindow('image')
    #ret, resized = cap.read(1)
    
    resized=cv2.imread("nitk.jpg")

    cv2.namedWindow('image')
    cv2.createTrackbar('x1','image',0,resized.shape[1],nothing)
    cv2.createTrackbar('y1','image',0,resized.shape[0],nothing)
    cv2.createTrackbar('x2','image',1,resized.shape[1],nothing)
    cv2.createTrackbar('y2','image',1,resized.shape[0],nothing)

    x1,y1=0,0
    (x2,y2)=resized.shape[:2]
    rot=0

    while(True):
        # Capture frame-by-frame
        #ret, resized = cap.read(1)
        #resized=cv2.imread("cropped.png")

        #to know which part we are extracting from original image lets draw a rectangle 
        black = (0, 0, 0)

        x1 = cv2.getTrackbarPos('x1','image')
        y1 = cv2.getTrackbarPos('y1','image')
        x2= cv2.getTrackbarPos('x2','image')        
        y2 = cv2.getTrackbarPos('y2','image')

        cv2.rectangle(resized,  (x1,y1), (x2, y2), black,2)
        cv2.imshow('mask',resized)
        black = (0, 0, 0)
        cv2.rectangle(resized,  (x1,y1), (x2, y2), black,2)
        if x2>x1 and y2>y1:
            cropped = resized[y1:y2 , x1:x2]
            cv2.imshow('cropped',cropped)
        p=open( "crop.txt","w")
        p.write(str(y1)+','+str(y2)+','+str(x1)+','+str(x2)+','+str(rot))
        p.close()
        #here we extracta rectangular region of the image, starting at (150, 113) and ending at (200, 200).
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print "crop done"
            cv2.destroyAllWindows()
            break
    cv2.namedWindow('img')
    cv2.createTrackbar('rot','img',0,360,nothing)
    while(True):
        # Capture frame-by-frame
        #ret, resized = cap.read(1)
        #resized=cv2.imread("cropped.png")
        cropped = resized[y1:y2 , x1:x2]
        rot = cv2.getTrackbarPos('rot','img')
        resized=imutils.rotate_bound(cropped,rot)
        cv2.imshow('cropped',resized)
        p=open( "crop.txt","w")
        p.write(str(y1)+','+str(y2)+','+str(x1)+','+str(x2)+','+str(rot))
        p.close()
        #here we extracta rectangular region of the image, starting at (150, 113) and ending at (200, 200).
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print "rotate done"
            break


        #cv2.imwrite('image_test.png',resized)
    # When everything done, release the capture
    #cap.release()
    cv2.destroyAllWindows()
    return y1,y2,x1,x2,rot