#trigger RVC training
import subprocess

from rvc_pipeline.config import EXPERIMENT_NAME, RVC_DIR

def train():
    subprocess.run(
        [
            "python",
            "infer/modules/train/train.py",
            "-e", EXPERIMENT_NAME,
            "-sr", "40k",
            "-f0", "1",
            "-bs", "8",
            "-g", "0"
        ],
        cwd=RVC_DIR  # Set the working directory to the RVC repository
    )