import librosa
import numpy as np
import soundfile as sf


def load_audio(file_path, sample_rate=None, mono=True):
    audio, sr = librosa.load(file_path, sr=sample_rate, mono=mono)
    return audio, sr

def normalize_audio(audio):
    return librosa.util.normalize(audio)

def split_audio(audio, top_db):
    # If the audio is completely silent, return an empty list to avoid issues with librosa
    if np.max(np.abs(audio)) < 1e-6:
        return []

    return librosa.effects.split(audio, top_db=abs(top_db))

def save_audio(file_path, audio, sample_rate):
    sf.write(file_path, audio, sample_rate)

#feature extraction functions

def compute_rms(audio, frame_length: int = 2048, hop_length: int = 512) -> float:
    #return computed RMS values as a 1D array
    return librosa.feature.rms(
        y=audio,
        frame_length=frame_length,
        hop_length=hop_length
    )[0]

#computes frequency energy distribution across audio
#i.e. high-pitched the sound is at each moment
def compute_audio_brightness(audio, sr):
    return librosa.feature.spectral_centroid(y=audio, sr=sr)

def compute_audio_noisiness(audio, sr):
    # Zero-crossing rate determines how frequently the audio waveform changes direction, 
    # i.e. how noisy or speech-like it is

    return librosa.feature.zero_crossing_rate(audio)
