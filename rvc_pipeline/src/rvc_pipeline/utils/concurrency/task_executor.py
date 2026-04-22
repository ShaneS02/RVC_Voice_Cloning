from rvc_pipeline.execution_results import ExecutionResult
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from tqdm import tqdm
import os



def execute_parallel_tasks(
    func,
    tasks,
    config=None,
    desc="",
    max_workers=os.cpu_count(),
):
    # Create a partial function with fixed parameters
    worker = partial(func, config=config)

    results = []

    # Parallel processing with ProcessPoolExecutor for better performance on multiple files
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # start processing tasks in parallel
        futures = {
            executor.submit(worker, task): task
            for task in tasks
        }

        # Log results and show progress with tqdm as tasks complete.
        # Note: as_complted returns futures as they finish, so we can log results in real-time.
        for future in tqdm(as_completed(futures), total=len(tasks), desc=desc):
            try:
                results.append(future.result())
            except Exception as e:
                results.append(
                    ExecutionResult.error(
                        input_path=str(futures[future]),
                        error_msg=str(e)
                    )
                )

    return results