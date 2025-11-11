---
title: Streaming ETL with Auto Loader & DLT
parent: Databricks Cookbooks
nav_order: 2
---

# Cookbook: Streaming ETL with Auto Loader & Delta Live Tables (DLT)

## 1. Problem Statement

You need to build a real-time, fault-tolerant, and scalable data pipeline that can incrementally process large volumes of data as it arrives in cloud storage. The pipeline must handle schema evolution automatically, ensure data quality, and be easy to manage and monitor.

## 2. Solution Overview

This cookbook provides a production-ready recipe for building a streaming ETL pipeline using two of Databricks' most powerful features: **Auto Loader** and **Delta Live Tables (DLT)**.

- **Auto Loader**: Incrementally and efficiently processes new data files as they arrive in cloud storage. It supports schema inference and evolution, preventing pipeline failures due to schema changes.
- **Delta Live Tables (DLT)**: A declarative framework for building reliable, maintainable, and testable data processing pipelines. DLT manages task orchestration, cluster management, monitoring, and data quality.

This recipe demonstrates the Medallion Architecture within a DLT pipeline:

1.  **Bronze Layer**: Auto Loader ingests raw JSON data into a streaming table, capturing the raw, unprocessed events.
2.  **Silver Layer**: The raw data is cleaned, validated, and transformed into a structured, queryable format. Data quality expectations are enforced.
3.  **Gold Layer**: The clean data is aggregated to create business-level metrics, ready for BI and analytics.

## 3. Step-by-Step Implementation

This cookbook is implemented as a single Delta Live Tables notebook. You can import this notebook and create a DLT pipeline from it.

**Notebook**: [`01_streaming_etl_with_dlt.py`](01_streaming_etl_with_dlt.py)

### Key Concepts Demonstrated

- **Declarative Pipeline Definition**: Using `@dlt.table` and `@dlt.view` decorators.
- **Streaming with Auto Loader**: `spark.readStream.format("cloudFiles")`
- **Schema Inference & Evolution**: `cloudFiles.schemaLocation` and `cloudFiles.schemaEvolutionMode`.
- **Data Quality Expectations**: Using `@dlt.expect` to define and manage data quality rules.
- **Incremental Processing**: DLT automatically handles watermarking and state management.
- **Pipeline Orchestration**: DLT builds and manages the DAG (Directed Acyclic Graph) of dependencies.
- **Parameterization**: Using widgets to parameterize the pipeline for different environments.

## 4. How to Use This Recipe

1.  **Import the Notebook**: Import the `01_streaming_etl_with_dlt.py` notebook into your Databricks workspace.
2.  **Create a DLT Pipeline**:
    - Go to **Workflows > Delta Live Tables > Create Pipeline**.
    - Select the imported notebook as the source.
    - Configure the **Target Schema** (e.g., `your_catalog.your_schema`) where the tables will be created.
    - Set the **Storage Location** for the pipeline logs and data.
    - Under **Compute**, you can configure the cluster policy and size.
3.  **Configure Parameters** (Optional):
    - You can add configuration parameters like `source_path` to point to your own data source.
4.  **Start the Pipeline**:
    - Click **Start** to run the pipeline. DLT will provision the cluster, create the tables, and start processing data.
5.  **Monitor the Pipeline**:
    - The DLT UI provides a visual graph of the pipeline, data quality metrics, and detailed logs.

## 5. Best Practices & Customization

- **Use DLT for Production**: DLT is the recommended way to build production-grade ETL/ELT pipelines on Databricks due to its robustness and manageability.
- **Separate DLT Pipelines**: For complex domains, consider splitting logic into multiple DLT pipelines to manage complexity.
- **Parameterize Everything**: Use configuration parameters for paths, table names, and thresholds to make your pipeline reusable across environments (dev, staging, prod).
- **Schema Location**: Always specify a `schemaLocation` for Auto Loader to enable robust schema evolution.
- **Data Quality Rules**: Start with simple rules (`expect("id IS NOT NULL")`) and add more complex business rules over time. Use `@dlt.expect_or_fail`, `@dlt.expect_or_drop`, or `@dlt.expect_or_ignore` to control the outcome of quality checks.
- **Attribution**: This recipe is inspired by best practices from the official Databricks documentation and solution accelerators.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
