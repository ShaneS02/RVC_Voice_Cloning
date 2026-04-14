#formatting audio files for RVC training
import os
import librosa
import soundfile as sf
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from config import TARGET_SR, RAW_AUDIO, PROCESSED_AUDIO

logging.basicConfig(level=logging.INFO) # Set up logging to display info messages

def process_file(input_path):
    try:
        #create a unique output path
        relative_path = os.path.relpath(input_path, RAW_AUDIO)
        safe_relative_path = relative_path.replace(os.sep, "_")  # Replace path separators with underscores
        output_path = os.path.join(PROCESSED_AUDIO, os.path.splitext(safe_relative_path)[0] + ".wav")

        #skip if already processed
        if os.path.exists(output_path):
            logging.info(f"Already processed: {input_path} -> {output_path}")
            return

        # Load audio, resample to TARGET_SR, and convert to mono
        audio, _ = librosa.load(input_path, sr=TARGET_SR, mono=True) 

        # Normalize (important for RVC)
        audio = librosa.util.normalize(audio)

        # Save
        sf.write(output_path, audio, TARGET_SR)

        # processing...
        logging.info(f"Processed: {relative_path}")
        return
    
    except Exception as e:
        logging.error(f"Error: {input_path} → {e}")


def preprocess_all():
    os.makedirs(PROCESSED_AUDIO, exist_ok=True) # Create processed audio directory if it doesn't exist

    tasks = [] 

    # Walk through all files in the raw audio directory and its subdirectories
    for root, _, files in os.walk(RAW_AUDIO): 
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac")):
                tasks.append(os.path.join(root, file)) # Add file path to processing tasks

    #Validate dataset
    if not tasks:
        logging.warning("No audio files found in the raw audio directory.")
        return
    
    logging.info(f"Found {len(tasks)} audio files to process. Starting preprocessing...")
    processed = 0
    failed = 0

    # Parallel processing with ProcessPoolExecutor for better performance on multiple files
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        #start processing tasks in parallel
        futures = {executor.submit(process_file, task): task for task in tasks}
            
        # Log results and show progress with tqdm as tasks complete. 
        # Note: as_complted returns futures as they finish, so we can log results in real-time.
        for future in tqdm(as_completed(futures), total=len(tasks), desc="Processing audio"):
            try:
                result = future.result() # Get the result of the processing task (if any)
                logging.info(result)
                processed += 1
            except Exception as e:
                failed += 1
                logging.error(f"Processing Failed: {e}")

    logging.info(f"Preprocessing complete → Success: {processed}, Failed: {failed}")