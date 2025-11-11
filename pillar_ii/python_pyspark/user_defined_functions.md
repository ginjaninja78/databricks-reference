---
title: User-Defined Functions (UDFs)
nav_order: 3
parent: Mastering Python & PySpark
grand_parent: Pillar II The Developer's Toolkit
---

# User-Defined Functions (UDFs): Extending Spark with Python

While PySpark's built-in functions are extensive and highly optimized, you will inevitably encounter situations where you need to apply a complex business rule or use a third-party library that isn't available in Spark's native API. This is where **User-Defined Functions (UDFs)** come in.

A UDF allows you to define a custom function in Python, register it with Spark, and then apply it to your DataFrames as if it were a built-in function. However, using UDFs comes with a significant performance cost, and understanding the different types of UDFs is critical to using them effectively.

**Golden Rule**: Always try to solve your problem using built-in Spark functions first. Only resort to a UDF when it is absolutely necessary. Native functions will always be faster.

## 1. Standard UDFs: The Row-at-a-Time Black Box

A standard UDF operates on a row-by-row basis. For each row in your DataFrame, Spark serializes the required column data from the JVM, sends it to a Python worker process, executes your Python function, and then sends the result back to the JVM. This constant serialization and context switching is what makes standard UDFs slow.

### When to Use a Standard UDF

-   When your logic is complex and cannot be expressed using Spark SQL functions.
-   When you need to use an external Python library (e.g., a specialized financial modeling library).

### Example: A Standard UDF

Let's create a UDF to categorize a product's price into "Low", "Medium", or "High".

```python
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

# 1. Define your Python function
def price_category(price):
    if price < 15.0:
        return "Low"
    elif 15.0 <= price < 50.0:
        return "Medium"
    else:
        return "High"

# 2. Register the function as a UDF, specifying its return type
# This is a critical step for Spark's optimizer.
price_category_udf = udf(price_category, StringType())

# 3. Apply the UDF to your DataFrame
# We'll use the sales_df from the previous chapter
sales_with_category_df = sales_df.withColumn(
    "price_category",
    price_category_udf(col("unit_price"))
)

sales_with_category_df.select("unit_price", "price_category").show()
```

**Performance Warning**: Because the Python function `price_category` is a "black box" to Spark's Catalyst Optimizer, Spark cannot optimize the execution. It must execute the function for every single row, which can be incredibly slow on large datasets.

## 2. Pandas UDFs (Vectorized UDFs): The High-Performance Alternative

To address the performance limitations of standard UDFs, Spark introduced **Pandas UDFs**, also known as Vectorized UDFs. Instead of operating row-by-row, a Pandas UDF operates on a `pandas.Series` or `pandas.DataFrame` at a time.

Spark transfers a batch of rows to the Python worker as a `pandas.Series`, your function processes the entire series at once using optimized pandas/NumPy code, and then the resulting `pandas.Series` is sent back to Spark. This dramatically reduces the overhead of serialization and context switching.

There are two main types of Pandas UDFs: Series to Series and Iterator of Series to Iterator of Series.

### Series to Series Pandas UDF

This is the most common type. It takes a `pandas.Series` as input and must return a `pandas.Series` of the same length.

### Example: A Pandas UDF

Let's rewrite our price categorization function as a Pandas UDF.

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd

# 1. Define your Python function to work on a pandas.Series
# Use the @pandas_udf decorator to register it.
@pandas_udf(StringType()) # Return type is specified in the decorator
def price_category_pandas(price_series: pd.Series) -> pd.Series:
    # Use efficient pandas vectorized operations
    return pd.cut(
        price_series,
        bins=[0, 15, 50, float('inf')],
        labels=['Low', 'Medium', 'High'],
        right=False
    )

# 2. Apply the UDF just like a regular function
sales_with_category_pandas_df = sales_df.withColumn(
    "price_category",
    price_category_pandas(col("unit_price"))
)

sales_with_category_pandas_df.select("unit_price", "price_category").show()
```

This version will be **orders of magnitude faster** than the standard UDF on large datasets because it leverages the efficiency of pandas and minimizes the overhead between the JVM and Python.

## 3. Pandas Function APIs (Grouped Map, Map, Co-grouped Map)

For even more complex operations, like performing a transformation on each group of a `groupBy`, you can use the Pandas Function APIs. The most common is `applyInPandas` (Grouped Map).

This function splits the Spark DataFrame into groups, converts each group to a `pandas.DataFrame`, applies a Python function to each `pandas.DataFrame`, and then combines the results back into a Spark DataFrame.

### Example: `applyInPandas` for Grouped Operations

Let's say we want to normalize the `total_price` for each country to be between 0 and 1.

```python
from pyspark.sql.functions import col
import pandas as pd

# We need a DataFrame with total_price
sales_with_total_df = sales_df.withColumn("total_price", col("quantity") * col("unit_price"))

# Define the schema of the output DataFrame
result_schema = StructType([
    StructField('country', StringType()),
    StructField('order_id', IntegerType()),
    StructField('total_price', DoubleType()),
    StructField('normalized_price', DoubleType())
])

# Define a Python function that takes a pandas.DataFrame and returns one
def normalize_prices(pdf: pd.DataFrame) -> pd.DataFrame:
    max_price = pdf['total_price'].max()
    min_price = pdf['total_price'].min()
    
    # Avoid division by zero if all prices in a group are the same
    if max_price == min_price:
        pdf['normalized_price'] = 0.5
    else:
        pdf['normalized_price'] = (pdf['total_price'] - min_price) / (max_price - min_price)
    
    return pdf[['country', 'order_id', 'total_price', 'normalized_price']]

# Group by country and apply the function
normalized_sales_df = (
    sales_with_total_df
    .groupBy("country")
    .applyInPandas(normalize_prices, schema=result_schema)
)

normalized_sales_df.show()
```

### UDF Best Practices: Summary

| UDF Type | Granularity | Performance | Use Case |
|---|---|---|---|
| **Built-in Function** | N/A | **Highest** | Always the first choice. Use whenever possible. |
| **Pandas UDF** | Vectorized (Series) | **High** | When you need custom logic that can be expressed with vectorized pandas/NumPy operations. The best choice for most custom column-wise operations. |
| **Pandas Function API** | Grouped (DataFrame) | **Medium-High** | For complex grouped operations that can't be done with Spark's `groupBy().agg()`. (e.g., group-wise normalization, running a regression per group). |
| **Standard UDF** | Row-at-a-time | **Very Low** | **Last resort**. Use only when the logic is complex, cannot be vectorized, and performance is not the primary concern (e.g., on very small datasets or during initial exploration). |

By choosing the right type of UDF for your task, you can extend Spark's capabilities to solve virtually any data problem without sacrificing the performance that makes Spark a powerful tool for big data processing.
