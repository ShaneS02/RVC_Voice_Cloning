from dataclasses import dataclass
from typing import Optional

@dataclass
class ExecutionResult:
    status: str  # "success", "skipped", "error"
    input: str
    output: Optional[str] = None
    message: Optional[str] = None

    def success(input_path, output_path):
        return ExecutionResult("success", input_path, output_path)

    def skipped(input_path, reason=None):
        return ExecutionResult("skipped", input_path, message=reason)

    def error(input_path, error_msg):
        return ExecutionResult("error", input_path, message=error_msg)
    

def summarize_results(results: list[ExecutionResult]):
    total = len(results)
    success = sum(1 for r in results if r.status == "success")
    skipped = sum(1 for r in results if r.status == "skipped")
    failed = sum(1 for r in results if r.status == "error")

    return {
        "total_files": total,
        "success": success,
        "skipped": skipped,
        "failed": failed
    }