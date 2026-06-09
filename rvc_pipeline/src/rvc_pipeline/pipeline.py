#main orchestrator
from .preprocess import preprocess_all
from .slicer import slice_audio
from .dataset import validate_dataset
from .train import train
from rvc_pipeline import ProcessConfig, setup_logging  

def run_pipeline():
    setup_logging(log_file="logs/app.log")
    config = ProcessConfig()

    print("Step 1: Preprocessing audio...")
    preprocess_all(config)

    print("Step 2: Slicing audio...")
    slice_audio(config)

    print("Step 3: Validating dataset...")
    validate_dataset(config)

    print("Step 4: Training model...")
    train(config)

    print("Pipeline complete.")