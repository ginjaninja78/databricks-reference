-- ============================================================================
-- Delta Lake Common Operations Reference
-- ============================================================================
-- This script demonstrates essential Delta Lake operations for managing
-- tables in the Databricks Lakehouse.
--
-- Topics covered:
-- 1. Table creation and management
-- 2. MERGE (upsert) operations
-- 3. Time travel and versioning
-- 4. Optimization and maintenance
-- 5. Schema evolution
-- ============================================================================

-- ============================================================================
-- 1. TABLE CREATION AND MANAGEMENT
-- ============================================================================

-- Create a managed Delta table with partitioning
CREATE TABLE IF NOT EXISTS dev.silver.customer_orders (
    order_id STRING,
    customer_id STRING,
    order_date DATE,
    total_amount DECIMAL(10,2),
    status STRING,
    country STRING,
    _ingestion_timestamp TIMESTAMP
)
USING DELTA
PARTITIONED BY (country)
COMMENT 'Silver layer customer orders table'
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
);

-- Create an external Delta table (data stored in specific location)
CREATE TABLE IF NOT EXISTS dev.bronze.raw_events (
    event_id STRING,
    event_type STRING,
    event_timestamp TIMESTAMP,
    payload STRING
)
USING DELTA
LOCATION '/mnt/datalake/bronze/events/'
COMMENT 'Bronze layer raw events';

-- View table properties
DESCRIBE EXTENDED dev.silver.customer_orders;

-- Show table history
DESCRIBE HISTORY dev.silver.customer_orders;

-- ============================================================================
-- 2. MERGE (UPSERT) OPERATIONS
-- ============================================================================

-- Basic MERGE: Insert new records and update existing ones
MERGE INTO dev.silver.customer_orders AS target
USING dev.bronze.new_orders AS source
ON target.order_id = source.order_id

WHEN MATCHED THEN
  UPDATE SET
    target.status = source.status,
    target.total_amount = source.total_amount,
    target._ingestion_timestamp = current_timestamp()

WHEN NOT MATCHED THEN
  INSERT (
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    country,
    _ingestion_timestamp
  )
  VALUES (
    source.order_id,
    source.customer_id,
    source.order_date,
    source.total_amount,
    source.status,
    source.country,
    current_timestamp()
  );

-- Advanced MERGE: Conditional updates and deletes
MERGE INTO dev.silver.customer_orders AS target
USING dev.bronze.order_updates AS source
ON target.order_id = source.order_id

-- Update only if the source data is newer
WHEN MATCHED AND source.last_modified > target._ingestion_timestamp THEN
  UPDATE SET *

-- Delete cancelled orders
WHEN MATCHED AND source.status = 'CANCELLED' THEN
  DELETE

-- Insert new orders
WHEN NOT MATCHED THEN
  INSERT *;

-- MERGE with multiple conditions
MERGE INTO dev.silver.customer_orders AS target
USING (
    SELECT 
        order_id,
        customer_id,
        order_date,
        total_amount,
        status,
        country
    FROM dev.bronze.new_orders
    WHERE order_date >= current_date() - INTERVAL 7 DAYS
) AS source
ON target.order_id = source.order_id

WHEN MATCHED AND target.status != 'COMPLETED' THEN
  UPDATE SET
    target.status = source.status,
    target.total_amount = source.total_amount

WHEN NOT MATCHED THEN
  INSERT *;

-- ============================================================================
-- 3. TIME TRAVEL AND VERSIONING
-- ============================================================================

-- Query a table as of a specific version
SELECT * FROM dev.silver.customer_orders VERSION AS OF 5;

-- Query a table as of a specific timestamp
SELECT * FROM dev.silver.customer_orders TIMESTAMP AS OF '2024-01-15 10:00:00';

-- Compare current data with a previous version
SELECT 
    current.order_id,
    current.status AS current_status,
    previous.status AS previous_status
FROM dev.silver.customer_orders AS current
LEFT JOIN dev.silver.customer_orders VERSION AS OF 5 AS previous
    ON current.order_id = previous.order_id
WHERE current.status != previous.status;

-- Restore a table to a previous version
RESTORE TABLE dev.silver.customer_orders TO VERSION AS OF 10;

-- Restore to a specific timestamp
RESTORE TABLE dev.silver.customer_orders TO TIMESTAMP AS OF '2024-01-15 10:00:00';

-- ============================================================================
-- 4. OPTIMIZATION AND MAINTENANCE
-- ============================================================================

-- Optimize table (compacts small files)
OPTIMIZE dev.silver.customer_orders;

-- Optimize with Z-ORDERING for better query performance
-- Z-ORDER on columns frequently used in WHERE clauses
OPTIMIZE dev.silver.customer_orders
ZORDER BY (order_date, customer_id);

-- Optimize specific partition
OPTIMIZE dev.silver.customer_orders
WHERE country = 'USA';

-- Vacuum old files (remove files older than retention period)
-- Default retention is 7 days
VACUUM dev.silver.customer_orders;

-- Vacuum with custom retention (30 days)
VACUUM dev.silver.customer_orders RETAIN 720 HOURS;

