from pathlib import Path
import numpy as np
import soundfile as sf

from rvc_pipeline.slicer import slice_file

# Helper function to create dummy audio files for testing
def create_audio(duration_sec=1.0, sample_rate=40000, silence=False):
    num_samples = int(duration_sec * sample_rate)
    
    return np.random.randn(num_samples).astype(np.float32)


# This test checks that a normal audio file is processed successfully and produces output files
def test_slice_file_success(config_with_dirs):
    # Create real audio file
    audio = create_audio(duration_sec=2.0)
    audio_path = Path(config_with_dirs.processed_audio) / "test.wav"
    sf.write(audio_path, audio, 16000)

    # change config setting
    config_with_dirs.chunk_length = 1000
    config_with_dirs.min_chunk_length = 500

    result = slice_file(audio_path, config_with_dirs)

    assert result.status == "success"

    # Verify files actually created
    output_files = list(Path(config_with_dirs.dataset_dir).glob("**/*.wav"))

    assert len(output_files) > 0

# This test checks that if the input file is too short to produce valid chunks, 
# we get an error result with the appropriate message instead of an exception
def test_slice_file_no_chunks(config_with_dirs):
    # Create very short audio file (0.1 sec)
    audio_path = Path(config_with_dirs.processed_audio) / "short.wav"

    audio = create_audio(duration_sec=0.1, sample_rate=16000) # 1600 samples @16kHz = 0.1 sec

    sf.write(audio_path, audio, 16000)

    # Config where min chunk length is too large
    config_with_dirs.chunk_length = 1000
    config_with_dirs.min_chunk_length = 500

    result = slice_file(audio_path, config_with_dirs)

    assert result.status == "error"
    assert "No valid chunks" in result.message

    # Verify no files written
    output_files = list(Path(config_with_dirs.dataset_dir).rglob("*.wav"))

    assert len(output_files) == 0

# This test checks that if the input file doesn't exist, 
# we get an error result instead of an exception
def test_slice_file_exception(config_with_dirs):
    missing_audio = Path("does_not_exist.wav")

    result = slice_file(missing_audio, config_with_dirs)

    assert result.status == "error"
    assert result.message is not None