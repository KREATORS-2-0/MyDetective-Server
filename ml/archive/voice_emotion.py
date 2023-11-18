import sounddevice as sd
import numpy as np
import torch
import torch.nn.functional as F
from transformers import Wav2Vec2FeatureExtractor, AutoConfig
from src.models import HubertForSpeechClassification
import io
from pynput import keyboard
import torchaudio
import time
from datetime import datetime

class VoiceAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = "m3hrdadfi/hubert-base-greek-speech-emotion-recognition"
        self.config = AutoConfig.from_pretrained(self.model_name)
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
        self.sampling_rate = self.feature_extractor.sampling_rate
        self.model = HubertForSpeechClassification.from_pretrained(self.model_name).to(self.device)
        self.is_listening = False
        self.data = dict()

    def record_audio(self, duration):
        """Record audio from the microphone."""
        audio = sd.rec(int(duration * self.sampling_rate), samplerate=self.sampling_rate, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        return audio.squeeze()

    def predict_emotion(self, audio):
        """Predict emotion from audio array."""
        audio = (audio * np.iinfo(np.int16).max).astype(np.int16)  # Convert to 16-bit
        buffer = io.BytesIO()
        torchaudio.save(buffer, torch.tensor(audio).unsqueeze(0), self.sampling_rate, format="wav")
        buffer.seek(0)
        speech_array, _ = torchaudio.load(buffer)
        inputs = self.feature_extractor(speech_array.squeeze().numpy(), sampling_rate=self.sampling_rate, return_tensors="pt", padding=True)
        inputs = {key: inputs[key].to(self.device) for key in inputs}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        highest_score_index = np.argmax(scores)
        highest_emotion = self.config.id2label[highest_score_index]
        if highest_emotion == 'disgust':
            highest_emotion = 'neutral'
        return highest_emotion

    def on_press(self, key):

        #################### Control ######################
        try:
            if key.char == 'r':
                print("Listening mode activated.")
                self.is_listening = True
            elif key.char == 's':
                print("Listening mode deactivated.")
                self.is_listening = False
                print(self.data)
                self.data['TimeStamp'] = []
                self.data['Emotion'] = []
        #################### Control ######################

        except AttributeError:
            pass

    def run(self):
        self.data['TimeStamp'] = []
        self.data['Emotion'] = []
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        while True:
            if self.is_listening:
                audio = self.record_audio(3)  # Record for 3 seconds
                emotion = self.predict_emotion(audio)
                self.data['TimeStamp'].append(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
                self.data['Emotion'].append(emotion)
                print("Detected Emotion:", emotion)
            else:
                time.sleep(1)

if __name__ == "__main__":
    voice_analyzer = VoiceAnalyzer()
    voice_analyzer.run()
