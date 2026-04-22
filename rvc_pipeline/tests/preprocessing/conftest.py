import pytest
from rvc_pipeline import setup_logging
from rvc_pipeline.config import ProcessConfig

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    setup_logging(level="DEBUG")


@pytest.fixture
def config_with_dirs(tmp_path):
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"

    raw_dir.mkdir()
    processed_dir.mkdir()

    return ProcessConfig(
        raw_audio=str(raw_dir),
        processed_audio=str(processed_dir),
        target_sr=16000
    )
