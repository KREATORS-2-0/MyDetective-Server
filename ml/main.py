from emotion_webcam import FaceAnalyzer
import time
def main():
    analyzer = FaceAnalyzer()
    analyzer.start_camera()
    for i in range(15):
        time.sleep(1)
        analyzer.run()
    print("\n  : ", analyzer.data)
    analyzer.stop_camera()   
main()