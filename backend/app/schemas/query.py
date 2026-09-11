from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)


class QueryResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    execution_time_ms: float
    engine: str
    cache_status: str
    rows_scanned: int | None


class ExplainResponse(BaseModel):
    plan: list[dict[str, Any]]
    execution_time_ms: float
    engine: str


class QueryHistoryResponse(BaseModel):
    id: int
    query: str
    engine: str
    cache_status: str
    execution_time_ms: float
    row_count: int
    created_at: datetime


class SavedQueryCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    query: str = Field(min_length=1)
    description: str | None = None


class SavedQueryUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    query: str | None = Field(default=None, min_length=1)
    description: str | None = None


class SavedQueryResponse(BaseModel):
    id: int
    name: str
    query: str
    description: str | None
    created_at: datetime
    updated_at: datetime
