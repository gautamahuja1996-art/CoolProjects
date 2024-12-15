# creating virtual mouse application
'''
1_handtracking.py :

structure of lminfo or results.multi_hand_landmarks:
[landmark{x1,y1,z1}landmark{x2,y2,z2}.....landmark{x20,y20,z20} , landmark{x1,y1,z1}landmark{x2,y2,z2}...landmark{x20,y20,z20}] : [hand1_lms , hand2_lms]


for hand in lminfo:
    print(hand)

structure of hand in case of 2 hands: 
landmark{x1,y1,z1}landmark{x2,y2,z2}.....landmark{x20,y20,z20}  
landmark{x1,y1,z1}landmark{x2,y2,z2}.....landmark{x20,y20,z20} 

'''
from mediapipe.python.solutions import hands , drawing_utils as easy_draw

import cv2
import time # to calculate fps
import autopy # to operate mouse
import numpy as np # for mapping ranges

camera = cv2.VideoCapture(0)
wframe = camera.get(3)
hframe = camera.get(4)
wframe = int(wframe)
hframe = int(hframe)

# object of type Hands
handtracker = hands.Hands(max_num_hands = 2 , min_detection_confidence=0.7 , min_tracking_confidence=0.7)

# previous time
ptime = 0

# finger tip index
finger_tip_index = [4,8,12,16,20]

# smoothening threshold
smoothening_constant = 7
plocx = 0
plocy = 0
clocx = 0
clocy = 0

# getting screen size
wscreen , hscreen = autopy.screen.size()
wscreen = int(wscreen)
hscreen = int(hscreen)

# points to be drawn
def draw_points(frame , lmlist , index_of_points , color = (255,0,0) , radius = 3):

    for index in index_of_points:
        cv2.circle(frame, (lmlist[index][0] , lmlist[index][1]), radius, color , -1)


# if camera is connected
while camera.isOpened():

    lmlist = [] # landmark list at the beginning of every frame
    open_status = [0]*len(finger_tip_index) # finger open or not, initially all closed : [0,0,0,0,0]
    status , frame = camera.read()
    if status:
        frame = cv2.flip(frame , 1)

        # converting frame to rgb format
        frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        result = handtracker.process(frame_rgb)
        lminfo = result.multi_hand_landmarks
        handinfo = result.multi_handedness

        # if something in lminfo [list of detected hands with its 21 landmarks]
        if lminfo:
            for hand in lminfo:
                for coordinate in hand.landmark:
                    x = int(coordinate.x*wframe)
                    y = int(coordinate.y*hframe)
                    lmlist.append((x,y))

            # drawing all landmarks
            # draw_points(frame, lmlist , [4,8,12,16,20])
            
            # checking if fingers are up or not
            for tip_index in finger_tip_index:
                if tip_index  ==  4:  # thumb
                    if lmlist[tip_index][0] > lmlist[tip_index - 1][0]:
                        open_status[finger_tip_index.index(tip_index)] = 1 # replacing element in array
                    else:
                        open_status[finger_tip_index.index(tip_index)] = 0
                
                else:
                    if lmlist[tip_index][1] < lmlist[tip_index - 2][1]:
                        open_status[finger_tip_index.index(tip_index)] = 1
                    else:
                        open_status[finger_tip_index.index(tip_index)] = 0

            # printing open status
            # print(open_status)

            # checking if index finger is up and middle finger is down : move mode
            if open_status[1]  ==  1 and open_status[2]  ==  0:

                # draw a circle at that point
                draw_points(frame, lmlist , [8] , (0,0,255) , 10)

                # drawing moving zone
                cv2.rectangle(frame, (100,100), (wframe - 200 , hframe - 200) , (255,255,255))

                # moving mouse
                xval , yval = lmlist[8][0] , lmlist[8][1]
                
                # constraining xval and yval
                xval = np.clip(xval, 100, wframe - 200)
                yval = np.clip(yval, 100, hframe - 200)
                # print(xval , yval) # xval and yval are constrained in 100 : 440 , 100 : 280

                # mapping xval
                xval = np.interp(xval, (100 , wframe - 200), (0 , wscreen))
                yval = np.interp(yval, (100 , hframe - 200), (0 , hscreen))
                # print(xval , yval) # mapped range
                # converting to int
                xval = int(xval) # screenwidth : 0 to 1366
                yval = int(yval) # screenheight : 0 to 768

                # moving mouse at xval and y val
                # print(xval , yval)

                # autopy.mouse.move(screenwidth , screenheight), shows out of bound for complete
                # screenwidth and height. i.e why we have done -1
                if xval >= wscreen:
                    xval = wscreen - 1
                if yval >= hscreen:
                    yval = hscreen - 1

                # mouse is hovering a lot.
                # due to minor change in finger tip coordinate, xval and yval are also changing
                # we can smoothen by writing, if change in position is over certain threshold, then only move
                # mymethod : not working properly


                # if xval - plocx > threshold  or  yval - plocy > threshold:

                #     # moving mouse
                #     autopy.mouse.move(xval , yval)

                # # updating plocx nad plocy
                # plocx = xval
                # plocy = yval




                # alternate method :
                clocx = plocx + (xval - plocx)/smoothening_constant
                clocy = plocy + (yval - plocy)/smoothening_constant
                autopy.mouse.move(clocx, clocy)
                plocx = clocx
                plocy = clocy


            elif open_status[1]  ==  1 and open_status[2]  ==  1: # click mode

                # draw circle at both finger tips
                draw_points(frame, lmlist, [8,12], (0,0,255) , 10) 

                # draw a line between them
                cv2.line(frame, (lmlist[8][0]  ,lmlist[8][1]), (lmlist[12][0]  ,lmlist[12][1]), (255,0,0) , 3)

                # draw a circle at the centre of line
                center_x = int((lmlist[8][0]  + lmlist[12][0]) / 2)
                center_y = int((lmlist[8][1]  + lmlist[12][1]) / 2)

                # distance between points
                # **2 : squared , **0.5 : square root
                distance = ((lmlist[12][0] - lmlist[8][0])**2 + (lmlist[12][1] - lmlist[8][1])**2)**0.5
                distance = int(distance)
                print(distance)

                if distance > 30:
                    cv2.circle(frame, (center_x , center_y), 10, (0,0,255), -1)
                else:
                    cv2.circle(frame, (center_x , center_y), 10, (255,0,0), -1)
                    autopy.mouse.click()

                


        # getting frame per second
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(frame, str(int(fps)), (10,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0))

        # showing the frame
        cv2.imshow('feed' , frame)
        code = cv2.waitKey(1)
        if code  ==  ord('q'):
            break

camera.release()
cv2.destroyAllWindows()