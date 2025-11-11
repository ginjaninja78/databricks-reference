---
title: CLI & REST API Automation
parent: Databricks Cookbooks
nav_order: 15
---

# Cookbook: Databricks CLI & REST API Automation

## 1. Problem Statement

You need to automate administrative and operational tasks in Databricks, such as creating clusters, managing jobs, and configuring permissions. Performing these tasks manually through the UI is not scalable or repeatable.

## 2. Solution Overview

This cookbook provides a practical guide for using the **Databricks CLI** and **REST API** to automate your Databricks environment. This is a critical skill for DevOps engineers, data platform administrators, and anyone responsible for managing a Databricks workspace.

This recipe demonstrates how to:

1.  **Set up Authentication**: Configure the CLI and prepare for REST API calls using a personal access token or service principal.
2.  **Script Common Tasks**: Provide shell script and Python examples for common automation scenarios.
    -   Managing clusters (create, start, stop)
    -   Deploying and running jobs
    -   Managing workspace objects (notebooks, libraries)

## 3. Step-by-Step Implementation

This cookbook consists of a series of shell scripts and Python scripts that you can adapt and run.

**Scripts**:
- [`01_cluster_management.sh`](01_cluster_management.sh): A shell script for managing clusters.
- [`02_job_management.py`](02_job_management.py): A Python script for managing jobs using the Databricks SDK.

### Key Concepts Demonstrated

- **Databricks CLI**: Using commands like `databricks clusters create` and `databricks jobs run-now`.
- **Databricks REST API**: Making direct calls to the API endpoints using tools like `curl` or Python's `requests` library.
- **Databricks SDK for Python**: A convenient Python wrapper for the REST API.
- **JSON Definitions**: Defining resources like clusters and jobs as JSON files for infrastructure-as-code.

## 4. How to Use This Recipe

1.  **Install the Databricks CLI**: Follow the [official instructions](https://docs.databricks.com/en/dev-tools/cli/index.html) to install and configure the CLI.
2.  **Install the Databricks SDK for Python**: `pip install databricks-sdk`
3.  **Review the Scripts**: Examine the provided shell and Python scripts to understand the patterns.
4.  **Customize and Run**: Adapt the scripts for your own environment and run them from your local machine or a CI/CD pipeline.

## 5. Best Practices & Customization

- **Use Service Principals for Automation**: For any automated workflow (especially in production), always use a service principal and its token for authentication. This is more secure and avoids tying automation to a specific user account.
- **Infrastructure as Code (IaC)**: Store your cluster and job definitions as JSON files in a Git repository. This allows you to version control your infrastructure and apply changes systematically.
- **Use the SDK for Complex Logic**: While the CLI is great for simple tasks, the Databricks SDK for Python is better suited for more complex automation logic that requires branching, looping, or error handling.
- **Error Handling**: In your scripts, always include robust error handling to catch and manage API failures.
- **Attribution**: This recipe is based on common automation patterns and best practices from the Databricks documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
