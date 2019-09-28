# Real-time Object Detection

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Defining object detector function - ORB 
# ORB - Oriented FAST and Rotated BRIEF

# FAST - Features from Accelerated Segment Test
# BRIEF - Binary Robust Independent Elementary Features 

# FAST keypoint descriptor finds the keypoints
# Descriptors are vectors which store information about the keypoints

# BRIEF is a faster method used for feature descriptor calculation and matching
# ORB - Fusion of FAST keypoint detector & BRIEF descriptor

def ORB(input_image, stored_image):
	# This function compares input image captured from webcam with stored image
	# ORB function returns matches between input image and stored image 
    
    # Convert RGB to gray using cv2.COLOR_BGR2GRAY built-in function
	# BGR (bytes are reversed)
	# cv2.cvtColor: Converts image from one color space to another
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # cv2.ORB is the built-in function used for object detection
    # cv2.ORB(keypoints, scalingfactor) 
    orb_detector = cv2.ORB(1600, 1.3)

    # Detecting keypoints on input image after converting to gray using cv2.ORB.detectAndCompute
    # cv2.ORB.detectAndCompute(gray, mask)
    (keypoints_1, descriptor_1) = orb_detector.detectAndCompute(gray, None)

    # Detecting keypoints on stored image using cv2.ORB.detectAndCompute
    # cv2.ORB.detectAndCompute(stored_image, mask)
    (keypoints_2, descriptor_2) = orb_detector.detectAndCompute(stored_image, None)

    # Brute-Force Matcher is used to match features between 2 images
    # cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck)
    
    # cv2.NORM_HAMMING uses Hamming distance as measurement
    # Hamming distance is the number of points at which
    # the corresponding bits are different
    
    # crossCheck=False by default 
    # True indicates 2 features in input image & stored image match each other
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the two descriptors using cv2.BFMatcher.match built-in function
    # cv2.BFMatcher.match(descriptor_1,descriptor_2)
    matches_found =  brute_force.match(descriptor_1,descriptor_2)

    # Matches found are sorted based on distances, smallest distance is best 
    # sorted(list, key)
    matches_found = sorted(matches_found, key=lambda val: val.distance)

    return len(matches_found)

# Initializing video capturing object
capture = cv2.VideoCapture(0)
# One camera will be connected by passing 0 OR -1
# Second camera can be selected by passing 2

# Load the stored image color image in grayscale
stored_image = cv2.imread('raspberry_pi.jpg', 0) 

while True:
	# Start capturing frames
	ret, capturing = capture.read()
    
    # Height and width of the frames are taken 
	frame_height, frame_width = capturing.shape[:2]

    # Define box dimensions at the center of the frame
	x1_top_left = frame_width / 3
	y1_top_left = (frame_height / 2) + (frame_height / 4)
	x2_bottom_right = (frame_width / 3) * 2
	y2_bottom_right = (frame_height / 2) - (frame_height / 4)
    
    # Rectangular box is drawn around the box dimensions using cv2.rectangle built-in function
    # cv2.rectangle(capturing, (x1,y1), (x2,y2), color, thickness)
	cv2.rectangle(capturing, (int(x1_top_left),int(y1_top_left)), (int(x2_bottom_right),int(y2_bottom_right)), (0,0,255), 4)
    
    # Rectangular box region defined above is cropped 
	cropped_box = capturing[int(y2_bottom_right):int(y1_top_left) ,int( x1_top_left):int(x2_bottom_right)]

    # Captured frame is flipped horizontally using cv2.flip built-in function
	# Horizontal flipping of images using value '1'
	capturing = cv2.flip(capturing,1)
    
    # ORB function is called to find matches 
	matches_found = ORB(cropped_box, stored_image)
    
    # Matches found are displayed using string
	string = "Matches Found = " + str(matches_found)
	# To input a text string cv2.putText is used
	#cv2.putText(image, string, orgin, font, fontScale, color, thickness)
	cv2.putText(capturing, string, (150,400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
    
    # Set threshold value depending on stored image Our threshold to indicate object deteciton
    # For new images or lightening conditions you may need to experiment a bit 
	set_threshold = 400
	# ORB detector gets top 1600 matches, 400 threshold indicates minimum 25% needs to match
    
    # When matches exceed the set threshold value, object is detected
	if matches_found > set_threshold:
		
		# Rectangular box is drawn after object detection using cv2.rectangle built-in function
		# cv2.rectangle(capturing, (x1,y1), (x2,y2), color, thickness)
		cv2.rectangle(capturing, (x1_top_left,y1_top_left), (x2_bottom_right,y2_bottom_right), (0,255,0), 4)
		
		# To input a text string cv2.putText is used
		#cv2.putText(image, string, orgin, font, fontScale, color, thickness)
		cv2.putText(capturing,'Object Detected',(200,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,255,0), 2)
    
	# Display object detected using imshow built-in function
	cv2.imshow('Real-time Object Detection', capturing)
    
    # Check if the user has pressed Esc key
	c = cv2.waitKey(1)
	if c == 27:
		break

# Close the capturing device
capture.release()

# Close all windows
cv2.destroyAllWindows()
