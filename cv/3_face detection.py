# HAAR CASCADES WONT WORK IF YOU PUT YOUR HAND IN FRONT OF THE FACE OR MOVE YOUR FACE TOWARDS LEFT,
# BUT MEDIAPIPE FACE DETECTION DETECTS ALL THAT

from mediapipe.python.solutions import face_detection , drawing_utils as easy_draw
import cv2

# making object of face detection class
face_detector = face_detection.FaceDetection()

# video feed
camera = cv2.VideoCapture(0)

# frame dimensions
framewidth = camera.get(3)
frameheight = camera.get(4)

while camera.isOpened():
    status , frame = camera.read()
    if status:
        frame = cv2.flip(frame , 1)

        # rgb frame needed to process
        frame_rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

        # using .process function
        results = face_detector.process(frame_rgb)

        # .process() returns a namedTuple object named 'detections'
        # print(results.detections)
        # detections has a list of faces where each face has : label id , score , location_data
        detected_face = results.detections

        # if there is a detected_face, then iterate the list
        if detected_face:

            for face in detected_face:

                # draw the bbox and landmarks on the detected face
                # easy_draw.draw_detection(frame , face)

                # getting info
                face_id = face.label_id
                face_score = face.score
                face_location = face.location_data

                # bounding box coordinates can be accessed as : face.location_data.relative_bounding_box
                face_coordinates = face_location.relative_bounding_box
                x = face_coordinates.xmin
                y = face_coordinates.ymin
                w = face_coordinates.width
                h = face_coordinates.height

                # normalised form --> pixel form
                x = int(x*framewidth)
                y = int(y*frameheight)
                w = int(w*framewidth)
                h = int(h*frameheight)

                # drawing rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)

                # face score and face_id are of type : 
                # <class 'google.protobuf.pyext._message.RepeatedScalarContainer'>
                # to convert them into ints or floats
                # face_score = face_score[0] # float form
                #
                # print(face_id , f' Confidence : {int(face_score*100)} %' , (x,y,w,h))
                



        cv2.imshow('frame' , frame)
        code = cv2.waitKey(1)
        if code  ==  ord('q'):
            break

camera.release()
cv2.destroyAllWindows()