_# Databricks notebook source

# DBTITLE 1,Structured Streaming Deep Dive
# MAGIC %md
# MAGIC # Cookbook: Structured Streaming Deep Dive
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to build custom, real-time data processing applications that go beyond the declarative framework of Delta Live Tables. You require fine-grained control over the streaming logic, state management, and output sinks.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a deep dive into **Structured Streaming**, the core stream processing engine in Apache Spark. While DLT is recommended for most ETL pipelines, understanding Structured Streaming is essential for building advanced streaming applications.

# COMMAND ----------

# DBTITLE 1,Input Source: Rate Stream
# MAGIC %md
# MAGIC We will use the `rate` stream source for testing. It generates data with a timestamp and a value.

# COMMAND ----------

from pyspark.sql.functions import *

# Create a streaming DataFrame
streaming_df = spark.readStream \
  .format("rate") \
  .option("rowsPerSecond", 1) \
  .load()

# COMMAND ----------

# DBTITLE 1,Transformations on Streaming DataFrames
# You can apply most standard DataFrame operations to a streaming DataFrame
transformed_df = streaming_df \
  .withColumn("is_even", col("value") % 2 == 0)

# COMMAND ----------

# DBTITLE 1,Stateful Streaming: Windowing and Aggregation
# Perform a 10-second tumbling window aggregation
windowed_counts = transformed_df \
  .withWatermark("timestamp", "10 seconds") \
  .groupBy(
    window("timestamp", "10 seconds", "5 seconds"),
    "is_even"
  ) \
  .count()

# COMMAND ----------

# DBTITLE 1,Output Sink: Console
# MAGIC %md
# MAGIC The console sink is useful for debugging.

# COMMAND ----------

query = windowed_counts.writeStream \
  .outputMode("update") \
  .format("console") \
  .start()

# COMMAND ----------

# DBTITLE 1,Output Sink: Delta Lake
# MAGIC %md
# MAGIC Writing to a Delta table is the most common use case for production streaming applications.

# COMMAND ----------

# Stop the console query
query.stop()

# Write the stream to a Delta table
query_delta = windowed_counts.writeStream \
  .outputMode("update") \
  .format("delta") \
  .option("checkpointLocation", "/tmp/delta/checkpoints") \
  .toTable("main.default.windowed_counts")

# COMMAND ----------

# DBTITLE 1,Best Practices Review
# MAGIC %md
# MAGIC ### Key Concepts Demonstrated
# MAGIC 
# MAGIC - **✅ Input Source**: Using the `rate` source for easy testing.
# MAGIC - **✅ Watermarking**: Using `withWatermark` to handle late-arriving data.
# MAGIC - **✅ Windowing**: Using `window` to perform time-based aggregations.
# MAGIC - **✅ Output Sinks**: Writing to both the console (for debugging) and a Delta table (for production).
# MAGIC - **✅ Checkpointing**: Using a checkpoint location to ensure fault tolerance.

# MAGIC ### Important Considerations
# MAGIC 
# MAGIC - **State Management**: Stateful streaming operations (like `groupBy` and `agg`) require Spark to maintain state. The size of this state can grow over time, so it's important to use watermarking to bound the state.
# MAGIC - **Output Modes**:
# MAGIC   - **`append`**: Only new rows are written to the sink.
# MAGIC   - **`complete`**: The entire result table is written to the sink each time.
# MAGIC   - **`update`**: Only the rows that were updated in the result table are written to the sink.
# MAGIC - **Monitoring**: Use the Spark UI to monitor your streaming queries. The "Structured Streaming" tab provides detailed information about the progress, latency, and throughput of your streams.
