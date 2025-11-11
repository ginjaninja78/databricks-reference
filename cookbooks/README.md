---
title: Sample Notebooks
nav_order: 5
has_children: false
---

# Sample Notebooks: End-to-End Medallion Architecture

This directory contains production-ready Databricks notebooks that demonstrate the complete Medallion Architecture (Bronze → Silver → Gold) pattern. These notebooks are designed to be copied, customized, and deployed in your own Databricks environment.

## Overview

The sample notebooks provide a complete, working example of a data pipeline that:

1.  **Ingests** raw data from cloud storage into a Bronze Delta table
2.  **Cleanses and validates** the data, writing to a Silver Delta table
3.  **Aggregates** the data into business-ready metrics in a Gold Delta table
4.  **Optimizes** tables for BI tool consumption (especially Power BI)

Each notebook is heavily commented with explanations, best practices, and links to relevant documentation in this repository.

## Notebook Structure

### Bronze Layer: Raw Data Ingestion

**Notebook**: [`bronze/01_ingest_raw_data_autoloader.py`](bronze/01_ingest_raw_data_autoloader.py)

**Purpose**: Ingest raw JSON files from cloud storage using Auto Loader.

**Key Concepts Demonstrated**:
-   Auto Loader (`cloudFiles`) for incremental ingestion
-   Schema inference and evolution
-   Metadata enrichment (source file, ingestion timestamp)
-   Exactly-once processing with checkpointing
-   Writing to Delta tables in append mode

**Prerequisites**:
-   Source data location (cloud storage path)
-   Unity Catalog with `bronze` schema created
-   Appropriate read permissions on source data

**Customization Points**:
-   `SOURCE_PATH`: Update to your cloud storage location
-   `CHECKPOINT_PATH`: Update to your checkpoint storage location
-   `TARGET_CATALOG` and `TARGET_SCHEMA`: Update to match your environment
-   File format: Change `cloudFiles.format` if not using JSON

### Silver Layer: Data Cleansing and Validation

**Notebook**: [`silver/02_cleanse_and_validate.py`](silver/02_cleanse_and_validate.py)

**Purpose**: Transform Bronze raw data into clean, validated Silver data.

**Key Concepts Demonstrated**:
-   Reading from Bronze Delta tables
-   Data cleansing: trimming, standardizing, type casting
-   Data validation: null checks, business rule enforcement
-   Deduplication using window functions
-   MERGE (upsert) operations for idempotent processing
-   Hash-based change detection
-   Table optimization with Z-ORDERING

**Prerequisites**:
-   Bronze table populated with raw data
-   Unity Catalog with `silver` schema created

**Customization Points**:
-   `SOURCE_CATALOG`, `SOURCE_SCHEMA`, `SOURCE_TABLE`: Update to match your Bronze table
-   `TARGET_CATALOG`, `TARGET_SCHEMA`, `TARGET_TABLE`: Update to match your Silver table
-   Cleansing rules: Modify transformations to match your data requirements
-   Validation rules: Add or modify business logic checks
-   Deduplication logic: Adjust window specification based on your unique key

### Gold Layer: Business Aggregations

**Notebook**: [`gold/03_business_aggregations.py`](gold/03_business_aggregations.py)

**Purpose**: Create business-ready aggregations from Silver data for BI consumption.

**Key Concepts Demonstrated**:
-   Reading from Silver Delta tables
-   Building daily aggregations with multiple metrics
-   Creating derived business metrics
-   MERGE operations for incremental updates
-   Partitioning by date for efficient queries
-   Z-ORDERING for BI query optimization
-   Creating summary views for quick insights
-   Granting permissions for BI tools

**Prerequisites**:
-   Silver table populated with clean data
-   Unity Catalog with `gold` schema created

**Customization Points**:
-   `SILVER_CATALOG`, `SILVER_SCHEMA`, `TRANSACTIONS_TABLE`: Update to match your Silver table
-   `GOLD_CATALOG`, `GOLD_SCHEMA`, `DAILY_SALES_TABLE`: Update to match your Gold table
-   Aggregation logic: Modify groupBy and agg functions to match your business requirements
-   Metrics: Add or remove calculated metrics based on your needs
-   Partitioning: Adjust partitioning strategy based on your data volume and query patterns

## Running the Notebooks

### Option 1: Interactive Execution in Databricks Workspace

1.  **Import the notebooks** into your Databricks workspace:
    -   Navigate to your workspace
    -   Right-click on a folder and select "Import"
    -   Upload the `.py` files from this directory

2.  **Create a cluster** or use an existing one:
    -   Recommended: DBR 13.3 LTS or higher
    -   Enable Unity Catalog

3.  **Update configuration** in each notebook:
    -   Modify the configuration cells with your environment-specific values

4.  **Run the notebooks in order**:
    -   Bronze → Silver → Gold

### Option 2: Automated Execution with Databricks Jobs

1.  **Create a Databricks Job** with three tasks:
    -   Task 1: Bronze ingestion notebook
    -   Task 2: Silver cleansing notebook (depends on Task 1)
    -   Task 3: Gold aggregation notebook (depends on Task 2)

