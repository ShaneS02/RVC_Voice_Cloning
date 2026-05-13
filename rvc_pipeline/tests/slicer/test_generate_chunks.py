import numpy as np

from rvc_pipeline.slicer import generate_chunks

# Test cases for generate_chunks function
def test_generate_chunks_basic(config_with_dirs):
    audio = np.arange(config_with_dirs.target_sr * 3)  # 3 seconds @16kHz
    intervals = [(0, len(audio))]

    config_with_dirs.chunk_length = 1000  # 1 second chunks
    chunks = list(generate_chunks(intervals, audio, config_with_dirs.target_sr, config_with_dirs))

    # 3 chunks of 1 second each
    assert len(chunks) == 3
    assert all(len(c) == config_with_dirs.target_sr for c in chunks)

# Test that chunks shorter than min_chunk_length are filtered out
def test_generate_chunks_min_length_filter(config_with_dirs):
    audio = np.arange(config_with_dirs.target_sr)  # 1 second
    intervals = [(0, len(audio))]

    config_with_dirs.min_chunk_length = 2000  # require 2 seconds

    chunks = list(generate_chunks(intervals, audio, config_with_dirs.target_sr, config_with_dirs))

    assert len(chunks) == 0

# Test that it correctly handles multiple intervals
def test_generate_chunks_multiple_intervals(config_with_dirs):
    number_of_seconds = 4
    audio = np.arange(config_with_dirs.target_sr * number_of_seconds) # 4 seconds @16kHz
    intervals = [
        (0, config_with_dirs.target_sr * 2), # 0-2 sec
        (config_with_dirs.target_sr * 2, config_with_dirs.target_sr * number_of_seconds) # 2-4 sec
    ]

    config_with_dirs.chunk_length = 2000  # 2 second chunks

    chunks = list(generate_chunks(intervals, audio, config_with_dirs.target_sr, config_with_dirs))

    assert len(chunks) == 2