'''
$ pip install SpeechRecognition
$ pip install pyaudio
'''

import speech_recognition as sr
from transformers import pipeline
from pynput import keyboard

class SpeechAnalyzer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.candidate_labels = ['happy', 'sad', 'angry', 'fear', 'neutral']
        self.model = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
        self.classifier = pipeline('zero-shot-classification', model=self.model)
        self.is_listening = False

    def on_press(self, key):
        try:
            if key.char == 'r':
                self.is_listening = True
            elif key.char == 's' or key.char == 'q':
                self.is_listening = False
        except AttributeError:
            pass

    def run(self):
        with sr.Microphone() as source:

            while True:
                try:
                     audio = self.r.listen(source, timeout=3, phrase_time_limit=None)
                     text = self.r.recognize_google(audio)
                     emotion = self.classify_emotion(text)
                     print(emotion)
                except Exception as e:
                    print("An unexpected error occurred:", e)
                    
    
    def classify_emotion(self, text):
        output = self.classifier(text, self.candidate_labels, multi_label=False)
        return output['labels'][0]

if __name__ == "__main__":
    speech_analyzer = SpeechAnalyzer()
    speech_analyzer.run()
    