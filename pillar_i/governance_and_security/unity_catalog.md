---
title: Unity Catalog Explained
nav_order: 1
parent: Data Governance & Security
grand_parent: Pillar I The Databricks Universe
---

# Unity Catalog: Unified Governance for Data and AI

**Unity Catalog (UC)** is the cornerstone of data and AI governance within the Databricks Lakehouse Platform. It provides a centralized, fine-grained governance solution for all data assets, including files, tables, views, and machine learning models. Before Unity Catalog, governance was often fragmented across different workspaces, leading to complexity and inconsistent security models.

Unity Catalog solves this by introducing a global, account-level metadata layer that applies uniformly across all workspaces.

## The Three-Level Namespace

Unity Catalog organizes data assets using a simple, three-level namespace, mirroring the structure used in standard SQL databases. This makes data organization intuitive for developers coming from a traditional data warehousing background.

`catalog.schema.table`

1.  **Catalog**: The top-most level of the hierarchy. A catalog is a container for schemas. You might organize your catalogs by environment (`dev`, `staging`, `prod`), business unit (`sales`, `finance`, `hr`), or major project.
2.  **Schema (Database)**: The middle level, which organizes data assets within a catalog. A schema contains tables, views, and models. The terms `schema` and `database` are used interchangeably.
3.  **Table/View/Model**: The lowest level, representing the data asset itself.

This structure provides a clean and logical way to segregate and manage data across the entire organization.

## Key Features and Benefits

| Feature | Description |
|---|---|
| **Centralized Governance** | Define and enforce access policies once at the account level, and they are automatically inherited by all current and future workspaces. This dramatically simplifies administration. |
| **Standard SQL Data Access Controls** | Use standard SQL `GRANT` and `REVOKE` statements to manage permissions on catalogs, schemas, tables, and views. This provides a familiar and powerful way to manage security. |
| **Fine-Grained Access Control** | Secure your data at the level you need. Unity Catalog supports permissions on catalogs, schemas, tables, and views, as well as **row-level security** and **column-level masking** to protect sensitive data. |
| **Centralized Auditing** | All access to data managed by Unity Catalog is centrally logged. This provides a comprehensive audit trail, showing who accessed what data, when, and from where. |
| **Data Discovery** | Unity Catalog provides a built-in data discovery UI. Users can search for datasets, view their schema, preview sample data, and understand their lineage, promoting data literacy and reuse. |
| **Data Lineage** | Unity Catalog automatically captures and visualizes data lineage at the column level. You can track how data flows from its source, through various transformations, and into dashboards. This is critical for impact analysis and regulatory compliance. |

## The Securable Objects Model

Unity Catalog manages a hierarchy of securable objects. Permissions are inherited down this hierarchy.

`Metastore -> Catalog -> Schema -> Table/View`

-   If you grant a user `USE_CATALOG` permission on a catalog, they will be able to see the catalog.
-   If you then grant them `USE_SCHEMA` on a schema within that catalog, they can see that schema.
-   Finally, if you grant them `SELECT` on a table within that schema, they can read from that table.

This inheritance model allows for broad policy definitions at higher levels, with the option to get more granular at lower levels.

### Example: Granting Permissions

Let's say you want to give a data analyst group, `analyst_team`, read-only access to the `daily_sales_by_region` Gold table.

```sql
-- First, the group needs to be able to access the parent catalog and schema
GRANT USE_CATALOG ON CATALOG prod_catalog TO `analyst_team`;

GRANT USE_SCHEMA ON SCHEMA prod_catalog.gold_data TO `analyst_team`;

-- Now, grant the specific SELECT permission on the table
GRANT SELECT ON TABLE prod_catalog.gold_data.daily_sales_by_region TO `analyst_team`;
```

Now, any member of the `analyst_team` can run `SELECT * FROM prod_catalog.gold_data.daily_sales_by_region` from any workspace attached to the metastore, but they cannot modify the table or even see other tables in the `gold_data` schema.

Unity Catalog is a fundamental shift in how governance is handled in Databricks. By unifying governance across the platform, it enables organizations to build a secure, scalable, and trustworthy Lakehouse that can serve the entire enterprise.
