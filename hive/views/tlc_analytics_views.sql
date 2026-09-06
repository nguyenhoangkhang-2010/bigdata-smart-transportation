USE smart_transportation;


-- ============================================================
-- 1. Daily trip summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_daily_summary AS
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


-- ============================================================
-- 2. Hourly trip summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_hourly_summary AS
SELECT
    pickup_hour,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_hour;


-- ============================================================
-- 3. Day-of-week summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_weekday_summary AS
SELECT
    pickup_day_of_week,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_day_of_week;


-- ============================================================
-- 4. Pickup location summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_pickup_location_summary AS
SELECT
    pickup_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY pickup_location_id;


-- ============================================================
-- 5. Dropoff location summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_dropoff_location_summary AS
SELECT
    dropoff_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY dropoff_location_id;


-- ============================================================
-- 6. Payment type summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_payment_summary AS
SELECT
    payment_type,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(tip_amount) AS avg_tip_amount
FROM tlc_trips
GROUP BY payment_type;


-- ============================================================
-- 7. Vendor summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_vendor_summary AS
SELECT
    vendor_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY vendor_id;


-- ============================================================
-- 8. Popular routes
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_route_summary AS
SELECT
    pickup_location_id,
    dropoff_location_id,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_trip_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes
FROM tlc_trips
GROUP BY
    pickup_location_id,
    dropoff_location_id;


-- ============================================================
-- 9. Daily-hourly summary
-- ============================================================

CREATE OR REPLACE VIEW vw_tlc_daily_hourly_summary AS
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