from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.job import JobRecord
from backend.app.models.pipeline import Pipeline
from backend.app.schemas.pipeline import JobResponse


router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
)


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: str,
    db: Session = Depends(get_db),
) -> JobResponse:
    job = (
        db.query(JobRecord)
        .filter(JobRecord.job_id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job not found: {job_id}",
        )

    pipeline = (
        db.query(Pipeline)
        .filter(Pipeline.id == job.pipeline_id)
        .first()
    )

    if pipeline is None:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline metadata not found for job: {job_id}",
        )

    return JobResponse(
        job_id=job.job_id,
        pipeline_id=job.pipeline_id,
        pipeline_name=pipeline.name,
        status=job.status,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error_message=job.error_message,
    )