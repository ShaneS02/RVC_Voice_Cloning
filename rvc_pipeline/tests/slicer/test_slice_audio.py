from pathlib import Path

import numpy as np
import soundfile as sf
from rvc_pipeline.slicer import slice_audio


# This test checks that if the processed_audio directory is empty,
# the slice_audio function runs without error and does not produce any output files
def test_slice_audio_empty(config_with_dirs):
    slice_audio(config_with_dirs)

    output_files = list(Path(config_with_dirs.dataset_dir).rglob("*.wav"))
    
    # Verify no output files created
    assert len(output_files) == 0


# This test checks that the full slice_audio function processes files 
# in the processed_audio directory and produces output files in the dataset_dir
def test_slice_audio_processes_files(config_with_dirs):
    # Create real audio file
    audio_path = Path(config_with_dirs.processed_audio) / "test.wav"

    # Create 1 second of random audio at 16kHz
    audio = np.random.randn(16000).astype(np.float32)
    sf.write(audio_path, audio, 16000)

    # Run full pipeline
    slice_audio(config_with_dirs)
    
    output_files = list(Path(config_with_dirs.dataset_dir).rglob("*.wav"))

    # Verify output files created
    assert len(output_files) > 0