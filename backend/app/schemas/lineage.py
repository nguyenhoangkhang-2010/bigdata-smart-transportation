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


class LineageExecution(BaseModel):
    event_id: str | None = None
    event_type: str
    staging_path: str
    input_path: str
    output_path: str
    spark_job: str
    hive_statements: list[str]
    created_at: datetime


class LineageResponse(BaseModel):
    pipeline: LineagePipeline
    jobs: list[LineageJob]
    executions: dict[str, LineageExecution]


class LineageListResponse(BaseModel):
    items: list[LineageResponse]