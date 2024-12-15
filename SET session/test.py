import cv2
import numpy as np

# Load an image
image = cv2.imread('image.jpeg', cv2.IMREAD_GRAYSCALE)

# Apply thresholding
threshold_value = 10 # Set your threshold value here
max_value = 255        # Maximum value for pixels after thresholding
ret, thresholded = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY)

# Display the original and thresholded images
cv2.imshow('Original Image', image)
cv2.imshow('Thresholded Image', thresholded)
cv2.waitKey(0)
cv2.destroyAllWindows()
