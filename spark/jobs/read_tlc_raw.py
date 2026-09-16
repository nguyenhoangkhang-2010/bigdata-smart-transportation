from pyspark.sql import SparkSession


HDFS_INPUT_PATH = (
    "hdfs://namenode:9000/"
    "data/smart_transportation/raw/tlc/"
    "yellow_tripdata_2026-01.parquet"
)


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("TLC-Raw-Reader")
        .getOrCreate()
    )

    try:
        df = spark.read.parquet(HDFS_INPUT_PATH)

        print("=" * 80)
        print("TLC RAW DATA - SPARK READ TEST")
        print("=" * 80)

        print(f"Input: {HDFS_INPUT_PATH}")
        print(f"Rows: {df.count()}")
        print(f"Columns: {len(df.columns)}")

        print("\nSchema:")
        df.printSchema()

        print("\nColumns:")
        print(df.columns)

        print("\nSample:")
        df.show(5, truncate=False)

        print("=" * 80)
        print("SPARK HDFS READ OK")
        print("=" * 80)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()