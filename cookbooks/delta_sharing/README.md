---
title: Delta Sharing
parent: Databricks Cookbooks
nav_order: 16
---

# Cookbook: Secure Data Sharing with Delta Sharing

## 1. Problem Statement

You need to securely share live data from your data lakehouse with external partners, customers, or other departments within your organization, without having to copy or move the data. The recipients may or may not be on Databricks.

## 2. Solution Overview

This cookbook provides a practical guide to using **Delta Sharing**, an open protocol for secure data sharing from Databricks.

Delta Sharing allows you to share read-only access to tables in your lakehouse with any recipient, regardless of the platform they use. The data is shared live, so recipients always have access to the latest version.

This recipe demonstrates:

1.  **Creating a Share**: A logical container for the tables you want to share.
2.  **Adding Tables to a Share**: Selecting the data to be shared.
3.  **Creating a Recipient**: Defining who you are sharing the data with.
4.  **Granting Access**: Granting the recipient access to the share.
5.  **Accessing Shared Data**: How a recipient can access the data using various clients (e.g., pandas, Power BI, Spark).

## 3. Step-by-Step Implementation

This cookbook is a Python notebook that walks through the process of sharing and accessing data with Delta Sharing.

**Notebook**: [`01_delta_sharing.py`](01_delta_sharing.py)

### Key Concepts Demonstrated

- **Shares**: The core object for grouping tables for sharing.
- **Recipients**: The entities (users, service principals) you share data with.
- **Activation Links**: A one-time link for recipients to download their credentials.
- **Open Protocol**: The ability to access shared data from any platform that supports the Delta Sharing protocol.

## 4. How to Use This Recipe

1.  **Prerequisites**: You must have the `CREATE SHARE` and `CREATE RECIPIENT` privileges in Unity Catalog.
2.  **Import the Notebook**: Import the `01_delta_sharing.py` notebook into your workspace.
3.  **Run the Notebook**: Execute the cells to create a share, add a table, create a recipient, and grant access.
4.  **Access as a Recipient**: Follow the instructions in the notebook to download the recipient credentials and access the shared data from a Python client.

## 5. Best Practices & Customization

- **Share at the Right Granularity**: You can share entire tables or specific partitions of a table. Choose the granularity that meets your security and business requirements.
- **Use IP Access Lists**: For added security, you can restrict recipient access to a specific range of IP addresses.
- **Monitor Usage**: Use the audit logs to monitor who is accessing your shared data and when.
- **Rotate Credentials**: For long-term sharing relationships, establish a process for rotating recipient credentials periodically.
- **Attribution**: This recipe is based on the official Databricks documentation for Delta Sharing.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
