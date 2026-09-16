from collections.abc import Callable

from worker.jobs.executor import JobExecutor
from worker.jobs.models import Job


class PipelineExecutor:
    def __init__(
        self,
        job_executor: JobExecutor | None = None,
    ) -> None:
        self.job_executor = job_executor or JobExecutor()

    def create_job(self, pipeline_name: str) -> Job:
        return Job(pipeline_name=pipeline_name)

    def execute(
        self,
        job: Job,
        operation: Callable[[], None],
    ) -> Job:
        return self.job_executor.execute(
            job=job,
            operation=operation,
        )