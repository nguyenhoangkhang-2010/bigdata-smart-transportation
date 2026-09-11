from typing import Any, Literal

from pydantic import BaseModel, Field


Aggregation = Literal[
    "count",
    "count_distinct",
    "sum",
    "avg",
    "min",
    "max",
]


class AnalyticsMeasure(BaseModel):
    column: str
    aggregation: Aggregation


class AnalyticsFilter(BaseModel):
    column: str
    operator: Literal[
        "=",
        "!=",
        ">",
        ">=",
        "<",
        "<=",
    ]
    value: Any


class AnalyticsOrderBy(BaseModel):
    column: str
    direction: Literal["asc", "desc"] = "asc"


class AnalyticsRequest(BaseModel):
    table: str
    dimensions: list[str] = Field(default_factory=list)
    measures: list[AnalyticsMeasure] = Field(default_factory=list)
    filters: list[AnalyticsFilter] = Field(default_factory=list)
    order_by: list[AnalyticsOrderBy] = Field(default_factory=list)
    limit: int = Field(default=1000, ge=1, le=10000)


class AnalyticsResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    execution_time_ms: float
    cache_status: Literal["HIT", "MISS"]
    engine: str