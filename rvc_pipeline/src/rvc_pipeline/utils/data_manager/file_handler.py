import os

def create_directory(dir):
    os.makedirs(dir, exist_ok=True) 

def load_audio_files(directory_path, extensions=(".mp3", ".wav", ".flac")):
    audio_files = []
    # Walk through all files in the raw audio directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(extensions):
                audio_files.append(
                    os.path.join(root, file)
                )  # Add file path to processing tasks 
    
    return audio_files

def get_relative_path(input_path, base_dir):
    return os.path.relpath(input_path, base_dir)

def create_audio_file_path(relative_path, output_dir, extension=".wav"):
    # create a unique output path
    output_path = os.path.join(output_dir, relative_path)
    output_path = os.path.splitext(output_path)[0] + extension
    return output_path

def get_directory_from_file_path(file_path):
    return os.path.dirname(file_path)

def file_path_exists(dir):
    return os.path.exists(dir)