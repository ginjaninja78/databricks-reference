_# Databricks notebook source

# DBTITLE 1,Change Data Capture (CDC) with Delta Live Tables (DLT)
# MAGIC %md
# MAGIC # Cookbook: Change Data Capture (CDC) with Delta Live Tables (DLT)
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to process and apply changes from a source database to a target Delta table. This is a common requirement in data warehousing and data lake scenarios.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This recipe demonstrates how to implement Change Data Capture (CDC) in Databricks using **Delta Live Tables (DLT)**.
# MAGIC 
# MAGIC DLT has built-in support for CDC, making it easy to handle inserts, updates, and deletes from a source system.

# COMMAND ----------

# DBTITLE 1,Import Libraries
import dlt

# COMMAND ----------

# DBTITLE 1,Create Sample CDC Data
# In a real-world scenario, this data would be coming from a streaming source like Kafka or a CDC tool like Debezium
cdc_data = [
    (1, "Alice", "insert"),
    (2, "Bob", "insert"),
    (1, "Alice Smith", "update"),
    (3, "Charlie", "insert"),
    (2, None, "delete")
]
cdc_columns = ["id", "name", "operation"]
cdc_df = spark.createDataFrame(cdc_data, cdc_columns)

# Write the CDC data to a Delta table to simulate a streaming source
cdc_df.write.mode("overwrite").saveAsTable("main.default.cdc_source")

# COMMAND ----------

# DBTITLE 1,Define the CDC Source
@dlt.table
def cdc_source():
  return spark.readStream.table("main.default.cdc_source")

# COMMAND ----------

# DBTITLE 1,Apply Changes (SCD Type 1)
# SCD Type 1: Overwrite the existing record with the new record
dlt.apply_changes(
  target = "target_table_scd1",
  source = "cdc_source",
  keys = ["id"],
  sequence_by = "id",
  apply_as_deletes = "operation = \'delete\\'",
  except_column_list = ["operation"]
)

# COMMAND ----------

# DBTITLE 1,Apply Changes (SCD Type 2)
# SCD Type 2: Keep a history of changes
dlt.apply_changes(
  target = "target_table_scd2",
  source = "cdc_source",
  keys = ["id"],
  sequence_by = "id",
  apply_as_deletes = "operation = \'delete\\'",
  except_column_list = ["operation"],
  stored_as_scd_type = 2
)

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### Use DLT for CDC
# MAGIC 
# MAGIC DLT is the recommended way to implement CDC in Databricks. It simplifies the process and provides built-in support for common CDC patterns.
# MAGIC 
# MAGIC ### Choose the Right SCD Type
# MAGIC 
# MAGIC - **SCD Type 1**: Use when you only need the latest version of the data.
# MAGIC - **SCD Type 2**: Use when you need to track the history of changes.
# MAGIC 
# MAGIC ### Handle Out-of-Order Data
# MAGIC 
# MAGIC Use the `track_history` option in `dlt.apply_changes()` to handle out-of-order data. This is important when dealing with streaming data that may arrive out of order.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the Databricks documentation.
