# formatting audio files for RVC training
import os
import time
import librosa
import soundfile as sf
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from functools import partial

# from config import TARGET_SR, RAW_AUDIO, PROCESSED_AUDIO

logging.basicConfig(level=logging.INFO)  # Set up logging to display info messages


def process_file(input_path, config):
    try:
        # create a unique output path
        relative_path = os.path.relpath(input_path, config.raw_audio)
        output_path = os.path.join(config.processed_audio, relative_path)
        output_path = os.path.splitext(output_path)[0] + ".wav"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # skip if already processed
        if os.path.exists(output_path):
            logging.info(f"Already processed: {input_path} -> {output_path}")
            return {"status": "skipped", "input": input_path, "output": output_path}

        # Load audio, resample to TARGET_SR, and convert to mono
        audio, _ = librosa.load(input_path, sr=config.target_sr, mono=True)

        if audio is None or len(audio) == 0:
            raise ValueError("Empty audio file")

        # Normalize (important for RVC)
        audio = librosa.util.normalize(audio)

        # Save
        sf.write(output_path, audio, config.target_sr)

        # processing...
        logging.info(f"Processed: {relative_path}")
        return {"status": "success", "input": input_path, "output": output_path}

    except Exception as e:
        logging.error(f"Error: {input_path} → {e}")
        return {"status": "failed", "input": input_path, "error": str(e)}


def preprocess_all(config):
    start_time = time.time()
    os.makedirs(
        config.processed_audio, exist_ok=True
    )  # Create processed audio directory if it doesn't exist

    tasks = []

    # Walk through all files in the raw audio directory and its subdirectories
    for root, _, files in os.walk(config.raw_audio):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac")):
                tasks.append(
                    os.path.join(root, file)
                )  # Add file path to processing tasks

    # Validate dataset
    if not tasks:
        logging.warning("No audio files found in the raw audio directory.")
        return {}

    logging.info(
        f"Found {len(tasks)} audio files to process. Starting preprocessing..."
    )
    processed = 0
    failed = 0

    # Parallel processing with ProcessPoolExecutor for better performance on multiple files
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        # Create a partial function with fixed parameters
        worker = partial(process_file, config=config)  

        # start processing tasks in parallel
        futures = {executor.submit(worker, task): task for task in tasks}
        results = []

        # Log results and show progress with tqdm as tasks complete.
        # Note: as_complted returns futures as they finish, so we can log results in real-time.
        for future in tqdm(
            as_completed(futures), total=len(tasks), desc="Processing audio"
        ):
            try:
                # Get the result of the processing task (if any)
                result = (future.result())  
                results.append(result)

                if result["status"] == "success":
                    logging.info(f"Processed: {result['input']}")
                elif result["status"] == "failed":
                    logging.error(f"Failed: {result['input']} -> {result['error']}")

            except Exception as e:
                logging.error(f"Processing Failed: {e}")

    # Summarize results
    processed = sum(1 for r in results if r and r["status"] == "success")
    failed = sum(1 for r in results if r and r["status"] == "failed")
    skipped = sum(1 for r in results if r and r["status"] == "skipped")
    logging.info(f"Preprocessing complete -> Success: {processed}, Failed: {failed}, Skipped: {skipped}")

    end_time = time.time() - start_time
    logging.info(f"Total preprocessing time: {end_time:.2f} seconds")

    return {
        "total": len(results),
        "processed": processed,
        "failed": failed,
        "skipped": skipped,
        "results": results,
    }