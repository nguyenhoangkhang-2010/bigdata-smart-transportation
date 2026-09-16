from datetime import datetime

from pydantic import BaseModel


class PipelineResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class JobResponse(BaseModel):
    job_id: str
    pipeline_id: int
    pipeline_name: str
    status: str
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None


class PipelineDetailResponse(BaseModel):
    pipeline: PipelineResponse
    jobs: list[JobResponse]