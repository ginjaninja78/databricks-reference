# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer: Business Aggregations for Analytics
# MAGIC 
# MAGIC **Purpose**: Create business-ready aggregations from Silver data for BI consumption.
# MAGIC 
# MAGIC **Pattern**: This notebook demonstrates the Gold layer aggregation pattern:
# MAGIC - Read from Silver Delta tables
# MAGIC - Join with dimension tables
# MAGIC - Create pre-aggregated metrics
# MAGIC - Build star schema for BI tools
# MAGIC - Optimize for Power BI DirectQuery
# MAGIC 
# MAGIC **Prerequisites**:
# MAGIC - Silver tables populated with clean data
# MAGIC - Dimension tables available
# MAGIC - Gold catalog and schema created

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

from pyspark.sql.functions import (
    col, sum, count, avg, max, min, round, to_date, 
    year, month, dayofmonth, date_format, current_timestamp
)

# Source configuration
SILVER_CATALOG = "dev"
SILVER_SCHEMA = "silver"
TRANSACTIONS_TABLE = "sales_transactions"

# Target configuration
GOLD_CATALOG = "prod"
GOLD_SCHEMA = "gold"
DAILY_SALES_TABLE = "daily_sales_by_product_country"

SOURCE_FULL_NAME = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.{TRANSACTIONS_TABLE}"
TARGET_FULL_NAME = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.{DAILY_SALES_TABLE}"

