import json
from datetime import datetime

from worker.pipelines.events import PipelineEvent


class PipelineEventParser:
    REQUIRED_FIELDS = {
        "event_type",
        "pipeline_name",
    }

    def parse(self, raw_value: bytes) -> PipelineEvent:
        try:
            data = json.loads(raw_value.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid pipeline event JSON.") from exc

        if not isinstance(data, dict):
            raise ValueError("Pipeline event must be a JSON object.")

        missing_fields = self.REQUIRED_FIELDS - data.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Missing required pipeline event fields: {missing}."
            )

        payload = data.get("payload", {})

        if not isinstance(payload, dict):
            raise ValueError(
                "Pipeline event payload must be an object."
            )

        created_at = data.get("created_at")

        parsed_created_at = None

        if created_at is not None:
            try:
                parsed_created_at = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                )
            except ValueError as exc:
                raise ValueError(
                    "Invalid pipeline event created_at."
                ) from exc

        return PipelineEvent(
            event_type=str(data["event_type"]),
            pipeline_name=str(data["pipeline_name"]),
            payload=payload,
            event_id=data.get("event_id"),
            created_at=parsed_created_at,
        )