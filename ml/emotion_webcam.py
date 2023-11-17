# # Detective Data:
# # {
# #     "1": {"command": ["initiate", "start", "pause", "terminate"]},
# #     "2": {"command": ["initiate", "start", "pause", "terminate"]},
# #     "3": {"command": ["initiate", "start", "pause", "terminate"]},
# # }

# # Emotion Data:
# # {
# #     "1": {"TimeStamp": ["2021-05-01 12:00:00", "2021-05-01 12:00:15"], "Emotion": ["happy", "sad", "angry", "neutral", "sad", "happy", "sad", "angry", "neutral", "sad", "happy", "sad", "angry", "neutral", "sad"]},
# #     "2": {"TimeStamp": ["2021-05-01 12:00:15", "2021-05-01 12:00:30"], "Emotion": ["happy", "sad", "angry", "neutral", "sad", "happy", "sad", "angry", "neutral", "sad", "happy", "sad", "angry", "neutral", "sad"]},
# # }


import cv2
import time
from deepface import DeepFace
import threading

class EmotionAnalyzer:
    def __init__(self):
        self.cap = None
        self.analysis_thread = None
        self.running = False

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Cannot open camera")
                return False
        return True

    def start_analysis(self, emotionData, detectiveIndex):
        if not self.start_camera():
            return
        self.running = True
        if self.analysis_thread is None or not self.analysis_thread.is_alive():
            self.analysis_thread = threading.Thread(target=analyze_emotions, args=(self, emotionData, detectiveIndex))
            self.analysis_thread.start()

    def stop_analysis(self):
        self.running = False
        if self.analysis_thread is not None:
            self.analysis_thread.join()
            self.analysis_thread = None

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        # cv2.destroyAllWindows()

def analyze_emotions(analyzer, emotionData, detectiveIndex):
    if analyzer.running and analyzer.cap.isOpened():
        ret, frame = analyzer.cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            return

        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dom_emotion = analysis['emotion']['dominant_emotion']
            print("Detected emotion:", dom_emotion)

            current_formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if detectiveIndex not in emotionData:
                emotionData[detectiveIndex] = {"TimeStamp": [], "Emotion": []}

            emotionData[detectiveIndex]["TimeStamp"].append(current_formatted_time)
            emotionData[detectiveIndex]["Emotion"].append(dom_emotion)
            print(emotionData)

        except Exception as e:
            print("An error occurred during emotion analysis:", e)

def main(detectiveData, emotionData, analyzer):
    while True:
        command_input = input("Enter command (initiate/start/pause/terminate): ").strip().lower()
        if command_input in ["initiate", "start", "pause", "terminate"]:
            detectiveIndex = str(len(detectiveData) + 1)
            detectiveData[detectiveIndex] = {"command": [command_input]}
            print(f"Command '{command_input}' added to detectiveData.")

            if command_input == "initiate":
                print("Initiating...")
                analyzer.start_camera()

            if command_input == "start":
                print("Starting...")
                analyzer.start_analysis(emotionData, detectiveIndex)

            if command_input == "pause":
                print("Pausing...")
                analyzer.stop_analysis()

            if command_input == "terminate":
                print("Terminating...")
                analyzer.stop_camera()
                return

        time.sleep(1)

if __name__ == "__main__":
    detectiveData = {}
    emotionData = {}
    analyzer = EmotionAnalyzer()
    main(detectiveData, emotionData, analyzer)

