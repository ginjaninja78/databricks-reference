---
title: Secrets Management
nav_order: 1
parent: Advanced Security & Networking
grand_parent: Pillar IV Enterprise Readiness
---

# Secrets Management: A Guide to Databricks Secrets

In any data pipeline, you will inevitably need to connect to external systems: databases, storage accounts, APIs, etc. These connections require credentials (passwords, API keys, tokens), which are highly sensitive secrets. Hardcoding these secrets directly in your notebooks is a major security risk.

**Databricks Secrets** provides a secure way to store and reference your secrets, ensuring they are never exposed in plaintext in your code, logs, or version control history.

A secret is a key-value pair stored in a **secret scope**. When you reference a secret in your code, Databricks automatically redacts the value from notebook output and logs, displaying `[REDACTED]` instead.

## Types of Secret Scopes

There are two types of secret scopes. The best practice for all enterprise use cases is to use an **Azure Key Vault-backed scope**.

1.  **Databricks-backed Scope**: Secrets are stored in an encrypted database managed by Databricks. This is simple to set up but less flexible than using a dedicated secret management service.

2.  **Azure Key Vault-backed Scope**: Secrets are stored in an **Azure Key Vault**, a centralized, hardware-secured secret management service from Microsoft. This is the recommended and most secure approach.

### Why Use an Azure Key Vault-backed Scope?

-   **Centralized Management**: It provides a single, central place to manage all your application secrets across your entire organization, not just for Databricks.
-   **Advanced Security Features**: Key Vault provides rich features like hardware security modules (HSMs), granular access policies, and detailed audit logging.
-   **Separation of Duties**: Your security team can manage the secrets in Key Vault, while your data engineers can be granted permission to *use* the secrets in Databricks without ever being able to see their actual values.

## Setting Up an Azure Key Vault-backed Scope

Setting this up is a one-time administrative task that involves creating a Key Vault and then linking it to your Databricks workspace.

1.  **Create an Azure Key Vault**: In the Azure portal, create a new Key Vault instance.
2.  **Add Secrets to Key Vault**: In your Key Vault, go to the **Secrets** tab and add your secrets (e.g., a secret named `my-database-password` with its value).
3.  **Create the Secret Scope in Databricks**: This is done via the Databricks UI or CLI. You will need to provide the **Vault URI** and **Resource ID** of your Azure Key Vault.
    -   Navigate to `https://<your-databricks-host>#secrets/createScope`.
    -   Enter a name for your scope (e.g., `kv-scope`).
    -   Paste the DNS Name and Resource ID from your Key Vault properties page in the Azure portal.

## Using Secrets in Your Code

Once the scope is created, you can easily access secrets using the `dbutils.secrets.get()` utility.

### Example: Connecting to a SQL Database

Let's say you have stored the username and password for an Azure SQL Database in your Key Vault-backed scope named `kv-scope`.

-   Secret Name for user: `sql-db-user`
-   Secret Name for password: `sql-db-password`

**In a Python Notebook:**

```python
# Retrieve the secrets using dbutils
# The values are never displayed in the notebook
username = dbutils.secrets.get(scope="kv-scope", key="sql-db-user")
password = dbutils.secrets.get(scope="kv-scope", key="sql-db-password")

# Use the secrets to build a JDBC connection string
jdbc_url = f"jdbc:sqlserver://<your-server>.database.windows.net;databaseName=<your-db>;user={username};password={password}"

# Now, you can use this URL to read from the database
df = (
    spark.read
    .format("jdbc")
    .option("url", jdbc_url)
    .option("dbtable", "dbo.my_table")
    .load()
)

head(df)
```

When you run this code, the output of the `dbutils.secrets.get()` calls will be `[REDACTED]`. The secrets are passed securely to the JDBC driver in the background, but they are never exposed in the notebook UI, logs, or revision history.

By always using Databricks Secrets backed by Azure Key Vault, you can build secure, enterprise-grade data pipelines that meet the strictest security and compliance requirements.
