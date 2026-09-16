from confluent_kafka import Producer

from backend.app.core.config import get_settings


def test_kafka_connection():
    settings = get_settings()

    producer = Producer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
        }
    )

    metadata = producer.list_topics(timeout=5)

    assert metadata is not None