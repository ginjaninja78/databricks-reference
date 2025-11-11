# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer: Data Cleansing and Validation
# MAGIC 
# MAGIC **Purpose**: Transform Bronze raw data into clean, validated Silver data.
# MAGIC 
# MAGIC **Pattern**: This notebook demonstrates the Silver layer transformation pattern:
# MAGIC - Read from Bronze Delta table
# MAGIC - Apply data quality rules and validations
# MAGIC - Deduplicate records
# MAGIC - Standardize data types and formats
# MAGIC - Write to Silver Delta table with MERGE (upsert)
# MAGIC 
# MAGIC **Prerequisites**:
# MAGIC - Bronze table populated with raw data
# MAGIC - Silver catalog and schema created

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

from pyspark.sql.functions import (
    col, trim, upper, to_timestamp, when, coalesce, 
    current_timestamp, sha2, concat_ws, row_number
)
from pyspark.sql.window import Window

# Source and target configuration
SOURCE_CATALOG = "dev"
SOURCE_SCHEMA = "bronze"
SOURCE_TABLE = "sales_transactions_raw"

TARGET_CATALOG = "dev"
TARGET_SCHEMA = "silver"
TARGET_TABLE = "sales_transactions"

SOURCE_FULL_NAME = f"{SOURCE_CATALOG}.{SOURCE_SCHEMA}.{SOURCE_TABLE}"
TARGET_FULL_NAME = f"{TARGET_CATALOG}.{TARGET_SCHEMA}.{TARGET_TABLE}"

