from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.job import JobRecord
from backend.app.models.pipeline import Pipeline
from backend.app.models.pipeline_execution import PipelineExecution


class LineageService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _build_response(
        self,
        pipeline: Pipeline,
        jobs: list[JobRecord],
        executions: list[PipelineExecution],
    ) -> dict:
        executions_by_job_id = {
            execution.job_id: {
                "event_id": execution.event_id,
                "event_type": execution.event_type,
                "staging_path": execution.staging_path,
                "input_path": execution.input_path,
                "output_path": execution.output_path,
                "spark_job": execution.spark_job,
                "hive_statements": execution.hive_statements,
                "created_at": execution.created_at,
            }
            for execution in executions
        }

        return {
            "pipeline": {
                "id": pipeline.id,
                "name": pipeline.name,
                "description": pipeline.description,
                "created_at": pipeline.created_at,
                "updated_at": pipeline.updated_at,
            },
            "jobs": [
                {
                    "job_id": job.job_id,
                    "status": job.status,
                    "created_at": job.created_at,
                    "started_at": job.started_at,
                    "finished_at": job.finished_at,
                    "error_message": job.error_message,
                }
                for job in jobs
            ],
            "executions": {
                job.job_id: executions_by_job_id[job.id]
                for job in jobs
                if job.id in executions_by_job_id
            },
        }

    def get_lineage(self) -> list[dict]:
        pipelines = self.db.scalars(
            select(Pipeline).order_by(Pipeline.id)
        ).all()

        if not pipelines:
            return []

        jobs = self.db.scalars(
            select(JobRecord).order_by(JobRecord.created_at)
        ).all()

        jobs_by_pipeline: dict[int, list[JobRecord]] = {}

        for job in jobs:
            jobs_by_pipeline.setdefault(
                job.pipeline_id,
                [],
            ).append(job)

        job_ids = [job.id for job in jobs]

        executions = self.db.scalars(
            select(PipelineExecution)
            .where(
                PipelineExecution.job_id.in_(job_ids)
            )
            .order_by(PipelineExecution.created_at)
        ).all()

        executions_by_pipeline: dict[int, list[PipelineExecution]] = {}

        for execution in executions:
            job = next(
                (
                    job
                    for job in jobs
                    if job.id == execution.job_id
                ),
                None,
            )

            if job is None:
                continue

            executions_by_pipeline.setdefault(
                job.pipeline_id,
                [],
            ).append(execution)

        return [
            self._build_response(
                pipeline,
                jobs_by_pipeline.get(pipeline.id, []),
                executions_by_pipeline.get(pipeline.id, []),
            )
            for pipeline in pipelines
        ]

    def get_pipeline_lineage(
        self,
        pipeline_name: str,
    ) -> dict | None:
        pipeline = self.db.scalar(
            select(Pipeline).where(
                Pipeline.name == pipeline_name,
            )
        )

        if pipeline is None:
            return None

        jobs = self.db.scalars(
            select(JobRecord)
            .where(JobRecord.pipeline_id == pipeline.id)
            .order_by(JobRecord.created_at)
        ).all()

        job_ids = [job.id for job in jobs]

        executions = self.db.scalars(
            select(PipelineExecution)
            .where(
                PipelineExecution.job_id.in_(job_ids)
            )
            .order_by(PipelineExecution.created_at)
        ).all()

        return self._build_response(
            pipeline,
            jobs,
            executions,
        )