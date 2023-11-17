'''
$ pip install SpeechRecognition
$ pip install pyaudio
'''

import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()


# Capture audio from the microphone
with sr.Microphone() as source:
    

    while True:
        
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=4)
            # Recognize the speech in the audio
            text = r.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error; {e}")
