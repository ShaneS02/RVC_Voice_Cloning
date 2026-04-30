#(remove silence + chunk)

import logging
from .config import ProcessConfig
from .utils.concurrency.task_executor import execute_parallel_tasks
from .execution_results import ExecutionResult, summarize_results
from .utils.data_manager.audio_handler import (
    load_audio, 
    split_audio,
    save_audio
)
from .utils.data_manager.file_handler import (
    create_audio_file_path, 
    create_directory, 
    get_directory_from_file_path,
    get_relative_path, load_audio_files
)

logger = logging.getLogger(__name__)

def generate_chunks(intervals, audio, sample_rate, config):
    chunk_samples = int(config.chunk_length * sample_rate / 1000)
    min_samples = int(config.min_chunk_length * sample_rate)

    # Process each non-silent interval and chunk it into smaller pieces
    for start, end in intervals:
        chunk = audio[start:end]

        for i in range(0, len(chunk), chunk_samples):
            sub_chunk = chunk[i:i + chunk_samples]

            # Skip very short clips 
            if len(sub_chunk) < min_samples:
                continue

            yield sub_chunk

def save_chunks(chunks, output_path, sample_rate):
    file_index = 1
    failed_count = 0

    # Process each non-silent interval and chunk it into smaller pieces
    for chunk in chunks:
        out_path = output_path.parent / f"{output_path.stem}_{file_index}.wav"
        
        try:
            save_audio(out_path, chunk, sample_rate) # Save chunk as .wav
            file_index += 1
        except Exception as e:
            failed_count += 1
            
    
    return {"saved": file_index - 1, "failed": failed_count}


def slice_file(audio_path, config: ProcessConfig) -> int:
    try:
        # create a unique output path
        relative_path = get_relative_path(audio_path, config.processed_audio)
        output_path = create_audio_file_path(relative_path, config.dataset_dir)

        # Ensure output directory exists
        create_directory(get_directory_from_file_path(output_path)) 
        
        # Load audio without resampling (keep original sample rate)
        audio, sample_rate = load_audio(audio_path, sample_rate=None)
        
        if audio is None or len(audio) == 0:
            raise ValueError("Empty audio file")

        # Split audio into non-silent intervals
        intervals = split_audio(audio, config.silence_threshold)

        # Generate chunks from non-silent intervals
        chunks = generate_chunks(intervals, audio, sample_rate, config)

        # Save chunks and get results
        save_results = save_chunks(chunks, output_path, sample_rate)

        if save_results["saved"] == 0:
            return ExecutionResult.error(
                input=audio_path,
                error="No valid chunks produced"
            )

        return ExecutionResult.success(input=audio_path, output=config.dataset_dir)

    except Exception as e:
        logger.error(f"Failed slicing {audio_path}: {e}")
        return ExecutionResult.error(input=audio_path, error=str(e))

def slice_audio(config: ProcessConfig):
    # Create dataset directory if it doesn't exist
    create_directory(config.dataset_dir)

    # Gather all processed .wav files 
    audio_files = load_audio_files(config.processed_audio, extensions=(".wav"))  
    
    logger.info(f"Found {len(audio_files)} files")
    
    # Process files in parallel
    results = execute_parallel_tasks(slice_file, audio_files, config=config, desc="Removing Silence and Chunking")

    # Summarize results
    summarize_results(results)