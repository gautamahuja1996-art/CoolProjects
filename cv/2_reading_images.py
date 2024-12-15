import cv2

# reading images in different formats
color_image = cv2.imread('obama.png', cv2.IMREAD_COLOR)
gray_image = cv2.imread('obama.png', cv2.IMREAD_GRAYSCALE)
unchanged_image = cv2.imread('obama.png', cv2.IMREAD_GRAYSCALE)

# dimension of images
print(color_image.shape)
print(gray_image.shape)
print(unchanged_image.shape)

# showing images
cv2.imshow('color image', color_image)
cv2.imshow('gray image', gray_image)
cv2.imshow('unchanged image', unchanged_image)
cv2.waitKey(0)

cv2.destroyAllWindows()