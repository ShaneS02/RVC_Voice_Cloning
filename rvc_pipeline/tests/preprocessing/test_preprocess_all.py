
import numpy as np
import soundfile as sf
import pytest


from rvc_pipeline import preprocess_all, ProcessConfig
from pathlib import Path

@pytest.fixture
def config_with_dirs(tmp_path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"

    raw_dir.mkdir()
    processed_dir.mkdir()

    return ProcessConfig(
        raw_audio=str(raw_dir),
        processed_audio=str(processed_dir),
        target_sr=16000
    )

# Helper function to create dummy audio files for testing
def create_dummy_wav(file_path, duration_sec=1.0, sample_rate=40000, silence=False):
    num_samples = int(duration_sec * sample_rate)

    if silence:
        audio = np.zeros(num_samples, dtype=np.float32)
    else:
        audio = np.random.randn(num_samples).astype(np.float32)

    sf.write(file_path, audio, sample_rate)

# Test that preprocess_all handles empty dataset gracefully
def test_preprocess_all_empty_dataset(config_with_dirs, caplog):
    result = preprocess_all(config_with_dirs)

    assert result == {}
    assert "No audio files found" in caplog.text

# Test that valid files of different types are processed and invalid files are ignored
def test_preprocess_all_mixed_file_types(config_with_dirs):
    raw_dir = Path(config_with_dirs.raw_audio)

    # Valid audio files
    create_dummy_wav(raw_dir / "a.wav")
    create_dummy_wav(raw_dir / "b.wav")
    create_dummy_wav(raw_dir / "c.flac")

    # Invalid / ignored files
    (raw_dir / "ignore.txt").write_text("not audio")
    (raw_dir / "data.json").write_text("{}")

    result = preprocess_all(config_with_dirs)

    assert result["total"] == 3
    assert result["processed"] == 3
    assert result["failed"] == 0

#Test parallel processing stability with multiple files and a corrupt file
def test_preprocess_all_parallel_stability(config_with_dirs):
    raw_dir = Path(config_with_dirs.raw_audio)

    # Create multiple files to trigger parallelism
    for i in range(10):
        create_dummy_wav(raw_dir / f"file_{i}.wav")
    
    (raw_dir / "bad.wav").write_text("corrupted") # Add a corrupt file to test error handling

    result = preprocess_all(config_with_dirs)

    assert result["total"] == 11
    assert result["processed"] == 10
    assert result["failed"] == 1

    # Ensure all outputs exist
    for i in range(10):
        assert (Path(config_with_dirs.processed_audio) / f"file_{i}.wav").exists()