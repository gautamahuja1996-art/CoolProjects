'''
1_handtracking.py :

Algorithm used : We can use the distance between upper eye and lower eye point as, if we move forward or
backward, that distance changes, so our system will give wrong results.

Instead, we can apply conditions of ratio of, distance between upper eye and lower eye point, to 
distance between leftmost point of eye and rightmost point of the eye.
'''


# importing FaceMesh class from face_mesh module
from mediapipe.python.solutions import face_mesh , drawing_utils as easy_draw
import cv2

# we have imported face_mesh module, let's import FaceMesh class from it
face_detector = face_mesh.FaceMesh(max_num_faces = 1)

# to calculate distance, import the math module
import math

lefteye_open = True
blink_counter = 0

# capturing video
camera = cv2.VideoCapture(0)
wframe = camera.get(3)
hframe = camera.get(4)

left_eye = [22 , 23 , 24 , 26 , 110 , 157 , 158 , 159 , 160 , 161 , 130 , 243]
lefteye_up_index = 159
lefteye_down_index = 23
lefteye_left_index = 130
lefteye_right_index = 243

# right_eye = []

while camera.isOpened():
    status , frame = camera.read()
    if status:

        # flipping the frame
        frame = cv2.flip(frame , 1)

        # converting frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # getting lms
        result = face_detector.process(frame)
        faces = result.multi_face_landmarks # list of faces and their lms
        
        # if sany face detected
        if faces:
            lms_list = [] # storing all facelms with their indices in a list
            for face in faces: # face is a list of 468 lms

                # let's simply draw face : frame and landmark list of a face
                # easy_draw.draw_landmarks(frame, face)

                for facial_landmark in face.landmark:
                    x = int(facial_landmark.x * wframe)
                    y = int(facial_landmark.y * hframe)
                    lms_list.append((x , y))

                # drawing left eye points
                cv2.circle(frame, lms_list[lefteye_up_index], 1, (255,255,255))
                cv2.circle(frame, lms_list[lefteye_down_index], 1, (255,255,255))
                cv2.circle(frame, lms_list[lefteye_left_index], 1, (255,255,255))
                cv2.circle(frame, lms_list[lefteye_right_index], 1, (255,255,255))
                cv2.line(frame, lms_list[lefteye_up_index] , lms_list[lefteye_down_index] , (0,0,255))
                cv2.line(frame, lms_list[lefteye_left_index] , lms_list[lefteye_right_index] , (0,0,255))

                # finding distance between points
                dist_vertical = math.sqrt(    
                    ((lms_list[lefteye_up_index][0] - lms_list[lefteye_down_index][0])**2)      +    
                    ((lms_list[lefteye_up_index][1] - lms_list[lefteye_down_index][1])**2))

                
                dist_horizontal = math.sqrt(    
                    ((lms_list[lefteye_left_index][0] - lms_list[lefteye_right_index][0])**2)      +    
                    ((lms_list[lefteye_left_index][1] - lms_list[lefteye_right_index][1])**2))


                distance_ratio = int((dist_horizontal / dist_vertical)*100)

                if distance_ratio > 310  and  lefteye_open ==  True:
                    blink_counter = blink_counter + 1
                    print('blink count : ' , blink_counter)
                    lefteye_open = False
                
                elif distance_ratio < 300:
                    lefteye_open = True




            




        cv2.imshow('video feed' , frame)
        code = cv2.waitKey(1)
        if code == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()