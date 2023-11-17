from emotion_webcam import EmotionAnalyzer
import time

analyzer = EmotionAnalyzer()
analyzer.start_camera()

emotions = []
for i in range(2):
    a = analyzer.start_analysis({}, i)

print(type(emotions))
analyzer.stop_camera()
