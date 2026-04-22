from pathlib import Path

import numpy as np
import soundfile as sf
import os

from rvc_pipeline import process_file, ExecutionResult

# Note: These tests focus on the process_file function

# Helper function to create dummy audio files for testing
def create_dummy_wav(file_path, duration_sec=1.0, sample_rate=40000, silence=False):
    num_samples = int(duration_sec * sample_rate)

    if silence:
        audio = np.zeros(num_samples, dtype=np.float32)
    else:
        audio = np.random.randn(num_samples).astype(np.float32)

    sf.write(file_path, audio, sample_rate)


# Test cases for process_file function
def test_process_file_returns_structure(config_with_dirs):
    dummy_audio = Path(config_with_dirs.raw_audio) / "test.wav"
    create_dummy_wav(dummy_audio, duration_sec=2.0, sample_rate=40000)
    result = process_file(str(dummy_audio), config_with_dirs)

    assert result is not None
    assert isinstance(result, ExecutionResult)

# Test that valid files are processed successfully
def test_process_file_valid(config_with_dirs):
    file_path = Path(config_with_dirs.raw_audio) / "test.wav"

    # create dummy audio
    create_dummy_wav(file_path, duration_sec=1.0, sample_rate=16000)

    # Process the file and assert success
    result = process_file(str(file_path), config_with_dirs)   
    assert result.status == "success"

    # Check output exists and has correct properties
    output_files = list(Path(config_with_dirs.processed_audio).glob("**/*.wav"))
    assert len(output_files) == 1

    #validate audio properties
    audio, sr = sf.read(output_files[0])
    assert sr == 16000
    assert audio.ndim == 1  # mono
    assert abs(audio).max() <= 1.01

# Test that corrupt files are handled gracefully
def test_process_file_corrupt(config_with_dirs):
    bad_file = Path(config_with_dirs.raw_audio) / "bad.wav"
    bad_file.write_text("not audio")
    process_file(str(bad_file), config_with_dirs)

    # Should not create output
    assert len(list(Path(config_with_dirs.processed_audio).glob("*"))) == 0

# Test that already processed files are skipped
def test_process_skips_processed_files(config_with_dirs):
    # Create input file
    input_file = Path(config_with_dirs.raw_audio) / "test.wav"
    create_dummy_wav(input_file, duration_sec=1.0, sample_rate=16000)

    # Create already processed output file
    output_file = Path(config_with_dirs.processed_audio) / "test.wav"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    create_dummy_wav(output_file, duration_sec=1.0, sample_rate=16000)

    result = process_file(str(input_file), config_with_dirs)

    assert result.status == "skipped"
    assert result.output == None

# Test that files in nested directories are processed and output structure is preserved
def test_process_file_nested_directories(config_with_dirs):
    raw_dir = Path(config_with_dirs.raw_audio)

    nested_dir = raw_dir / "speaker1" / "sessionA"
    nested_dir.mkdir(parents=True)

    input_file = nested_dir / "voice.wav"
    create_dummy_wav(input_file, duration_sec=1.0, sample_rate=16000)

    result = process_file(str(input_file), config_with_dirs)

    processed_dir = Path(config_with_dirs.processed_audio)
    expected_output = processed_dir / "speaker1" / "sessionA" / "voice.wav"

    assert result.status == "success"
    assert expected_output.exists()
    assert result.output == str(expected_output)
    assert os.path.commonpath([expected_output, processed_dir]) == config_with_dirs.processed_audio