-- Dry run to see what would be deleted
VACUUM dev.silver.customer_orders DRY RUN;

-- Analyze table to collect statistics for query optimization
ANALYZE TABLE dev.silver.customer_orders COMPUTE STATISTICS;

-- Analyze specific columns
ANALYZE TABLE dev.silver.customer_orders COMPUTE STATISTICS FOR COLUMNS order_date, customer_id;

-- ============================================================================
-- 5. SCHEMA EVOLUTION
-- ============================================================================

-- Add a new column
ALTER TABLE dev.silver.customer_orders 
ADD COLUMN discount_amount DECIMAL(10,2) COMMENT 'Discount applied to order';

-- Rename a column
ALTER TABLE dev.silver.customer_orders 
RENAME COLUMN total_amount TO order_total;

-- Change column comment
ALTER TABLE dev.silver.customer_orders 
ALTER COLUMN status COMMENT 'Order status: PENDING, PROCESSING, COMPLETED, CANCELLED';

-- Drop a column (requires rewriting the table)
ALTER TABLE dev.silver.customer_orders 
DROP COLUMN discount_amount;

-- Enable schema evolution for MERGE operations
SET spark.databricks.delta.schema.autoMerge.enabled = true;

-- ============================================================================
-- 6. DATA MANIPULATION
-- ============================================================================

-- UPDATE records
UPDATE dev.silver.customer_orders
SET status = 'COMPLETED'
WHERE order_date < current_date() - INTERVAL 30 DAYS
  AND status = 'PROCESSING';

-- DELETE records
DELETE FROM dev.silver.customer_orders
WHERE status = 'CANCELLED'
  AND order_date < current_date() - INTERVAL 90 DAYS;

-- Conditional DELETE
DELETE FROM dev.silver.customer_orders
WHERE order_id IN (
    SELECT order_id 
    FROM dev.silver.fraudulent_orders
);

-- ============================================================================
-- 7. CLONING TABLES
-- ============================================================================

-- Deep clone (copies data and metadata)
CREATE TABLE dev.silver.customer_orders_backup
DEEP CLONE dev.silver.customer_orders;

-- Shallow clone (copies only metadata, references same data files)
CREATE TABLE dev.silver.customer_orders_dev
SHALLOW CLONE dev.silver.customer_orders;

-- Clone as of a specific version
CREATE TABLE dev.silver.customer_orders_snapshot
SHALLOW CLONE dev.silver.customer_orders VERSION AS OF 10;

-- ============================================================================
-- 8. TABLE PROPERTIES AND CONSTRAINTS
-- ============================================================================

-- Add table properties
ALTER TABLE dev.silver.customer_orders
SET TBLPROPERTIES (
    'delta.deletedFileRetentionDuration' = 'interval 30 days',
    'delta.logRetentionDuration' = 'interval 90 days'
);

-- Add a check constraint
ALTER TABLE dev.silver.customer_orders
ADD CONSTRAINT valid_amount CHECK (total_amount >= 0);

-- Drop a constraint
ALTER TABLE dev.silver.customer_orders
DROP CONSTRAINT valid_amount;

-- ============================================================================
-- 9. MONITORING AND METADATA
-- ============================================================================

-- View table details
SHOW CREATE TABLE dev.silver.customer_orders;

-- View table properties
SHOW TBLPROPERTIES dev.silver.customer_orders;

-- View partitions
SHOW PARTITIONS dev.silver.customer_orders;

-- Get detailed table information
DESCRIBE DETAIL dev.silver.customer_orders;

-- View table history with details
DESCRIBE HISTORY dev.silver.customer_orders LIMIT 10;

-- ============================================================================
-- 10. BEST PRACTICES EXAMPLES
-- ============================================================================

-- Best Practice: Incremental processing with watermark
CREATE OR REPLACE TEMP VIEW new_orders_to_process AS
SELECT *
FROM dev.bronze.new_orders
WHERE _ingestion_timestamp > (
    SELECT COALESCE(MAX(_ingestion_timestamp), '1970-01-01') 
    FROM dev.silver.customer_orders
);

-- Best Practice: Idempotent MERGE with hash for change detection
MERGE INTO dev.silver.customer_orders AS target
USING (
    SELECT 
        *,
        sha2(concat_ws('||', order_id, customer_id, total_amount, status), 256) AS _row_hash
    FROM dev.bronze.new_orders
) AS source
ON target.order_id = source.order_id

WHEN MATCHED AND target._row_hash != source._row_hash THEN
  UPDATE SET *

WHEN NOT MATCHED THEN
  INSERT *;

-- Best Practice: Partition pruning for efficient queries
SELECT *
FROM dev.silver.customer_orders
WHERE country = 'USA'  -- Uses partition pruning
  AND order_date >= '2024-01-01';

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
-- For more information, see:
-- - Delta Lake Documentation: https://docs.delta.io/
-- - Databricks Delta Lake Guide: https://docs.databricks.com/delta/
-- - Repository: /pillar_ii/databricks_sql/delta_lake_dml.md
-- ============================================================================
