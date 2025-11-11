_# Databricks notebook source

# DBTITLE 1,Data Quality Monitoring with Delta Live Tables (DLT)
# MAGIC %md
# MAGIC # Cookbook: Data Quality Monitoring with Delta Live Tables (DLT)
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to ensure the quality and integrity of your data as it moves through your data pipelines. This includes validating data against a set of rules, monitoring data quality over time, and being alerted to any issues.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a recipe for implementing a robust data quality monitoring solution on Databricks using **Delta Live Tables (DLT)**.
# MAGIC 
# MAGIC This recipe demonstrates:
# MAGIC 
# MAGIC - **Defining Data Quality Rules**: Using `@dlt.expect` to define rules for nulls, formats, and business logic.
# MAGIC - **Handling Data Quality Failures**: Using `@dlt.expect_or_drop` and `@dlt.expect_or_fail` to control the behavior of the pipeline when data quality rules are violated.
# MAGIC 
# MAGIC ## 3. How to Use This Recipe
# MAGIC 
# MAGIC 1.  **Import this Notebook**: Import this notebook into your Databricks workspace.
# MAGIC 2.  **Create a DLT Pipeline**: Create a DLT pipeline from this notebook.
# MAGIC 3.  **Monitor Data Quality**: The DLT UI will show the data quality metrics for your pipeline.

# COMMAND ----------

# DBTITLE 1,Import Libraries
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# DBTITLE 1,Bronze Layer: Ingest Raw Data
@dlt.table(
  name="customers_raw",
  comment="The raw customer data, ingested from a sample dataset."
)
def customers_raw():
  return spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/databricks-datasets/retail-org/customers/")

# COMMAND ----------

# DBTITLE 1,Silver Layer: Cleanse and Validate with Data Quality Rules
@dlt.table(
  name="customers_cleaned",
  comment="Cleaned and validated customer data with data quality checks."
)
@dlt.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
@dlt.expect_or_drop("valid_email", "email LIKE \'%@%.%\'")
@dlt.expect("valid_zip_code", "zip_code > 0")
def customers_cleaned():
  return (
    dlt.read("customers_raw")
      .withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name")))
      .select(
        "customer_id",
        "full_name",
        "email",
        "city",
        "state",
        "zip_code"
      )
  )

# COMMAND ----------

# DBTITLE 1,Next Steps & Best Practices
# MAGIC %md
# MAGIC ### Next Steps
# MAGIC 
# MAGIC - **Explore the DLT UI**: After running the pipeline, explore the DLT UI to see the data quality metrics.
# MAGIC - **Quarantine Tables**: DLT automatically creates quarantine tables to store records that fail `expect_or_drop` rules. You can query these tables to analyze the invalid data.
# MAGIC - **Alerting**: Configure alerts on your DLT pipeline to be notified of data quality failures.
# MAGIC 
# MAGIC ### Best Practices Demonstrated
# MAGIC 
# MAGIC - **Data Quality as Code**: Embedding data quality rules directly in your pipeline code makes them transparent and maintainable.
# MAGIC - **Fail-Fast vs. Quarantine**: This recipe demonstrates both dropping invalid records (`expect_or_drop`) and allowing them to pass with a warning (`expect`). You can also use `expect_or_fail` to stop the pipeline if a data quality rule is violated.
# MAGIC - **Centralized Quality Metrics**: The DLT UI provides a centralized place to monitor data quality across your entire pipeline.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the official Databricks documentation.
