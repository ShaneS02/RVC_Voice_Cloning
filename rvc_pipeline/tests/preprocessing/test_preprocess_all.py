
import logging
import numpy as np
import soundfile as sf
from rvc_pipeline import preprocess_all
from pathlib import Path

logger = logging.getLogger(__name__)  # Create a logger for this module

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

    results = preprocess_all(config_with_dirs)

    assert results["summary"]["total_files"] == 3
    assert results["summary"]["success"] == 3
    assert results["summary"]["failed"] == 0
    assert results["summary"]["skipped"] == 0

#Test parallel processing stability with multiple files and a corrupt file
def test_preprocess_all_parallel_stability(config_with_dirs):
    raw_dir = Path(config_with_dirs.raw_audio)

    # Create multiple files to trigger parallelism
    for i in range(10):
        create_dummy_wav(raw_dir / f"file_{i}.wav")
    
    (raw_dir / "bad.wav").write_text("corrupted") # Add a corrupt file to test error handling

    result = preprocess_all(config_with_dirs)

    assert result["summary"]["total_files"] == 11
    assert result["summary"]["success"] == 10
    assert result["summary"]["failed"] == 1
    assert result["summary"]["skipped"] == 0

    # Ensure all outputs exist
    for i in range(10):
        assert (Path(config_with_dirs.processed_audio) / f"file_{i}.wav").exists()