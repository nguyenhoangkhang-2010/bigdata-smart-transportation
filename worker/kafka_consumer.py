from confluent_kafka import Consumer, KafkaException

from backend.app.core.config import get_settings
from backend.app.core.database import SessionLocal
from backend.app.core.kafka import get_kafka_consumer
from backend.app.services.job_metadata import JobMetadataService
from worker.jobs.models import Job, JobStatus
from worker.pipelines.event_parser import PipelineEventParser
from worker.pipelines.events import PipelineEvent
from worker.pipelines.executor import PipelineExecutor
from worker.pipelines.hive import HivePipelineRunner
from worker.pipelines.spark import SparkPipelineRunner
from worker.pipelines.staging import HDFSStagingClient


class PipelineEventConsumer:
    def __init__(
        self,
        consumer: Consumer | None = None,
        parser: PipelineEventParser | None = None,
        pipeline_executor: PipelineExecutor | None = None,
        staging_client: HDFSStagingClient | None = None,
        spark_runner: SparkPipelineRunner | None = None,
        hive_runner: HivePipelineRunner | None = None,
        metadata_service: JobMetadataService | None = None,
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

        self.hive_runner = (
            hive_runner or HivePipelineRunner()
        )

        self.metadata_service = metadata_service

    def process_message(self, message) -> Job:
        event = self.parser.parse(message.value())

        db = None

        if self.metadata_service is not None:
            metadata_service = self.metadata_service
        else:
            db = SessionLocal()
            metadata_service = JobMetadataService(db)

        job = self.pipeline_executor.create_job(
            pipeline_name=event.pipeline_name,
        )

        try:
            pipeline = metadata_service.get_or_create_pipeline(
                name=event.pipeline_name,
            )

            metadata_service.create_job(
                job_id=job.job_id,
                pipeline=pipeline,
                status=job.status.value,
                created_at=job.created_at,
            )

            metadata_service.commit()

            result = self.pipeline_executor.execute(
                job=job,
                operation=lambda: self._execute_pipeline(event),
            )

            job_record = metadata_service.get_job(
                result.job_id
            )

            if job_record is None:
                raise RuntimeError(
                    f"Job metadata not found: {result.job_id}"
                )

            metadata_service.update_job(
                job=job_record,
                status=result.status.value,
                started_at=result.started_at,
                finished_at=result.finished_at,
                error_message=result.error_message,
            )

            metadata_service.commit()

            return result

        except Exception:
            metadata_service.rollback()
            raise

        finally:
            if db is not None:
                db.close()

    def _execute_pipeline(
        self,
        event: PipelineEvent,
    ) -> None:
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

        self.hive_runner.execute(
            statements=[
                "MSCK REPAIR TABLE tlc_trips",
            ]
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

                job = self.process_message(message)

                if job.status != JobStatus.SUCCESS:
                    raise RuntimeError(
                        f"Pipeline job failed: {job.error_message}"
                    )

                self.consumer.commit(message)

                consumed += 1

        finally:
            self.consumer.close()

        return consumed