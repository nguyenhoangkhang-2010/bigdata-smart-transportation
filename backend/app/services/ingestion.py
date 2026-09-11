import json
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

from confluent_kafka import Producer

from backend.app.core.config import get_settings
from backend.app.core.kafka import get_kafka_producer


class IngestionService:
    def __init__(
        self,
        producer: Producer | None = None,
    ) -> None:
        self.settings = get_settings()
        self.producer = producer or get_kafka_producer()

    def publish_pipeline_event(
        self,
        *,
        event_type: str,
        pipeline_name: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        event_id = str(uuid4())
        created_at = datetime.now(timezone.utc)

        event = {
            "event_id": event_id,
            "event_type": event_type,
            "pipeline_name": pipeline_name,
            "payload": payload,
            "created_at": created_at.isoformat(),
        }

        value = json.dumps(
            event,
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")

        topic = self.settings.kafka_pipeline_topic

        self.producer.produce(
            topic=topic,
            value=value,
        )

        self.producer.flush(timeout=10)

        return {
            "event_id": event_id,
            "event_type": event_type,
            "pipeline_name": pipeline_name,
            "topic": topic,
            "created_at": created_at,
            "status": "published",
        }