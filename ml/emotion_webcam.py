'''
$ pip install cv2
$ pip install deepface
'''

import cv2
import time
from deepface import DeepFace

# Initialize the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

# Initialize a variable to store the time of the last analysis
last_analysis_time = time.time()

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
            
            dom_emotion = analysis[0]['dominant_emotion']

            print(dom_emotion)

            # Update the last analysis time
            last_analysis_time = current_time

        except Exception as e:
            # print("An error occurred:", e)
            pass

    # Display the resulting frame
    cv2.imshow('Webcam Feed', frame)

    # Press 'q' on the keyboard to exit
    if cv2.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
