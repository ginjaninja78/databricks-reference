_# Databricks notebook source

# DBTITLE 1,Secure Data Sharing with Delta Sharing
# MAGIC %md
# MAGIC # Cookbook: Secure Data Sharing with Delta Sharing
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to securely share live data from your data lakehouse with external partners, customers, or other departments within your organization, without having to copy or move the data.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a practical guide to using **Delta Sharing**, an open protocol for secure data sharing from Databricks.

# COMMAND ----------

# DBTITLE 1,Step 1: Create a Share
# MAGIC %sql
# MAGIC -- A share is a logical container for the tables you want to share.
# MAGIC CREATE SHARE IF NOT EXISTS my_awesome_share
# MAGIC   COMMENT 'A share for my awesome data';

# COMMAND ----------

# DBTITLE 1,Step 2: Add a Table to the Share
# MAGIC %sql
# MAGIC -- Add a table to the share. You can share a whole table or specific partitions.
# MAGIC ALTER SHARE my_awesome_share ADD TABLE main.default.gold_daily_sales;

# COMMAND ----------

# DBTITLE 1,Step 3: Create a Recipient
# MAGIC %sql
# MAGIC -- A recipient is the entity you are sharing the data with.
# MAGIC CREATE RECIPIENT IF NOT EXISTS my_awesome_recipient
# MAGIC   COMMENT 'A recipient for my awesome data';

# COMMAND ----------

# DBTITLE 1,Step 4: Grant Access to the Recipient
# MAGIC %sql
# MAGIC -- Grant the recipient access to the share.
# MAGIC GRANT SELECT ON SHARE my_awesome_share TO RECIPIENT my_awesome_recipient;

# COMMAND ----------

# DBTITLE 1,Step 5: Retrieve the Recipient Activation Link
# MAGIC %sql
# MAGIC -- This will generate a one-time activation link for the recipient.
# MAGIC -- Securely send this link to the recipient.
# MAGIC DESCRIBE RECIPIENT my_awesome_recipient;

# COMMAND ----------

# DBTITLE 1,Step 6: Accessing the Shared Data (as a Recipient)
# MAGIC %md
# MAGIC The recipient will perform the following steps:
# MAGIC 
# MAGIC 1.  Open the activation link in a browser to download a credential file (`.share` format).
# MAGIC 2.  Use the credential file to access the shared data from their client of choice.

# COMMAND ----------

# DBTITLE 1,Example: Accessing with Python
# MAGIC %md
# MAGIC The recipient would run this code on their own machine (not in your Databricks workspace).

# COMMAND ----------

# First, install the Delta Sharing client
# pip install delta-sharing

import delta_sharing

# Path to the downloaded credential file
profile_file = "/path/to/your/config.share"

# Create a SharingClient
client = delta_sharing.SharingClient(profile_file)

# List all tables in the share
tables = client.list_all_tables()

# Create a url to access a table
# The url is pre-signed and can be used to load the data into a pandas DataFrame
url = delta_sharing.load_as_pandas_url(profile_file, table_name="gold_daily_sales", schema_name="default", share_name="my_awesome_share")

# Load the data into a pandas DataFrame
# In a real scenario, you would use a library like pandas to read the data from the url
# For this example, we will just print the url
print(url)

# COMMAND ----------

# DBTITLE 1,Best Practices Review
# MAGIC %md
# MAGIC ### Key Concepts Demonstrated
# MAGIC 
# MAGIC - **✅ Secure by Default**: Delta Sharing is secure by default. You must explicitly grant access to shares and recipients.
# MAGIC - **✅ Open Protocol**: Recipients can use any client that supports the open Delta Sharing protocol.
# MAGIC - **✅ Live Data**: The data is shared live. There are no data copies or replication pipelines to manage.
# MAGIC - **✅ Centralized Governance**: All sharing activities are managed and audited through Unity Catalog.

# MAGIC ### Important Considerations
# MAGIC 
# MAGIC - **Credential Management**: The recipient activation link is a one-time use link. The recipient is responsible for securely storing their credential file.
# MAGIC - **Network Egress**: While there are no storage costs for sharing data, you will be charged for network egress when recipients access the data.
# MAGIC - **Data Privacy**: Ensure that you are only sharing data that you are authorized to share and that you are complying with all relevant data privacy regulations.
