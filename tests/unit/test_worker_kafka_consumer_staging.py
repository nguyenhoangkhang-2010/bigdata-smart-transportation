import json
from unittest.mock import Mock

from worker.jobs.models import JobStatus
from worker.kafka_consumer import PipelineEventConsumer


def test_process_message_stages_pipeline_payload():
    message = Mock()

    event = {
        "event_type": "pipeline.started",
        "pipeline_name": "example_pipeline",
        "payload": {
            "staging_path": "pipeline/example/input.json",
            "content": "{\"status\": \"ready\"}",
        },
        "event_id": "event-001",
        "created_at": "2026-09-09T10:00:00+00:00",
    }

    message.value.return_value = json.dumps(event).encode(
        "utf-8"
    )

    staging_client = Mock()

    consumer = PipelineEventConsumer(
        consumer=Mock(),
        staging_client=staging_client,
    )

    job = consumer.process_message(message)

    assert job.status == JobStatus.SUCCESS

    staging_client.write_text.assert_called_once_with(
        hdfs_path=(
            "/data/smart_transportation/staging/"
            "pipeline/example/input.json"
        ),
        content='{"status": "ready"}',
    )