2.  **Configure a schedule**:
    -   Example: Daily at 2 AM UTC

3.  **Set up alerts**:
    -   Configure email notifications for job failures

4.  **Use Job Clusters**:
    -   For cost optimization, use Job Clusters instead of All-Purpose Clusters

### Option 3: CI/CD Deployment with GitHub Actions

See the [GitHub Integration Bible](/pillar_iii/github_integration_bible/) for a complete guide to deploying these notebooks via CI/CD pipelines.

## Data Flow Diagram

```
Cloud Storage (JSON files)
        ↓
    [Auto Loader]
        ↓
┌─────────────────┐
│  Bronze Layer   │  ← Raw, unprocessed data
│  Delta Table    │     with metadata
└─────────────────┘
        ↓
   [Cleansing &
    Validation]
        ↓
┌─────────────────┐
│  Silver Layer   │  ← Clean, validated,
│  Delta Table    │     deduplicated data
└─────────────────┘
        ↓
   [Aggregation &
    Business Logic]
        ↓
┌─────────────────┐
│   Gold Layer    │  ← Business-ready
│  Delta Table    │     aggregations
└─────────────────┘
        ↓
    [Power BI /
     BI Tools]
```

## Expected Data Schema

These notebooks expect a sales transaction dataset with the following structure:

**Bronze Layer (Raw)**:
```json
{
  "transaction_id": "TXN-12345",
  "customer_id": "CUST-67890",
  "product_id": "PROD-11111",
  "transaction_date": "2024-01-15 14:30:00",
  "quantity": 2,
  "unit_price": 29.99,
  "total_amount": 59.98,
  "country": "USA"
}
```

**Silver Layer (Cleansed)**:
-   All Bronze fields, cleansed and validated
-   Additional metadata: `_source_file`, `_ingestion_timestamp`, `_silver_processed_timestamp`, `_record_hash`

**Gold Layer (Aggregated)**:
-   Daily aggregations by `transaction_date`, `product_id`, `country`
-   Metrics: `total_transactions`, `total_quantity_sold`, `total_sales_amount`, `avg_unit_price`, etc.

## Customization for Your Use Case

These notebooks are templates. To adapt them for your specific use case:

1.  **Update the schema**: Modify the column names and data types to match your source data
2.  **Adjust cleansing rules**: Add or remove data quality checks based on your requirements
3.  **Change aggregation logic**: Modify the groupBy and aggregation functions for your business metrics
4.  **Add error handling**: Implement custom error handling and alerting logic
5.  **Integrate with your catalog**: Update catalog, schema, and table names to match your Unity Catalog structure

## Best Practices Demonstrated

These notebooks follow industry best practices:

✅ **Idempotent processing**: Can be re-run safely without duplicating data  
✅ **Incremental ingestion**: Only processes new or changed data  
✅ **Schema evolution**: Handles schema changes gracefully  
✅ **Data lineage**: Tracks source files and processing timestamps  
✅ **Optimization**: Uses Z-ORDERING and partitioning for query performance  
✅ **Metadata enrichment**: Adds processing metadata for debugging and auditing  
✅ **Error resilience**: Uses checkpointing for fault tolerance  

## Troubleshooting

### Common Issues

**Issue**: "Table or view not found"  
**Solution**: Ensure the source table exists and you have SELECT permissions. Check catalog and schema names.

**Issue**: "Path does not exist"  
**Solution**: Verify the `SOURCE_PATH` and `CHECKPOINT_PATH` are correct and accessible.

**Issue**: "Permission denied"  
**Solution**: Ensure your service principal or user has appropriate permissions on the storage account and Unity Catalog.

**Issue**: "Schema mismatch"  
**Solution**: Enable schema evolution with `mergeSchema` option or adjust the target table schema.

## Related Documentation

-   [Pillar I: Medallion Architecture](/pillar_i/medallion_architecture/)
    -   [Bronze Layer Deep Dive](/pillar_i/medallion_architecture/bronze_layer.md)
    -   [Silver Layer Deep Dive](/pillar_i/medallion_architecture/silver_layer.md)
    -   [Gold Layer Deep Dive](/pillar_i/medallion_architecture/gold_layer.md)
-   [Pillar II: PySpark Mastery](/pillar_ii/python_pyspark/)
-   [Pillar II: Delta Lake DML](/pillar_ii/databricks_sql/delta_lake_dml.md)
-   [Pillar IV: Power BI Integration](/pillar_iv/bi_and_visualization/power_bi_integration.md)

## Next Steps

After running these sample notebooks:

1.  **Extend the pipeline**: Add more layers or intermediate transformations
2.  **Connect Power BI**: Follow the [Power BI Integration Guide](/pillar_iv/bi_and_visualization/power_bi_integration.md)
3.  **Set up monitoring**: Implement data quality monitoring and alerting
4.  **Automate deployment**: Use the [CI/CD patterns](/pillar_iii/github_integration_bible/) to deploy via GitHub Actions
5.  **Scale up**: Apply these patterns to your production data

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
