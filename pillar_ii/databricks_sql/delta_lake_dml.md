---
title: Delta Lake DML Deep Dive
nav_order: 1
parent: Databricks SQL Deep Dive
grand_parent: Pillar II The Developer's Toolkit
---

# Delta Lake DML: Bringing ACID Transactions to the Data Lake

One of the most revolutionary features of Delta Lake is its support for standard Data Manipulation Language (DML) operations like `UPDATE`, `DELETE`, and `MERGE`. Historically, data lakes were immutable; changing a single record required rewriting entire partitions. Delta Lake, with its transactional log, brings the power and simplicity of database-style operations directly to your files in cloud storage.

This is a game-changer for building modern data platforms, enabling use cases that were previously difficult or impossible to implement efficiently in a data lake.

## `UPDATE`: Modifying Records in Place

The `UPDATE` command allows you to modify rows that match a predicate. This is essential for handling corrections, late-arriving data, or any scenario where records need to be changed after they have been ingested.

### Syntax

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE predicate;
```

### Example: Correcting a Data Entry Error

Imagine we have a `silver.products` table and we discover that the category for a specific product was entered incorrectly.

```sql
-- Before the update
SELECT product_id, product_name, category
FROM silver.products
WHERE product_id = 123;

-- Result:
-- +----------+----------------+----------+
-- | product_id | product_name   | category |
-- +----------+----------------+----------+
-- | 123      | Ultra Widget   | Gadgets  |
-- +----------+----------------+----------+

-- Now, run the UPDATE command
UPDATE silver.products
SET category = 'Electronics'
WHERE product_id = 123;

-- After the update
SELECT product_id, product_name, category
FROM silver.products
WHERE product_id = 123;

-- Result:
-- +----------+----------------+----------+
-- | product_id | product_name   | category    |
-- +----------+----------------+----------+
-- | 123      | Ultra Widget   | Electronics |
-- +----------+----------------+----------+
```

Behind the scenes, Delta Lake identifies the data file(s) containing the record for `product_id = 123`, rewrites those files with the updated data, and commits the change to the transaction log as a single, atomic operation.

## `DELETE`: Removing Records

The `DELETE` command allows you to remove rows that match a predicate. This is critical for handling data privacy requirements (like GDPR/CCPA "right to be forgotten" requests) and for removing erroneous data.

### Syntax

```sql
DELETE FROM table_name
WHERE predicate;
```

### Example: Handling a GDPR Deletion Request

A customer with `customer_id = 456` has requested that their data be deleted from the `silver.customers` table.

```sql
-- Run the DELETE command
DELETE FROM silver.customers
WHERE customer_id = 456;
```

Just like `UPDATE`, Delta Lake performs this operation transactionally, ensuring that the record is permanently and safely removed.

## `MERGE`: The Ultimate Upsert and SCD Tool

The `MERGE` command is the most powerful DML operation in Delta Lake. It allows you to perform "upserts"—inserting new records and updating existing ones—in a single, atomic statement. This is the backbone of most modern ELT pipelines and is essential for handling Slowly Changing Dimensions (SCDs).

### Syntax

```sql
MERGE INTO target_table AS target
USING source_table AS source
ON target.key = source.key
WHEN MATCHED THEN
  UPDATE SET target.col1 = source.col1, ...
WHEN NOT MATCHED THEN
  INSERT (col1, col2, ...) VALUES (source.col1, source.col2, ...);
```

### Example: A Classic Upsert Pattern

We have a stream of new order data arriving in a temporary table, `bronze.new_orders_staging`. We want to merge this data into our main `silver.orders` table.

-   If an order from the staging table already exists in the silver table (matched on `order_id`), we update the record.
-   If it's a new order, we insert it.

```sql
MERGE INTO silver.orders AS target
USING bronze.new_orders_staging AS source
ON target.order_id = source.order_id

-- If the order already exists, update its status and modification time
WHEN MATCHED THEN
  UPDATE SET
    target.status = source.status,
    target.last_modified_timestamp = current_timestamp()

-- If it's a new order, insert the full record
WHEN NOT MATCHED THEN
  INSERT (order_id, customer_id, product_id, quantity, total_price, order_date, status, last_modified_timestamp)
  VALUES (source.order_id, source.customer_id, source.product_id, source.quantity, source.total_price, source.order_date, source.status, current_timestamp());
```

This single, atomic statement prevents race conditions and data duplication, ensuring that your target table is always a consistent and accurate reflection of the source data.

### Advanced `MERGE`: Type 2 Slowly Changing Dimensions

`MERGE` can also have multiple `WHEN MATCHED` and `WHEN NOT MATCHED` clauses, allowing for very sophisticated logic. A classic example is building a Type 2 SCD table, which tracks the history of changes.

```sql
-- Target table: gold.customers_scd2
-- Columns: customer_id, address, is_current, effective_date, end_date

MERGE INTO gold.customers_scd2 AS target
USING silver.customer_updates AS source
ON target.customer_id = source.customer_id

-- Case 1: The customer exists and their address has changed, and we are looking at the current record.
WHEN MATCHED AND target.is_current = true AND target.address <> source.address THEN
  -- Expire the old record
  UPDATE SET target.is_current = false, target.end_date = current_date()

-- After expiring the old one, we need to insert the new one. This requires a second pass or a more complex INSERT statement.
-- A common pattern is to insert all new/changed records first, then merge to expire.

-- A more complete pattern often involves a separate INSERT statement after the MERGE:
INSERT INTO gold.customers_scd2
SELECT customer_id, address, true AS is_current, current_date() AS effective_date, NULL AS end_date
FROM silver.customer_updates src
WHERE NOT EXISTS (
  SELECT 1 FROM gold.customers_scd2 tgt
  WHERE tgt.customer_id = src.customer_id AND tgt.address = src.address
);
```

By providing these powerful, transactional DML capabilities, Delta Lake bridges the gap between traditional data warehouses and data lakes, allowing you to build reliable, enterprise-grade data platforms with the simplicity and familiarity of SQL.
