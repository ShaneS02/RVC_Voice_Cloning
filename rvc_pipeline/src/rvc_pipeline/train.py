#trigger RVC training
import subprocess

from .config.process_config import ProcessConfig

def train(config : ProcessConfig):
    subprocess.run(
        [
            "python",
            "infer/modules/train/train.py",
            "-e", config.experiment_name,
            "-sr", "40k",
            "-f0", "1",
            "-bs", "8",
            "-g", "0"
        ],
        cwd=config.rvc_dir  # Set the working directory to the RVC repository
    )