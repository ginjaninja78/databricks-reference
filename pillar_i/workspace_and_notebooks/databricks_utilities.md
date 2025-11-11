---
title: Databricks Utilities (dbutils)
nav_order: 2
parent: Workspace & Notebooks
grand_parent: Pillar I The Databricks Universe
---

# Databricks Utilities (dbutils): Your Toolkit for Interacting with the Workspace

While notebooks provide the interactive canvas, **Databricks Utilities (`dbutils`)** provide the programmatic toolkit to interact with the Databricks environment itself. `dbutils` is a powerful, exclusive library available only within the Databricks platform that allows you to perform essential tasks that are not part of the standard Spark API.

Understanding and using `dbutils` is a key step in moving from a casual user to a power user of Databricks. It enables automation, parameterization, and interaction with the underlying file system and secrets management, which are crucial for building production-grade pipelines.

`dbutils` is automatically available in all notebooks—no import is required. It is organized into several modules, each handling a specific area of functionality.

## `dbutils.fs`: Interacting with the File System

This is arguably the most frequently used module. `dbutils.fs` allows you to perform file system operations on the Databricks File System (DBFS) and mounted cloud storage (like S3 or ADLS).

> **Note:** While `dbutils.fs` is convenient for exploration, for production code, it is often recommended to use Spark's native APIs (`spark.read`, `spark.write`) for better performance and portability.

### Common `dbutils.fs` Commands:

-   **`ls()`**: List the contents of a directory.
    ```python
    # List files in the root of DBFS
    display(dbutils.fs.ls("/"))
    ```
-   **`mkdirs()`**: Create a directory (and any necessary parent directories).
    ```python
    dbutils.fs.mkdirs("/tmp/my-new-directory")
    ```
-   **`put()`**: Write a string to a file. Useful for creating small configuration or test files.
    ```python
    dbutils.fs.put("/tmp/my-file.txt", "Hello, World!", overwrite=True)
    ```
-   **`head()`**: Read the first few bytes of a file.
    ```python
    print(dbutils.fs.head("/tmp/my-file.txt"))
    ```
-   **`cp()` and `mv()`**: Copy or move files and directories.
    ```python
    dbutils.fs.cp("/tmp/my-file.txt", "/tmp/my-file-copy.txt")
    dbutils.fs.mv("/tmp/my-file-copy.txt", "/tmp/my-new-directory/")
    ```
-   **`rm()`**: Remove a file or directory.
    ```python
    dbutils.fs.rm("/tmp/my-new-directory", recurse=True) # recurse=True is needed for directories
    ```
-   **`mount()`**: (For administrators) Mount cloud storage to a path in DBFS, making it accessible like a local directory. This is a powerful feature for simplifying access to data.

## `dbutils.widgets`: Parameterizing Notebooks

As introduced in the previous section, `dbutils.widgets` allows you to create and interact with input widgets in your notebook. This is the primary way to pass parameters to notebooks, making them dynamic and reusable.

### Widget Types:

-   **`text()`**: A simple text input box.
-   **`dropdown()`**: A dropdown list of choices.
-   **`combobox()`**: A combination of a text box and a dropdown.
-   **`multiselect()`**: A dropdown that allows selecting multiple options.

### Example: Using a Dropdown Widget

```python
# Create a dropdown widget with a list of choices
dbutils.widgets.dropdown("region", "North America", ["North America", "Europe", "Asia"], "Select a Region")

# Get the selected value
selected_region = dbutils.widgets.get("region")

print(f"Processing data for the {selected_region} region.")
```

## `dbutils.secrets`: Securely Managing Credentials

Hardcoding secrets like API keys, database passwords, or storage account keys in your notebooks is a major security risk. `dbutils.secrets` provides a secure way to retrieve these secrets from a managed secret store, such as **Databricks Secrets** or **Azure Key Vault**.

### Key Commands:

-   **`listScopes()`**: List the available secret scopes.
-   **`list()`**: List the secrets within a specific scope.
-   **`get()`**: Retrieve a secret value.

### Example: Retrieving a Database Password

```python
# Assume a secret scope named "database-scope" and a secret named "db-password" exist

# Retrieve the password
db_password = dbutils.secrets.get(scope="database-scope", key="db-password")

# Use the password in a JDBC connection string
# Note: The actual password value is redacted from the notebook output for security
jdbc_url = f"jdbc:sqlserver://<server>.database.windows.net;databaseName=<db>;user=<user>;password={db_password}"

print("JDBC URL has been configured.")
```

When you use `dbutils.secrets.get()`, the secret value is **never displayed** in the notebook output. This prevents accidental exposure of sensitive credentials.

## `dbutils.notebook`: Chaining Notebooks into Workflows

This module allows you to execute other notebooks from within your current notebook, enabling you to build complex workflows by chaining modular notebooks together.

### Key Commands:

-   **`run()`**: Execute another notebook and optionally pass parameters to it. This command returns the exit value of the called notebook.
-   **`exit()`**: Exit the current notebook with a specific value, which can be returned to a calling notebook.

### Example: A Simple ETL Workflow

**Notebook 1: `run_etl`**
```python
# This notebook orchestrates the ETL process

print("Starting ETL workflow...")

# Run the ingestion notebook and pass a date parameter
ingestion_output = dbutils.notebook.run("./ingest_data", timeout_seconds=3600, arguments={"ingestion_date": "2024-10-26"})

print(f"Ingestion finished with status: {ingestion_output}")

# Run the transformation notebook
transformation_output = dbutils.notebook.run("./transform_data", timeout_seconds=3600)

print(f"Transformation finished with status: {transformation_output}")
```

**Notebook 2: `ingest_data`**
```python
# This notebook handles data ingestion

# Get the date parameter passed from the calling notebook
ingestion_date = dbutils.widgets.get("ingestion_date")

print(f"Ingesting data for {ingestion_date}...")

# ... (ingestion logic here) ...

# Exit the notebook with a success message
dbutils.notebook.exit("Ingestion successful")
```

This modular approach is a best practice for building maintainable and testable data pipelines in Databricks.

By mastering these four key modules of `dbutils`, you unlock a new level of control and automation within the Databricks environment, enabling you to build sophisticated, secure, and robust data applications.
