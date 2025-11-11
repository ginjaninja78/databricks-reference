---
title: Change Data Capture (CDC)
parent: Databricks Cookbooks
nav_order: 7
---

# Cookbook: Change Data Capture (CDC)

## 1. Problem Statement

You need to process and apply changes from a source database to a target Delta table. This is a common requirement in data warehousing and data lake scenarios.

## 2. Solution Overview

This cookbook provides a recipe for implementing Change Data Capture (CDC) in Databricks using **Delta Live Tables (DLT)**.

DLT has built-in support for CDC, making it easy to handle inserts, updates, and deletes from a source system.

This recipe demonstrates:

- **Applying Changes**: Using `dlt.apply_changes()` to apply CDC data to a target table.
- **SCD Type 1 and 2**: Implementing both Slowly Changing Dimension (SCD) Type 1 and Type 2.

## 3. Step-by-Step Implementation

This cookbook is implemented as a Delta Live Tables notebook.

**Notebook**: [`01_cdc_with_dlt.py`](01_cdc_with_dlt.py)

## 4. How to Use This Recipe

1.  **Import the Notebook**: Import the `01_cdc_with_dlt.py` notebook into your Databricks workspace.
2.  **Create a DLT Pipeline**: Create a DLT pipeline from this notebook.
3.  **Run the Pipeline**: Run the pipeline to see the CDC logic in action.

## 5. Best Practices & Customization

- **Use DLT for CDC**: DLT is the recommended way to implement CDC in Databricks.
- **Choose the Right SCD Type**: Choose the SCD type that best fits your business requirements.
- **Handle Out-of-Order Data**: Use the `track_history` option in `dlt.apply_changes()` to handle out-of-order data.
- **Attribution**: This recipe is based on best practices from the Databricks documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
