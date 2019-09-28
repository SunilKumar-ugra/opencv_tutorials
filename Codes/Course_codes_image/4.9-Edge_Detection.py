# Edge Detection using Canny edge detector
# Edges are set of points(lines), where image brightness changes sharply

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Read the image using imread built-in function
image = cv2.imread('image_8.jpg')

# Display original image using imshow built-in function
cv2.imshow("Original", image)

# Wait until any key is pressed
cv2.waitKey(0)

# cv2.Canny is the built-in function used to detect edges
# cv2.Canny(image, threshold_1, threshold_2)
canny = cv2.Canny(image, 150, 255)

# Display edge detected output image using imshow built-in function
cv2.imshow('Canny Edge Detection', canny)

# Wait until any key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
