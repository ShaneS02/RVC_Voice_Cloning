import numpy as np
from rvc_pipeline.slicer import split_audio, generate_chunks


# Test edge case with all silent audio
def test_all_silent_audio(config_with_dirs):
    audio = np.zeros(16000)
    config_with_dirs.chunk_length = 1000
    config_with_dirs.min_chunk_length = 500

    intervals = split_audio(audio, config_with_dirs.silence_threshold)
    chunks = list(generate_chunks(intervals, audio, 16000, config_with_dirs))

    # depends on whether you added silence filtering
    assert len(chunks) == 0

# Test edge case with very short audio that is shorter than the minimum chunk length
def test_very_short_audio(config_with_dirs):
    audio = np.arange(1000)
    intervals = split_audio(audio, config_with_dirs.silence_threshold)

    config_with_dirs.chunk_length = 1000
    config_with_dirs.min_chunk_length = 200  # too large for this audio

    chunks = list(generate_chunks(intervals, audio, 16000, config_with_dirs))

    assert len(chunks) == 0

# Test edge case with no silence in the audio
def test_no_silence_large_audio(config_with_dirs):
    audio = np.arange(16000 * 5)
    intervals = split_audio(audio, config_with_dirs.silence_threshold)

    config_with_dirs.chunk_length = 1000
    config_with_dirs.min_chunk_length = 500
    chunks = list(generate_chunks(intervals, audio, 16000, config_with_dirs))

    assert len(chunks) == 5