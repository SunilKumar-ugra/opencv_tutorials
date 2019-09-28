# Load, Display and Save Images

# Import Computer Vision package - cv2
import cv2

# Read the image using imread built-in function
image = cv2.imread('image_1.jpg')

# Display original image using imshow built-in function
cv2.imshow("name", image)

# Wait until any key is pressed


# Save the image using imwrite built-in function
cv2.imwrite("Saved Image.jpg", image)
cv2.waitKey(0)
