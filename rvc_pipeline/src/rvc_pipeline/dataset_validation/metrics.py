import numpy as np
import pyloudnorm as pyln
from .models import AudioMetrics
from ..utils.data_manager.audio_handler import(
    compute_rms, 
    compute_audio_brightness,
    compute_audio_noisiness
)

#np.ndarray is the format returned by librosa.load, used to retrive audi data


def compute_rms(audio: np.ndarray) -> float:  
    return np.sqrt(np.mean(audio ** 2))
    
def compute_peak_db(audio: np.ndarray) -> float:
    peak = np.max(np.abs(audio))
    if peak == 0:
        return -100.0  # Return a very low dB value for silence
    
    return 20 * np.log10(peak) # Convert to decibels

def compute_clipping_ratio(audio: np.ndarray) -> float:
    
    # Count samples that are at or above the clipping threshold 
    # (0.999 for normalized audio) and divide by total samples
    return np.mean(np.abs(audio) >= 0.999) 

# Compute the ratio of silent frames in the audio based on RMS threshold
def compute_silence_ratio(audio: np.ndarray, threshold: float = 0.01, frame_length: int = 2048, hop_length: int = 512) -> float:
    rms = compute_rms(audio, frame_length, hop_length)

    silent_frames = rms < threshold
    silence_ratio = np.mean(silent_frames)
    return silence_ratio

# Compute the duration of the audio in seconds
def compute_duration(audio: np.ndarray, sr: int) -> float:
    return (len(audio) / sr ) 

# Additional feature extraction functions for dataset validation

# Compute the integrated loudness in LUFS using pyloudnorm
# This provides a more perceptually relevant measure of loudness than simple RMS or peak dB
def compute_lufs(audio: np.ndarray, sr: int) -> float:
    meter = pyln.Meter(sr)
    return meter.integrated_loudness(audio)

# Compute the spectral centroid, which indicates the "brightness" of the audio
def compute_spectral_centroid(audio: np.ndarray, sr: int) -> float:
    return float(np.mean(compute_audio_brightness(audio, sr)))

# Compute the zero-crossing rate, which can indicate noisiness or speech-like qualities
def compute_zero_crossing_rate(audio: np.ndarray, sr: int) -> float:
    return float(np.mean(compute_audio_noisiness(audio, sr)))
    

# Central function to compute all validation metrics for a given audio clip
def analyze_audio(audio: np.ndarray, sr: int) -> AudioMetrics:

    return AudioMetrics(
        duration_ms=compute_duration(audio, sr) * 1000,
        rms=compute_rms(audio),
        peak_dbfs=compute_peak_db(audio),
        clipping_ratio=compute_clipping_ratio(audio),
        silence_ratio=compute_silence_ratio(audio)
    )