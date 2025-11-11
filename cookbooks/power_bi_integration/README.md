---
title: Power BI Integration
parent: Databricks Cookbooks
nav_order: 13
---

# Cookbook: Power BI Integration

## 1. Problem Statement

You need to connect Power BI to your Databricks data lakehouse to build interactive reports and dashboards. You want to ensure that the connection is secure, performant, and easy to manage.

## 2. Solution Overview

This cookbook provides a comprehensive guide to integrating **Power BI** with **Databricks**. It covers the entire process, from connecting to your data to optimizing your reports for performance.

This recipe demonstrates:

- **Connecting Power BI to Databricks**: Using the built-in Databricks connector in Power BI Desktop.
- **DirectQuery vs. Import Mode**: Understanding the pros and cons of each mode and when to use them.
- **Optimizing for Performance**: Best practices for ensuring your Power BI reports are fast and responsive.

## 3. Step-by-Step Implementation

This cookbook is a combination of a conceptual guide and a practical notebook for preparing your data.

**Notebook**: [`01_prepare_data_for_power_bi.py`](01_prepare_data_for_power_bi.py)

### Key Concepts Demonstrated

- **Gold Layer for BI**: The importance of creating aggregated, business-ready tables in your Gold layer specifically for BI consumption.
- **Databricks SQL Endpoints**: Using Databricks SQL endpoints to provide a high-performance, low-latency connection for Power BI.
- **Row-Level Security (RLS)**: Implementing RLS in Databricks to ensure that users only see the data they are authorized to see in Power BI.

## 4. How to Use This Recipe

1.  **Prepare Your Data**: Run the `01_prepare_data_for_power_bi.py` notebook to create an optimized Gold table for your Power BI report.
2.  **Connect from Power BI Desktop**:
    -   Open Power BI Desktop and go to **Get Data**.
    -   Search for and select the **Databricks** connector.
    -   Enter your Databricks server hostname and HTTP path.
    -   Choose your authentication method (e.g., Azure Active Directory).
    -   Select your Gold table and choose **DirectQuery** or **Import** mode.
3.  **Build Your Report**: Create your report in Power BI Desktop.
4.  **Publish to Power BI Service**: Publish your report to the Power BI service to share it with others.

## 5. Best Practices & Customization

- **Use DirectQuery for Real-Time Data**: If you need real-time or near-real-time data in your reports, use DirectQuery. Be aware that this can put more load on your Databricks cluster.
- **Use Import Mode for Performance**: If your data is not too large and doesn't need to be real-time, use Import mode. This will provide the best performance as the data is cached in Power BI.
- **Optimize Your Gold Tables**: Before connecting Power BI, make sure your Gold tables are optimized for BI queries. This includes using Z-ORDERING, partitioning, and creating pre-aggregated tables.
- **Use a Databricks SQL Endpoint**: For the best performance and concurrency, use a Databricks SQL endpoint instead of an all-purpose cluster.
- **Attribution**: This recipe is based on best practices from the official Databricks and Microsoft documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