print(f"Source: {SOURCE_FULL_NAME}")
print(f"Target: {TARGET_FULL_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read from Bronze

# COMMAND ----------

# Read the Bronze table
bronze_df = spark.table(SOURCE_FULL_NAME)

print(f"Bronze records to process: {bronze_df.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Cleansing
# MAGIC 
# MAGIC Apply transformations to clean and standardize the data:
# MAGIC - Trim whitespace from string fields
# MAGIC - Standardize text case
# MAGIC - Parse and validate timestamps
# MAGIC - Handle null values with business rules

# COMMAND ----------

# Apply cleansing transformations
cleansed_df = (
    bronze_df
    # Trim and standardize string fields
    .withColumn("transaction_id", trim(col("transaction_id")))
    .withColumn("customer_id", trim(col("customer_id")))
    .withColumn("product_id", trim(col("product_id")))
    .withColumn("country", upper(trim(col("country"))))
    
    # Parse timestamp with fallback
    .withColumn(
        "transaction_timestamp",
        coalesce(
            to_timestamp(col("transaction_date"), "yyyy-MM-dd HH:mm:ss"),
            to_timestamp(col("transaction_date"), "yyyy-MM-dd'T'HH:mm:ss"),
            to_timestamp(col("transaction_date"))
        )
    )
    
    # Ensure numeric fields are properly typed
    .withColumn("quantity", col("quantity").cast("integer"))
    .withColumn("unit_price", col("unit_price").cast("decimal(10,2)"))
    .withColumn("total_amount", col("total_amount").cast("decimal(10,2)"))
    
    # Calculate total_amount if missing
    .withColumn(
        "total_amount",
        when(col("total_amount").isNull(), col("quantity") * col("unit_price"))
        .otherwise(col("total_amount"))
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Validation
# MAGIC 
# MAGIC Apply business rules and filter out invalid records.

# COMMAND ----------

# Define data quality rules
validated_df = (
    cleansed_df
    # Filter out records with missing critical fields
    .filter(col("transaction_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("product_id").isNotNull())
    .filter(col("transaction_timestamp").isNotNull())
    
    # Filter out records with invalid business logic
    .filter(col("quantity") > 0)
    .filter(col("unit_price") > 0)
    .filter(col("total_amount") > 0)
)

# Calculate data quality metrics
total_records = cleansed_df.count()
valid_records = validated_df.count()
invalid_records = total_records - valid_records

print(f"Total records: {total_records:,}")
print(f"Valid records: {valid_records:,}")
print(f"Invalid records: {invalid_records:,}")
print(f"Data quality rate: {(valid_records/total_records*100):.2f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deduplication
# MAGIC 
# MAGIC Remove duplicate records, keeping the most recent version based on ingestion timestamp.

# COMMAND ----------

# Define window for deduplication
window_spec = Window.partitionBy("transaction_id").orderBy(col("_ingestion_timestamp").desc())

# Deduplicate: keep the most recent record for each transaction_id
deduplicated_df = (
    validated_df
    .withColumn("row_num", row_number().over(window_spec))
    .filter(col("row_num") == 1)
    .drop("row_num")
)

duplicates_removed = validated_df.count() - deduplicated_df.count()
print(f"Duplicate records removed: {duplicates_removed:,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add Silver Metadata

# COMMAND ----------

# Add Silver layer metadata
final_df = (
    deduplicated_df
    .withColumn("_silver_processed_timestamp", current_timestamp())
    .withColumn(
        "_record_hash",
        sha2(concat_ws("||", 
            col("transaction_id"),
            col("customer_id"),
            col("product_id"),
            col("quantity"),
            col("unit_price")
        ), 256)
    )
    .select(
        "transaction_id",
        "customer_id",
        "product_id",
        "transaction_timestamp",
        "quantity",
        "unit_price",
        "total_amount",
        "country",
        "_source_file",
        "_ingestion_timestamp",
        "_silver_processed_timestamp",
        "_record_hash"
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Silver with MERGE (Upsert)
# MAGIC 
# MAGIC Use Delta Lake's MERGE command to upsert data into the Silver table.
# MAGIC This ensures idempotency and handles late-arriving updates.

# COMMAND ----------

# Create the Silver table if it doesn't exist
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {TARGET_FULL_NAME} (
    transaction_id STRING,
    customer_id STRING,
    product_id STRING,
    transaction_timestamp TIMESTAMP,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    country STRING,
    _source_file STRING,
    _ingestion_timestamp TIMESTAMP,
    _silver_processed_timestamp TIMESTAMP,
    _record_hash STRING
)
USING DELTA
PARTITIONED BY (country)
""")

# COMMAND ----------

# Register the DataFrame as a temporary view for MERGE
final_df.createOrReplaceTempView("silver_updates")

# Execute MERGE statement
merge_result = spark.sql(f"""
MERGE INTO {TARGET_FULL_NAME} AS target
USING silver_updates AS source
ON target.transaction_id = source.transaction_id

WHEN MATCHED AND target._record_hash != source._record_hash THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *
""")

print("MERGE operation completed successfully")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Silver Table

# COMMAND ----------

# Display Silver table statistics
silver_df = spark.table(TARGET_FULL_NAME)
print(f"Total rows in Silver table: {silver_df.count():,}")

# Display sample data
display(silver_df.orderBy(col("transaction_timestamp").desc()).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimize the Silver Table
# MAGIC 
# MAGIC Run OPTIMIZE and Z-ORDER for better query performance.

# COMMAND ----------

# Optimize the table
spark.sql(f"OPTIMIZE {TARGET_FULL_NAME} ZORDER BY (transaction_timestamp, customer_id)")

print("Table optimization completed")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC 
# MAGIC The Silver table now contains clean, validated, and deduplicated data.
# MAGIC 
# MAGIC **Recommended Next Steps**:
# MAGIC 1. Create a **Gold layer** notebook to build business aggregations
# MAGIC 2. Set up **data quality monitoring** with expectations
# MAGIC 3. Implement **alerting** for data quality failures
# MAGIC 4. Schedule this notebook as part of an **orchestrated pipeline**
# MAGIC 
# MAGIC **Related Documentation**:
# MAGIC - [Silver Layer Deep Dive](/pillar_i/medallion_architecture/silver_layer.md)
# MAGIC - [Delta Lake MERGE](/pillar_ii/databricks_sql/delta_lake_dml.md)
