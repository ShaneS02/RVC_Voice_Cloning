from .models import (
    AudioMetrics, 
    ValidationResult,
    IssueType, 
    IssueSeverity, 
    ValidationIssue
)

from ..config.validation_config import ValidationConfig


class DatasetValidator:
     
    def __init__(self, config: ValidationConfig):
        self.config = config

    

    def validate(self, file_path: str, metrics: AudioMetrics) -> ValidationResult:
        issues = []

        self._validate_duration(metrics, issues)
        self._validate_silence(metrics, issues)

        self._validate_clipping(metrics, issues)
        self._validate_rms(metrics, issues)
        self._validate_peak(metrics, issues)

        valid = not any(issue.severity == IssueSeverity.ERROR for issue in issues)       

        return ValidationResult(
            file_path=file_path,
            valid=valid,
            metrics=metrics,
            issues=issues
        )
        

    #Validation functions for each metric 



    def _validate_duration(self, metrics: AudioMetrics, issues: list[ValidationIssue]):
        if metrics.duration_ms < self.config.min_duration_ms:
            issues.append(ValidationIssue(
                type=IssueType.DURATION,
                severity=IssueSeverity.ERROR,
                message=f"Audio duration {metrics.duration_ms:.2f} ms is below the minimum threshold of {self.config.min_duration_ms} ms.",
            ))
        
        if metrics.duration_ms > self.config.max_duration_ms:
            issues.append(ValidationIssue(
                type=IssueType.DURATION,
                severity=IssueSeverity.ERROR,
                message=f"Audio duration {metrics.duration_ms:.2f} ms exceeds the recommended maximum of {self.config.max_duration_ms} ms.",
            ))
    
    def _validate_silence(self, metrics: AudioMetrics, issues: list[ValidationIssue]):
        if metrics.silence_ratio > self.config.max_silence_ratio:
            issues.append(ValidationIssue(
                type=IssueType.SILENCE_RATIO,
                severity=IssueSeverity.ERROR,
                message=f"Audio clip contains excessive silence ({metrics.silence_ratio:.2%} of the duration), which may affect model performance.",
            ))
    
    def _validate_clipping(self, metrics: AudioMetrics, issues: list[ValidationIssue]):
        if metrics.clipping_ratio > self.config.max_clipping_ratio:
            issues.append(ValidationIssue(
                type=IssueType.CLIPPING_RATIO,
                severity=IssueSeverity.ERROR,
                message=f"Audio contains clipping ({metrics.clipping_ratio:.2%} of samples), which can degrade model quality.",
            ))

    def _validate_rms(self, metrics: AudioMetrics, issues: list[ValidationIssue]):
        if metrics.rms < self.config.min_rms:
            issues.append(ValidationIssue(
                type=IssueType.RMS,
                severity=IssueSeverity.WARNING,
                message=f"Audio has low RMS ({metrics.rms:.4f}), which may indicate it's too quiet and could lead to poor model performance.",
            ))
        
        if metrics.rms > self.config.max_rms:
            issues.append(ValidationIssue(
                type=IssueType.RMS,
                severity=IssueSeverity.WARNING,
                message=f"Audio has high RMS ({metrics.rms:.4f}), which may indicate it's too loud and could lead to distortion in the model.",
            ))
    

    def _validate_peak(self, metrics: AudioMetrics, issues: list[ValidationIssue]):
        if metrics.peak_db < self.config.min_peak_db:
            issues.append(ValidationIssue(
                type=IssueType.PEAK_DB,
                severity=IssueSeverity.WARNING,
                message=f"Audio has low peak level ({metrics.peak_db:.2f} dB), which may indicate it's too quiet and could lead to poor model performance.",
            ))

        if metrics.peak_db > self.config.max_peak_db:
            issues.append(ValidationIssue(
                type=IssueType.PEAK_DB,
                severity=IssueSeverity.WARNING,
                message=f"Audio has high peak level ({metrics.peak_db:.2f} dB), which may indicate it's too loud and could lead to distortion in the model.",
            ))
