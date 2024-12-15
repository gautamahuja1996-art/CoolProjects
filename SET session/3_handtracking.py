from mediapipe.python.solutions import hands, drawing_utils as easy_draw
import cv2

# making object of class Hands
hand_tracker = hands.Hands(max_num_hands = 2)
# getting video feed
camera = cv2.VideoCapture(2)
framewidth = camera.get(3)
frameheight = camera.get(4)
while camera.isOpened():
    status , frame = camera.read()
    if status:
        frame = cv2.flip(frame , 1)
        frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        result = hand_tracker.process(frame_rgb)

        # results has multiple things, 2 of them are : multi_hand_landmarks and multi_handedness
        detected_hands = result.multi_hand_landmarks
        handedness = result.multi_handedness

        # if there are hands to detect
        if detected_hands != None:
           for hand in detected_hands:
                # easy_draw.draw_landmarks(frame , hand , hands.HAND_CONNECTIONS) # default function to draw landmarks

                for index , landmark in enumerate(hand.landmark):
                    x = int((landmark.x)*framewidth)
                    y = int((landmark.y)*frameheight)
                    cv2.circle(frame , (x,y) , 2 , (255,255,255) , -1)
                    cv2.putText(frame , str(index) , (x,y+10) , cv2.FONT_HERSHEY_SIMPLEX , 0.5 , (255,255,255) , 1 , cv2.LINE_AA)


        cv2.imshow('video feed' , frame)
        code = cv2.waitKey(1)
        if code  ==  ord('q'):
            break

camera.release()
cv2.destroyAllWindows()


