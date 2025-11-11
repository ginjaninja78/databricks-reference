_# Databricks notebook source

# DBTITLE 1,Prepare Data for Power BI
# MAGIC %md
# MAGIC # Cookbook: Prepare Data for Power BI
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to create an optimized Gold table in your data lakehouse that is specifically designed for consumption by Power BI. This table should be aggregated, easy to understand, and performant.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This notebook demonstrates how to create a business-ready Gold table from a Silver table. This Gold table will serve as the foundation for a Power BI report.
# MAGIC 
# MAGIC The process is as follows:
# MAGIC 
# MAGIC 1.  **Read from the Silver Layer**: Start with a clean, validated Silver table.
# MAGIC 2.  **Create Business Aggregations**: Group and aggregate the data to create business-level metrics.
# MAGIC 3.  **Optimize the Gold Table**: Use techniques like Z-ORDERING to optimize the table for BI queries.
# MAGIC 4.  **Grant Permissions**: Ensure that your Power BI users or service principals have the necessary permissions to access the Gold table.

# COMMAND ----------

# DBTITLE 1,Read from the Silver Layer
# In a real-world scenario, you would read from your own Silver table
# For this example, we will create a sample Silver table

silver_data = [
    (1, "2023-01-01", "USA", 100.0),
    (2, "2023-01-01", "USA", 150.0),
    (3, "2023-01-01", "Canada", 80.0),
    (4, "2023-01-02", "USA", 200.0),
    (5, "2023-01-02", "Canada", 120.0)
]
silver_columns = ["transaction_id", "transaction_date", "country", "amount"]
silver_df = spark.createDataFrame(silver_data, silver_columns)

silver_df.write.mode("overwrite").saveAsTable("main.default.silver_sales")

# COMMAND ----------

# DBTITLE 1,Create Business Aggregations
# Create a Gold table with daily sales by country
gold_df = silver_df.groupBy("transaction_date", "country") \
  .agg(
    sum("amount").alias("total_sales"),
    count("transaction_id").alias("total_transactions")
  )

display(gold_df)

# COMMAND ----------

# DBTITLE 1,Optimize and Save the Gold Table
# Save the Gold table, partitioned by date for better performance
gold_df.write.mode("overwrite") \
  .partitionBy("transaction_date") \
  .saveAsTable("main.default.gold_daily_sales")

# Optimize the table with Z-ORDERING
spark.sql("OPTIMIZE main.default.gold_daily_sales ZORDER BY (country)")

# COMMAND ----------

# DBTITLE 1,Grant Permissions
# MAGIC %sql
# MAGIC -- Grant SELECT access to the Power BI service principal or user group
# MAGIC -- Replace `power-bi-users` with your actual group name
# MAGIC GRANT SELECT ON TABLE main.default.gold_daily_sales TO `power-bi-users`;

# COMMAND ----------

# DBTITLE 1,Next Steps
# MAGIC %md
# MAGIC ### Connect from Power BI
# MAGIC 
# MAGIC Now that you have an optimized Gold table, you can connect to it from Power BI Desktop:
# MAGIC 
# MAGIC 1.  Use the **Databricks** connector.
# MAGIC 2.  Enter your server hostname and HTTP path.
# MAGIC 3.  Choose **DirectQuery** or **Import** mode.
# MAGIC 4.  Select the `main.default.gold_daily_sales` table.
# MAGIC 
# MAGIC ### Best Practices Review
# MAGIC 
# MAGIC - **✅ Aggregated Data**: The Gold table is pre-aggregated, which will make your Power BI reports much faster.
# MAGIC - **✅ Partitioning**: The table is partitioned by date, which is a common pattern for time-series data and will speed up queries that filter by date.
# MAGIC - **✅ Z-ORDERING**: Z-ORDERING by country will co-locate data for the same country, which will improve the performance of queries that filter by country.
# MAGIC - **✅ Permissions**: Permissions are granted at the table level, ensuring that Power BI only has access to the data it needs.
