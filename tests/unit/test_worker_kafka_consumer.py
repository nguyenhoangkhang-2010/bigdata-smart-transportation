import json

import pytest

from worker.pipelines.event_parser import PipelineEventParser


def test_parse_valid_pipeline_event() -> None:
    event = {
        "event_type": "pipeline.started",
        "pipeline_name": "example_pipeline",
        "payload": {
            "source": "example",
        },
        "event_id": "event-001",
        "created_at": "2026-09-09T10:00:00+00:00",
    }

    parser = PipelineEventParser()

    result = parser.parse(
        json.dumps(event).encode("utf-8")
    )

    assert result.event_type == "pipeline.started"
    assert result.pipeline_name == "example_pipeline"
    assert result.payload["source"] == "example"
    assert result.event_id == "event-001"


def test_parse_invalid_json() -> None:
    parser = PipelineEventParser()

    with pytest.raises(ValueError, match="Invalid pipeline event JSON"):
        parser.parse(b"invalid-json")


def test_parse_missing_required_field() -> None:
    event = {
        "event_type": "pipeline.started",
    }

    parser = PipelineEventParser()

    with pytest.raises(
        ValueError,
        match="pipeline_name",
    ):
        parser.parse(
            json.dumps(event).encode("utf-8")
        )