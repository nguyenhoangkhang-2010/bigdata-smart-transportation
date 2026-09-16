from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass
class Job:
    pipeline_name: str
    job_id: str = field(default_factory=lambda: str(uuid4()))
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error_message: str | None = None

    def mark_running(self) -> None:
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)

    def mark_success(self) -> None:
        self.status = JobStatus.SUCCESS
        self.finished_at = datetime.now(timezone.utc)

    def mark_failed(self, error_message: str) -> None:
        self.status = JobStatus.FAILED
        self.finished_at = datetime.now(timezone.utc)
        self.error_message = error_message