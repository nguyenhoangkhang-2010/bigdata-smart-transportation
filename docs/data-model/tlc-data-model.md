# TLC Data Model

## 1. Purpose

This document defines the logical data model and data grain for the
processed NYC TLC Yellow Taxi Trip dataset used by the
BigData Smart Transportation platform.

The model is derived from the actual processed TLC dataset schema.

This document defines the data contract only.
It does not create or modify physical Hive tables.

---

## 2. Data Source

### Dataset

NYC TLC Yellow Taxi Trip Records

### Dataset Period

January 2026

### Source Format

Parquet

### Processing Flow

```text
Raw TLC Dataset
      |
      v
HDFS Raw
      |
      v
Spark Transformation
      |
      v
HDFS Processed
      |
      v
Hive External Table: tlc_trips
```

---

## 3. Data Grain

The primary grain of the processed dataset is:

> One row represents one processed taxi trip.

The trip record is the atomic analytical unit of the TLC warehouse.

All trip-level measures and attributes are associated with this grain.

---

## 4. Main Fact

### Logical Fact

`tlc_trips`

The existing Hive table `tlc_trips` represents the primary trip-level
fact dataset.

The table contains trip-level measures and descriptive attributes.

The current physical Hive table is an external table stored as Parquet
on HDFS and partitioned by `pickup_date`.

---

## 5. Trip Measures

The following fields represent numerical measures associated with a trip.

| Field | Type | Description |
|---|---|---|
| `passenger_count` | INT | Passenger count recorded for the trip |
| `trip_distance` | DOUBLE | Trip distance recorded by the source |
| `fare_amount` | DOUBLE | Fare amount |
| `extra` | DOUBLE | Extra charge |
| `mta_tax` | DOUBLE | MTA tax |
| `tip_amount` | DOUBLE | Tip amount |
| `tolls_amount` | DOUBLE | Toll amount |
| `improvement_surcharge` | DOUBLE | Improvement surcharge |
| `total_amount` | DOUBLE | Total trip amount |
| `congestion_surcharge` | DOUBLE | Congestion surcharge |
| `airport_fee` | DOUBLE | Airport fee |
| `cbd_congestion_fee` | DOUBLE | CBD congestion fee |
| `trip_duration_minutes` | DOUBLE | Derived trip duration in minutes |

The interpretation of each field follows the source dataset schema and
the Spark transformation pipeline.

No additional business semantics are introduced by this data model.

---

## 6. Trip Attributes

The following fields describe categorical or identifying properties
associated with a trip.

| Field | Type |
|---|---|
| `vendor_id` | INT |
| `rate_code_id` | BIGINT |
| `store_and_fwd_flag` | STRING |
| `pickup_location_id` | INT |
| `dropoff_location_id` | INT |
| `payment_type` | BIGINT |

These identifiers are retained as source attributes.

No business meaning is assigned to identifier values in this data model
unless supported by an authoritative metadata source.

For example, this document does not define specific meanings for
individual `vendor_id`, `rate_code_id`, `payment_type`,
`pickup_location_id`, or `dropoff_location_id` values.

---

## 7. Temporal Attributes

The processed dataset contains the following temporal attributes.

| Field | Type | Origin |
|---|---|---|
| `pickup_datetime` | TIMESTAMP | Source field |
| `dropoff_datetime` | TIMESTAMP | Source field |
| `pickup_date` | DATE | Derived from `pickup_datetime` |
| `pickup_hour` | INT | Derived from `pickup_datetime` |
| `pickup_day_of_week` | INT | Derived from `pickup_datetime` |
| `trip_duration_minutes` | DOUBLE | Derived from pickup/dropoff timestamps |

These fields support temporal aggregation, filtering, and partition-based
analysis.

---

## 8. Physical Partitioning

The Hive table `tlc_trips` is partitioned by:

`pickup_date`

The partitioning strategy supports queries that filter trips by pickup
date and allows Hive to perform partition pruning.

Example analytical access pattern:

```sql
SELECT
    pickup_date,
    COUNT(*) AS trip_count
FROM tlc_trips
WHERE pickup_date = '2026-01-15'
GROUP BY pickup_date;
```

The current processed dataset contains partitions for the dates present
in the transformed data.

---

## 9. Processed Dataset Schema

The current processed TLC dataset contains 24 columns.

### Source and Identifying Fields

```text
vendor_id
pickup_datetime
dropoff_datetime
passenger_count
trip_distance
rate_code_id
store_and_fwd_flag
pickup_location_id
dropoff_location_id
payment_type
fare_amount
extra
mta_tax
tip_amount
tolls_amount
improvement_surcharge
total_amount
congestion_surcharge
airport_fee
cbd_congestion_fee
```

### Derived Fields

```text
pickup_date
pickup_hour
pickup_day_of_week
trip_duration_minutes
```

### Complete Processed Schema

| # | Field | Type | Category |
|---:|---|---|---|
| 1 | `vendor_id` | INT | Attribute |
| 2 | `pickup_datetime` | TIMESTAMP | Temporal |
| 3 | `dropoff_datetime` | TIMESTAMP | Temporal |
| 4 | `passenger_count` | INT | Measure |
| 5 | `trip_distance` | DOUBLE | Measure |
| 6 | `rate_code_id` | BIGINT | Attribute |
| 7 | `store_and_fwd_flag` | STRING | Attribute |
| 8 | `pickup_location_id` | INT | Attribute |
| 9 | `dropoff_location_id` | INT | Attribute |
| 10 | `payment_type` | BIGINT | Attribute |
| 11 | `fare_amount` | DOUBLE | Measure |
| 12 | `extra` | DOUBLE | Measure |
| 13 | `mta_tax` | DOUBLE | Measure |
| 14 | `tip_amount` | DOUBLE | Measure |
| 15 | `tolls_amount` | DOUBLE | Measure |
| 16 | `improvement_surcharge` | DOUBLE | Measure |
| 17 | `total_amount` | DOUBLE | Measure |
| 18 | `congestion_surcharge` | DOUBLE | Measure |
| 19 | `airport_fee` | DOUBLE | Measure |
| 20 | `cbd_congestion_fee` | DOUBLE | Measure |
| 21 | `pickup_date` | DATE | Derived Temporal / Partition |
| 22 | `pickup_hour` | INT | Derived Temporal |
| 23 | `pickup_day_of_week` | INT | Derived Temporal |
| 24 | `trip_duration_minutes` | DOUBLE | Derived Measure |

---

## 10. Data Quality Rules

The Spark transformation currently produces the processed dataset by
removing records that do not satisfy the following conditions:

- `pickup_datetime` is not null.
- `dropoff_datetime` is not null.
- `dropoff_datetime` is later than `pickup_datetime`.
- `trip_distance` is not null.
- `trip_distance` is greater than zero.
- `passenger_count` is not null.
- `passenger_count` is greater than or equal to zero.
- `total_amount` is not null.
- `total_amount` is greater than or equal to zero.

The data-quality rules belong to the Spark transformation layer.

The Hive layer consumes the resulting processed dataset.

### Transformation Result

The current transformation produced:

| Metric | Value |
|---|---:|
| Raw rows | 3,724,889 |
| Processed rows | 2,522,852 |
| Removed rows | 1,202,037 |

The values above correspond to the currently loaded January 2026 TLC
dataset and the current Spark transformation rules.

---

## 11. Warehouse Relationship

The current logical warehouse flow is:

```text
TLC Raw Dataset
      |
      v
HDFS Raw
      |
      v
Spark Transformation
      |
      v
HDFS Processed
      |
      v
tlc_trips
      |
      +-------------------------+
      |                         |
      v                         v
Analytical Views        Summary Tables
      |                         |
      +------------+------------+
                   |
                   v
               Analytics
```

The `tlc_trips` table is the primary trip-level dataset.

Analytical views and summary tables are derived from `tlc_trips`.

---

## 12. Summary Tables

The current warehouse contains the following physical summary tables.

### 12.1 `tlc_daily_summary`

Grain:

> One row per `pickup_date`.

Current columns:

| Field | Type |
|---|---|
| `pickup_date` | DATE |
| `trip_count` | BIGINT |
| `total_revenue` | DOUBLE |
| `avg_trip_amount` | DOUBLE |
| `avg_trip_distance` | DOUBLE |
| `avg_trip_duration_minutes` | DOUBLE |
| `avg_passenger_count` | DOUBLE |

---

### 12.2 `tlc_hourly_summary`

Grain:

> One row per `pickup_hour`.

Current columns:

| Field | Type |
|---|---|
| `pickup_hour` | INT |
| `trip_count` | BIGINT |
| `total_revenue` | DOUBLE |
| `avg_trip_amount` | DOUBLE |
| `avg_trip_distance` | DOUBLE |
| `avg_trip_duration_minutes` | DOUBLE |

---

### 12.3 `tlc_daily_hourly_summary`

Grain:

> One row per existing `pickup_date` and `pickup_hour` combination in the
> processed dataset.

Current columns:

| Field | Type |
|---|---|
| `pickup_date` | DATE |
| `pickup_hour` | INT |
| `trip_count` | BIGINT |
| `total_revenue` | DOUBLE |
| `avg_trip_amount` | DOUBLE |
| `avg_trip_distance` | DOUBLE |
| `avg_trip_duration_minutes` | DOUBLE |

These summary tables are derived from the trip-level `tlc_trips`
dataset.

They are physical warehouse tables used to reduce repeated aggregation
work for common analytical access patterns.

---

## 13. Analytical Views

The current warehouse also contains analytical views derived from
`tlc_trips`.

Current views:

```text
vw_tlc_daily_summary
vw_tlc_hourly_summary
vw_tlc_weekday_summary
vw_tlc_pickup_location_summary
vw_tlc_dropoff_location_summary
vw_tlc_payment_summary
vw_tlc_vendor_summary
vw_tlc_route_summary
vw_tlc_daily_hourly_summary
```

These views provide reusable logical analytical access without changing
the underlying trip-level grain.

---

## 14. Data Flow and Analytical Grain

The relationship between the trip-level dataset and aggregated datasets
is:

```text
                         tlc_trips
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
        Daily Grain     Hourly Grain   Daily-Hourly Grain
             |               |               |
             v               v               v
    tlc_daily_summary  tlc_hourly_summary  tlc_daily_hourly_summary
```

The trip-level dataset remains the source of truth for the current
warehouse aggregations.

---

## 15. Data Model Principles

### 15.1 Dataset-Driven

The model is derived from the actual processed TLC schema.

No fields are introduced solely because they are common in transportation
data models.

---

### 15.2 Grain-First

Every analytical table must explicitly define its grain.

The primary fact grain is:

> One processed record represents one taxi trip.

Aggregated tables define their own grain explicitly.

---

### 15.3 No Invented Semantics

Source identifiers must not receive unsupported business meanings.

Examples include:

- `vendor_id`
- `rate_code_id`
- `payment_type`
- `pickup_location_id`
- `dropoff_location_id`

Their value-level meanings should only be introduced after the relevant
authoritative metadata has been incorporated into the platform.

---

### 15.4 Logical and Physical Separation

This document defines the logical data contract.

Physical implementation details such as:

- Hive tables
- external table locations
- partitions
- Parquet storage
- table statistics
- column statistics
- summary tables

are implemented separately in the corresponding Hive and Spark
components.

---

### 15.5 Reusable Analytical Foundation

The trip-level fact provides the foundation for:

- temporal analysis
- location-based analysis
- payment analysis
- vendor analysis
- route analysis
- revenue analysis
- trip-distance analysis
- trip-duration analysis

These analytical capabilities must be derived from available dataset
fields rather than hard-coded business assumptions.

---

### 15.6 Extensibility

Future dimensions or enrichment datasets may be introduced when their
source metadata and relationships are established.

Potential future enrichment may include authoritative metadata for
locations, vendors, rate codes, payment types, or other transportation
entities.

Such enrichment is outside the scope of the current data model contract.

---

## 16. Current Data Model Summary

The current logical model can be represented as:

```text
                         TLC TRIP
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
      Temporal          Attributes        Measures
          |                 |                 |
          |                 |                 +-- passenger_count
          |                 |                 +-- trip_distance
          |                 |                 +-- fare_amount
          |                 |                 +-- extra
          |                 |                 +-- mta_tax
          |                 |                 +-- tip_amount
          |                 |                 +-- tolls_amount
          |                 |                 +-- improvement_surcharge
          |                 |                 +-- total_amount
          |                 |                 +-- congestion_surcharge
          |                 |                 +-- airport_fee
          |                 |                 +-- cbd_congestion_fee
          |                 |                 +-- trip_duration_minutes
          |                 |
          |                 +-- vendor_id
          |                 +-- rate_code_id
          |                 +-- store_and_fwd_flag
          |                 +-- pickup_location_id
          |                 +-- dropoff_location_id
          |                 +-- payment_type
          |
          +-- pickup_datetime
          +-- dropoff_datetime
          +-- pickup_date
          +-- pickup_hour
          +-- pickup_day_of_week
```

The trip record is the central analytical entity of the current
BigData Smart Transportation warehouse.

---

## 17. Current Warehouse Validation

The current warehouse maintains consistency between the trip-level fact
and its summary tables.

Current processed trip count:

```text
2,522,852
```

Current summary table row counts:

| Table | Row Count |
|---|---:|
| `tlc_trips` | 2,522,852 |
| `tlc_daily_summary` | 33 |
| `tlc_hourly_summary` | 24 |
| `tlc_daily_hourly_summary` | 746 |

The total trip count represented by each summary table is consistent
with the trip-level dataset:

```text
SUM(tlc_daily_summary.trip_count)
    = 2,522,852

SUM(tlc_hourly_summary.trip_count)
    = 2,522,852

SUM(tlc_daily_hourly_summary.trip_count)
    = 2,522,852
```

---

## 18. Scope of This Commit

This data model contract establishes:

1. The primary TLC trip grain.
2. The logical fact dataset.
3. Trip measures.
4. Trip attributes.
5. Temporal attributes.
6. Derived fields.
7. Data-quality assumptions from the Spark transformation.
8. Hive partitioning context.
9. Relationships between the fact dataset and summary tables.
10. Design principles for future extensions.

This commit does not implement:

- Kafka producers.
- Kafka consumers.
- Kafka event contracts.
- New Hive tables.
- New Spark transformations.
- FastAPI endpoints.
- React components.
- Redis caching.
- PostgreSQL models.
- MongoDB models.

Those capabilities belong to separate features and commits.

---

## 19. Source of Truth

The data model must remain synchronized with the actual processed TLC
schema and transformation pipeline.

When the source dataset or Spark transformation changes, this document
must be reviewed before dependent warehouse or application components
are modified.