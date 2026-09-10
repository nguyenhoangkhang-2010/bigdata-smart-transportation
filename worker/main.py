import argparse

from worker.kafka_consumer import PipelineEventConsumer

from backend.app.core.database import init_db


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the pipeline event worker."
    )

    parser.add_argument(
        "--max-messages",
        type=int,
        default=None,
        help="Maximum number of pipeline events to consume.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    init_db()

    if args.max_messages is not None and args.max_messages <= 0:
        raise ValueError(
            "--max-messages must be greater than 0."
        )

    consumer = PipelineEventConsumer()

    consumed = consumer.consume(
        max_messages=args.max_messages
    )

    print(
        f"Worker finished: consumed={consumed}"
    )


if __name__ == "__main__":
    main()