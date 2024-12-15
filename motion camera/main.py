# importing the pyserial library
import serial
import time
import cv2

# baud rate and comport
baud_rate = 9600
com_port = 'COM4'

# Creating an object of type serial
myserial = serial.Serial(port=com_port, baudrate=baud_rate)

# let's attach our webcam by creating an object of VideoCapture class
# 0 --> Index or number of Webcam in case of multiple camera
camera = cv2.VideoCapture(0)

# it's a good practice to give some time delay after establishing serial communication
time.sleep(2)

# let's use a loop to accept serial data again and again
while True:

    # let's check if there is any data to read
    # in_waiting --> returns the total characters coming into serial buffer
    if myserial.in_waiting > 0:

        # let's read the data, if it's there
        data = myserial.readline()

        # let's convert the byte data to string
        data = data.decode()

        # let's remove unwanted characters
        data = data.strip()

        # let's take a picture when Arduino sends motion
        if data == "Motion":

            # let's take some time to be ready
            time.sleep(2)

            # let's take a picture
            status, picture = camera.read()

            # let's display the picture
            cv2.imshow('My Image', picture)

            # let's wait until a key is pressed
            cv2.waitKey(0)