print(f"Source: {SOURCE_FULL_NAME}")
print(f"Target: {TARGET_FULL_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Silver Data

# COMMAND ----------

# Read Silver transactions
transactions_df = spark.table(SOURCE_FULL_NAME)

print(f"Silver transactions: {transactions_df.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Business Aggregations
# MAGIC 
# MAGIC Build daily sales summaries aggregated by product and country.
# MAGIC This is a common Gold layer pattern for BI dashboards.

# COMMAND ----------

# Create daily aggregations
daily_sales_df = (
    transactions_df
    # Extract date components
    .withColumn("transaction_date", to_date(col("transaction_timestamp")))
    .withColumn("year", year(col("transaction_date")))
    .withColumn("month", month(col("transaction_date")))
    .withColumn("day", dayofmonth(col("transaction_date")))
    .withColumn("month_name", date_format(col("transaction_date"), "MMMM"))
    .withColumn("day_of_week", date_format(col("transaction_date"), "EEEE"))
    
    # Group by date, product, and country
    .groupBy(
        "transaction_date",
        "year",
        "month",
        "day",
        "month_name",
        "day_of_week",
        "product_id",
        "country"
    )
    
    # Calculate aggregated metrics
    .agg(
        count("transaction_id").alias("total_transactions"),
        sum("quantity").alias("total_quantity_sold"),
        round(sum("total_amount"), 2).alias("total_sales_amount"),
        round(avg("unit_price"), 2).alias("avg_unit_price"),
        round(avg("total_amount"), 2).alias("avg_transaction_value"),
        max("total_amount").alias("max_transaction_value"),
        min("total_amount").alias("min_transaction_value"),
        count(col("customer_id").distinct()).alias("unique_customers")
    )
    
    # Add metadata
    .withColumn("_gold_processed_timestamp", current_timestamp())
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Add Calculated Business Metrics

# COMMAND ----------

# Add derived business metrics
enriched_gold_df = (
    daily_sales_df
    # Calculate average items per transaction
    .withColumn(
        "avg_items_per_transaction",
        round(col("total_quantity_sold") / col("total_transactions"), 2)
    )
    
    # Calculate revenue per customer
    .withColumn(
        "revenue_per_customer",
        round(col("total_sales_amount") / col("unique_customers"), 2)
    )
    
    # Sort for better data organization
    .orderBy("transaction_date", "country", "product_id")
)

# Display sample
display(enriched_gold_df.limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write to Gold Table
# MAGIC 
# MAGIC Use MERGE to handle incremental updates to the Gold table.

# COMMAND ----------

# Create Gold table if it doesn't exist
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {TARGET_FULL_NAME} (
    transaction_date DATE,
    year INT,
    month INT,
    day INT,
    month_name STRING,
    day_of_week STRING,
    product_id STRING,
    country STRING,
    total_transactions BIGINT,
    total_quantity_sold BIGINT,
    total_sales_amount DECIMAL(18,2),
    avg_unit_price DECIMAL(10,2),
    avg_transaction_value DECIMAL(10,2),
    max_transaction_value DECIMAL(10,2),
    min_transaction_value DECIMAL(10,2),
    unique_customers BIGINT,
    avg_items_per_transaction DECIMAL(10,2),
    revenue_per_customer DECIMAL(10,2),
    _gold_processed_timestamp TIMESTAMP
)
USING DELTA
PARTITIONED BY (year, month)
""")

# COMMAND ----------

# Register as temp view for MERGE
enriched_gold_df.createOrReplaceTempView("gold_updates")

# Execute MERGE
spark.sql(f"""
MERGE INTO {TARGET_FULL_NAME} AS target
USING gold_updates AS source
ON target.transaction_date = source.transaction_date
   AND target.product_id = source.product_id
   AND target.country = source.country

WHEN MATCHED THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *
""")

print("Gold table updated successfully")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimize for BI Performance

# COMMAND ----------

# Optimize the Gold table with Z-ORDERING
# This dramatically improves query performance for BI tools
spark.sql(f"""
OPTIMIZE {TARGET_FULL_NAME}
ZORDER BY (transaction_date, country, product_id)
""")

print("Table optimized for BI queries")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Gold Table

# COMMAND ----------

# Display Gold table statistics
gold_df = spark.table(TARGET_FULL_NAME)

print(f"Total rows in Gold table: {gold_df.count():,}")
print(f"Date range: {gold_df.agg(min('transaction_date')).collect()[0][0]} to {gold_df.agg(max('transaction_date')).collect()[0][0]}")
print(f"Countries: {gold_df.select('country').distinct().count()}")
print(f"Products: {gold_df.select('product_id').distinct().count()}")

# Display sample data
display(gold_df.orderBy(col("transaction_date").desc()).limit(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Summary Statistics View

# COMMAND ----------

# Create a summary view for quick insights
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_CATALOG}.{GOLD_SCHEMA}.sales_summary_stats AS
SELECT
    country,
    COUNT(DISTINCT transaction_date) as days_with_sales,
    SUM(total_transactions) as total_transactions,
    SUM(total_sales_amount) as total_revenue,
    AVG(avg_transaction_value) as overall_avg_transaction_value,
    SUM(unique_customers) as total_unique_customers
FROM {TARGET_FULL_NAME}
GROUP BY country
ORDER BY total_revenue DESC
""")

print("Summary statistics view created")

# Display the summary
display(spark.sql(f"SELECT * FROM {GOLD_CATALOG}.{GOLD_SCHEMA}.sales_summary_stats"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Grant Access for BI Tools

# COMMAND ----------

# Grant SELECT permissions to the analytics team
# Uncomment and modify for your environment
# spark.sql(f"GRANT SELECT ON TABLE {TARGET_FULL_NAME} TO `analytics_team`")
# spark.sql(f"GRANT SELECT ON VIEW {GOLD_CATALOG}.{GOLD_SCHEMA}.sales_summary_stats TO `analytics_team`")

print("Permissions configured (modify as needed)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC 
# MAGIC The Gold table is now ready for BI consumption.
# MAGIC 
# MAGIC **Recommended Next Steps**:
# MAGIC 1. **Connect Power BI** to this Gold table using DirectQuery or Import mode
# MAGIC 2. Create **additional Gold tables** for other business domains
# MAGIC 3. Set up **scheduled refreshes** for this aggregation pipeline
# MAGIC 4. Implement **data quality monitoring** on Gold metrics
# MAGIC 5. Create **documentation** for business users on available metrics
# MAGIC 
# MAGIC **Power BI Connection Details**:
# MAGIC - Server: Your Databricks SQL Warehouse hostname
# MAGIC - Database: `prod.gold`
# MAGIC - Table: `daily_sales_by_product_country`
# MAGIC - Recommended Mode: **Import** (for best performance with this aggregated data)
# MAGIC 
# MAGIC **Related Documentation**:
# MAGIC - [Gold Layer Deep Dive](/pillar_i/medallion_architecture/gold_layer.md)
# MAGIC - [Power BI Integration Best Practices](/pillar_iv/bi_and_visualization/power_bi_integration.md)
# MAGIC - [Performance Optimization](/pillar_ii/python_pyspark/advanced_techniques.md)
