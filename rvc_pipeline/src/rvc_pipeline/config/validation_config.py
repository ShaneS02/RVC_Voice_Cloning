from pydantic import BaseModel, Field, model_validator

# Configuration for validating processed audio clips before they are added to the training dataset
class ValidationConfig(BaseModel):
    """
    Validation thresholds and parameters are given in 
    milliseconds, decibels, and ratios as appropriate for audio processing

    
    Validation rules for dataset quality control in voice cloning pipeline.
    """

    
    min_duration_ms: float = Field(default=2000, gt=0) 
    max_duration_ms: float = Field(default=15000, gt=0)

    max_clipping_ratio: float = Field(default=0.001, ge=0)
    max_silence_ratio: float = Field(default=0.20, ge=0)

    min_rms: float = Field(default=0.01, ge=0)
    max_rms: float = Field(default=0.30, ge=0)

    min_peak_db: float = Field(default=-20, ge=-100)
    max_peak_db: float = Field(default=-0.5, le=0)

    duplicate_similarity_threshold: float = Field(default=0.97)

    speaker_similarity_threshold: float = Field(default=0.75)

    @model_validator(mode="after")
    def check_duration_logic(self):
        if self.min_duration_ms >= self.max_duration_ms:
            raise ValueError("min_duration_ms must be < max_duration_ms")
        return self
    
    @model_validator(mode="after")
    def check_rms_logic(self):
        if self.min_rms >= self.max_rms:
            raise ValueError("min_rms must be < max_rms")
        return self

    @model_validator(mode="after")
    def check_peak_db_logic(self):
        if self.min_peak_db >= self.max_peak_db:
            raise ValueError("min_peak_db must be < max_peak_db")
        return self