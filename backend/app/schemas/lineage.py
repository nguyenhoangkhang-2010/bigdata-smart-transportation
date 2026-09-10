from datetime import datetime

from pydantic import BaseModel


class LineageJob(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None


class LineagePipeline(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime


class LineageResponse(BaseModel):
    pipeline: LineagePipeline
    jobs: list[LineageJob]


class LineageListResponse(BaseModel):
    items: list[LineageResponse]