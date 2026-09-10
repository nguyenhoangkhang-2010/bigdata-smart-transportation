from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.job import JobRecord
from backend.app.models.pipeline import Pipeline


class LineageService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _build_response(
        self,
        pipeline: Pipeline,
        jobs: list[JobRecord],
    ) -> dict:
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

        return [
            self._build_response(
                pipeline,
                jobs_by_pipeline.get(pipeline.id, []),
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

        return self._build_response(
            pipeline,
            jobs,
        )