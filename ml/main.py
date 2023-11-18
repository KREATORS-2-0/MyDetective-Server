from emotion_webcam import FaceAnalyzer
from transcribe_emotion import SpeechAnalyzer
from queue import Queue
import threading 
import time

def facialEmotion(result_queue):
    analyzer = FaceAnalyzer()
    analyzer.start_camera()
    for i in range(15):
        time.sleep(1)
        analyzer.run()
    analyzer.stop_camera()
    result_queue.put(analyzer.data)
    
    
def transcribeEmotion(result_queue):
    speechAnalyzer = SpeechAnalyzer() 
    speechAnalyzer.run()
    result_queue.put(speechAnalyzer.data)   
    
    
def main():
    result_queue = Queue()
    p1= threading.Thread(target=facialEmotion(result_queue))
    p2= threading.Thread(target= transcribeEmotion(result_queue))
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    facial_emotion_result = result_queue.get()
    transcribe_emotion_result = result_queue.get()

    print("Facial Emotion Result:", facial_emotion_result)
    print("Transcribe Emotion Result:", transcribe_emotion_result)

main()