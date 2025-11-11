---
title: The Grand Tour of DataFrame Transformations
nav_order: 2
parent: Mastering Python & PySpark
grand_parent: Pillar II The Developer's Toolkit
---

# The Grand Tour of DataFrame Transformations

This is the heart of PySpark programming: manipulating DataFrames. The DataFrame API provides a rich, expressive, and powerful set of functions to transform your data. Because transformations are lazy and build upon each other, you can chain them together to create complex data pipelines that are both readable and highly performant.

This guide provides an exhaustive tour of the most critical transformations, complete with enterprise-grade examples. We'll use a sample DataFrame of sales data throughout.

### Our Sample Data

Let's assume we have the following DataFrame, `sales_df`, loaded for all our examples.

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql import Row
import datetime

data = [
    Row(order_id=101, customer_id=1, product_id=10, quantity=2, unit_price=12.50, order_date=datetime.datetime(2024, 10, 1, 10, 30, 0), country="USA"),
    Row(order_id=102, customer_id=2, product_id=20, quantity=1, unit_price=25.00, order_date=datetime.datetime(2024, 10, 1, 11, 0, 0), country="USA"),
    Row(order_id=103, customer_id=1, product_id=30, quantity=5, unit_price=2.75, order_date=datetime.datetime(2024, 10, 2, 14, 0, 0), country="Canada"),
    Row(order_id=104, customer_id=3, product_id=10, quantity=10, unit_price=12.00, order_date=datetime.datetime(2024, 10, 2, 15, 45, 0), country="Mexico"),
    Row(order_id=105, customer_id=2, product_id=20, quantity=2, unit_price=24.50, order_date=datetime.datetime(2024, 10, 3, 9, 15, 0), country="USA"),
    Row(order_id=106, customer_id=1, product_id=40, quantity=1, unit_price=150.00, order_date=datetime.datetime(2024, 10, 4, 18, 0, 0), country="Canada"),
    Row(order_id=107, customer_id=4, product_id=10, quantity=3, unit_price=12.50, order_date=datetime.datetime(2024, 10, 4, 18, 30, 0), country="USA"),
    Row(order_id=108, customer_id=3, product_id=20, quantity=4, unit_price=24.00, order_date=datetime.datetime(2024, 10, 5, 12, 0, 0), country="Mexico"),
]

schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("order_date", TimestampType(), True),
    StructField("country", StringType(), True),
])

sales_df = spark.createDataFrame(data, schema)
```

## 1. Selecting and Accessing Columns: `select()` and `col()`

The most basic transformation is selecting the columns you need. The `select()` method creates a new DataFrame with only the specified columns.

```python
from pyspark.sql.functions import col

# Select specific columns
product_and_country_df = sales_df.select("product_id", "country")

# You can also use the col() function for more clarity and to perform operations
product_and_country_df = sales_df.select(
    col("product_id"),
    col("country")
)

product_and_country_df.show()
```

## 2. Creating New Columns: `withColumn()`

This is one of the most frequently used transformations. `withColumn()` adds a new column to the DataFrame or replaces an existing one. It takes two arguments: the name of the new column and the expression that defines its value.

```python
from pyspark.sql.functions import round

# Create a new column 'total_price' by multiplying quantity and unit_price
sales_with_total_df = sales_df.withColumn(
    "total_price",
    round(col("quantity") * col("unit_price"), 2)
)

sales_with_total_df.show()
```

## 3. Filtering Rows: `filter()` or `where()`

To select a subset of rows based on a condition, use `filter()` or its alias `where()`. You can build complex conditions using standard logical operators (`&` for AND, `|` for OR, `~` for NOT).

```python
# Filter for all sales in the USA where the quantity is greater than 1
usa_large_orders_df = sales_df.filter(
    (col("country") == "USA") & (col("quantity") > 1)
)

usa_large_orders_df.show()

# Using where() with a SQL-like expression string
canada_orders_df = sales_df.where("country = 'Canada'")

canada_orders_df.show()
```

## 4. Aggregating Data: `groupBy()` and `agg()`

Aggregations are at the core of data analysis. The `groupBy()` method groups the DataFrame by one or more columns, and the `agg()` method is then used to perform aggregations on those groups.

```python
from pyspark.sql.functions import sum, avg, count, max

