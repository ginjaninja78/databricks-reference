---
title: JDBC Connections
parent: Databricks Cookbooks
nav_order: 9
---

# Cookbook: Connecting to External Data Sources via JDBC

## 1. Problem Statement

You need to read data from or write data to an external relational database (like SQL Server, PostgreSQL, MySQL, etc.) from within Databricks. This is a common requirement for integrating with legacy systems or other data stores.

## 2. Solution Overview

This cookbook provides a secure and efficient recipe for connecting to external databases using the **JDBC (Java Database Connectivity)** driver in Databricks.

This recipe demonstrates how to:

1.  **Securely Store Credentials**: Use Databricks Secrets to store your database username and password.
2.  **Construct the JDBC URL**: Build the connection string for your specific database.
3.  **Read Data**: Load data from a database table into a Spark DataFrame.
4.  **Write Data**: Write data from a Spark DataFrame to a database table.

This approach is fundamental for any data engineer working in a hybrid environment where data resides in multiple systems.

## 3. Step-by-Step Implementation

This cookbook is a Python notebook that provides a clear, reusable pattern for JDBC connections.

**Notebook**: [`01_connecting_with_jdbc.py`](01_connecting_with_jdbc.py)

### Key Concepts Demonstrated

- **Databricks Secrets**: Securely managing sensitive connection details.
- **Spark JDBC DataSource**: Using `spark.read.jdbc(...)` and `df.write.jdbc(...)`.
- **Connection Properties**: Passing options like `user`, `password`, and `driver`.
- **Predicate Pushdown**: Optimizing read performance by pushing down `WHERE` clauses to the source database.

## 4. How to Use This Recipe

1.  **Store Your Credentials in Secrets**:
    -   Open the Databricks CLI or use the UI to create a secret scope: `databricks secrets create-scope --scope my_jdbc_scope`
    -   Add your database username and password as secrets:
        -   `databricks secrets put --scope my_jdbc_scope --key db_user --string-value "your_username"`
        -   `databricks secrets put --scope my_jdbc_scope --key db_password --string-value "your_password"`
2.  **Import the Notebook**: Import the `01_connecting_with_jdbc.py` notebook into your workspace.
3.  **Customize the Notebook**:
    -   Update the `jdbc_hostname`, `jdbc_port`, and `jdbc_database` variables to match your target database.
    -   Modify the `secret_scope` and `secret_key` names if you used different ones.
4.  **Run the Notebook**: Execute the cells to connect to your database, read data, and write data.

## 5. Best Practices & Customization

- **Never Hardcode Credentials**: This is the most critical best practice. Always use Databricks Secrets to avoid exposing sensitive information in your notebooks.
- **Use Predicate Pushdown**: When reading data, provide a `WHERE` clause in your query to filter data at the source. This significantly reduces the amount of data transferred to Spark and improves performance.
- **Manage Connection Pooling**: For high-concurrency workloads, be mindful of the number of connections being opened to your source database. You may need to adjust the `numPartitions` option when reading to control parallelism.
- **Driver Installation**: Ensure the appropriate JDBC driver for your database is installed on your Databricks cluster. You can install it as a library from Maven.
- **Attribution**: This recipe is a standard industry pattern and is based on best practices from the official Apache Spark and Databricks documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
