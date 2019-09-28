# Bitwise Operations - AND, OR, XOR, NOT

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# np.zeros(shape, dtype)
rectangle = np.zeros((200, 200), np.uint8)
# dimension of the rectangle is 200 x 200
# uint8: is an unsigned integer (0 to 255)

# Creating rectangle using cv2.rectangle built-in function
# cv2.rectangle(image, (x1,y1), (x2,y2), color, thickness)
cv2.rectangle(rectangle, (20, 20), (180, 180), 255, -1)
# Display created rectangle 
cv2.imshow("Rect", rectangle)

# Wait until any key is pressed
cv2.waitKey(0)

# np.zeros(shape, dtype)
circle = np.zeros((200, 200), dtype = "uint8")
# dimension of the circle is 200 x 200
# uint8: is an unsigned integer (0 to 255)

# Creating circle using cv2.circle built-in function
# cv2.circle(image, centre, radius, color, thickness)
cv2.circle(circle, (100, 100), 100, 255, -1)

# Display created circle 
cv2.imshow("Circle", circle)

# Wait until any key is pressed
cv2.waitKey(0)

# Performing bitwise AND operation on rectangle, circle
# cv2.bitwise_and(src1, src2)
And = cv2.bitwise_and(rectangle, circle)

# AND operation
# A B Output
# 0 0 0
# 0 1 0
# 1 0 0
# 1 1 1 

# Display AND operation result on rectangle, circle
cv2.imshow("AND", And)

# Wait until any key is pressed
cv2.waitKey(0)

# Performing bitwise OR operation on rectangle, circle
# cv2.bitwise_or(src1, src2)
Or = cv2.bitwise_or(rectangle, circle)

# OR operation
# A B Output
# 0 0 0
# 0 1 1
# 1 0 1
# 1 1 1 

# Display OR operation result
cv2.imshow("OR", Or)

# Wait until any key is pressed
cv2.waitKey(0) 

# Performing bitwise XOR operation on rectangle, circle
# cv2.bitwise_xor(src1, src2)
Xor = cv2.bitwise_xor(rectangle, circle)

# XOR operation
# A B Output
# 0 0 0
# 0 1 1
# 1 0 1
# 1 1 0 

# Display XOR operation result
cv2.imshow("XOR", Xor)

# Wait until any key is pressed
cv2.waitKey(0) 

# Performing bitwise NOT operation on rectangle
# cv2.bitwise_not(src1)
Not_rect = cv2.bitwise_not(rectangle)

# NOT operation
# A Output
# 0 1
# 1 0

# Display NOT operation result on rectangle
cv2.imshow("NOT1", Not_rect)

# Wait until any key is pressed
cv2.waitKey(0) 

# Performing bitwise NOT operation on circle
# cv2.bitwise_not(src1)
Not_circ = cv2.bitwise_not(circle)

# NOT operation
# A Output
# 0 1
# 1 0

# Display NOT operation result on circle
cv2.imshow("NOT2", Not_circ)

# Wait until any key is pressed
cv2.waitKey(0) 

# Close all windows
cv2.destroyAllWindows()

