# importing the pytesseract module
# reads text from images using OCR (Optical character recorgnition)
import pytesseract
import cv2

# referring the engine
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

# getting the image: BGR format
img = cv2.imread('book image.jpg')

# converting it to BGR
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# extracting text
text = pytesseract.image_to_string(img)
print(text)

# displaying the image
cv2.imshow('image', img)

# waiting for key press
cv2.waitKey(0)

# destroy all windows
cv2.destroyAllWindows()