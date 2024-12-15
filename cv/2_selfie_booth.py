import cv2

cam = cv2.VideoCapture(0)

while cam.isOpened():
    status, frame = cam.read()
    if status:
        frame = cv2.flip(frame, 1)
        cv2.imshow('selfie booth', frame)
        code = cv2.waitKey(1)
        if code == ord('q'):
            break
        elif code == ord('s'):
            cv2.imwrite('selfie.png', frame)

cam.release()
cv2.destroyAllWindows()