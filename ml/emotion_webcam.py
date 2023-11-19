import cv2
import time
from deepface import DeepFace
from datetime import datetime

class FaceAnalyzer:
    def __init__(self):
        self.cap = None
        self.frame = None
        self.last_analysis_time = time.time()
        self.collect_data = False
        self.data = dict()
  
    def start_camera(self):
        self.data['TimeStamp'] = []
        self.data['Emotion'] = []
        
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            #self.place_circle() 
            if not self.cap.isOpened():
                print("Cannot open camera")
                return False

        return True

    def run(self):
        ret, self.frame = self.cap.read()
        if not ret:
            print("Can't receive frame. Exiting...")  # put red circle in screen (deepface detects face well in center)
            return
        self.analyze_emotions()
        # self.stop_camera()

    def analyze_emotions(self):
        try:
            analysis = DeepFace.analyze(self.frame, actions=['emotion'])
            print(analysis[0]['dominant_emotion'])
            self.last_analysis_time = time.time()
            human_readable_time = datetime.fromtimestamp(self.last_analysis_time).strftime('%Y-%m-%d %H:%M:%S')
            self.data['TimeStamp'].append(human_readable_time)
            self.data['Emotion'].append(analysis[0]['dominant_emotion'])
        except Exception as e:
            # print("An error occurred:", e)
            pass

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
    def reset_data(self):
        self.data =dict()
    
    def place_circle(self):
        height, width = self.frame.shape[:2]
        center = (width // 2, height // 2)
        cv2.circle(img=self.frame, center=center, radius=300, color=(0,0,255), thickness=2)
    

