import os

def create_directory(dir : str):
    os.makedirs(dir, exist_ok=True) 

def load_audio_files(directory_path : str, extensions=(".mp3", ".wav", ".flac")) -> list:
    audio_files = []
    # Walk through all files in the raw audio directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(extensions):
                audio_files.append(
                    os.path.join(root, file)
                )  # Add file path to processing tasks 
    
    return audio_files

def get_relative_path(input_path, base_dir) -> str:
    return os.path.relpath(input_path, base_dir)

def create_audio_file_path(relative_path : str, output_dir : str, extension=".wav") -> str:
    # create a unique output path
    output_path = os.path.join(output_dir, relative_path)
    removed_extension, _ = split_file_path(output_path)
    output_path = removed_extension + extension
    return output_path

def split_file_path(file_path : str) -> tuple:
    path, extension = os.path.splitext(file_path)
    return path, extension

def get_directory_from_file_path(file_path : str) -> str:
    return os.path.dirname(file_path)

def file_path_exists(dir : str) -> bool:
    return os.path.exists(dir)