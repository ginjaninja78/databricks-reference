_# Databricks notebook source

# DBTITLE 1,Streaming ETL with Auto Loader & Delta Live Tables (DLT)
# MAGIC %md
# MAGIC # Cookbook: Streaming ETL with Auto Loader & Delta Live Tables (DLT)
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to build a real-time, fault-tolerant, and scalable data pipeline that can incrementally process large volumes of data as it arrives in cloud storage. The pipeline must handle schema evolution automatically, ensure data quality, and be easy to manage and monitor.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a production-ready recipe for building a streaming ETL pipeline using two of Databricks' most powerful features: **Auto Loader** and **Delta Live Tables (DLT)**.
# MAGIC 
# MAGIC - **Auto Loader**: Incrementally and efficiently processes new data files as they arrive in cloud storage. It supports schema inference and evolution, preventing pipeline failures due to schema changes.
# MAGIC - **Delta Live Tables (DLT)**: A declarative framework for building reliable, maintainable, and testable data processing pipelines. DLT manages task orchestration, cluster management, monitoring, and data quality.
# MAGIC 
# MAGIC This recipe demonstrates the Medallion Architecture within a DLT pipeline:
# MAGIC 
# MAGIC 1.  **Bronze Layer**: Auto Loader ingests raw JSON data into a streaming table, capturing the raw, unprocessed events.
# MAGIC 2.  **Silver Layer**: The raw data is cleaned, validated, and transformed into a structured, queryable format. Data quality expectations are enforced.
# MAGIC 3.  **Gold Layer**: The clean data is aggregated to create business-level metrics, ready for BI and analytics.
# MAGIC 
# MAGIC ## 3. How to Use This Recipe
# MAGIC 
# MAGIC 1.  **Import this Notebook**: Import this notebook into your Databricks workspace.
# MAGIC 2.  **Create a DLT Pipeline**:
# MAGIC     - Go to **Workflows > Delta Live Tables > Create Pipeline**.
# MAGIC     - Select this notebook as the source.
# MAGIC     - Configure the **Target Schema** (e.g., `your_catalog.your_schema`) where the tables will be created.
# MAGIC     - Set the **Storage Location** for the pipeline logs and data.
# MAGIC 3.  **Start the Pipeline**:
# MAGIC     - Click **Start** to run the pipeline. DLT will provision the cluster, create the tables, and start processing data.

# COMMAND ----------

# DBTITLE 1,Import Libraries & Initialize Widgets
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# DBTITLE 1,Define Pipeline Parameters
# MAGIC %md
# MAGIC It's a best practice to parameterize your DLT pipelines. This allows you to reuse the same pipeline logic for different environments (e.g., dev, staging, prod) by simply changing the configuration.

# COMMAND ----------

# In a real-world scenario, you would get this from a widget or a configuration file.
source_data_path = "/databricks-datasets/retail-org/sales_orders/"

# COMMAND ----------

# DBTITLE 1,Bronze Layer: Ingest Raw Data with Auto Loader
@dlt.table(
  name="sales_orders_raw",
  comment="The raw sales orders data, ingested from cloud storage."
)
def sales_orders_raw():
  return (
    spark.readStream.format("cloudFiles")
      .option("cloudFiles.format", "json")
      .option("cloudFiles.schemaLocation", "/tmp/dlt_schemas/sales_orders_raw")
      .load(source_data_path)
  )

# COMMAND ----------

# DBTITLE 1,Silver Layer: Cleanse and Validate Data
@dlt.table(
  name="sales_orders_cleaned",
  comment="Cleaned and validated sales orders data with data quality checks."
)
@dlt.expect_or_drop("valid_order_number", "order_number IS NOT NULL")
@dlt.expect("valid_quantity", "quantity > 0")
def sales_orders_cleaned():
  return (
    dlt.read_stream("sales_orders_raw")
      .withColumn("order_timestamp", to_timestamp(col("order_datetime"), "yyyy-MM-dd HH:mm:ss"))
      .withColumn("total_price", col("quantity") * col("unit_price"))
      .select(
        "customer_id",
        "order_number",
        "order_timestamp",
        "total_price",
        "quantity"
      )
  )

# COMMAND ----------

# DBTITLE 1,Gold Layer: Create Business Aggregates
@dlt.table(
  name="daily_customer_sales",
  comment="Daily aggregated sales data by customer."
)
def daily_customer_sales():
  return (
    dlt.read("sales_orders_cleaned")
      .groupBy(
        "customer_id",
        window("order_timestamp", "1 day").alias("order_date")
      )
      .agg(
        sum("total_price").alias("total_daily_sales"),
        count("order_number").alias("total_daily_orders")
      )
  )

# COMMAND ----------

# DBTITLE 1,Next Steps & Best Practices
# MAGIC %md
# MAGIC ### Next Steps
# MAGIC 
# MAGIC - **Connect to BI Tools**: Connect your favorite BI tool (like Power BI) to the `daily_customer_sales` table.
# MAGIC - **Add More Layers**: Extend the pipeline with more complex transformations or join with other datasets.
# MAGIC - **Set Up Alerts**: Configure alerts on your DLT pipeline to be notified of failures or data quality issues.
# MAGIC 
# MAGIC ### Best Practices Demonstrated
# MAGIC 
# MAGIC - **Declarative Pipelines**: Using `@dlt` decorators makes the code easy to read and maintain.
# MAGIC - **Data Quality as Code**: `@dlt.expect` rules are embedded directly in the pipeline, making data quality a first-class citizen.
# MAGIC - **Automatic Schema Handling**: Auto Loader handles schema drift automatically, making the pipeline more robust.
# MAGIC - **Incremental Processing**: DLT and Auto Loader work together to process data incrementally, saving time and resources.
# MAGIC - **Separation of Concerns**: The Medallion Architecture separates raw, cleaned, and aggregated data, making the pipeline easier to manage and debug.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is inspired by best practices from the official Databricks documentation and solution accelerators. It is intended to be a starting point for building your own production-grade streaming pipelines.
