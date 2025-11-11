# Databricks Quick Reference Cheat Sheet

A rapid-fire reference for common Databricks operations. For detailed explanations, see the full documentation in each pillar.

## 🔥 Most Common Operations

### Reading Data

```python
# Read CSV
df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True)

# Read JSON
df = spark.read.json("path/to/file.json")

# Read Parquet
df = spark.read.parquet("path/to/file.parquet")

# Read Delta Table
df = spark.read.format("delta").load("path/to/delta/table")
df = spark.table("catalog.schema.table_name")

# Read with Auto Loader (streaming)
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load("path/to/files/"))
```

### Writing Data

```python
# Write CSV
df.write.csv("path/to/output", header=True, mode="overwrite")

# Write Parquet
df.write.parquet("path/to/output", mode="overwrite")

# Write Delta Table
df.write.format("delta").mode("overwrite").save("path/to/delta/table")
df.write.mode("overwrite").saveAsTable("catalog.schema.table_name")

# Append to Delta Table
df.write.format("delta").mode("append").save("path/to/delta/table")

# Write stream to Delta
(df.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "path/to/checkpoint")
    .toTable("catalog.schema.table_name"))
```

### Delta Lake Operations

```sql
-- MERGE (Upsert)
MERGE INTO target_table AS t
USING source_table AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Time Travel
SELECT * FROM table_name VERSION AS OF 10;
SELECT * FROM table_name TIMESTAMP AS OF '2024-01-15';

-- Optimize
OPTIMIZE table_name;
OPTIMIZE table_name ZORDER BY (column1, column2);

-- Vacuum (remove old files)
VACUUM table_name RETAIN 168 HOURS;

-- Update
UPDATE table_name SET column = value WHERE condition;

-- Delete
DELETE FROM table_name WHERE condition;
```

### Common Transformations

```python
from pyspark.sql.functions import col, when, lit, concat, upper, lower, trim

# Select columns
df.select("col1", "col2")

# Filter rows
df.filter(col("age") > 25)
df.where(col("status") == "active")

# Add/modify columns
df.withColumn("new_col", col("old_col") * 2)
df.withColumn("full_name", concat(col("first_name"), lit(" "), col("last_name")))

# Rename columns
df.withColumnRenamed("old_name", "new_name")

# Drop columns
df.drop("col1", "col2")

# Conditional logic
df.withColumn("category", 
    when(col("amount") > 1000, "High")
    .when(col("amount") > 100, "Medium")
    .otherwise("Low"))
```

### Aggregations

```python
from pyspark.sql.functions import sum, avg, count, max, min

# Group by and aggregate
df.groupBy("category").agg(
    count("*").alias("total_count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount")
)

# Multiple aggregations
df.groupBy("country", "product").agg(
    sum("sales").alias("total_sales"),
    count("transaction_id").alias("num_transactions")
)
```

### Joins

```python
# Inner join
df1.join(df2, df1.id == df2.id, "inner")

# Left join
df1.join(df2, df1.id == df2.id, "left")

# Right join
df1.join(df2, df1.id == df2.id, "right")

# Full outer join
df1.join(df2, df1.id == df2.id, "outer")

# Anti join (rows in df1 not in df2)
df1.join(df2, df1.id == df2.id, "left_anti")
```

### Window Functions

```python
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead

# Define window
window_spec = Window.partitionBy("category").orderBy(col("amount").desc())

# Row number
df.withColumn("row_num", row_number().over(window_spec))

# Rank
df.withColumn("rank", rank().over(window_spec))

# Lag/Lead
df.withColumn("prev_amount", lag("amount", 1).over(window_spec))
df.withColumn("next_amount", lead("amount", 1).over(window_spec))
```

## 🛠️ dbutils Commands

```python
# File system operations
dbutils.fs.ls("path/")
dbutils.fs.mkdirs("path/")
dbutils.fs.rm("path/", recurse=True)
dbutils.fs.cp("source/", "dest/", recurse=True)

# Secrets
secret_value = dbutils.secrets.get(scope="my-scope", key="my-key")

# Widgets (notebook parameters)
dbutils.widgets.text("param_name", "default_value")
param_value = dbutils.widgets.get("param_name")

# Notebook workflow
dbutils.notebook.run("path/to/notebook", timeout_seconds=600, arguments={"key": "value"})
dbutils.notebook.exit("return_value")
```

## 📊 SQL Quick Reference

```sql
-- Create Delta table
CREATE TABLE catalog.schema.table_name (
    id STRING,
    name STRING,
    amount DECIMAL(10,2)
)
USING DELTA
PARTITIONED BY (date);

-- Insert data
INSERT INTO table_name VALUES (1, 'Alice', 100.00);

-- Copy table
CREATE TABLE new_table AS SELECT * FROM old_table;

-- Clone table
CREATE TABLE backup_table DEEP CLONE source_table;

-- Describe table
DESCRIBE EXTENDED table_name;

-- Show history
DESCRIBE HISTORY table_name;

-- Restore table
RESTORE TABLE table_name TO VERSION AS OF 5;
```

## 🎯 Performance Tips

```python
# Cache frequently used DataFrames
df.cache()
df.persist()

# Repartition for better parallelism
df.repartition(200)

# Coalesce to reduce partitions
df.coalesce(10)

# Broadcast small tables in joins
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), "key")

# Use partitioning for large tables
df.write.partitionBy("date", "country").format("delta").save("path/")
```

## 🔐 Unity Catalog

```sql
-- Grant permissions
GRANT SELECT ON TABLE catalog.schema.table TO `user@example.com`;
GRANT ALL PRIVILEGES ON SCHEMA catalog.schema TO `data-engineers`;

-- Revoke permissions
REVOKE SELECT ON TABLE catalog.schema.table FROM `user@example.com`;

-- Show grants
SHOW GRANTS ON TABLE catalog.schema.table;

-- Create catalog
CREATE CATALOG IF NOT EXISTS my_catalog;

-- Create schema
CREATE SCHEMA IF NOT EXISTS my_catalog.my_schema;
```

## 🚀 Auto Loader

```python
# Basic Auto Loader
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "path/to/schema")
    .load("path/to/source/"))

# With schema evolution
df = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", "path/to/schema")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .load("path/to/source/"))
```

## 📈 Monitoring & Debugging

```python
# Show execution plan
df.explain()
df.explain(extended=True)

# Count records
df.count()

# Show sample data
df.show(10)
df.display()  # In Databricks notebooks

# Print schema
df.printSchema()

# Get column statistics
df.describe().show()

# Check for nulls
from pyspark.sql.functions import col, sum as spark_sum, when
df.select([spark_sum(when(col(c).isNull(), 1).otherwise(0)).alias(c) for c in df.columns]).show()
```

## 🔗 Quick Links

- **Full Documentation**: [GitHub Pages](https://ginjaninja78.github.io/databricks-reference/)
- **Sample Notebooks**: [/sample_notebooks/](/sample_notebooks/)
- **Code Examples**: [/sample_code/](/sample_code/)
- **The LibrAIrian**: [.github/LibrAIrian.agent.md](.github/LibrAIrian.agent.md)

---

**Need more details?** Dive into the full documentation in the four pillars or ask The LibrAIrian!
