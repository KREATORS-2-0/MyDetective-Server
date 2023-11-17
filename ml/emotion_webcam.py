import cv2
import time
from deepface import DeepFace

def process_frame(cap, emotionData, emotionIndex):
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return False, None

    # Your frame processing code here...
    # For example, analyzing the frame for emotions
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], silent=True)
        dom_emotion = analysis['dominant_emotion']
        print(dom_emotion)
        return True, dom_emotion
    except Exception as e:
        print("An error occurred during frame analysis:", e)
        return True, None

def main(detectiveData, emotionData):
    cap = None
    last_analysis_time = time.time()
    emotionIndex = 1
    detectiveIndex = 1

    while True:
        command = detectiveData[detectiveIndex].get("command", "")
        if command == "initiate":
            print("Initiating...")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Cannot open camera")
                break

        elif command == "start" and cap is not None:
            print("Starting...")
            current_time = time.time()
            if current_time - last_analysis_time >= 1.5:
                success, emotion = process_frame(cap, emotionData, emotionIndex)
                if not success:
                    break
                if emotion:
                    emotionData[emotionIndex]["Emotion"] = emotion
                last_analysis_time = current_time

        elif command == "pause":
            print("Pausing...")
            if cap:
                cap.release()
            break

        elif command == "terminate":
            print("Terminating...")
            if cap:
                cap.release()
            cv2.destroyAllWindows()
            break

        time.sleep(0.1)  # Add a small delay to prevent CPU overuse

# Test function
def test():
    emotionData = {"1": {"TimeStamp": "", "Emotion": ""}}
    detectiveData = {"1": {"command": ""}}

    while True:
        command = input("Enter a command: ")
        detectiveData["1"]["command"] = command
        main(detectiveData, emotionData)
        if command == "terminate":
            break

if __name__ == "__main__":
    test()
