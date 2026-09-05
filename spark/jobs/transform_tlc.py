from pyspark.sql import SparkSession
from pyspark.sql import functions as F


INPUT = (
    "hdfs://namenode:9000/"
    "data/smart_transportation/raw/tlc/"
    "yellow_tripdata_2026-01.parquet"
)

OUTPUT = (
    "hdfs://namenode:9000/"
    "data/smart_transportation/processed/tlc/"
)


def main() -> None:
    spark = (
        SparkSession.builder
        .appName("TLC-Transform")
        .getOrCreate()
    )

    try:
        # 1. Read raw data
        df = spark.read.parquet(INPUT)

        raw_count = df.count()

        # 2. Filter clearly invalid records
        df = df.filter(
            F.col("tpep_pickup_datetime").isNotNull()
            & F.col("tpep_dropoff_datetime").isNotNull()
            & (F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime"))
            & F.col("trip_distance").isNotNull()
            & (F.col("trip_distance") > 0)
            & F.col("passenger_count").isNotNull()
            & (F.col("passenger_count") >= 0)
            & F.col("total_amount").isNotNull()
            & (F.col("total_amount") >= 0)
        )

        # 3. Normalize column names
        df = df.select(
            F.col("VendorID").alias("vendor_id"),
            F.col("tpep_pickup_datetime").alias("pickup_datetime"),
            F.col("tpep_dropoff_datetime").alias("dropoff_datetime"),
            F.col("passenger_count"),
            F.col("trip_distance"),
            F.col("RatecodeID").alias("rate_code_id"),
            F.col("store_and_fwd_flag"),
            F.col("PULocationID").alias("pickup_location_id"),
            F.col("DOLocationID").alias("dropoff_location_id"),
            F.col("payment_type"),
            F.col("fare_amount"),
            F.col("extra"),
            F.col("mta_tax"),
            F.col("tip_amount"),
            F.col("tolls_amount"),
            F.col("improvement_surcharge"),
            F.col("total_amount"),
            F.col("congestion_surcharge"),
            F.col("Airport_fee").alias("airport_fee"),
            F.col("cbd_congestion_fee"),
        )

        # 4. Derive analytical fields
        df = (
            df
            .withColumn(
                "pickup_date",
                F.to_date("pickup_datetime")
            )
            .withColumn(
                "pickup_hour",
                F.hour("pickup_datetime")
            )
            .withColumn(
                "pickup_day_of_week",
                F.dayofweek("pickup_datetime")
            )
            .withColumn(
                "trip_duration_minutes",
                (
                    F.unix_timestamp("dropoff_datetime")
                    - F.unix_timestamp("pickup_datetime")
                ) / 60.0
            )
        )

        # 5. Cast warehouse-ready numeric types
        df = (
            df
            .withColumn("passenger_count", F.col("passenger_count").cast("int"))
            .withColumn("trip_distance", F.col("trip_distance").cast("double"))
            .withColumn(
                "trip_duration_minutes",
                F.col("trip_duration_minutes").cast("double")
            )
        )

        processed_count = df.count()

        # 6. Write processed data
        (
            df.write
            .mode("overwrite")
            .partitionBy("pickup_date")
            .parquet(OUTPUT)
        )

        # 7. Validation output
        print("=" * 60)
        print("TLC TRANSFORMATION")
        print("=" * 60)

        print(f"Raw rows: {raw_count}")
        print(f"Processed rows: {processed_count}")
        print(f"Removed rows: {raw_count - processed_count}")
        print(f"Output: {OUTPUT}")

        print("\nProcessed schema:")
        df.printSchema()

        print("\nSample:")
        df.select(
            "vendor_id",
            "pickup_datetime",
            "dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "pickup_date",
            "pickup_hour",
            "pickup_day_of_week",
            "trip_duration_minutes",
            "total_amount",
        ).show(5, truncate=False)

        print("=" * 60)
        print("TLC TRANSFORMATION OK")
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()