from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class QueryHistory(Base):
    __tablename__ = "query_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    engine: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    cache_status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )

    execution_time_ms: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
