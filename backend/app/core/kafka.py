from confluent_kafka import Consumer, Producer

from backend.app.core.config import get_settings


def get_kafka_producer() -> Producer:
    settings = get_settings()

    return Producer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
        }
    )


def get_kafka_consumer(
    group_id: str,
    auto_offset_reset: str = "earliest",
) -> Consumer:
    settings = get_settings()

    return Consumer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset,
        }
    )