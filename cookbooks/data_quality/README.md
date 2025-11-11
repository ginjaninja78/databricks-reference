---
title: Data Quality Monitoring
parent: Databricks Cookbooks
nav_order: 4
---

# Cookbook: Data Quality Monitoring

## 1. Problem Statement

You need to ensure the quality and integrity of your data as it moves through your data pipelines. This includes validating data against a set of rules, monitoring data quality over time, and being alerted to any issues.

## 2. Solution Overview

This cookbook provides a recipe for implementing a robust data quality monitoring solution on Databricks. It leverages:

- **Delta Live Tables (DLT)**: For defining and enforcing data quality expectations directly within the data pipeline.
- **Custom Python Libraries**: For creating reusable data quality checks that can be applied across multiple pipelines.

This recipe demonstrates:

- **Defining Data Quality Rules**: Using `@dlt.expect` to define rules for nulls, formats, and business logic.
- **Handling Data Quality Failures**: Using `@dlt.expect_or_drop` and `@dlt.expect_or_fail` to control the behavior of the pipeline when data quality rules are violated.
- **Creating a Reusable Data Quality Framework**: Building a Python class for data quality checks that can be used in any Databricks notebook.

## 3. Step-by-Step Implementation

This cookbook includes two components:

1.  A Delta Live Tables notebook that demonstrates how to embed data quality checks directly into a DLT pipeline.
2.  A reusable Python module for data quality that can be imported into any notebook.

**DLT Notebook**: [`01_data_quality_with_dlt.py`](01_data_quality_with_dlt.py)
**Python Module**: [`../../code_recipes/python/data_quality_utils.py`](../../code_recipes/python/data_quality_utils.py)

### Key Concepts Demonstrated

- **Data Quality as Code**: Embedding data quality rules directly in your pipeline code.
- **Quarantine Tables**: DLT automatically creates quarantine tables to store records that fail data quality checks.
- **Data Quality Metrics**: The DLT UI provides detailed metrics on data quality, including the number of records that passed or failed each rule.
- **Modularity and Reusability**: Creating a separate Python module for data quality checks promotes code reuse and consistency.

## 4. How to Use This Recipe

### Using the DLT Notebook

1.  **Import the Notebook**: Import the `01_data_quality_with_dlt.py` notebook into your Databricks workspace.
2.  **Create a DLT Pipeline**: Follow the instructions in the [Streaming ETL with DLT cookbook](streaming_etl/) to create a DLT pipeline from this notebook.
3.  **Monitor Data Quality**: The DLT UI will show the data quality metrics for your pipeline.

### Using the Python Module

1.  **Import the Module**: You can import the `DataQualityChecker` class from the `data_quality_utils` module into any notebook.
2.  **Create a Checker Instance**: `checker = DataQualityChecker(df)`
3.  **Run Checks**: `results = checker.run_all_checks()`

## 5. Best Practices & Customization

- **Start with the Basics**: Begin with simple data quality checks (e.g., null checks, format checks) and gradually add more complex business rules.
- **Use DLT for New Pipelines**: For new data pipelines, DLT is the recommended way to manage data quality.
- **Create a Centralized Quality Framework**: For existing pipelines, or for checks that need to be applied across multiple pipelines, create a centralized Python library for data quality.
- **Alert on Failures**: Configure alerts on your DLT pipelines or your custom data quality framework to be notified of any issues.
- **Attribution**: This recipe is inspired by best practices from the Databricks documentation and various open-source data quality tools.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
