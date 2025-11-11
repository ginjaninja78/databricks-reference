_# Databricks notebook source

# DBTITLE 1,Caching and Persistence
# MAGIC %md
# MAGIC # Cookbook: Caching and Persistence
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You have a large DataFrame that is used multiple times in your notebook, and you want to avoid recomputing it every time. This is common in iterative algorithms (like in machine learning) and interactive data analysis.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC Spark provides two methods for caching DataFrames: `cache()` and `persist()`.
# MAGIC 
# MAGIC - **`cache()`**: A shorthand for `persist(StorageLevel.MEMORY_ONLY)`.
# MAGIC - **`persist()`**: Allows you to specify the storage level (e.g., memory only, memory and disk, etc.).
# MAGIC 
# MAGIC This recipe demonstrates how to use `cache()` and `persist()` to speed up your workloads.

# COMMAND ----------

# DBTITLE 1,Generate Sample Data
# Generate a large DataFrame
df = spark.range(10000000).toDF("id")

# COMMAND ----------

# DBTITLE 1,Without Caching
# MAGIC %timeit -n 1 -r 1
# MAGIC # Perform two actions on the DataFrame
# MAGIC df.count()
# MAGIC df.count()

# COMMAND ----------

# DBTITLE 1,With Caching
# Cache the DataFrame
df.cache()

# COMMAND ----------

# MAGIC %timeit -n 1 -r 1
# MAGIC # Perform two actions on the DataFrame
# MAGIC df.count()
# MAGIC df.count()

# COMMAND ----------

# DBTITLE 1,Unpersist the DataFrame
# It's a good practice to unpersist the DataFrame when you're done with it
df.unpersist()

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### When to Use Caching
# MAGIC 
# MAGIC - When you have a large DataFrame that is used multiple times.
# MAGIC - In iterative algorithms (e.g., machine learning).
# MAGIC - In interactive data analysis.
# MAGIC 
# MAGIC ### When Not to Use Caching
# MAGIC 
# MAGIC - When you have a small DataFrame that is cheap to recompute.
# MAGIC - When you only use the DataFrame once.
# MAGIC 
# MAGIC ### `cache()` vs. `persist()`
# MAGIC 
# MAGIC - Use `cache()` for simplicity when you just want to cache the DataFrame in memory.
# MAGIC - Use `persist()` when you need more control over the storage level (e.g., `StorageLevel.MEMORY_AND_DISK`).
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the Databricks documentation and the book "Optimizing Databricks Workloads" by Packt Publishing.
