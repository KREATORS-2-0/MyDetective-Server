from emotion_webcam import FaceAnalyzer
import threading 
import time

def facialEmotion():
    analyzer = FaceAnalyzer()
    analyzer.start_camera()
    for i in range(15):
        time.sleep(1)
        analyzer.run()
    print("\n  : ", analyzer.data)
    analyzer.stop_camera()
def transcribeEmotion():
    speechAnalyzer = speechAnalyzer() 
    speechAnalyzer.run()
    print(speechAnalyzer.data)  
    
    
def main():
    p1= threading.Thread(target=facialEmotion)
    p2= threading.Thread(targeet= transcribeEmotion)
    p1.start()
    p2.start()

main()