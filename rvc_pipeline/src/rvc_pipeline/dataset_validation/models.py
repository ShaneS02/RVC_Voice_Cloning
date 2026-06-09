from enum import Enum
from pydantic import BaseModel, Field
from typing import List


class IssueType(str, Enum):
    DURATION = "duration"
    RMS = "rms"
    PEAK_DB = "peak_db"
    CLIPPING_RATIO = "clipping_ratio"
    SILENCE_RATIO = "silence_ratio"
    LUFS = "lufs"

class IssueSeverity(str, Enum):
    WARNING = "warning"
    ERROR = "error"

class ValidationIssue(BaseModel):
    type: IssueType    
    severity: IssueSeverity
    message: str


class AudioMetrics(BaseModel):
    duration_ms: float
    rms: float
    peak_db: float
    clipping_ratio: float
    silence_ratio: float
    lufs: float | None = None


class ValidationResult(BaseModel):
    file_path: str
    valid: bool

    metrics: AudioMetrics

    issues: List[ValidationIssue] = Field(default_factory=list)