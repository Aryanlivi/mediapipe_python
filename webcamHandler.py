import cv2
import mediapipe as mp
from pythonosc import udp_client
# Initialize OSC client.
client = udp_client.SimpleUDPClient("127.0.0.1", 39539)
class WebcamHandler:
    def __init__(self,camera_index=0):
        self.webCam=cv2.VideoCapture(camera_index)
        if not self.webCam.isOpened():
            raise Exception("Error:Couldn't Open Webcam")

    def init_mp(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
    def start(self,detect_pose=False,exit_key='q'):
        if(detect_pose):
            self.init_mp()
        while self.webCam.isOpened():
            ret,frame=self.webCam.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            if detect_pose:
                self.detect_pose(frame)
            else:
                cv2.imshow('WebcamFeed', frame)
            # Break the loop on 'q' key press.
            if cv2.waitKey(1) & 0xFF == ord(exit_key):
                break
            
        self.release()
    def detect_pose(self,frame):
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results =self.pose.process(image_rgb)
        
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image_bgr, results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                if idx==16:#right wrist
                    x = landmark.x
                    y = landmark.y
                    z = landmark.z
                    visibility = landmark.visibility
                    # VMC protocol expects OSC messages for each joint.
                    # Format your OSC message here. Example format:
                    client.send_message(f"/VMC/Ext/Bone/Pos/{idx}", [x,y,z, visibility])
        cv2.imshow('MediaPipe Pose Detection', image_bgr)
    
    def get_fps(self):
        self.fps = self.webCam.get(cv2.CAP_PROP_FPS)
        return self.fps
    def get_size(self):
        self.width=self.webCam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height=self.webCam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return (self.width,self.height)
        
    def release(self):
        self.webCam.release()
        cv2.destroyAllWindows()

webcam_handler=WebcamHandler()