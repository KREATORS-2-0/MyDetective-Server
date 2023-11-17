from emotion_webcam import FaceAnalyzer
import time
def main():
    analyzer = FaceAnalyzer()
    analyzer.start_camera()

    for i in range(2):
        time.sleep(2)
        analyzer.run()
    print("\n herehere: ", analyzer.data)
    analyzer.stop_camera()   
