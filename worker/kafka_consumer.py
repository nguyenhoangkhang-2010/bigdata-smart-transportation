from confluent_kafka import Consumer, KafkaException

from backend.app.core.config import get_settings
from backend.app.core.kafka import get_kafka_consumer
from worker.jobs.models import Job
from worker.pipelines.event_parser import PipelineEventParser
from worker.pipelines.executor import PipelineExecutor
from worker.pipelines.staging import HDFSStagingClient
from worker.pipelines.spark import SparkPipelineRunner


class PipelineEventConsumer:
    def __init__(
        self,
        consumer: Consumer | None = None,
        parser: PipelineEventParser | None = None,
        pipeline_executor: PipelineExecutor | None = None,
        staging_client: HDFSStagingClient | None = None,
        spark_runner: SparkPipelineRunner | None = None,
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

        self.staging_client = (
            staging_client or HDFSStagingClient()
        )

        self.spark_runner = (
            spark_runner or SparkPipelineRunner()
        )

    def process_message(self, message) -> Job:
        event = self.parser.parse(message.value())

        def execute_pipeline() -> None:
            staging_path = event.payload.get("staging_path")
            content = event.payload.get("content")
            input_path = event.payload.get("input_path")
            output_path = event.payload.get("output_path")

            if not isinstance(staging_path, str) or not staging_path:
                raise ValueError(
                    "Pipeline event payload requires "
                    "a non-empty staging_path."
                )

            if not isinstance(content, str):
                raise ValueError(
                    "Pipeline event payload requires "
                    "content as a string."
                )

            if not isinstance(input_path, str) or not input_path:
                raise ValueError(
                    "Pipeline event payload requires "
                    "a non-empty input_path."
                )

            if not isinstance(output_path, str) or not output_path:
                raise ValueError(
                    "Pipeline event payload requires "
                    "a non-empty output_path."
                )

            self.staging_client.write_text(
                hdfs_path=(
                    "/data/smart_transportation/staging/"
                    f"{staging_path.lstrip('/')}"
                ),
                content=content,
            )

            self.spark_runner.run_transformation(
                input_path=input_path,
                output_path=output_path,
            )

        return self.pipeline_executor.execute(
            pipeline_name=event.pipeline_name,
            operation=execute_pipeline,
        )

    def consume(
        self,
        max_messages: int | None = None,
    ) -> int:
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