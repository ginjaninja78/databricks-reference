_# Databricks notebook source

# DBTITLE 1,Connecting to External Data Sources via JDBC
# MAGIC %md
# MAGIC # Cookbook: Connecting to External Data Sources via JDBC
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to read data from or write data to an external relational database (like SQL Server, PostgreSQL, MySQL, etc.) from within Databricks. This is a common requirement for integrating with legacy systems or other data stores.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a secure and efficient recipe for connecting to external databases using the **JDBC (Java Database Connectivity)** driver in Databricks.
# MAGIC 
# MAGIC This recipe demonstrates how to:
# MAGIC 
# MAGIC 1.  **Securely Store Credentials**: Use Databricks Secrets to store your database username and password.
# MAGIC 2.  **Construct the JDBC URL**: Build the connection string for your specific database.
# MAGIC 3.  **Read Data**: Load data from a database table into a Spark DataFrame.
# MAGIC 4.  **Write Data**: Write data from a Spark DataFrame to a database table.
# MAGIC 
# MAGIC ## 3. How to Use This Recipe
# MAGIC 
# MAGIC 1.  **Store Your Credentials in Secrets**:
# MAGIC     -   Create a secret scope: `databricks secrets create-scope --scope my_jdbc_scope`
# MAGIC     -   Add your database username and password:
# MAGIC         -   `databricks secrets put --scope my_jdbc_scope --key db_user --string-value "your_username"`
# MAGIC         -   `databricks secrets put --scope my_jdbc_scope --key db_password --string-value "your_password"`
# MAGIC 2.  **Customize the Notebook**:
# MAGIC     -   Update the JDBC connection variables below.
# MAGIC 3.  **Run the Notebook**.

# COMMAND ----------

# DBTITLE 1,Configuration
# MAGIC %md
# MAGIC ### Customize these variables for your environment

# COMMAND ----------

# JDBC connection parameters
jdbc_hostname = "your_database_hostname"  # e.g., your-sql-server.database.windows.net
jdbc_port = 1433
jdbc_database = "your_database_name"

# Databricks Secrets configuration
secret_scope = "my_jdbc_scope"
user_secret_key = "db_user"
password_secret_key = "db_password"

# Table to read from and write to
source_table = "source_table_name"
target_table = "new_target_table_name"

# COMMAND ----------

# DBTITLE 1,Retrieve Credentials Securely
# Retrieve credentials from Databricks Secrets
# This prevents hardcoding sensitive information in your notebook

jdbc_username = dbutils.secrets.get(scope=secret_scope, key=user_secret_key)
jdbc_password = dbutils.secrets.get(scope=secret_scope, key=password_secret_key)

# COMMAND ----------

# DBTITLE 1,Construct JDBC URL and Connection Properties
# Construct the JDBC URL
# This example is for SQL Server. The format will vary for other databases.
jdbc_url = f"jdbc:sqlserver://{jdbc_hostname}:{jdbc_port};database={jdbc_database}"

# Create a properties dictionary for the connection
connection_properties = {
  "user": jdbc_username,
  "password": jdbc_password,
  "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver" # Example for SQL Server
}

# COMMAND ----------

# DBTITLE 1,Read Data from the External Database
# Use spark.read.jdbc to load data from the external table
# The `dbtable` option can be a table name or a subquery

print(f"Reading data from table: {source_table}")

pushdown_query = f"(SELECT * FROM {source_table} WHERE some_column = 'some_value') AS filtered_data"

# Using a pushdown query is a best practice for performance
df_read = spark.read.jdbc(
  url=jdbc_url,
  table=pushdown_query, # or just use `source_table` to read the whole table
  properties=connection_properties
)

display(df_read)

# COMMAND ----------

# DBTITLE 1,Write Data to the External Database
# Create a sample DataFrame to write
sample_data = [("A", 1), ("B", 2), ("C", 3)]
columns = ["col1", "col2"]
sample_df = spark.createDataFrame(sample_data, columns)

print(f"Writing data to new table: {target_table}")

# Use df.write.jdbc to save the DataFrame to a new table
# The `mode` option can be "overwrite", "append", "ignore", or "error"
sample_df.write.jdbc(
  url=jdbc_url,
  table=target_table,
  mode="overwrite", # Be careful with overwrite in production!
  properties=connection_properties
)

print("Write complete.")

# COMMAND ----------

# DBTITLE 1,Best Practices Review
# MAGIC %md
# MAGIC ### Key Best Practices in this Notebook
# MAGIC 
# MAGIC - **✅ Secrets Management**: Credentials are not hardcoded. They are retrieved at runtime from Databricks Secrets.
# MAGIC - **✅ Predicate Pushdown**: The read operation uses a subquery (`pushdown_query`). This pushes the `WHERE` clause down to the source database, which filters the data *before* it is transferred to Spark. This is a critical performance optimization.
# MAGIC - **✅ Clear Configuration**: All connection parameters are defined in a single configuration cell, making the notebook easy to adapt.
# MAGIC - **✅ Driver Specification**: The JDBC driver class is explicitly specified in the connection properties.

# MAGIC ### Important Considerations
# MAGIC 
# MAGIC - **Driver Installation**: Ensure the appropriate JDBC driver for your database is installed on your Databricks cluster. You can typically install this as a library from Maven Central.
# MAGIC - **Network Security**: Your Databricks workspace must have network access to the target database. This may involve configuring VNet injection, peering, or firewall rules.
# MAGIC - **Parallelism**: When reading large tables, you can control the parallelism by providing `numPartitions`, `partitionColumn`, `lowerBound`, and `upperBound` options to the `.jdbc()` call. This can prevent overwhelming the source database with too many concurrent connections.
