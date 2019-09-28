# Real-time Human Face Recognition - 1
# Capturing images from webcam and storing in human_faces folder

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Load human face cascade file using cv2.CascadeClassifier built-in function
# cv2.CascadeClassifier([filename]) 
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Check if human face cascade file is loaded
if face_detect.empty():
	raise IOError('Unable to haarcascade_frontalface_default.xml file')

# Defining face_detector function 
def face_detector(image):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns the input image
    
    # Convert RGB to gray using cv2.COLOR_BGR2GRAY built-in function
	# BGR (bytes are reversed)
	# cv2.cvtColor: Converts image from one color space to another
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    # Detect objects(faces) of different sizes using cv2.CascadeClassifier.detectMultiScale
    # cv2.CascadeClassifier.detectMultiScale(gray, scaleFactor, minNeighbors)
   
    # scaleFactor: Specifies the image size to be reduced
    # Faces closer to the camera appear bigger than those faces in the back.
    
    # minNeighbors: Specifies the number of neighbors each rectangle should have to retain it
    # Higher value results in less detections but with higher quality
        
    face_detection = face_detect.detectMultiScale(gray, 1.3, 5)
    
    if face_detection is ():
        return None
    
    # Faces are cropped when they detected
    for (x,y,w,h) in face_detection:
        face_cropped = image[y:y+h, x:x+w]

    return face_cropped

# Initializing video capturing object
capture = cv2.VideoCapture(0)
# One camera will be connected by passing 0 OR -1
# Second camera can be selected by passing 2

# Initialize face_count to zero
face_count = 0

# Initialize While Loop and execute until Esc key is pressed OR face_count == 20
while True:
	# Start capturing frames
	ret, capturing = capture.read()
	
	if face_detector(capturing) is not None:
		face_count += 1
		# Resize the frame using cv2.resize built-in function
		# cv2.resize(capturing, output image size, x scale, y scale, interpolation)
		resized_frame = cv2.resize(face_detector(capturing), (250, 250))
		
		# Convert RGB to gray using cv2.COLOR_BGR2GRAY built-in function
		# BGR (bytes are reversed)
		# cv2.cvtColor: Converts image from one color space to another
		gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        # Cropped faces are saved in human_faces folder
        # Unique name is given to each cropped face 
		path = './human_faces/' + str(face_count) + '.jpg'
		
		# Save cropped faces in specified path using imwrite built-in function
		cv2.imwrite(path, gray)
		
        
        # Display face_count on cropped faces using cv2.putText
		#cv2.putText(image, string, orgin, font, fontScale, color, thickness)
		cv2.putText(gray, str(face_count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
		
		# Display cropped faces using imshow built-in function
		cv2.imshow('Cropped', gray)
        
	else:
		print("Face NOT detected")
		pass

	if cv2.waitKey(1) == 27 or face_count == 20: # 27 is the Esc Key
		break
        
# Close the capturing device
capture.release()

# Close all windows
cv2.destroyAllWindows()
   
print("All cropped faces are saved in human_faces folder")
