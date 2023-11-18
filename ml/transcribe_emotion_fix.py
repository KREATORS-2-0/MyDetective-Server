import speech_recognition as sr
from transformers import pipeline
from pynput import keyboard


class SpeechAnaylzer:
    def __init__(self):
        self.r = sr.Recognizer()
        self.candidate_labels = ['happy', 'sad', 'angry', 'fear', 'neutral']
        self.model = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
        self.classifier = pipeline(
            'zero-shot-classification', model=self.model)
        self.is_listening = False
        self.data = {"Emotion": None}
        self.transcription = ""

    def on_press(self, key):
        try:
            if key.char == 's' or key.char == 'q':
                self.is_listening = False
                return False
        except AttributeError:
            pass

    def transcribe(self):
        self.is_listening = True
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        with sr.Microphone() as source:

            try:
                self.r.adjust_for_ambient_noise(source, duration=0.5)
                if self.is_listening:
                    print("Listening...")
                    audio = self.r.listen(
                        source, timeout=5, phrase_time_limit=None)
                    self.transcription = self.r.recognize_google(audio)
                    return self.transcription

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def classify_emotion(self):
        output = self.classifier(
            self.transcription, self.candidate_labels, multi_label=False)
        return output['labels'][0]

    def clear_transcription(self):
        self.transcription = ""


if __name__ == "__main__":
    speech_analyzer = SpeechAnaylzer()

    transcription = speech_analyzer.transcribe()
    print(transcription)

    emotion = speech_analyzer.classify_emotion()
    print(emotion)
