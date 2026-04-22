# formatting audio files for RVC training
import time
import librosa
import soundfile as sf
import logging

from .execution_results import ExecutionResult, summarize_results
from .utils.concurrency.task_executor import execute_parallel_tasks
from .utils.data_manager.file_handler import (
    create_directory,
    load_audio_files,
    get_relative_path,
    create_audio_file_path,
    get_directory_from_file_path,
    file_path_exists,
)

logger = logging.getLogger(__name__)  # Create a logger for this module

def process_file(input_path, config):
    try:
        # create a unique output path
        relative_path = get_relative_path(input_path, config.raw_audio)
        output_path = create_audio_file_path(relative_path, config.processed_audio)

        # Ensure output directory exists
        create_directory(get_directory_from_file_path(output_path))  

        # skip if already processed
        if file_path_exists(output_path):
            logger.info(f"Skipping already processed file: {input_path} -> {output_path}")
            return ExecutionResult.skipped(
                input_path, 
                reason=f"Already processed: {input_path} -> {output_path}"
            )

        # Load audio, resample to TARGET_SR, and convert to mono
        audio, _ = librosa.load(input_path, sr=config.target_sr, mono=True)

        if audio is None or len(audio) == 0:
            raise ValueError("Empty audio file")

        # Normalize (important for RVC)
        audio = librosa.util.normalize(audio)

        # Save 
        sf.write(output_path, audio, config.target_sr)

        # processing...
        logger.info(f"Processed: {relative_path}")
        return ExecutionResult.success(input_path, output_path)

    except Exception as e:
        logger.error(f"Error: {input_path} → {e}")
        return ExecutionResult.error(input_path, str(e))


def preprocess_all(config):
    start_time = time.time()
    
    #create processed audio directory if it doesn't exist
    create_directory(config.processed_audio)

    # Gather all audio files from the raw audio directory
    audio_files = load_audio_files(config.raw_audio)

    # Validate audio files exists before processing
    if not audio_files:
        logger.warning("No audio files found in the raw audio directory.")
        return {}

    logger.info(f"Found {len(audio_files)} audio files to process. Starting preprocessing...")
    
    # Process files in parallel
    results = execute_parallel_tasks(process_file, audio_files, config, "Preprocessing audio files")
    
    # Summarize results
    summary = summarize_results(results)

    end_time = time.time() - start_time
    logger.info(f"Total preprocessing time: {end_time:.2f} seconds")

    logger.info(f"Preprocessing complete -> Success: {summary['success']}, Failed: {summary['failed']}, Skipped: {summary['skipped']}")

    return {
        "results": results,
        "summary": summary
    }