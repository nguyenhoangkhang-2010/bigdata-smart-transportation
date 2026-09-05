CREATE DATABASE IF NOT EXISTS smart_transportation;

USE smart_transportation;

CREATE EXTERNAL TABLE IF NOT EXISTS tlc_trips (
    vendor_id INT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INT,
    trip_distance DOUBLE,
    rate_code_id BIGINT,
    store_and_fwd_flag STRING,
    pickup_location_id INT,
    dropoff_location_id INT,
    payment_type BIGINT,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    congestion_surcharge DOUBLE,
    airport_fee DOUBLE,
    cbd_congestion_fee DOUBLE,
    pickup_hour INT,
    pickup_day_of_week INT,
    trip_duration_minutes DOUBLE
)
PARTITIONED BY (
    pickup_date DATE
)
STORED AS PARQUET
LOCATION 'hdfs://namenode:9000/data/smart_transportation/processed/tlc/';