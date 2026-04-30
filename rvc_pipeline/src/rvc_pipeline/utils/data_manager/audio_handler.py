import librosa
import soundfile as sf


def load_audio(file_path, sample_rate=None, mono=True):
    audio, sr = librosa.load(file_path, sr=sample_rate, mono=mono)
    return audio, sr

def normalize_audio(audio):
    return librosa.util.normalize(audio)

def split_audio(audio, top_db):
    return librosa.effects.split(audio, top_db=abs(top_db))

def save_audio(file_path, audio, sample_rate):
    sf.write(file_path, audio, sample_rate)
