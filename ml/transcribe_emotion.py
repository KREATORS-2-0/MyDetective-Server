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
        self.data = {"Emotion": None}
        self.full_text = ""



    def run(self):
        self.is_listening = True
    

        with sr.Microphone() as source:
            while True:
                try:
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                    if self.is_listening:
                        print("Listening...")
                        audio = self.r.listen(source, timeout=3, phrase_time_limit=None)
                        text = self.r.recognize_google(audio)
                        self.full_text += (text + '\n')
                        emotion = self.classify_emotion(text)
                        self.data["Emotion"] = emotion
                    else:
                        break
                except sr.WaitTimeoutError:
                    # Timeout error, no speech detected
                    pass
                except sr.UnknownValueError:
                    # Google Speech Recognition couldn't understand the audio
                    pass
                except sr.RequestError:
                    # Could not request results from Google Speech Recognition service
                    pass
                except Exception as e:
                    # Other unexpected errors
                    print(f"An unexpected error occurred: {e}")

    def classify_emotion(self, text):
        output = self.classifier(text, self.candidate_labels, multi_label=False)
        return output['labels'][0]
    def reset_data(self):
        self.data = {"Emotion": None}
        self.full_text = ""
        

if __name__ == "__main__":
    speech_analyzer = SpeechAnalyzer()
    speech_analyzer.run()