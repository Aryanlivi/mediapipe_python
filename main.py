import cv2
import mediapipe 


webCam=cv2.VideoCapture(0)
if not webCam.isOpened():
    print("Error:Couldn't open webCam")
    exit()
while True:
    ret,frame=webCam.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('Webcam', frame)

    # Break the loop on 'q' key press.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


webCam.release()
cv2.destroyAllWindows()