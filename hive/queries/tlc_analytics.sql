USE smart_transportation;

-- 1. Tổng quan dữ liệu
SELECT
    COUNT(*) AS total_trips,
    COUNT(DISTINCT vendor_id) AS vendor_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
    AVG(passenger_count) AS avg_passenger_count
FROM tlc_trips;


-- 2. Số chuyến và doanh thu theo ngày
SELECT
    pickup_date,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount
FROM tlc_trips
GROUP BY pickup_date
ORDER BY pickup_date;


-- 3. Phân tích theo giờ
SELECT
    pickup_hour,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_hour
ORDER BY pickup_hour;


-- 4. Phân tích theo thứ trong tuần
SELECT
    pickup_day_of_week,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_day_of_week
ORDER BY pickup_day_of_week;


-- 5. Top pickup locations theo số chuyến
SELECT
    pickup_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance
FROM tlc_trips
GROUP BY pickup_location_id
ORDER BY trip_count DESC
LIMIT 10;


-- 6. Top dropoff locations theo số chuyến
SELECT
    dropoff_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance
FROM tlc_trips
GROUP BY dropoff_location_id
ORDER BY trip_count DESC
LIMIT 10;


-- 7. Phân tích theo payment type
SELECT
    payment_type,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(tip_amount) AS avg_tip_amount
FROM tlc_trips
GROUP BY payment_type
ORDER BY trip_count DESC;


-- 8. Phân tích theo vendor
SELECT
    vendor_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY vendor_id
ORDER BY trip_count DESC;


-- 9. Các tuyến pickup -> dropoff phổ biến nhất
SELECT
    pickup_location_id,
    dropoff_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY
    pickup_location_id,
    dropoff_location_id
ORDER BY trip_count DESC
LIMIT 20;


-- 10. Phân tích doanh thu theo ngày và giờ
SELECT
    pickup_date,
    pickup_hour,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount
FROM tlc_trips
GROUP BY
    pickup_date,
    pickup_hour
ORDER BY
    pickup_date,
    pickup_hour;