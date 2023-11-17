'''
$ pip install SpeechRecognition
$ pip install pyaudio
'''

import speech_recognition as sr
from transformers import pipeline

# Initialize recognizer
r = sr.Recognizer()


classifier = pipeline('zero-shot-classification', model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
candidate_labels = ['happy', 'sad', 'angry', 'fear', 'neutral']


# Capture audio from the microphone
with sr.Microphone() as source:
    

    while True:
        
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=5)
            # Recognize the speech in the audio
            text = r.recognize_google(audio)
            
            output = classifier(text, candidate_labels, multi_label=False)
            dom_emotion = output['labels'][0]
            print(dom_emotion)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error; {e}")
