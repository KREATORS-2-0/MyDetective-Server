'''
$ pip install cv2
$ pip install deepface
'''

import cv2
import time
from deepface import DeepFace

# Emotion Data:
# {
#     "1": {"TimeStamp": "2021-05-01 12:00:00, 2021-05-01 12:00:15", "Emotion": "happy, sad, angry, neutral, sad, happy, sad, angry, neutral, sad, happy, sad, angry, neutral, sad"},
#     "2": {"TimeStamp": "2021-05-01 12:00:00, 2021-05-01 12:00:15", "Emotion": "happy, sad, angry, neutral, sad, happy, sad, angry, neutral, sad, happy, sad, angry, neutral, sad"},
# } 
# Detective Data:
# {
#     "1": {"command": "initiate, start, pause"},
#     "2": {"command": "initiate, start, pause"},
#     "3": {"command": "initiate, start, pause"},
# }

def main(detectiveData, emotionData):
    # setup the variables
    detectiveIndex = 1
    emotionIndex = 1
    while True:
        try:
            # detectiveIndex is the index of the detective that is currently being analyzed
            if detectiveData[detectiveIndex]["command"] == "initiate":
                print("Initiating...")
                # Initialize the webcam (0 is the default webcam)
                cap = cv2.VideoCapture(0)

                # Initialize a variable to store the time of the last analysis
                last_analysis_time = time.time()

                if not cap.isOpened():
                    print("Cannot open camera")
                    exit()

                if detectiveData[detectiveIndex]["command"] == "start":
                    print("Starting...")
                    # Capture frame-by-frame
                    while True:
                        # Capture frame-by-frame
                        ret, frame = cap.read()

                        # If frame is read correctly, ret is True
                        if not ret:
                            print("Can't receive frame (stream end?). Exiting ...")
                            break
                        
                        height, width = frame.shape[:2]
                        center = (width // 2, height // 2)
                        cv2.circle(img=frame, center=center, radius=300, color=(0,0,255), thickness=2)

                        # Check if 3 seconds have passed since the last analysis
                        current_time = time.time()
                        if current_time - last_analysis_time >= 1.5:

                            try:
                                # Analyze the captured frame for emotion
                                analysis = DeepFace.analyze(frame, actions=['emotion'], silent=True)

                                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))

                                emotionData[emotionIndex]["TimeStamp"] = current_time

                                emotionData[emotionIndex]["Emotion"] = analysis[0]['dominant_emotion']
                                
                                dom_emotion = analysis[0]['dominant_emotion']

                                print(dom_emotion)

                                # Update the last analysis time
                                last_analysis_time = current_time

                            except Exception as e:
                                # print("An error occurred:", e)
                                pass

                        # Display the resulting frame
                        cv2.imshow('Webcam Feed', frame)

                        if detectiveData[detectiveIndex]["command"] == "pause":
                            print("Pausing...")
                            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                            emotionData[emotionIndex]["TimeStamp"] += ", " + current_time
                            # When everything done, release the capture
                            detectiveIndex += 1
                            break

                        # # Press 'q' on the keyboard to exit
                        # if cv2.waitKey(1) == ord('q'):
                        #     break

                # When everything is done, release the capture
            elif detectiveData[detectiveIndex]["command"] == "terminate": 
                cap.release()
                cv2.destroyAllWindows()
                detectiveIndex += 1
                break
        except Exception as e:
            print("An error occurred:", e)
            pass


# I want to make a command line testing for the main function
def test():
    emotionData = {
        "1": {"TimeStamp": "", "Emotion": ""},
    }
    detectiveData = {
        "1": {"command": ""},
    }
    main(detectiveData, emotionData)
    detectiveIndex = 1
    emotionIndex = 1
    while True:
        try:
            print("Enter a command: ")
            command = input()
            detectiveData[detectiveIndex]["command"] = command
            if command == "initiate":
                detectiveData[detectiveIndex]["command"] = command
                main(detectiveData, emotionData)
                print("Initiating...")
                print("Enter a command: ")
                command = input()
            elif command == "start":
                detectiveData[detectiveIndex]["command"] = command
                main(detectiveData, emotionData)
                print("Starting...")
                print("Enter a command: ")
                command = input()
            elif command == "pause":
                detectiveData[detectiveIndex]["command"] = command
                main(detectiveData, emotionData)
                print("Pausing...")
                print("Enter a command: ")
                command = input()
            elif command == "terminate":
                detectiveData[detectiveIndex]["command"] = command
                main(detectiveData, emotionData)
                print("Terminating...")
                print("Enter a command: ")
                command = input()
        except Exception as e:
            print("An error occurred:", e)
            pass


if __name__ == "__main__":
    test()           
            




