_# Databricks notebook source

# DBTITLE 1,Attribute-Based Access Control (ABAC) with Unity Catalog
# MAGIC %md
# MAGIC # Cookbook: Attribute-Based Access Control (ABAC) with Unity Catalog
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need a more scalable and flexible way to manage data access than traditional role-based access control (RBAC). Instead of granting access to specific tables or schemas, you want to grant access based on the attributes (tags) of the data.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This recipe demonstrates how to implement **Attribute-Based Access Control (ABAC)** in Unity Catalog using **tags**.
# MAGIC 
# MAGIC The process is as follows:
# MAGIC 
# MAGIC 1.  **Tag Your Data**: Apply tags to your catalogs, schemas, and tables to classify them (e.g., `pii: true`, `sensitivity: high`).
# MAGIC 2.  **Grant Privileges on Tags**: Grant privileges (like `SELECT`) on a specific tag to a group.
# MAGIC 3.  **Automatic Enforcement**: Unity Catalog automatically enforces these privileges. Any user in the group will have the granted privilege on all objects that have that tag.

# COMMAND ----------

# DBTITLE 1,Tag a Table
# MAGIC %sql
# MAGIC -- Apply a tag to a table
# MAGIC -- Replace with your own catalog, schema, and table
# MAGIC ALTER TABLE main.default.sales_data SET TAGS (
# MAGIC   'sensitivity' = 'high',
# MAGIC   'pii' = 'true'
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Grant Privileges on a Tag
# MAGIC %sql
# MAGIC -- Grant SELECT access on all tables with the 'sensitivity' = 'high' tag to the 'analysts' group
# MAGIC GRANT SELECT ON TAG `sensitivity` = 'high' TO `analysts`;

# COMMAND ----------

# DBTITLE 1,Query the Tagged Table
# MAGIC %md
# MAGIC Now, any user who is a member of the `analysts` group will be able to query the `main.default.sales_data` table, as well as any other table that has the `sensitivity` = 'high' tag.

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### Establish a Tagging Strategy
# MAGIC 
# MAGIC Before you start tagging your data, it's important to establish a clear and consistent tagging strategy. This will ensure that your tags are meaningful and can be used effectively for governance.
# MAGIC 
# MAGIC ### Use Tags for More Than Just Access Control
# MAGIC 
# MAGIC Tags can also be used for:
# MAGIC 
# MAGIC - **Data Discovery**: Help users find relevant data.
# MAGIC - **Cost Management**: Track costs by project or department.
# MAGIC - **Data Retention**: Define data retention policies.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the official Databricks documentation.
