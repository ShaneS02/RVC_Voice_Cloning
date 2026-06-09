from .dataset_validation.validator import DatasetValidator
from .config.process_config import ProcessConfig
from .config.validation_config import ValidationConfig

from .dataset_validation.metrics import analyze_audio
from .utils.data_manager.audio_handler import load_audio
from .utils.data_manager.file_handler import load_audio_files
import logging

logger = logging.getLogger(__name__)
    
def validate_dataset(config: ProcessConfig):
    files = load_audio_files(config.dataset_dir)

    logger.info(f"Total dataset clips: {len(files)}")

    if len(files) < config.min_dataset_clips:
        logger.warning(f"Only {len(files)} clips found. Dataset may be too small for good results.")

    validator = DatasetValidator(ValidationConfig()) 
    results = []

    for file in files:
        audio, sr = load_audio(file)

        metrics = analyze_audio(audio, sr)

        result = validator.validate(file, metrics)

        results.append(result)
    

    # Log summary of validation results
    summary = _summarize_validation_results(results)
    logger.info(f"Validation Summary: {summary}")
    
    return results



def _summarize_validation_results(results: list) -> dict:
    total_files = len(results)
    valid_files = sum(1 for r in results if r.valid)
    rejected_files = sum(1 for r in results if not r.valid)
    average_rms = sum(r.metrics.rms for r in results) / total_files
    average_duration_ms = sum(r.metrics.duration_ms for r in results) / total_files
    average_silence_ratio = sum(r.metrics.silence_ratio for r in results) / total_files 

    
    return {
        "total_files": total_files,
        "valid_files": valid_files,
        "rejected_files": rejected_files,
        "average_rms": average_rms,
        "average_duration_ms": average_duration_ms,
        "average_silence_ratio": average_silence_ratio,
    }




    return results