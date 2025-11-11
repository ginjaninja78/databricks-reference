---
title: Building ELT Pipelines with SQL
nav_order: 3
parent: Databricks SQL Deep Dive
grand_parent: Pillar II The Developer's Toolkit
---

# Building ELT Pipelines with SQL: The Modern Data Warehouse

One of the most powerful patterns in the modern data stack is the **ELT (Extract, Load, Transform)** pipeline, and Databricks SQL is a perfect environment for building them. In this model, data is first extracted from source systems and loaded into the Lakehouse (the Bronze layer) with minimal changes. Then, all transformations to create the Silver and Gold layers are performed *in-situ* using the power of the data platform's compute engine—in this case, Databricks SQL.

This approach has several advantages over traditional ETL:

-   **Simplicity**: Using a single, declarative language (SQL) for all transformations simplifies development and maintenance.
-   **Performance**: It leverages the massively parallel processing power of the Databricks engine to perform transformations at scale.
-   **Flexibility**: Raw data is always available in the Bronze layer, so you can easily rebuild or create new transformations without having to re-ingest data from the source.

Databricks makes this pattern even more powerful with **Delta Live Tables (DLT)**, a framework for building reliable, maintainable, and testable data processing pipelines. While DLT can also use Python, its declarative nature is a perfect fit for SQL.

## The Declarative Nature of a SQL ELT Pipeline

A DLT pipeline is defined as a series of SQL queries that create tables and views. You don't define the *order* of execution; you simply declare the dependencies between tables, and DLT builds the execution graph for you.

### Example: A Simple Bronze-to-Silver DLT Pipeline

Let's define a pipeline that reads raw JSON data from a cloud storage location, loads it into a Bronze table, and then transforms it into a clean Silver table.

**Step 1: Create the Bronze Table**

This table uses Databricks' `cloud_files` Auto Loader, a powerful feature that incrementally and efficiently processes new files as they arrive in cloud storage.

```sql
-- DLT Syntax: CREATE STREAMING LIVE TABLE
-- This creates a table that incrementally processes new source data.
CREATE STREAMING LIVE TABLE bronze_orders (
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION FAIL UPDATE
)
COMMENT "Raw orders data from cloud storage, ingested incrementally."
AS SELECT * FROM cloud_files("/path/to/raw/orders/json", "json");
```

**Key DLT Concepts:**

-   `LIVE`: This keyword signifies that the table is part of a DLT pipeline.
-   `STREAMING`: This tells DLT to process the data incrementally. New data arriving in the source will be processed in the next pipeline run without having to re-read the entire source.
-   `cloud_files`: The Auto Loader source.
-   `CONSTRAINT`: DLT allows you to define data quality expectations directly in your table definitions. Here, we are stating that `order_id` must not be null. If a record violates this, the pipeline will fail, preventing bad data from propagating.

**Step 2: Create the Silver Table**

Now, we define a Silver table that reads from our Bronze table, cleans the data, and enforces a stricter schema.

```sql
-- DLT Syntax: CREATE LIVE TABLE
-- This creates a table that is fully recomputed when the pipeline runs, or incrementally if its source is streaming.
CREATE LIVE TABLE silver_orders (
  CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW
)
COMMENT "Cleaned and conformed orders data."
AS
SELECT
  order_id::int,
  order_timestamp::timestamp,
  customer_id::int,
  product_id::int,
  quantity::int,
  total_price::decimal(10, 2)
FROM LIVE.bronze_orders; -- Use LIVE. to reference other tables in the pipeline
```

**Key DLT Concepts:**

-   `LIVE.bronze_orders`: This is how you declare the dependency. DLT now knows that it must create `bronze_orders` before it can create `silver_orders`.
-   `ON VIOLATION DROP ROW`: This is another data quality rule. If a record from the Bronze table has a null `customer_id`, it will be silently dropped and not included in the Silver table.

## Running the Pipeline

To run this pipeline, you would:

1.  Save these SQL queries in a Databricks Notebook.
2.  Go to the **Workflows** tab in Databricks, select **Delta Live Tables**, and create a new pipeline.
3.  Point the pipeline to your notebook.
4.  Configure settings (like the target catalog/schema) and start the pipeline.

DLT will automatically:

-   Provision the necessary compute infrastructure.
-   Analyze the dependencies and create a Directed Acyclic Graph (DAG) of the pipeline.
-   Execute the queries in the correct order.
-   Collect and report on data quality metrics.
-   Handle retries and error reporting.

This declarative, SQL-first approach to building ELT pipelines is incredibly powerful. It allows data analysts and engineers who are comfortable with SQL to build and manage sophisticated, production-grade data pipelines without needing to write complex orchestration code. It's a cornerstone of the modern Data Lakehouse architecture.
