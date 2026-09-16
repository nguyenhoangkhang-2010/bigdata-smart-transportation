from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class PipelineEvent:
    event_type: str
    pipeline_name: str
    payload: dict[str, Any]
    event_id: str | None = None
    created_at: datetime | None = None