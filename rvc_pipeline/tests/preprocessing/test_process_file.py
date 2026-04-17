import numpy as np
import soundfile as sf

from rvc_pipeline import process_file, ProcessConfig

# Helper function to create dummy audio files for testing
def create_dummy_wav(file_path, duration_sec=1.0, sample_rate=40000, silence=False):
    num_samples = int(duration_sec * sample_rate)

    if silence:
        audio = np.zeros(num_samples, dtype=np.float32)
    else:
        audio = np.random.randn(num_samples).astype(np.float32)

    sf.write(file_path, audio, sample_rate)


# Test cases for process_file function

def test_process_file_returns_structure(tmp_path):
    dummy_audio = tmp_path / "test.wav"
    create_dummy_wav(dummy_audio, duration_sec=2.0, sample_rate=40000)
    config = ProcessConfig()
    result = process_file(str(dummy_audio), config)

    assert result is not None
    assert "status" in result
    assert "input" in result

def test_process_file_valid(tmp_path):
    # Setup temporary directories
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()
    processed_dir.mkdir()
    
    # create dummy audio
    file_path = raw_dir / "test.wav"
    create_dummy_wav(file_path, duration_sec=1.0, sample_rate=22050)

    
    config = ProcessConfig(
        raw_audio=str(raw_dir),
        processed_audio=str(processed_dir),
        target_sr=16000
    )

    # Process the file and assert success
    result = process_file(str(file_path), config)   
    assert result["status"] == "success"

    # Check output exists and has correct properties
    output_files = list(processed_dir.glob("**/*.wav"))
    assert len(output_files) == 1

    #validate audio properties
    audio, sr = sf.read(output_files[0])
    assert sr == 16000
    assert audio.ndim == 1  # mono
    assert abs(audio).max() <= 1.01

def test_process_file_corrupt(tmp_path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir()
    processed_dir.mkdir()

    bad_file = raw_dir / "bad.wav"
    bad_file.write_text("not audio")
    config = ProcessConfig(
        raw_audio=str(raw_dir),
        processed_audio=str(processed_dir),
        target_sr=16000
    )

    process_file(str(bad_file), config)

    # Should not create output
    assert len(list(processed_dir.glob("*"))) == 0