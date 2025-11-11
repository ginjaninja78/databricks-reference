_# Databricks notebook source

# DBTITLE 1,Row-Level Security
# MAGIC %md
# MAGIC # Cookbook: Row-Level Security
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to restrict access to rows in a table based on the user or group that is querying the table. For example, you might want to allow sales managers to see only the data for their own region.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This recipe demonstrates how to implement row-level security in Databricks using **dynamic views** in **Unity Catalog**.
# MAGIC 
# MAGIC A dynamic view is a view whose contents are determined by the identity of the user querying it. This is achieved by using functions like `current_user()` or `is_member()` in the view definition.

# COMMAND ----------

# DBTITLE 1,Create Sample Data and Table
# Create a sample DataFrame
data = [('Alice', 'USA'), ('Bob', 'USA'), ('Charlie', 'Canada')]
columns = ['name', 'country']
df = spark.createDataFrame(data, columns)

# Write the DataFrame to a Delta table in Unity Catalog
# Replace with your own catalog and schema
df.write.mode('overwrite').saveAsTable('main.default.sales_data')

# COMMAND ----------

# DBTITLE 1,Create a Dynamic View
# MAGIC %sql
# MAGIC -- Create a dynamic view that filters rows based on the user's country
# MAGIC -- In a real-world scenario, you would likely use a mapping table to map users to countries
# MAGIC CREATE OR REPLACE VIEW main.default.sales_data_rls AS
# MAGIC SELECT * FROM main.default.sales_data
# MAGIC WHERE country = CASE
# MAGIC   WHEN is_member('usa-sales') THEN 'USA'
# MAGIC   WHEN is_member('canada-sales') THEN 'Canada'
# MAGIC   ELSE NULL
# MAGIC END;

# COMMAND ----------

# DBTITLE 1,Query the Dynamic View
# MAGIC %sql
# MAGIC -- When a user in the 'usa-sales' group queries this view, they will only see rows where country = 'USA'
# MAGIC -- When a user in the 'canada-sales' group queries this view, they will only see rows where country = 'Canada'
# MAGIC SELECT * FROM main.default.sales_data_rls;

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### Use Unity Catalog
# MAGIC 
# MAGIC Unity Catalog is the recommended way to manage data governance and security in Databricks.
# MAGIC 
# MAGIC ### Use Groups for Permissions
# MAGIC 
# MAGIC It's a best practice to manage permissions through groups rather than individual users. This makes it easier to manage access as users join or leave your organization.
# MAGIC 
# MAGIC ### Use a Mapping Table
# MAGIC 
# MAGIC For more complex scenarios, consider using a mapping table to map users or groups to the data they are allowed to see. This can make your dynamic views more flexible and easier to maintain.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the Databricks documentation and community blogs.
