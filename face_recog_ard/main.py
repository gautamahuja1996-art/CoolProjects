import cv2
import numpy as np
import tensorflow as tf
import serial
import time

# Initialize Arduino connection
arduino = serial.Serial('COM3', 9600)  # Adjust 'COM3' with your Arduino's port

# Load the Teachable Machine model
model_path = 'path_to_your_model_directory'  # Replace with the actual path
model = tf.keras.models.load_model(model_path)

# Initialize your webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Preprocess the frame (resize, normalize pixel values, etc.)
    frame = cv2.resize(frame, (224, 224))  # Adjust the size to match the model input size
    frame = frame / 255.0  # Normalize pixel values to [0, 1]

    # Make a prediction using the model
    prediction = model.predict(np.expand_dims(frame, axis=0))

    # Extract the class with the highest probability
    predicted_class = np.argmax(prediction)

    # Control Arduino based on the predicted class
    if predicted_class == 0:  # Assuming class 0 corresponds to 'Your Face'
        arduino.write(b'G')  # Send 'G' to Arduino for green light
    else:
        arduino.write(b'R')  # Send 'R' to Arduino for red light

    # Display the frame with the result
    cv2.imshow('Frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close windows
cap.release()
cv2.destroyAllWindows()
