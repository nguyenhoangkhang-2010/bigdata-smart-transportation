from pyspark.sql import SparkSession
from pyspark.sql import functions as F

INPUT = (
    "hdfs://namenode:9000/"
    "data/smart_transportation/raw/tlc/"
    "yellow_tripdata_2026-01.parquet"
)


def main():
    spark = (
        SparkSession.builder
        .appName("TLC-Raw-Profile")
        .getOrCreate()
    )

    try:
        df = spark.read.parquet(INPUT)

        print("=" * 60)
        print("TLC DATA PROFILE")
        print("=" * 60)

        # 1. Tổng quan
        print(f"Rows: {df.count()}")
        print(f"Columns: {len(df.columns)}")
        print(f"Column names: {df.columns}")

        # 2. Khoảng thời gian
        df.select(
            F.min("tpep_pickup_datetime").alias("min_pickup"),
            F.max("tpep_pickup_datetime").alias("max_pickup"),
            F.min("tpep_dropoff_datetime").alias("min_dropoff"),
            F.max("tpep_dropoff_datetime").alias("max_dropoff"),
        ).show(truncate=False)

        # 3. Null tổng
        nulls = df.select(
            sum(
                F.sum(F.col(c).isNull().cast("int"))
                for c in df.columns
            ).alias("total_nulls")
        ).first()["total_nulls"]

        print(f"Total null values: {nulls}")

        # 4. Giá trị bất thường
        invalid = df.select(
            F.sum((F.col("trip_distance") <= 0).cast("int")).alias(
                "invalid_distance"
            ),
            F.sum((F.col("passenger_count") < 0).cast("int")).alias(
                "invalid_passenger"
            ),
            F.sum(
                (
                    F.col("tpep_dropoff_datetime")
                    <= F.col("tpep_pickup_datetime")
                ).cast("int")
            ).alias("invalid_time"),
            F.sum((F.col("total_amount") < 0).cast("int")).alias(
                "invalid_total"
            ),
        ).first()

        print(f"Invalid trip_distance <= 0: {invalid['invalid_distance']}")
        print(f"Invalid passenger_count < 0: {invalid['invalid_passenger']}")
        print(f"Invalid dropoff <= pickup: {invalid['invalid_time']}")
        print(f"Invalid total_amount < 0: {invalid['invalid_total']}")

        # 5. Thống kê numeric
        df.select(
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "tip_amount",
            "total_amount",
        ).summary("min", "mean", "max").show()

        print("=" * 60)
        print("TLC PROFILE OK")
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()