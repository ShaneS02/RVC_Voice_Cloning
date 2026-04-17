import os
from pydantic import BaseModel

class ProcessConfig(BaseModel):

    raw_audio: str = "data/raw" # input audio files
    processed_audio: str = "data/processed" # cleaned full audio files
    dataset_dir: str = "data/dataset" # final training clips

    target_sr: int = 40000 # Target sampling rate for audio processing, standard for RVC training
    chunk_length: int = 8000  # milliseconds (8 sec)
    min_silence_length: int = 400 # milliseconds (0.4 sec) - minimum length of silence to be considered as silence
    silence_threshold: int = -40 # Volume level (in dB) below which audio is considered “silent”.

    experiment_name: str = "voice_model_1" #folder name where your model + training data lives

    rvc_dir: str = os.path.join("models", "rvc")  # Path to the RVC repository
    rvc_train_script: str = os.path.join("infer", "modules", "train", "train.py") # Path to the RVC training script from RVC repository

