import os
from pydantic import BaseModel, Field

class ProcessConfig(BaseModel):

    raw_audio: str = "data/raw" # input audio files
    processed_audio: str = "data/processed" # cleaned full audio files
    dataset_dir: str = "data/dataset" # final training clips

    # Target sampling rate for audio processing, standard for RVC training
    target_sr: int = Field(default=40000, gt=0)

    chunk_length: int = Field(
        default=8000, # milliseconds (8 sec)
        gt=0,
        description="Chunk length in milliseconds"
    )

    min_chunk_length: int = Field(
        default=300, # milliseconds (0.3 sec)
        gt=0,
        description="Minimum chunk length in milliseconds"
    )

    min_silence_length: int = Field(
        default=400, # milliseconds (0.4 sec)
        gt=0,
        description="Minimum silence length in milliseconds"
    )

    silence_threshold: int = Field(
        default=-40,
        description="Volume level (in dB) below which audio is considered “silent”."
    )

    min_dataset_clips: int = Field(
        default=50,
        gt=0,
        description="Minimum number of audio clips required in the dataset for training"
    )

    experiment_name: str = "voice_model_1" #folder name where your model + training data lives

    rvc_dir: str = os.path.join("models", "rvc")  # Path to the RVC repository
    
    # Path to the RVC training script from RVC repository
    rvc_train_script: str = os.path.join(
        "infer", 
        "modules", 
        "train", 
        "train.py"
    ) 

