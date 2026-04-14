import os

RAW_AUDIO = "data/raw" # input audio files
PROCESSED_AUDIO = "data/processed" # cleaned full audio files
DATASET_DIR = "data/dataset" # final training clips

TARGET_SR = 40000 # Target sampling rate for audio processing, standard for RVC training
CHUNK_LENGTH = 8000  # milliseconds (8 sec)
MAX_CHUNK_LENGTH = 10000  # milliseconds (10 sec)
MIN_SILENCE_LENGTH = 400 # milliseconds (0.4 sec) - minimum length of silence to be considered as silence
SILENCE_THRESHOLD = -40 # Volume level (in dB) below which audio is considered “silent”.

EXPERIMENT_NAME = "voice_model_1" #folder name where your model + training data lives

RVC_DIR = os.path.join("models", "rvc")  # Path to the RVC repository
RVC_TRAIN_SCRIPT = os.path.join("infer", "modules", "train", "train.py") # Path to the RVC training script from RVC repository

