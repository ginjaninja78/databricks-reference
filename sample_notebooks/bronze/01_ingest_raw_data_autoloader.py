# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Layer: Raw Data Ingestion with Auto Loader
# MAGIC 
# MAGIC **Purpose**: Ingest raw JSON files from cloud storage into a Bronze Delta table using Auto Loader.
# MAGIC 
# MAGIC **Pattern**: This notebook demonstrates the foundational Bronze layer pattern:
# MAGIC - Incremental ingestion of raw data
# MAGIC - Schema inference and evolution
# MAGIC - Metadata enrichment (source file, ingestion timestamp)
# MAGIC - Idempotent processing
# MAGIC 
# MAGIC **Prerequisites**:
# MAGIC - Source data location configured
# MAGIC - Target catalog and schema created in Unity Catalog
# MAGIC - Appropriate permissions granted

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# Import required libraries
from pyspark.sql.functions import current_timestamp, input_file_name, col

# Configuration parameters
SOURCE_PATH = "/mnt/raw-data/sales-transactions/"  # Replace with your source path
CHECKPOINT_PATH = "/mnt/checkpoints/bronze_sales/"  # Replace with your checkpoint path
TARGET_CATALOG = "dev"
TARGET_SCHEMA = "bronze"
TARGET_TABLE = "sales_transactions_raw"

# Full table name
FULL_TABLE_NAME = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.{TARGET_TABLE}"

print(f"Source Path: {SOURCE_PATH}")
print(f"Checkpoint Path: {CHECKPOINT_PATH}")
print(f"Target Table: {FULL_TABLE_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest Raw Data with Auto Loader
# MAGIC 
# MAGIC Auto Loader (`cloudFiles`) is Databricks' recommended solution for incrementally ingesting data from cloud storage.
# MAGIC 
# MAGIC **Key Features**:
# MAGIC - Automatic schema inference and evolution
# MAGIC - Efficient file discovery (uses file notifications or directory listing)
# MAGIC - Exactly-once processing guarantees
# MAGIC - Handles millions of files efficiently

# COMMAND ----------

# Read streaming data from cloud storage using Auto Loader
raw_stream_df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")  # Source file format
    .option("cloudFiles.schemaLocation", CHECKPOINT_PATH + "/schema")  # Schema evolution tracking
    .option("cloudFiles.inferColumnTypes", "true")  # Infer data types
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")  # Handle schema changes
    .load(SOURCE_PATH)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Enrich with Metadata
# MAGIC 
# MAGIC Add metadata columns to track data lineage and enable debugging.

# COMMAND ----------

# Add metadata columns
enriched_df = (
    raw_stream_df
    .withColumn("_source_file", input_file_name())
    .withColumn("_ingestion_timestamp", current_timestamp())
)

# Display the schema
enriched_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Bronze Delta Table
# MAGIC 
# MAGIC Write the enriched stream to a Bronze Delta table with the following settings:
# MAGIC - **Append mode**: New data is appended to the table
# MAGIC - **Checkpointing**: Ensures exactly-once processing
# MAGIC - **Optimized writes**: Improves write performance
# MAGIC - **Auto compaction**: Automatically compacts small files

# COMMAND ----------

# Write the stream to the Bronze Delta table
query = (
    enriched_df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_PATH)
    .option("mergeSchema", "true")  # Allow schema evolution
    .trigger(availableNow=True)  # Process all available data, then stop
    .toTable(FULL_TABLE_NAME)
)

# Wait for the stream to finish processing
query.awaitTermination()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Ingestion

# COMMAND ----------

# Display row count
row_count = spark.table(FULL_TABLE_NAME).count()
print(f"Total rows in {FULL_TABLE_NAME}: {row_count:,}")

# Display sample data
display(spark.table(FULL_TABLE_NAME).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC 
# MAGIC This Bronze table now contains raw, unprocessed data with full lineage metadata.
# MAGIC 
# MAGIC **Recommended Next Steps**:
# MAGIC 1. Create a **Silver layer** notebook to cleanse and validate this data
# MAGIC 2. Set up **data quality monitoring** to track ingestion metrics
# MAGIC 3. Schedule this notebook as a **Databricks Job** for automated ingestion
# MAGIC 4. Configure **alerts** for ingestion failures
# MAGIC 
# MAGIC **Related Documentation**:
# MAGIC - [Bronze Layer Deep Dive](/pillar_i/medallion_architecture/bronze_layer.md)
# MAGIC - [Auto Loader Best Practices](https://docs.databricks.com/ingestion/auto-loader/index.html)
