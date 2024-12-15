import cv2

cam = cv2.VideoCapture(0)

# take message and coordinate input
message = input("Enter the text to be displayed : ")
x = int(input("Enter the x coordinate : "))
y = int(input("Enter the y coordinate : "))

# main loop
while cam.isOpened():
    status, frame = cam.read()
    if status:
        frame = cv2.flip(frame, 1)
        cv2.imshow('selfie booth', frame)
        code = cv2.waitKey(1)
        if code == ord('q'):
            break
        elif code == ord('s'):
            cv2.putText(frame, message, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imwrite('selfie.png', frame)

cam.release()
cv2.destroyAllWindows()