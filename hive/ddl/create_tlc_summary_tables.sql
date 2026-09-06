USE smart_transportation;

CREATE TABLE IF NOT EXISTS tlc_daily_summary (
    pickup_date DATE,
    trip_count BIGINT,
    total_revenue DOUBLE,
    avg_trip_amount DOUBLE,
    avg_trip_distance DOUBLE,
    avg_trip_duration_minutes DOUBLE,
    avg_passenger_count DOUBLE
)
STORED AS PARQUET;

CREATE TABLE IF NOT EXISTS tlc_hourly_summary (
    pickup_hour INT,
    trip_count BIGINT,
    total_revenue DOUBLE,
    avg_trip_amount DOUBLE,
    avg_trip_distance DOUBLE,
    avg_trip_duration_minutes DOUBLE
)
STORED AS PARQUET;

CREATE TABLE IF NOT EXISTS tlc_daily_hourly_summary (
    pickup_date DATE,
    pickup_hour INT,
    trip_count BIGINT,
    total_revenue DOUBLE,
    avg_trip_amount DOUBLE,
    avg_trip_distance DOUBLE,
    avg_trip_duration_minutes DOUBLE
)
STORED AS PARQUET;