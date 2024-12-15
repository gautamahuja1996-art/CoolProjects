# There are many ways to do finger counting, but an easy method with some restrictions is using hand
# landmark module

from mediapipe.python.solutions import hands, drawing_utils as easy_draw
import cv2
import os
import numpy as np

# list everything in finger image directory
mylist = os.listdir('finger images')

# making image paths
image_path = []
for element in mylist:
    path = 'finger images' + '\\' + element
    image_path.append(path)

# making an object of type Hands. Passing max hands that can be detected as 2
hand_detector = hands.Hands(max_num_hands=1)

# capturing image
camera = cv2.VideoCapture(0)

# framewidth and height
framewidth = camera.get(3)
frameheight = camera.get(4)

# tip points
finger_tips = [4, 8, 12, 16, 20]


# making a function to get hand_lms
def get_hand_lms(frame, draw_circle=True, draw_points=True):
    # rgb frame needs to detection and tracking
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # getting results
    results = hand_detector.process(frame_rgb)

    # result have 2 things : handedness , list of detected hands with 21 landmarks.hand_detector
    lms_info = results.multi_hand_landmarks
    hand_info = results.multi_handedness

    # lms list
    lms = []

    # if something in lms_info
    if lms_info:

        # the above can have multiple detected hands
        for hand in lms_info:

            # drawing lms
            # easy_draw.draw_landmarks(frame, hand , connections = hands.HAND_CONNECTIONS)

            # hand is a normalised list which contains 21 lms with their coordinates
            # print(type(hand))

            for lms_number, coordinate in enumerate(hand.landmark):

                x = int((coordinate.x) * framewidth)
                y = int((coordinate.y) * frameheight)
                lms.append([x, y])

                # putting circles and number over those lms
                if draw_circle:
                    cv2.circle(frame, (x, y), 3, (255, 255, 255), -1)
                if draw_points:
                    cv2.putText(frame, str(lms_number), (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5,
                                (255, 255, 255))

        return lms


while camera.isOpened():

    status, frame = camera.read()
    if status:
        frame = cv2.flip(frame, 1)
        lms_list = get_hand_lms(frame, False, False)

        # if something is in lms_list
        if lms_list:

            # open fingers check
            open_fingers = [0] * len(finger_tips)

            # checking if thumb is open or closed
            if lms_list[4][0] > lms_list[3][0]:
                open_fingers[0] = 1

            # checking if other fingers are open or not
            for i in range(1, len(finger_tips)):
                if lms_list[finger_tips[i]][1] < lms_list[finger_tips[i] - 2][1]:
                    open_fingers[i] = 1

            # print(open_fingers)

            # counting how many fingers are open. How many 1s' in the list, using .count() method
            finger_count = open_fingers.count(1)
            # print(finger_count)

            # printing image according to fingers open
            mypath = image_path[finger_count - 1]
            myimage = cv2.imread(mypath)
            height, width, channel = myimage.shape

            # before replacing in frame, take frame area in myimage, where its black
            # myimage = np.where(myimage  ==  0 , frame , myimage)
            frame[0:height, 0:width] = myimage

        cv2.imshow('feed', frame)
        code = cv2.waitKey(1)
        if code == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()