# Calculate total sales, average quantity, and number of orders per country
country_sales_summary_df = (
    sales_df
    .withColumn("total_price", col("quantity") * col("unit_price"))
    .groupBy("country")
    .agg(
        round(sum("total_price"), 2).alias("total_sales"),
        round(avg("quantity"), 2).alias("avg_quantity"),
        count("order_id").alias("number_of_orders")
    )
)

country_sales_summary_df.show()
```

## 5. Sorting Data: `orderBy()` or `sort()`

To order the rows in your DataFrame, use `orderBy()` or `sort()`. You can specify ascending or descending order.

```python
from pyspark.sql.functions import desc

# Sort the country summary by total sales in descending order
sorted_summary_df = country_sales_summary_df.orderBy(desc("total_sales"))
# or country_sales_summary_df.orderBy(col("total_sales").desc())

sorted_summary_df.show()
```

## 6. Joining DataFrames: `join()`

Joining is a fundamental operation for combining data from different sources. Spark supports all standard join types (`inner`, `left`, `right`, `full_outer`, `left_semi`, `left_anti`).

Let's create a `customers_df` to join with our sales data.

```python
customer_data = [
    Row(customer_id=1, customer_name="Alice"),
    Row(customer_id=2, customer_name="Bob"),
    Row(customer_id=3, customer_name="Charlie"),
    Row(customer_id=5, customer_name="Eve") # A customer with no orders
]
customer_schema = StructType([
    StructField("customer_id", IntegerType(), True),
    StructField("customer_name", StringType(), True)
])
customers_df = spark.createDataFrame(customer_data, customer_schema)

# Perform an inner join to add customer names to sales data
sales_with_customers_df = sales_df.join(
    customers_df,
    sales_df.customer_id == customers_df.customer_id, # The join condition
    "inner" # The join type
)

# Drop the duplicate customer_id column
sales_with_customers_df = sales_with_customers_df.drop(customers_df.customer_id)

sales_with_customers_df.show()

# Perform a left outer join to see all sales, even if the customer is unknown
left_join_df = sales_df.join(customers_df, on="customer_id", how="left")
left_join_df.show()
```

## 7. Other Essential Transformations

-   **`withColumnRenamed(existing_name, new_name)`**: Renames a column.
-   **`drop(*cols)`**: Removes one or more columns.
-   **`distinct()`**: Returns a new DataFrame with only the unique rows.
-   **`union(other_df)`**: Combines two DataFrames with the same schema (like SQL `UNION ALL`).
-   **`limit(n)`**: Returns a new DataFrame with only the first `n` rows.

### Example Chain

Let's chain many of these transformations together to answer a complex question: "What are the top 2 products by total sales amount in the USA?"

```python
from pyspark.sql.functions import lit

# Assume we have a products DataFrame
product_data = [Row(product_id=10, product_name="Widget A"), Row(product_id=20, product_name="Widget B")]
product_schema = StructType([StructField("product_id", IntegerType(), True), StructField("product_name", StringType(), True)])
products_df = spark.createDataFrame(product_data, product_schema)


top_products_usa_df = (
    sales_df
    # 1. Filter for USA
    .filter(col("country") == "USA")
    # 2. Calculate total price for each order
    .withColumn("total_price", col("quantity") * col("unit_price"))
    # 3. Group by product
    .groupBy("product_id")
    # 4. Aggregate to get total sales per product
    .agg(sum("total_price").alias("total_sales"))
    # 5. Join with products table to get product names
    .join(products_df, on="product_id", how="inner")
    # 6. Order by total sales to find the top sellers
    .orderBy(desc("total_sales"))
    # 7. Select and rename columns for the final report
    .select(
        col("product_name"),
        round(col("total_sales"), 2).alias("total_sales_usd")
    )
    # 8. Take only the top 2
    .limit(2)
)

top_products_usa_df.show()
```

This example demonstrates the power of PySpark's fluent, chainable API. Each step is a logical, immutable transformation that builds upon the last, resulting in a query plan that Spark's Catalyst Optimizer can turn into highly efficient distributed code.
