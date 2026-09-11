from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        unique=True,
        nullable=False,
    )

    event_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    staging_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    input_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    output_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    spark_job: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hive_statements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )