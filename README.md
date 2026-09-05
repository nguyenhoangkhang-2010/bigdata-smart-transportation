# Big Data Analytics Platform — Smart Transportation

> A scalable Big Data Analytics Platform for **Smart Transportation**, built around **Apache Hive Data Warehouse** and a distributed data processing architecture using **Kafka, HDFS, Spark, Hive, FastAPI, Redis, React, PostgreSQL, MongoDB, Prometheus, and Grafana**.

---

## Overview

**Big Data Analytics Platform — Smart Transportation** is a complete Big Data platform designed to collect, process, store, analyze, and visualize large-scale transportation data.

The project focuses on building a **real Big Data data pipeline** rather than a traditional CRUD application.

The core data flow is:

```text
Data Source
    ↓
Kafka
    ↓
Worker / Pipeline Orchestration
    ↓
HDFS
    ↓
Spark ETL
    ↓
HDFS Processed Data
    ↓
Apache Hive Data Warehouse
    ↓
HiveQL Analytics
    ↓
Redis Cache
    ↓
FastAPI
    ↓
React Dashboard
```

The platform also provides:

* Data ingestion
* Distributed storage
* Batch processing
* Data Warehouse
* SQL analytics using HiveQL
* Query Workspace
* Transportation analytics
* Relationship/graph exploration
* Data lineage
* Monitoring and observability

---

# Project Goals

The main goal is to demonstrate how a modern Big Data platform can be designed and implemented around a centralized **Data Warehouse and Analytics layer using Apache Hive**.

The project demonstrates several important areas of Big Data Engineering:

### 1. Data Engineering

```text
Ingestion
   ↓
Kafka
   ↓
Worker
   ↓
HDFS
   ↓
Spark ETL
```

### 2. Data Warehouse

```text
HDFS
  ↓
Apache Hive
  ↓
Fact / Dimension / Summary
```

### 3. Big Data Analytics

```text
HiveQL
  ↓
Aggregation
  ↓
KPI
  ↓
Trend
  ↓
Distribution
  ↓
Top-N
  ↓
Comparison
```

### 4. Distributed Systems

The platform uses:

* Apache Kafka
* HDFS
* Apache Spark
* Apache Hive

to build a distributed Big Data processing pipeline.

### 5. Data Governance

The platform provides:

* Dataset metadata
* Schema information
* Data Explorer
* Data Lineage
* Pipeline history
* Query history

### 6. Observability

The system monitors:

* API latency
* Kafka throughput
* Kafka consumer lag
* Redis hit rate
* Worker success/failure
* HDFS storage
* Spark jobs
* Service health

---

# System Architecture

```text
                                      USER
                                        │
                                        ▼
                                ┌───────────────┐
                                │ React         │
                                │ Frontend      │
                                │ Dashboard     │
                                └───────┬───────┘
                                        │ REST
                                        ▼
                                ┌───────────────┐
                                │   FastAPI     │
                                │ API / Gateway │
                                └───────┬───────┘
                                        │
             ┌──────────────────────────┼─────────────────────────┐
             │                          │                         │
             ▼                          ▼                         ▼
      ┌─────────────┐          ┌─────────────┐           ┌─────────────┐
      │    Redis    │          │ PostgreSQL  │           │  MongoDB    │
      │    Cache    │          │  Metadata   │           │ Documents   │
      └──────┬──────┘          └─────────────┘           └──────┬──────┘
             │                                                   │
             └──────────────────────┬────────────────────────────┘
                                    ▼
                            ┌─────────────────┐
                            │      Kafka      │
                            │  Event / Data   │
                            │      Bus        │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ Python Worker   │
                            │ Job / Pipeline  │
                            │ Orchestration   │
                            └────────┬────────┘
                                     │
                       ┌─────────────┴─────────────┐
                       │                           │
                       ▼                           ▼
                ┌─────────────┐             ┌─────────────┐
                │    HDFS     │             │    Spark    │
                │ Distributed │             │ ETL / Batch │
                │   Storage   │             │ Processing  │
                └──────┬──────┘             └──────┬──────┘
                       │                           │
                       └─────────────┬─────────────┘
                                     ▼
                              ╔═══════════════╗
                              ║    APACHE     ║
                              ║     HIVE      ║
                              ║               ║
                              ║ DATA          ║
                              ║ WAREHOUSE     ║
                              ║               ║
                              ║    HiveQL     ║
                              ╚═══════╤═══════╝
                                      │
                    ┌─────────────────┼──────────────────┐
                    │                 │                  │
                    ▼                 ▼                  ▼
                 KPI /             Trends /          Summary /
                Analytics          Analysis          Aggregation
                    │                 │                  │
                    └─────────────────┼──────────────────┘
                                      ▼
                                ┌─────────────┐
                                │    Redis    │
                                │    Cache    │
                                └──────┬──────┘
                                       │
                                       ▼
                                    FastAPI
                                       │
                                       ▼
                                    React
```

---

# Apache Hive — System Core

Apache Hive is the **central component** of the platform.

Hive is responsible for:

* Data Warehouse
* Analytical tables
* Fact tables
* Dimension tables
* Summary tables
* Partitioning
* Bucketing
* Aggregation
* HiveQL queries
* Analytical workloads

The project intentionally places Hive at the center of the architecture.

```text
HDFS
  │
  ▼
Apache Hive
  │
  ├── Data Warehouse
  │
  ├── Fact Tables
  │
  ├── Dimension Tables
  │
  ├── Summary Tables
  │
  └── HiveQL
        │
        ├── KPI
        ├── Trends
        ├── Aggregations
        ├── Top-N
        └── Comparisons
```

The platform is therefore not simply a web application connected to a database.

It is a **Big Data Analytics Platform built around a Hive-based Data Warehouse**.

---

# Smart Transportation Domain

The project uses **Smart Transportation** as its real-world domain.

The platform processes transportation-related data and provides analytical insights into transportation operations.

Potential analytical dimensions include:

* Vehicles
* Routes
* Stations
* Locations
* Time
* Transportation events
* Traffic/activity patterns

The exact schema is designed to be **dataset-driven** rather than hard-coded prematurely.

Example conceptual event:

```text
Transportation Event
├── event information
├── timestamp
├── vehicle information
├── route information
├── location information
├── movement information
└── operational status
```

The final schema will depend on the selected transportation dataset and business requirements.

---

# End-to-End Data Flow

The complete platform pipeline is:

```text
① DATA SOURCE
   │
   ├── CSV
   ├── JSON
   ├── API
   └── Streaming Data
   │
   ▼
② INGESTION
   │
   ▼
③ KAFKA
   │
   ▼
④ WORKER
   │
   ▼
⑤ HDFS RAW
   │
   ▼
⑥ SPARK ETL
   │
   ├── Cleaning
   ├── Validation
   ├── Transformation
   └── Enrichment
   │
   ▼
⑦ HDFS PROCESSED
   │
   ▼
⑧ APACHE HIVE
   │
   ├── Data Warehouse
   ├── Fact
   ├── Dimension
   └── Summary
   │
   ▼
⑨ ANALYTICS
   │
   ├── KPI
   ├── Trend
   ├── Distribution
   ├── Top-N
   └── Comparison
   │
   ▼
⑩ REDIS
   │
   ▼
⑪ FASTAPI
   │
   ▼
⑫ REACT DASHBOARD
```

---

# Technology Stack

| Layer          | Technology     | Responsibility                     |
| -------------- | -------------- | ---------------------------------- |
| Frontend       | React          | Dashboard and visualization        |
| API            | FastAPI        | REST API / application layer       |
| Cache          | Redis          | Analytics/query result caching     |
| Metadata       | PostgreSQL     | Platform metadata and system state |
| Documents      | MongoDB        | Semi-structured/document data      |
| Streaming      | Apache Kafka   | Event and data streaming           |
| Orchestration  | Python Worker  | Jobs and pipeline orchestration    |
| Storage        | HDFS           | Distributed Big Data storage       |
| Processing     | Apache Spark   | ETL and batch processing           |
| Data Warehouse | Apache Hive    | DWH and analytical queries         |
| Query          | HiveQL         | Big Data SQL analytics             |
| Metrics        | Prometheus     | Metrics collection                 |
| Monitoring     | Grafana        | Monitoring dashboards              |
| Deployment     | Docker Compose | Infrastructure orchestration       |

---

# Storage Architecture

HDFS is organized conceptually into multiple data zones:

```text
HDFS
│
├── /raw
│
├── /staging
│
├── /processed
│
└── /warehouse
     │
     ├── fact
     ├── dimension
     └── summary
```

### Raw

Original ingested data.

### Staging

Temporary data used during processing.

### Processed

Cleaned and transformed data produced by Spark.

### Warehouse

Analytical data consumed by Hive.

---

# Data Warehouse

The Data Warehouse is implemented using Apache Hive.

The conceptual model follows a dimensional architecture:

```text
                  ┌─────────────┐
                  │   Time      │
                  │ Dimension   │
                  └──────┬──────┘
                         │
                         ▼
┌──────────────┐   ┌───────────────┐   ┌──────────────┐
│ Vehicle      │──▶│ Transportation│◀──│ Route        │
│ Dimension    │   │ Fact          │   │ Dimension    │
└──────────────┘   └───────┬───────┘   └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Location   │
                    │  Dimension   │
                    └──────────────┘
```

This is a conceptual model.

The final dimensions and fact tables will be derived from the actual transportation dataset and analytical requirements.

---

# Analytics

The Analytics layer is responsible for turning transportation data into meaningful information.

Supported analytical categories include:

### KPI

Examples:

* Transportation activity
* Vehicle activity
* Route utilization
* Average movement metrics
* Total events

### Trend Analysis

```text
Time
 │
 ├── Hourly
 ├── Daily
 ├── Weekly
 └── Monthly
```

### Distribution Analysis

Analyze how transportation activity is distributed across relevant dimensions.

### Top-N Analysis

Identify the highest/lowest ranked entities according to selected metrics.

### Comparison

Compare:

* Time periods
* Routes
* Locations
* Vehicles
* Operational metrics

### Aggregation

Use HiveQL to perform large-scale aggregations over the Data Warehouse.

---

# Query Workspace

The platform includes a dedicated **Query Workspace**.

Its purpose is to demonstrate that Apache Hive is actually being used as the analytical engine.

Users can:

* Write HiveQL
* Execute queries
* Format SQL
* View query results
* View execution time
* View rows returned
* View query history
* Save queries
* Use `EXPLAIN`
* Observe Redis cache HIT/MISS

Query flow:

```text
User
 │
 ▼
Query Workspace
 │
 ▼
FastAPI
 │
 ├── Redis HIT
 │      │
 │      └── Return cached result
 │
 └── Redis MISS
        │
        ▼
       Hive
        │
        ▼
      Result
        │
        ▼
      Redis
        │
        ▼
      FastAPI
        │
        ▼
      React
```

This allows the project to demonstrate the difference between:

```text
Hive Query
vs
Cached Query
```

including query latency and cache behavior.

---

# Graph Analytics

The platform provides a Graph visualization layer for exploring relationships in transportation data.

The graph is generated from analytical data stored in Hive.

```text
Hive
 │
 ▼
Relationship Query
 │
 ▼
FastAPI
 │
 ▼
Graph JSON
 │
 ▼
React
```

The frontend supports:

* Nodes
* Edges
* Zoom
* Pan
* Search
* Filtering
* Node details
* Relationship exploration

A separate graph database is **not required in the baseline architecture**.

If future requirements involve large-scale graph traversal, a graph database can be evaluated as an extension.

---

# Data Lineage

The platform provides end-to-end data lineage.

```text
Source
  ↓
MongoDB / Kafka
  ↓
HDFS
  ↓
Spark
  ↓
Hive
  ↓
Analytics
  ↓
Redis
  ↓
FastAPI
  ↓
React Dashboard
```

Users can inspect how data moves through the platform.

Lineage is used to improve:

* Data governance
* Data traceability
* Debugging
* Pipeline understanding
* Dataset management

---

# Frontend

The React application contains 10 major pages.

```text
OVERVIEW

DATA
├── Ingestion
├── Pipelines
├── Data Explorer
└── Lineage

ANALYTICS
├── Analytics
├── Graph
└── Query Workspace

SYSTEM
├── System
└── Monitoring
```

## 1. Overview

Provides a high-level view of the platform.

Includes:

* Platform KPIs
* Ingestion trend
* Pipeline status
* System health
* Analytics summary

## 2. Ingestion

Provides:

* CSV ingestion
* JSON ingestion
* API ingestion
* Streaming ingestion
* Records received
* Throughput
* Error information
* Current ingestion status

## 3. Pipelines

Visualizes:

```text
SOURCE
  ↓
INGEST
  ↓
VALIDATE
  ↓
SPARK
  ↓
HDFS
  ↓
HIVE
  ↓
ANALYTICS
```

Users can inspect:

* Stage duration
* Input records
* Output records
* Errors
* Logs
* Pipeline status

## 4. Data Explorer

Provides a Big Data data browser.

Users can inspect:

* Datasets
* Hive tables
* Schemas
* Partitions
* Storage information
* Data previews
* Statistics
* Lineage

It is intentionally designed as a **data exploration tool**, not a traditional CRUD interface.

## 5. Lineage

Visualizes the movement of data throughout the platform.

## 6. Analytics

Provides:

* KPI
* Trends
* Distribution
* Top-N
* Comparison
* Aggregation
* Time-series analysis

## 7. Graph

Provides transportation relationship exploration.

## 8. Query Workspace

Provides direct HiveQL interaction.

## 9. System

Provides infrastructure/service health.

## 10. Monitoring

Provides monitoring dashboards based on Prometheus and Grafana.

---

# Streaming Architecture

Kafka acts as the event backbone.

Conceptually:

```text
Producer
   │
   ▼
Kafka Topic
   │
   ▼
Worker
   │
   ▼
Processing Pipeline
```

Kafka can handle:

* Transportation events
* Streaming data
* Dataset events
* Pipeline events
* Analytics requests

Examples of platform events:

```text
dataset.uploaded
dataset.validated
pipeline.started
pipeline.completed
pipeline.failed
analytics.requested
```

The event model is extensible and can evolve with the platform.

---

# Worker

The Python Worker is responsible for orchestration.

It can handle:

* Kafka consumption
* Data validation
* Job creation
* Pipeline orchestration
* ETL triggering
* Job status updates
* Error handling
* Pipeline events

The Worker does **not** replace Spark or Hive.

Its responsibility is orchestration.

```text
Kafka
  ↓
Worker
  ↓
Spark
  ↓
HDFS
  ↓
Hive
```

---

# Spark ETL

Apache Spark performs distributed data processing.

Typical processing stages include:

```text
Raw Data
   ↓
Schema Validation
   ↓
Data Cleaning
   ↓
Transformation
   ↓
Enrichment
   ↓
Processed Data
```

Spark writes processed data to HDFS for downstream Hive workloads.

---

# Redis Cache

Redis is used to improve analytical query performance.

The main use case is caching:

```text
Hive Query Result
       ↓
     Redis
       ↓
    FastAPI
       ↓
     React
```

The platform can demonstrate:

```text
First Query
→ Redis MISS
→ Hive
→ Store Result
→ Return Result

Second Query
→ Redis HIT
→ Return Cached Result
```

This allows the platform to measure:

* Query latency
* Cache latency
* Cache hit rate
* Cache miss rate

---

# PostgreSQL

PostgreSQL stores platform metadata and operational information.

Potential metadata includes:

```text
users
datasets
jobs
pipeline_runs
query_history
saved_queries
system_config
audit_logs
```

PostgreSQL is **not used as the Big Data Data Warehouse**.

Hive remains the analytical warehouse.

---

# MongoDB

MongoDB is used for document and semi-structured data.

Potential data includes:

* Raw JSON events
* Dynamic metadata
* Variable-schema records
* Document-oriented data

MongoDB is **not the central Data Warehouse**.

---

# Observability

The platform integrates:

```text
FastAPI ──┐
Kafka ────┤
Redis ────┤
Worker ───┤
HDFS ─────┤
Spark ────┘
     │
     ▼
 Prometheus
     │
     ▼
 Grafana
```

Monitoring metrics include:

### API

* Request count
* Request latency
* Error rate
* Endpoint performance

### Kafka

* Throughput
* Messages
* Consumer lag
* Errors

### Redis

* Cache hits
* Cache misses
* Hit rate
* Memory usage

### Worker

* Jobs processed
* Success rate
* Failure rate
* Processing duration

### Spark

* Job execution
* Processing time
* Input/output information

### HDFS

* Storage usage
* Capacity
* Data volume

---

# Deployment

The infrastructure is designed to run using Docker Compose.

The goal is to provide a reproducible local Big Data environment.

Conceptually:

```text
Docker Compose
│
├── FastAPI
├── React
├── PostgreSQL
├── MongoDB
├── Redis
├── Kafka
├── Worker
├── HDFS
├── Spark
├── Hive
├── Prometheus
└── Grafana
```

---

# Project Structure

The project will be organized into independent components:

```text
bigdata-smart-transportation/
│
├── backend/
│   ├── app/
│   └── worker/
│
├── frontend/
│
├── data/
│   ├── raw/
│   ├── sample/
│   └── generated/
│
├── kafka/
│
├── spark/
│   ├── jobs/
│   └── transformations/
│
├── hive/
│   ├── ddl/
│   ├── queries/
│   ├── views/
│   └── warehouse/
│
├── hdfs/
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── scripts/
│
├── docs/
│
├── tests/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

> The structure may evolve as implementation progresses, but architectural responsibilities will remain separated.

---

# Development Roadmap

The project will be developed incrementally.

## Phase 1 — Infrastructure Foundation

```text
01. Project Structure
02. Docker Compose
03. PostgreSQL
04. MongoDB
05. Redis
06. Kafka
07. Infrastructure Verification
```

## Phase 2 — Data Ingestion

```text
01. Transportation Data Generator
02. Kafka Producer
03. Transportation Events
04. Ingestion Pipeline
```

## Phase 3 — Big Data Processing

```text
01. HDFS
02. Raw Data Storage
03. Spark ETL
04. Processed Data
05. Apache Hive
06. Data Warehouse
```

## Phase 4 — Analytics

```text
01. HiveQL Analytics
02. KPI
03. Trend Analysis
04. Aggregations
05. Summary Tables
06. Query Workspace
```

## Phase 5 — API Layer

```text
01. FastAPI
02. Analytics APIs
03. Query APIs
04. Metadata APIs
05. Redis Cache
```

## Phase 6 — Frontend

```text
01. React
02. Overview
03. Ingestion
04. Pipelines
05. Data Explorer
06. Lineage
07. Analytics
08. Graph
09. Query Workspace
10. System
11. Monitoring
```

## Phase 7 — Observability

```text
01. Prometheus
02. Grafana
03. Application Metrics
04. Kafka Metrics
05. Redis Metrics
06. Worker Metrics
07. Spark/HDFS Metrics
```

---

# Testing Strategy

Testing will be performed at multiple levels.

### Unit Tests

Test individual components:

```text
ETL transformations
Data validation
API services
Cache logic
Utility functions
```

### Integration Tests

Test communication between:

```text
Kafka ↔ Worker
Worker ↔ Spark
Spark ↔ HDFS
HDFS ↔ Hive
FastAPI ↔ Hive
FastAPI ↔ Redis
```

### End-to-End Test

The final system should support:

```text
Data Source
   ↓
Kafka
   ↓
Worker
   ↓
HDFS
   ↓
Spark
   ↓
Hive
   ↓
HiveQL
   ↓
FastAPI
   ↓
React
```

---

# Demonstration Scenario

The final project demonstration will follow a complete data journey.

### Step 1 — Ingest Transportation Data

A transportation dataset is introduced into the platform.

```text
CSV / JSON / Stream
        ↓
     Kafka
```

### Step 2 — Process Data

```text
Kafka
  ↓
Worker
  ↓
HDFS
  ↓
Spark
```

### Step 3 — Build Data Warehouse

```text
Processed Data
      ↓
     HDFS
      ↓
     Hive
```

### Step 4 — Run Analytics

Execute HiveQL queries for:

```text
KPI
Trend
Distribution
Top-N
Aggregation
Comparison
```

### Step 5 — Query Through Workspace

Demonstrate:

```text
HiveQL
  ↓
Redis MISS
  ↓
Hive
  ↓
Result
```

Then execute the same query again:

```text
HiveQL
  ↓
Redis HIT
  ↓
Cached Result
```

Compare execution latency.

### Step 6 — Explore Relationships

```text
Hive
  ↓
Relationship Query
  ↓
FastAPI
  ↓
Graph
```

### Step 7 — Monitor the Platform

Show:

```text
Prometheus
    ↓
Grafana
```

with infrastructure and application metrics.

---

# What This Project Demonstrates

This project is designed to demonstrate practical knowledge in:

### Big Data

* Apache Hadoop
* HDFS
* Apache Spark
* Apache Hive
* HiveQL
* Distributed processing

### Data Engineering

* Data ingestion
* ETL
* Data validation
* Data transformation
* Pipeline orchestration
* Streaming architecture

### Data Warehouse

* Dimensional modeling
* Fact tables
* Dimension tables
* Summary tables
* Partitioning
* Bucketing

### Data Analytics

* SQL analytics
* Aggregation
* KPI
* Trend analysis
* Time-series analysis
* Top-N
* Comparison

### Backend Engineering

* FastAPI
* REST API
* PostgreSQL
* MongoDB
* Redis
* Background workers

### Distributed Systems

* Kafka
* HDFS
* Spark
* Hive

### Frontend

* React
* Data visualization
* Analytics dashboard
* Query interface
* Graph visualization

### DevOps / Observability

* Docker
* Docker Compose
* Prometheus
* Grafana
* Logging
* Monitoring

---

# Architectural Principles

The project follows several important principles.

### 1. Hive is the analytical core

Apache Hive is the center of the Data Warehouse and analytical query layer.

### 2. Do not use CRUD as the center

This is a **Big Data Analytics Platform**, not a transportation CRUD application.

The main workflow is:

```text
Ingestion
   ↓
Processing
   ↓
Storage
   ↓
Data Warehouse
   ↓
Analytics
   ↓
Visualization
```

### 3. Separate responsibilities

Each technology has a clear role.

```text
Kafka   → Streaming
Worker  → Orchestration
HDFS    → Storage
Spark   → Processing
Hive    → Warehouse + Analytics
Redis   → Cache
FastAPI → API
React   → Visualization
```

### 4. Dataset-driven modeling

Transportation entities, dimensions, relationships, and analytical models should be derived from actual requirements and datasets rather than arbitrarily hard-coded.

### 5. Extensible architecture

The system should be capable of supporting additional:

* Data sources
* Transportation datasets
* Analytical models
* Pipelines
* Metrics
* Visualization types
* Query patterns

without requiring major architectural changes.

---

# Project Status

> **Currently under development**

Current stage:

```text
Project Initialization
        ↓
Infrastructure Foundation
        ↓
Data Ingestion
        ↓
Big Data Processing
        ↓
Hive Data Warehouse
        ↓
Analytics
        ↓
API
        ↓
Frontend
        ↓
Monitoring
```

---

# Contributing

Contributions are welcome.

A contribution should ideally follow the existing architecture and preserve separation between:

```text
Ingestion
Processing
Storage
Warehouse
Analytics
API
Frontend
Monitoring
```

For larger changes, please open an issue or discussion before implementation.

---

# License

This project is currently intended as an educational and portfolio project.

A formal open-source license can be added when the repository's distribution policy is finalized.

---

#  Project Focus

**Domain:** Smart Transportation
**Architecture:** Big Data Analytics Platform
**Core:** Apache Hive Data Warehouse
**Processing:** Apache Spark
**Storage:** HDFS
**Streaming:** Apache Kafka
**Backend:** FastAPI
**Frontend:** React
**Cache:** Redis
**Metadata:** PostgreSQL
**Documents:** MongoDB
**Monitoring:** Prometheus + Grafana
**Deployment:** Docker Compose

---

## Core Concept

```text
                    SMART TRANSPORTATION
                            │
                            ▼
                    BIG DATA PLATFORM
                            │
              ┌─────────────┴─────────────┐
              │                           │
         DATA ENGINEERING            DATA ANALYTICS
              │                           │
        Kafka → HDFS → Spark        HiveQL → Hive
              │                           │
              └─────────────┬─────────────┘
                            ▼
                    APACHE HIVE DWH
                            │
                  ┌─────────┼─────────┐
                  │         │         │
                 KPI      Trends    Graph
                  │         │         │
                  └─────────┼─────────┘
                            ▼
                         FastAPI
                            │
                            ▼
                      React Dashboard
                            │
                            ▼
                    Prometheus/Grafana
```

> **The core idea of this project is to build a complete Big Data platform where transportation data flows from ingestion to distributed processing, enters an Apache Hive Data Warehouse, and is transformed into analytical insights, queries, graphs, and dashboards.**
