import cv2
from mediapipe.python.solutions import hands, drawing_utils
import numpy as np

# hand detector
hand_detector = hands.Hands(max_num_hands=1)

# reading top color palette and getting its dimensions
palette = cv2.imread('virtual painting.png')
palette_height, palette_width, channel = palette.shape

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
tip_points = [8, 12]
xp = 0
yp = 0
draw_color = (0, 0, 255)
pen_width = 2

# creating an empty canvas
canvas = np.zeros((frame_height, frame_width, 3), np.uint8)

while cam.isOpened():

    # getting feed
    status, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame[0:palette_height, 0:palette_width] = palette
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # getting landmark list
    result = hand_detector.process(frame_rgb)
    detected_hands = result.multi_hand_landmarks
    handedness = result.multi_handedness
    landmark_list = []
    if detected_hands:
        for hand in detected_hands:
            # drawing_utils.draw_landmarks(frame, hand, hands.HAND_CONNECTIONS)
            for coordinate in hand.landmark:
                x_val = int(coordinate.x * frame_width)
                y_val = int(coordinate.y * frame_height)
                landmark_list.append((x_val, y_val))

        # checking which fingers are up
        finger_up = [0]*2
        for tip_point in tip_points:
            index = tip_points.index(tip_point)
            if landmark_list[tip_point][1] < landmark_list[tip_point-2][1]:
                finger_up[index] = 1
            else:
                finger_up[index] = 0

        # coordinates on index and middle finger
        x_index = landmark_list[8][0]
        y_index = landmark_list[8][1]
        x_middle = landmark_list[12][0]
        y_middle = landmark_list[12][1]
        index_finger = (x_index, y_index)
        middle_finger = (x_middle, y_middle)

        # selection and drawing mode
        if finger_up[0] == 1 and finger_up[1] == 1:  # selection mode
            if y_index < 90:  # selecting from palette
                if 0 < x_index <= 150:
                    draw_color = (0, 0, 255)
                    pen_width = 2
                elif 150 < x_index <= 300:
                    draw_color = (0, 255, 0)
                    pen_width = 2
                elif 300 < x_index <= 450:
                    draw_color = (255, 0, 0)
                    pen_width = 2
                elif 450 < x_index <= 600:
                    draw_color = (0, 0, 0)
                    pen_width = 60
            cv2.line(frame, index_finger, middle_finger, draw_color, 2)
            xp = 0
            yp = 0

        elif finger_up[0] == 1 and finger_up[1] == 0:
            cv2.circle(frame, index_finger, 5, draw_color, -1)
            if xp == 0 and yp == 0:
                xp = x_index
                yp = y_index
            previous_point = (xp, yp)
            cv2.line(canvas, index_finger, previous_point, draw_color, pen_width)
            xp = x_index
            yp = y_index

    # making changes to the canvas : method 1
    frame = np.where(canvas == 0, frame, canvas)

    # making changes to the canvas : method 2
    # thresholding canvas, only grayscale images can be threshold.
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)  # single channel image
    _, canvas_threshold = cv2.threshold(canvas_gray, 50, 255, cv2.THRESH_BINARY_INV)
    canvas_threshold = cv2.cvtColor(canvas_threshold, cv2.COLOR_GRAY2BGR)  # converting back to 3 channel
    frame = cv2.bitwise_and(frame, canvas_threshold)
    frame = cv2.bitwise_or(frame, canvas)

    # displaying frame
    cv2.imshow('feed', frame)
    # cv2.imshow('canvas', canvas)
    # cv2.imshow('gray canvas', canvas_gray)
    # cv2.imshow('threshold canvas', canvas_threshold)
    code = cv2.waitKey(1)
    if code == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()