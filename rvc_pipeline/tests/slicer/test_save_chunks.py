import numpy as np

from rvc_pipeline.slicer import save_chunks

# Helper function to create dummy audio files for testing
def create_audio(duration_sec=1.0, sample_rate=40000, silence=False):
    num_samples = int(duration_sec * sample_rate)
    
    return np.random.randn(num_samples).astype(np.float32)

# Test cases for save_chunks function 
def test_save_chunks_calls_save_audio(tmp_path, mocker):
    chunks = [create_audio(sample_rate=16000), create_audio(sample_rate=16000)]

    mock_save = mocker.patch("rvc_pipeline.slicer.save_audio")

    output_path = tmp_path / "test.wav"

    result = save_chunks(chunks, output_path, 16000)

    assert result["saved"] == 2
    assert result["failed"] == 0
    assert mock_save.call_count == 2

# Test that save_chunks actually writes files to disk
def test_save_chunks_writes_files(tmp_path):
    chunks = [create_audio(sample_rate=16000), create_audio(sample_rate=16000)]
    output_path = tmp_path / "test.wav"

    save_chunks(chunks, output_path, 16000)
    saved_files = list(tmp_path.glob("*.wav"))

    assert len(saved_files) == 2
    

def test_save_chunks_failure(tmp_path, mocker):
    chunks = [create_audio(sample_rate=16000), create_audio(sample_rate=16000)]

    mocker.patch(
        "rvc_pipeline.slicer.save_audio",
        side_effect=Exception("fail")
    )

    output_path = tmp_path / "test.wav"

    result = save_chunks(chunks, output_path, 16000)

    assert result["saved"] == 0
    assert result["failed"] == 2