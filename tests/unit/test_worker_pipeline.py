from worker.jobs.models import JobStatus
from worker.pipelines.executor import PipelineExecutor


def test_pipeline_execution_succeeds() -> None:
    executed = False

    def operation() -> None:
        nonlocal executed
        executed = True

    executor = PipelineExecutor()

    job = executor.execute(
        pipeline_name="test_pipeline",
        operation=operation,
    )

    assert executed is True
    assert job.pipeline_name == "test_pipeline"
    assert job.status == JobStatus.SUCCESS
    assert job.started_at is not None
    assert job.finished_at is not None
    assert job.error_message is None


def test_pipeline_execution_fails() -> None:
    def operation() -> None:
        raise RuntimeError("pipeline failed")

    executor = PipelineExecutor()

    job = executor.execute(
        pipeline_name="test_pipeline",
        operation=operation,
    )

    assert job.status == JobStatus.FAILED
    assert job.started_at is not None
    assert job.finished_at is not None
    assert job.error_message == "pipeline failed"


def test_new_job_is_pending() -> None:
    from worker.jobs.models import Job

    job = Job(pipeline_name="test_pipeline")

    assert job.status == JobStatus.PENDING
    assert job.started_at is None
    assert job.finished_at is None
    assert job.error_message is None