from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    execution_time_ms: float


class ExplainResponse(BaseModel):
    plan: list[dict[str, Any]]
    execution_time_ms: float