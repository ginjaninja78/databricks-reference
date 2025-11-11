---
title: Advanced SQL Functions
nav_order: 2
parent: Databricks SQL Deep Dive
grand_parent: Pillar II The Developer's Toolkit
---

# Advanced SQL Functions: A Treasure Trove for Data Manipulation

Databricks SQL offers a vast library of functions that go far beyond the standard SQL-92 set. These functions are designed to tackle the complex data types and analytical challenges common in modern data workloads. Mastering them allows you to perform sophisticated transformations and analyses directly within your SQL queries, often eliminating the need for more complex PySpark code.

This guide explores some of the most powerful categories of advanced functions.

## 1. Working with Semi-Structured Data (JSON)

It is extremely common to ingest data that contains JSON. Databricks SQL provides a powerful set of functions to parse, traverse, and construct JSON directly in your queries.

### Example: Parsing JSON from a String Column

Imagine a table `bronze.iot_events` with a string column `payload` containing JSON data.

```sql
-- Sample payload: {"device_id": "d-123", "timestamp": 1678886400, "readings": {"temperature": 25.5, "humidity": 60.1}}

SELECT
  -- Use the colon syntax to extract values. The type is inferred.
  payload:device_id::string AS device_id,
  payload:timestamp::timestamp AS event_timestamp,
  payload:readings.temperature::double AS temperature,
  payload:readings.humidity::double AS humidity
FROM bronze.iot_events;
```

### Key JSON Functions

| Function | Description |
|---|---|
| `get_json_object(json_str, path)` | Extracts a JSON object from a JSON string based on a JSON path expression. |
| `from_json(json_str, schema)` | Parses a JSON string column into a struct, which you can then access with dot notation. This is more performant for extracting multiple fields. |
| `to_json(struct)` | Converts a struct column into a JSON string. |
| `json_object_keys(json_str)` | Returns all the keys of the top-level JSON object as an array. |
| `explode(json_array)` | A table-valued generator function that transforms an array of JSON objects into multiple rows. |

## 2. Higher-Order Functions: Operating on Arrays

Higher-order functions take lambda functions as arguments, allowing you to perform complex operations on array data directly in SQL. This is incredibly powerful and avoids the need for complex UDFs.

### Example: Transforming an Array with `TRANSFORM`

Suppose you have a table with an array of product IDs and you want to prepend a prefix to each ID.

```sql
-- Table: silver.orders
-- Column: product_ids (ARRAY<INT>)

SELECT
  order_id,
  product_ids,
  -- The TRANSFORM function takes an array and a lambda function.
  -- The lambda function (x -> ...) is applied to each element of the array.
  TRANSFORM(product_ids, x -> 'PROD-' || x) AS prefixed_product_ids
FROM silver.orders;
```

### Key Higher-Order Functions

| Function | Description |
|---|---|
| `TRANSFORM(array, func)` | Applies a function to each element in an array and returns a new array of the results. |
| `FILTER(array, func)` | Returns a new array containing only the elements of the input array for which the boolean function is true. |
| `EXISTS(array, func)` | Returns true if the boolean function is true for at least one element in the array. |
| `REDUCE(array, start, merge, finish)` | Aggregates the elements of an array into a single value. |

## 3. Window Functions: Beyond `GROUP BY`

Window functions perform a calculation across a set of table rows that are somehow related to the current row. Unlike a `GROUP BY` aggregation, a window function does not collapse the rows; it returns a value for each row based on the "window" of related rows.

### Example: Calculating a Running Total

We want to calculate the running total of sales for each customer over time.

```sql
SELECT
  customer_id,
  order_date,
  total_price,
  -- The OVER clause defines the window.
  -- PARTITION BY splits the data into groups (like GROUP BY).
  -- ORDER BY sorts the data within each partition.
  -- The SUM() is then applied cumulatively over the sorted rows.
  SUM(total_price) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM silver.orders;
```

### Key Window Functions

| Function | Description |
|---|---|
| `ROW_NUMBER()` | Assigns a unique number to each row within a partition, starting from 1. |
| `RANK()` / `DENSE_RANK()` | Assigns a rank to each row based on the ordering within a partition. `RANK` leaves gaps for ties, `DENSE_RANK` does not. |
| `LAG(col, n)` / `LEAD(col, n)` | Accesses the value of a column from a preceding (`LAG`) or succeeding (`LEAD`) row. |
| `NTILE(n)` | Divides the rows in a partition into `n` ranked groups (e.g., quartiles, deciles). |

## 4. Other Powerful Functions

-   **`PIVOT`**: Transforms rows into columns, summarizing data and making it easier to read.
-   **`APPROX_COUNT_DISTINCT` / `APPROX_PERCENTILE`**: Approximate aggregation functions that provide extremely fast results on massive datasets with a very small, configurable error margin. Essential for interactive dashboards.
-   **`HLL_SKETCH_AGG` / `HLL_UNION`**: Functions for using HyperLogLog sketches to perform high-performance, approximate distinct counts on massive streams of data.

By integrating these advanced functions into your SQL toolkit, you can build more efficient, more elegant, and more powerful data pipelines on Databricks, pushing the boundaries of what is possible with pure SQL.
