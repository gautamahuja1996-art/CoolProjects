import mediapipe as mp
import cv2
import math # to calculate distance between points
import pycaw # to change computer audio (python core audio windows library)
import numpy as np # to use the interp function (works like map funtion)



# volume code
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

# get volume range function returns a tuple with min and max limit of your vol
volume_range = volume.GetVolumeRange() # to get the range of your speaker (-65.25 which is 0 to 0 which is 100)
min_vol = volume_range[0]
max_vol = volume_range[1]



camera = cv2.VideoCapture(2)

camera.set(3, 640) # setting frame width
camera.set(4, 480) # setting frame height

# accessing different modules / scripts
mphands = mp.solutions.hands
mpdraw = mp.solutions.drawing_utils
myconnect = mp.solutions.hands_connections

# making objects
myhands = mphands.Hands()

framewidth = camera.get(3)
frameheight = camera.get(4) # to convert normalised data to pixel form
x4 , y4 , x8 , y8 = 0 , 0 , 0 , 0

while camera.isOpened():

	status , frame = camera.read()

	if status:

		frame = cv2.flip(frame , 1)
		frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
		result = myhands.process(frame_rgb)

		if result.multi_hand_landmarks != None:

			for hand in result.multi_hand_landmarks:

				for index , coordinate in enumerate(hand.landmark):
					px , py = int(coordinate.x * framewidth) , int(coordinate.y * frameheight)

					if index  ==  4:
						x4 = px
						y4 = py
						frame = cv2.circle(frame , (x4 , y4) , 15 , (255,0,0) , -1)

					elif index  ==  8:
						x8 = px
						y8 = py
						frame = cv2.circle(frame , (x8 , y8) , 15 , (255,0,0) , -1)


					frame = cv2.line(frame , (x4,y4) , (x8,y8) , (255,255,255) , 1)

					# getting center of line
					cx , cy = (x4+x8)//2 , (y4+y8)//2
					frame = cv2.circle(frame , (cx , cy) , 15 , (255,0,255) ,  -1)


					# calculating distance between the points
					distance = math.sqrt(((x4 - x8) ** 2) + ((y4 - y8) ** 2))
					# distance = int(math.dist((x4 , y4) , (x8 , y8)))

					if distance > 300:
						distance = 300
						frame = cv2.circle(frame , (cx , cy) , 15 , (0,255,0) ,  -1)
					elif distance < 50:
						distance = 50
						frame = cv2.circle(frame , (cx , cy) , 15 , (0,0,255) ,  -1)

					#print(distance) # max : 300 , min : 50


					# we need to map distance into volume range
					# map distance from 50 to 300 and return corresponding output from -65 (0 vol) to 0 (100 vol)
					vol = np.interp(distance , [50 , 300] , [min_vol , max_vol])
					volume.SetMasterVolumeLevel(vol, None) # to set the volume
					print(vol)




		cv2.imshow('video feed' , frame)
		code = cv2.waitKey(1)
		if code  ==  ord('q'):
			break

camera.release()
cv2.destroyAllWindows()