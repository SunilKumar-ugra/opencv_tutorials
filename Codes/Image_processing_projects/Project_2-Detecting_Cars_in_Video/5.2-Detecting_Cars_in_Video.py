# Detecting Cars in Video

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Import Time Python package - time which contains sleep() function
import time

# Load Car cascade file using cv2.CascadeClassifier built-in function
# cv2.CascadeClassifier([filename]) 
cars_detect = cv2.CascadeClassifier('haarcascade_car.xml')

# Initializing video capturing object for video file 
capture = cv2.VideoCapture('cars.avi')

# Initialize While Loop and execute until Esc key is pressed
#VideoCapture.isOpened returns True if the video is successfully opened

while capture.isOpened():

	#time.sleep(secs) 
	# secs- Number of seconds Python program should pause execution
    time.sleep(.05)

    # Start capturing frames
    ret, frame = capture.read()
    
    # Convert RGB to gray using cv2.COLOR_BGR2GRAY built-in function
	# BGR (bytes are reversed)
	# cv2.cvtColor: Converts image from one color space to another
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   
    # Detect objects(cars) of different sizes using cv2.CascadeClassifier.detectMultiScale
    # cv2.CascadeClassifier.detectMultiScale(gray, scaleFactor, minNeighbors)
   
    # scaleFactor: Specifies the image size to be reduced
    # Cars closer to the camera appear bigger than those cars in the back.
    
    # minNeighbors: Specifies the number of neighbors each rectangle should have to retain it
    # Higher value results in less detections but with higher quality
    
    cars_detected = cars_detect.detectMultiScale(gray, 1.4, 2)
    
    # Extract bounding boxes for any bodies identified
    # Rectangles are drawn around the cars using cv2.rectangle built-in function
	# cv2.rectangle(frame, (x1,y1), (x2,y2), color, thickness)
    for (x,y,w,h) in cars_detected:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        
        # Display cars detected using imshow built-in function
        cv2.imshow('Detecting Cars', frame)

    # Check if the user has pressed Esc key
    c = cv2.waitKey(1)
    if c == 27:
        break

# Close the capturing device
capture.release()

# Close all windows
cv2.destroyAllWindows()


