import os

import pytest
from rvc_pipeline import setup_logging
from rvc_pipeline.config import ProcessConfig

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging(level="DEBUG")


@pytest.fixture
def config_with_dirs(tmp_path):
    config = ProcessConfig()


    processed_dir = tmp_path / config.processed_audio
    data_dir = tmp_path / config.dataset_dir

    os.makedirs(processed_dir, exist_ok=True) 
    os.makedirs(data_dir, exist_ok=True)

    config.processed_audio = str(processed_dir)
    config.dataset_dir = str(data_dir)
    config.target_sr = 16000

    return config
