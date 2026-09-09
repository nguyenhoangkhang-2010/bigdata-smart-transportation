from collections.abc import Callable

from worker.jobs.models import Job


class JobExecutor:
    def execute(
        self,
        job: Job,
        operation: Callable[[], None],
    ) -> Job:
        job.mark_running()

        try:
            operation()
        except Exception as exc:
            job.mark_failed(str(exc))
        else:
            job.mark_success()

        return job