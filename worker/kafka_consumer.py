from confluent_kafka import Consumer, KafkaException

from backend.app.core.config import get_settings
from backend.app.core.kafka import get_kafka_consumer
from worker.pipelines.event_parser import PipelineEventParser
from worker.pipelines.executor import PipelineExecutor


class PipelineEventConsumer:
    def __init__(
        self,
        consumer: Consumer | None = None,
        parser: PipelineEventParser | None = None,
        pipeline_executor: PipelineExecutor | None = None,
    ) -> None:
        settings = get_settings()

        self.consumer = consumer or get_kafka_consumer(
            group_id="pipeline-worker",
            auto_offset_reset="earliest",
        )

        self.consumer.subscribe([settings.kafka_pipeline_topic])

        self.parser = parser or PipelineEventParser()
        self.pipeline_executor = (
            pipeline_executor or PipelineExecutor()
        )

    def process_message(self, message) -> None:
        event = self.parser.parse(message.value())

        self.pipeline_executor.execute(
            pipeline_name=event.pipeline_name,
            operation=lambda: None,
        )

    def consume(self, max_messages: int | None = None) -> int:
        consumed = 0

        try:
            while (
                max_messages is None
                or consumed < max_messages
            ):
                message = self.consumer.poll(1.0)

                if message is None:
                    continue

                if message.error():
                    raise KafkaException(message.error())

                self.process_message(message)
                self.consumer.commit(message)

                consumed += 1

        finally:
            self.consumer.close()

        return consumed