import argparse
import json
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from confluent_kafka import Producer

from backend.app.core.config import get_settings


def create_kafka_producer() -> Producer:
    settings = get_settings()

    return Producer(
        {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
        }
    )


def create_webhdfs_session() -> requests.Session:
    return requests.Session()


def get_webhdfs_base_url() -> str:
    settings = get_settings()

    if not settings.tlc_processed_path.startswith("hdfs://"):
        raise ValueError(
            "TLC processed path must use an hdfs:// URI."
        )

    _, remainder = settings.tlc_processed_path.split(
        "hdfs://",
        1,
    )

    authority, _, path = remainder.partition("/")

    if ":" not in authority:
        raise ValueError(
            "TLC processed path must include an HDFS host and port."
        )

    host, port = authority.rsplit(":", 1)

    return f"http://{host}:9870/webhdfs/v1/{path.rstrip('/')}"


def list_hdfs_directory(
    session: requests.Session,
    path: str,
) -> list[dict[str, Any]]:
    response = session.get(
        f"http://namenode:9870/webhdfs/v1{path}",
        params={"op": "LISTSTATUS"},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    return data["FileStatuses"]["FileStatus"]


def find_parquet_files(
    session: requests.Session,
    root_path: str,
) -> list[str]:
    parquet_files: list[str] = []

    def walk(path: str) -> None:
        entries = list_hdfs_directory(session, path)

        for entry in entries:
            child_path = f"{path.rstrip('/')}/{entry['pathSuffix']}"

            if entry["type"] == "DIRECTORY":
                walk(child_path)

            elif (
                entry["type"] == "FILE"
                and entry["pathSuffix"].endswith(".parquet")
            ):
                parquet_files.append(child_path)

    walk(root_path)

    return parquet_files


def read_hdfs_file(
    session: requests.Session,
    path: str,
) -> bytes:
    response = session.get(
        f"http://namenode:9870/webhdfs/v1{path}",
        params={"op": "OPEN"},
        timeout=120,
    )
    response.raise_for_status()

    return response.content


def delivery_report(err: Any, message: Any) -> None:
    if err is not None:
        print(f"Delivery failed: {err}")
        return

    print(
        f"Delivered to {message.topic()} "
        f"[partition={message.partition()}] "
        f"offset={message.offset()}"
    )


def publish_tlc_records(limit: int | None = None) -> int:
    settings = get_settings()

    session = create_webhdfs_session()
    producer = create_kafka_producer()

    root_path = (
        settings.tlc_processed_path
        .split("://", 1)[1]
        .split("/", 1)[1]
    )

    root_path = f"/{root_path.rstrip('/')}"

    parquet_files = find_parquet_files(
        session,
        root_path,
    )

    rows_published = 0

    for parquet_path in parquet_files:
        parquet_data = read_hdfs_file(
            session,
            parquet_path,
        )

        table = pq.read_table(
            pa.BufferReader(parquet_data)
        )

        for record in table.to_pylist():
            payload = json.dumps(
                record,
                default=str,
                ensure_ascii=False,
            ).encode("utf-8")

            producer.produce(
                topic=settings.kafka_tlc_topic,
                value=payload,
                callback=delivery_report,
            )

            producer.poll(0)

            rows_published += 1

            if (
                limit is not None
                and rows_published >= limit
            ):
                producer.flush()
                return rows_published

    producer.flush()

    return rows_published


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Publish processed TLC records "
            "from HDFS to Kafka."
        )
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of records to publish.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.limit is not None and args.limit <= 0:
        raise ValueError(
            "--limit must be greater than 0."
        )

    count = publish_tlc_records(
        limit=args.limit
    )

    print(
        f"Published {count} TLC records to Kafka."
    )


if __name__ == "__main__":
    main()