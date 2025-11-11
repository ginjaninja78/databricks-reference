---
title: Data Lineage
nav_order: 3
parent: Data Governance & Security
grand_parent: Pillar I The Databricks Universe
---

# Data Lineage: Visualizing the Journey of Your Data

**Data lineage** is a critical component of data governance that provides a complete, end-to-end map of how data flows and transforms through the Lakehouse. It answers the fundamental questions of "Where did this data come from?" and "What is the impact of changing it?".

Unity Catalog revolutionizes lineage by **automatically capturing and visualizing it in real-time** for any query, table, or dashboard. This works across all languages supported by Databricks (SQL, Python, R, Scala) and provides both table-level and column-level granularity.

## Why is Data Lineage So Important?

Automated data lineage provides immense value across several key areas:

| Benefit | Description |
|---|---|
| **Impact Analysis** | Before changing a table or a pipeline, you can instantly see every downstream table, notebook, and dashboard that depends on it. This prevents accidental breakages and allows for proactive communication with stakeholders. |
| **Root Cause Analysis** | When a user reports an error in a dashboard, you can trace the lineage backward from the dashboard to the source table, examining every transformation along the way. This dramatically accelerates debugging and troubleshooting. |
| **Regulatory Compliance & Auditing** | For regulations like GDPR and CCPA, you must be able to prove the provenance of your data. Lineage provides an auditable, visual map of how sensitive data is used and transformed, making it easy to demonstrate compliance. |
| **Data Discovery & Trust** | When a data analyst discovers a new table, they can view its lineage to understand its origins, what transformations were applied, and whether it comes from a trusted source. This builds confidence and trust in the data. |

## How Unity Catalog Captures Lineage

Because Unity Catalog is the central governance layer for all data access in Databricks, it sees every query that runs. When a query executes, Unity Catalog's lineage service parses it and records the relationships between the source and target assets.

For example, when you run a job that reads from `silver.orders` and writes to `gold.daily_sales`, Unity Catalog automatically records that dependency.

This process is:

-   **Automatic**: No manual tagging or declaration is required.
-   **Real-Time**: Lineage information is available within seconds of a query completing.
-   **Column-Level**: Unity Catalog tracks lineage down to the individual column. You can see that the `total_sales` column in the Gold table was derived from the `total_amount` column in the Silver table.

## Visualizing Lineage in the Data Explorer

The primary way to interact with lineage is through the **Data Explorer** in the Databricks UI.

1.  Navigate to the **Data** tab.
2.  Select a table or view.
3.  Click on the **Lineage** tab.

This will display an interactive, directed acyclic graph (DAG) showing:

-   **Upstream Lineage**: The tables, notebooks, or dashboards that feed into the selected table.
-   **Downstream Lineage**: The tables, notebooks, or dashboards that consume data from the selected table.

![Data Lineage Graph](https://docs.databricks.com/_images/lineage-graph.png)
*Source: Databricks Documentation*

You can click on any node in the graph to expand it and explore its own lineage, allowing you to navigate the entire data flow from end to end.

### Column-Level Lineage

For even more granular insight, you can click on an individual column in the table's schema view to see the lineage specific to that column. This is incredibly powerful for understanding how specific metrics are calculated.

## Lineage for All Assets

Lineage in Unity Catalog is not limited to tables. It provides a holistic view across all assets in the Lakehouse:

-   **Notebooks**: See which tables a notebook reads from and writes to.
-   **Workflows**: Understand the data dependencies of your scheduled jobs.
-   **Dashboards**: See which tables power a specific dashboard, making it easy to validate the source of the data being presented.

By providing this comprehensive, automated, and real-time view of the data landscape, Unity Catalog's data lineage feature transforms data governance from a painful, manual exercise into a powerful, automated tool for building trust, ensuring quality, and accelerating development in the Lakehouse.
