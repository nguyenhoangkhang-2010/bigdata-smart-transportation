from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.job import JobRecord
from backend.app.models.pipeline import Pipeline
from backend.app.models.pipeline_execution import PipelineExecution


class JobMetadataService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_pipeline(
        self,
        name: str,
        description: str | None = None,
    ) -> Pipeline:
        pipeline = self.db.scalar(
            select(Pipeline).where(Pipeline.name == name)
        )

        if pipeline is not None:
            return pipeline

        pipeline = Pipeline(
            name=name,
            description=description,
        )

        self.db.add(pipeline)
        self.db.flush()

        return pipeline

    def create_job(
        self,
        job_id: str,
        pipeline: Pipeline,
        status: str,
        created_at: datetime,
    ) -> JobRecord:
        job = JobRecord(
            job_id=job_id,
            pipeline_id=pipeline.id,
            status=status,
            created_at=created_at,
        )

        self.db.add(job)
        self.db.flush()

        return job

    def create_execution(
        self,
        *,
        job: JobRecord,
        event_id: str | None,
        event_type: str,
        staging_path: str,
        input_path: str,
        output_path: str,
        spark_job: str,
        hive_statements: list[str],
        created_at: datetime,
    ) -> PipelineExecution:
        execution = PipelineExecution(
            job_id=job.id,
            event_id=event_id,
            event_type=event_type,
            staging_path=staging_path,
            input_path=input_path,
            output_path=output_path,
            spark_job=spark_job,
            hive_statements=hive_statements,
            created_at=created_at,
        )

        self.db.add(execution)
        self.db.flush()

        return execution

    def get_job(self, job_id: str) -> JobRecord | None:
        return self.db.scalar(
            select(JobRecord).where(
                JobRecord.job_id == job_id
            )
        )

    def get_executions_by_job_ids(
        self,
        job_ids: list[int],
    ) -> list[PipelineExecution]:
        if not job_ids:
            return []

        return self.db.scalars(
            select(PipelineExecution)
            .where(
                PipelineExecution.job_id.in_(job_ids)
            )
            .order_by(PipelineExecution.created_at)
        ).all()

    def update_job(
        self,
        job: JobRecord,
        *,
        status: str,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
        error_message: str | None = None,
    ) -> JobRecord:
        job.status = status

        if started_at is not None:
            job.started_at = started_at

        if finished_at is not None:
            job.finished_at = finished_at

        if error_message is not None:
            job.error_message = error_message

        self.db.flush()

        return job

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
