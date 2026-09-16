from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.job import JobRecord
from backend.app.models.pipeline import Pipeline
from backend.app.schemas.pipeline import (
    JobResponse,
    PipelineDetailResponse,
    PipelineResponse,
)


router = APIRouter(
    prefix="/api/pipelines",
    tags=["pipelines"],
)


@router.get(
    "",
    response_model=list[PipelineResponse],
)
def list_pipelines(
    db: Session = Depends(get_db),
) -> list[PipelineResponse]:
    pipelines = (
        db.query(Pipeline)
        .order_by(Pipeline.id)
        .all()
    )

    return [
        PipelineResponse(
            id=pipeline.id,
            name=pipeline.name,
            description=pipeline.description,
            created_at=pipeline.created_at,
            updated_at=pipeline.updated_at,
        )
        for pipeline in pipelines
    ]


@router.get(
    "/{pipeline_name}",
    response_model=PipelineDetailResponse,
)
def get_pipeline(
    pipeline_name: str,
    db: Session = Depends(get_db),
) -> PipelineDetailResponse:
    pipeline = (
        db.query(Pipeline)
        .filter(Pipeline.name == pipeline_name)
        .first()
    )

    if pipeline is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pipeline not found: {pipeline_name}",
        )

    jobs = (
        db.query(JobRecord)
        .filter(JobRecord.pipeline_id == pipeline.id)
        .order_by(JobRecord.created_at.desc())
        .all()
    )

    return PipelineDetailResponse(
        pipeline=PipelineResponse(
            id=pipeline.id,
            name=pipeline.name,
            description=pipeline.description,
            created_at=pipeline.created_at,
            updated_at=pipeline.updated_at,
        ),
        jobs=[
            JobResponse(
                job_id=job.job_id,
                pipeline_id=job.pipeline_id,
                pipeline_name=pipeline.name,
                status=job.status,
                created_at=job.created_at,
                started_at=job.started_at,
                finished_at=job.finished_at,
                error_message=job.error_message,
            )
            for job in jobs
        ],
    )