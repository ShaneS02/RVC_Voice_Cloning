import logging
import sys
from pathlib import Path


def setup_logging(log_file: str | None = None, level=logging.INFO):
    """
    Configure global logging for the entire application.
    
    Args:
        log_file (str | None): Optional file path to write logs if needed in the future.
        level: Logging level (default: INFO)
    """
    handlers = []

    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)

    # File handler (for future use)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Apply configuration
    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True,  # ensures reconfiguration works if called multiple times
    )