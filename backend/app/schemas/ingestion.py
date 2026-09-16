from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class IngestionRequest(BaseModel):
    event_type: str = Field(min_length=1)
    pipeline_name: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class IngestionResponse(BaseModel):
    event_id: str
    event_type: str
    pipeline_name: str
    topic: str
    created_at: datetime
    status: str