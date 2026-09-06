USE smart_transportation;

INSERT OVERWRITE TABLE tlc_daily_summary
SELECT
    pickup_date,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
    AVG(passenger_count) AS avg_passenger_count
FROM tlc_trips
GROUP BY pickup_date;

INSERT OVERWRITE TABLE tlc_hourly_summary
SELECT
    pickup_hour,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_hour;

INSERT OVERWRITE TABLE tlc_daily_hourly_summary
SELECT
    pickup_date,
    pickup_hour,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY
    pickup_date,
    pickup_hour;