from worker.pipelines.executor import PipelineExecutor


def main() -> None:
    executor = PipelineExecutor()

    job = executor.execute(
        pipeline_name="example_pipeline",
        operation=lambda: None,
    )

    print(f"Job ID: {job.job_id}")
    print(f"Pipeline: {job.pipeline_name}")
    print(f"Status: {job.status.value}")


if __name__ == "__main__":
    main()