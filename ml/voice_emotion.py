import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import AutoConfig, Wav2Vec2FeatureExtractor
from src.models import Wav2Vec2ForSpeechClassification, HubertForSpeechClassification

import librosa
import IPython.display as ipd
import numpy as np
import pandas as pd

class VoiceAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = "m3hrdadfi/hubert-base-greek-speech-emotion-recognition"
        self.config = AutoConfig.from_pretrained(self.model_name)
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(self.model_name)
        self.sampling_rate = self.feature_extractor.sampling_rate
        self.model = HubertForSpeechClassification.from_pretrained(self.model_name).to(self.device)
    def speech_file_to_array_fn(self, path, sampling_rate):
        speech_array, _sampling_rate = torchaudio.load(path)
        resampler = torchaudio.transforms.Resample(_sampling_rate)
        speech = resampler(speech_array).squeeze().numpy()
        return speech

    def predict(self, path, sampling_rate):
        speech = self.speech_file_to_array_fn(path, sampling_rate)
        inputs = self.feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
        inputs = {key: inputs[key].to(self.device) for key in inputs}

        with torch.no_grad():
            logits = self.model(**inputs).logits

        scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
        outputs = [{"Emotion": self.config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
        return outputs

if __name__ == "__main__":
    path = "/Users/taekwan/Desktop/a01.wav"
    voice_analyzer = VoiceAnalyzer()
    outputs = voice_analyzer.predict(path, voice_analyzer.sampling_rate)
    print(outputs)
