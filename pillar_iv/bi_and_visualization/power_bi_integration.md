---
title: Power BI Integration
nav_order: 1
parent: BI & Visualization Integration
grand_parent: Pillar IV Enterprise Readiness
---

# Power BI & Databricks: A Best Practices Guide

Microsoft Power BI is one of the most popular business intelligence tools in the world, and its integration with Databricks is a cornerstone of the modern Microsoft data stack. By combining Power BI's powerful visualization and self-service capabilities with the massive scalability and computational power of the Databricks Lakehouse, organizations can build end-to-end analytics solutions that are both powerful and user-friendly.

This guide provides a deep dive into the best practices for connecting Power BI to Databricks, covering connectivity modes, architecture, and security.

## Connectivity Modes: Import vs. DirectQuery

When connecting Power BI to Databricks, you have two primary connectivity modes to choose from. The choice between them is one of the most critical architectural decisions you will make and has significant implications for performance, cost, and data freshness.

### 1. Import Mode

In **Import mode**, Power BI loads a copy of the data from your Databricks tables into its own internal, highly compressed, in-memory columnar engine (VertiPaq). All visuals and DAX queries in the Power BI report then run against this in-memory copy.

**When to Use Import Mode:**

-   When you need the **highest possible query performance** and a fast, interactive user experience.
-   When your dataset size is **less than 1 GB** (or larger with Power BI Premium).
-   When your data freshness requirement is not real-time (e.g., daily or hourly refreshes are acceptable).
-   When you want to use the full capabilities of the DAX language.

### 2. DirectQuery Mode

In **DirectQuery mode**, Power BI does **not** store a copy of the data. Instead, every time a user interacts with a visual in the report (e.g., clicking a slicer), Power BI generates a SQL query in real-time and sends it directly to the Databricks SQL Warehouse. The visual is then rendered based on the results of that query.

**When to Use DirectQuery Mode:**

-   When your dataset is **too large to fit into memory** (e.g., many terabytes).
-   When you need **near real-time data freshness**, as every query goes directly to the source.
-   When you need to enforce complex, source-side security rules (like row-level security) in Databricks.

### Comparison of Connectivity Modes

| Feature | Import Mode | DirectQuery Mode |
|---|---|---|
| **Performance** | **Highest**. Queries run against the in-memory VertiPaq engine. | **Variable**. Depends on the performance of the underlying Databricks SQL Warehouse and the complexity of the generated query. |
| **Data Volume** | Limited by memory (typically < 1-10 GB). | Virtually unlimited, constrained only by the source. |
| **Data Freshness** | Stale. Data is as fresh as the last scheduled refresh. | Near real-time. Data is always as fresh as the source. |
| **DAX Support** | Full. All DAX functions are available. | Limited. Some DAX functions that cannot be translated into SQL are not supported. |
| **Databricks Load** | Load occurs only during scheduled refresh. | Load occurs with every user interaction in the report. Can lead to high query concurrency. |
| **Cost** | Potentially lower Databricks compute cost, as queries are offloaded to Power BI. | Potentially higher Databricks compute cost due to high query volume. Requires a properly sized SQL Warehouse. |

**Best Practice**: Start with **Import mode** whenever possible. The performance and user experience are generally superior. Only move to DirectQuery when your data volume or real-time requirements make Import mode infeasible.

## Connecting Power BI to Databricks

1.  In Power BI Desktop, click **Get Data**.
2.  Search for and select **Azure Databricks**.
3.  You will be prompted for the connection details:
    -   **Server Hostname**: You can find this in the **Connection Details** tab of your Databricks SQL Warehouse.
    -   **HTTP Path**: Also found in the Connection Details tab.
    -   **Data Connectivity mode**: Choose **Import** or **DirectQuery**.
4.  For authentication, the recommended method is to sign in with your **Azure Active Directory** account. This enables single sign-on (SSO) and allows for user identity to be passed from Power BI to Databricks, which is essential for enforcing security.

## Architectural Best Practices

-   **Serve BI from the Gold Layer**: Your Power BI reports should **always** connect to tables in your **Gold layer**. These tables should be designed specifically for analytics: denormalized, aggregated, and with user-friendly column names. Never point a BI tool directly to your raw Bronze or cleansed Silver data.
-   **Create Aggregate Tables**: If you are using DirectQuery on a very large fact table, performance can suffer. A common and highly effective pattern is to create an **aggregate table** in your Gold layer. For example, if your main fact table has billions of rows of transactional data, create a daily summary table with pre-aggregated metrics. Point your high-level Power BI report to the aggregate table and allow users to drill through to the detailed table only when necessary.
-   **Optimize Your SQL Warehouse**: When using DirectQuery, the performance of your Power BI report is directly tied to the performance of your Databricks SQL Warehouse. Ensure your warehouse is properly sized (e.g., Medium, Large) for your expected user concurrency. Use serverless warehouses to handle bursting query loads automatically.
-   **Use Star Schemas**: Structure your Gold layer using a classic star schema with centralized fact tables and surrounding dimension tables. This model is highly optimized for the types of queries that BI tools generate.
