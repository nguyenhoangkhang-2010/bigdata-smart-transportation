from collections.abc import Callable

from worker.jobs.executor import JobExecutor
from worker.jobs.models import Job


class PipelineExecutor:
    def __init__(self, job_executor: JobExecutor | None = None) -> None:
        self.job_executor = job_executor or JobExecutor()

    def execute(
        self,
        pipeline_name: str,
        operation: Callable[[], None],
    ) -> Job:
        job = Job(pipeline_name=pipeline_name)

        return self.job_executor.execute(
            job=job,
            operation=operation,
        )