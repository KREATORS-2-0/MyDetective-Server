from keras.models import load_model
from keras import backend as K
import numpy as np
import librosa
import pickle
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

class VoiceAnalyzer:
    def __init__(self):
        self.lb = None
        self.model = None
        self.initialize()

    def recall_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision_m(self, y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

    def f1_m(self, y_true, y_pred):
        precision = self.precision_m(y_true, y_pred)
        recall = self.recall_m(y_true, y_pred)
        return 2*((precision*recall)/(precision+recall+K.epsilon()))

    def mfcc(self, data, sr, frame_length=2048, hop_length=512, flatten: bool = True):
        mfcc_feature = librosa.feature.mfcc(y=data, sr=sr)
        return np.squeeze(mfcc_feature.T) if not flatten else np.ravel(mfcc_feature.T)

    def rmse(self, data, frame_length=2048, hop_length=512):
        rmse = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)
        return np.squeeze(rmse)

    def zcr(self, data, frame_length=2048, hop_length=512):
        zcr = librosa.feature.zero_crossing_rate(y=data, frame_length=frame_length, hop_length=hop_length)
        return np.squeeze(zcr)

    def noise(self, data, random=False, rate=0.035, threshold=0.075):
        """Add some noise to sound sample. Use random if you want to add random noise with some threshold.
        Or use rate Random=False and rate for always adding fixed noise."""
        if random:
            rate = np.random.random() * threshold
        noise_amp = rate*np.random.uniform()*np.amax(data)
        data = data + noise_amp*np.random.normal(size=data.shape[0])
        return data

    def pitch(self, data, sampling_rate, pitch_factor=0.7, random=False):
        if random:
            pitch_factor = np.random.random() * pitch_factor
        return librosa.effects.pitch_shift(data, sr=sampling_rate, n_steps=pitch_factor)

    def extract_features(self, data, sr, frame_length=2048, hop_length=512):
        result = np.array([])
        result = np.hstack((result,
                            self.zcr(data, frame_length, hop_length),
                            self.rmse(data, frame_length, hop_length),
                            self.mfcc(data, sr, frame_length, hop_length)
                                        ))
        return result

    def get_features(self, path, duration=2.5, offset=0.6):
        # duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
        data, sample_rate = librosa.load(path, duration=duration, offset=offset)

        # without augmentation
        res1 = self.extract_features(data, sample_rate)
        result = np.array(res1)

        # data with noise
        noise_data = self.noise(data, random=True)
        res2 = self.extract_features(noise_data, sample_rate)
        result = np.vstack((result, res2)) # stacking vertically

        # data with pitching
        pitched_data = self.pitch(data, sample_rate, random=True)
        res3 = self.extract_features(pitched_data, sample_rate)
        result = np.vstack((result, res3)) # stacking vertically

        # data with pitching and white_noise
        new_data = self.pitch(data, sample_rate, random=True)
        data_noise_pitch = self.noise(new_data, random=True)
        res3 = self.extract_features(data_noise_pitch, sample_rate)
        result = np.vstack((result, res3)) # stacking vertically
        # Flatten the result to a single vector per sample
        flattened_result = result.flatten()

        # Make sure the flattened result has length 2376
        # You might need to adjust this depending on how you want to handle different lengths
        flattened_result = np.resize(flattened_result, 2376)

        return flattened_result

    def initialize(self):
        with open('label_encoder.pkl', 'rb') as f:
            self.lb = pickle.load(f)
        
        self.model = load_model('res_model.h5', custom_objects={'f1_m': self.f1_m, 'precision_m': self.precision_m, 'recall_m': self.recall_m})

    def analyze_emotion(self, path):
        # Extract features using the path to the audio file
        features = self.get_features(path)
        features = features.reshape(1, 2376, 1)  # Reshape for the model: 1 sample, 2376 features, 1 dimension
        prediction = self.model.predict(features)
        predicted_class = np.argmax(prediction, axis=1)
        predicted_emotion = self.lb.inverse_transform(predicted_class)
        print(predicted_emotion)

    def run(self):
        duration = 2
        sample_rate = 22050
        print("Starting live voice-emotion analysis")

if __name__ == "__main__":
    voice_analyzer = VoiceAnalyzer()
    voice_analyzer.run()




