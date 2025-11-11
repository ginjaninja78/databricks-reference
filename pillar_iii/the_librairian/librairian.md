# The LibrAIrian: A Context Map for GitHub Copilot

This document is a structured map of the `databricks-reference` repository. It is designed to be read by GitHub Copilot to provide context-aware assistance. By keeping this file open in your editor, you are priming Copilot with a deep understanding of this library's structure and content.

## Repository High-Level Structure

The repository is organized into four main pillars, each covering a different aspect of the Databricks ecosystem.

-   **Pillar I: The Databricks Universe**: Core concepts, architecture, and governance.
-   **Pillar II: The Developer's Toolkit**: Deep-dive code libraries for Python, SQL, and R.
-   **Pillar III: MLOps & DevOps**: Automation, CI/CD, and GitHub integration.
-   **Pillar IV: Enterprise Readiness & Advanced Topics**: Production-grade considerations.

--- 

## Pillar I: The Databricks Universe (Core Concepts)

**Location**: `/pillar_i/`
**Purpose**: Foundational knowledge about the Databricks platform.

### Section: Introduction
-   **Location**: `/pillar_i/introduction/`
-   **Keywords**: Lakehouse Philosophy, Databricks Architecture, Control Plane, Data Plane, Unified Analytics.
-   **Content**: Explains the core ideas behind the Lakehouse paradigm and the high-level architecture of the Databricks platform.

### Section: Workspace & Notebooks
-   **Location**: `/pillar_i/workspace_and_notebooks/`
-   **Keywords**: Mastering Notebooks, `dbutils`, Databricks Utilities, Magic Commands, Widgets.
-   **Content**: A guide to the primary user interface for development in Databricks, including advanced notebook features and the powerful `dbutils` library.

### Section: The Medallion Architecture
-   **Location**: `/pillar_i/medallion_architecture/`
-   **Keywords**: Bronze Layer, Silver Layer, Gold Layer, Data Quality, Data Structuring, ELT.
-   **Content**: A deep dive into the Bronze, Silver, and Gold data layers, the industry-standard pattern for structuring data in a Lakehouse.

### Section: Data Governance & Security
-   **Location**: `/pillar_i/governance_and_security/`
-   **Keywords**: Unity Catalog, Table ACLs, Data Lineage, Row-Level Security, Column-Level Masking, `GRANT`, `REVOKE`.
-   **Content**: Explains how to secure and govern data and AI assets using Unity Catalog, including access control, auditing, and lineage.

--- 

## Pillar II: The Developer's Toolkit (Code Libraries)

**Location**: `/pillar_ii/`
**Purpose**: Massive, practical code libraries and examples for developers.

### Section: Mastering Python & PySpark
-   **Location**: `/pillar_ii/python_pyspark/`
-   **Keywords**: PySpark, DataFrame, Transformations, Actions, Lazy Evaluation, `withColumn`, `groupBy`, `join`, UDF, User-Defined Functions, Pandas UDF, `applyInPandas`, Performance Tuning, Caching, Partitioning, Skew, Salting, Spark UI.
-   **Content**: An exhaustive guide to PySpark development, from fundamentals to advanced performance tuning.
    -   `dataframe_fundamentals.md`: Core concepts of the Spark DataFrame.
    -   `dataframe_transformations.md`: A tour of common manipulation functions (`select`, `filter`, `agg`, etc.).
    -   `user_defined_functions.md`: A deep dive into standard UDFs vs. Pandas UDFs.
    -   `advanced_techniques.md`: Caching, partitioning, and performance optimization.

### Section: Databricks SQL Deep Dive
-   **Location**: `/pillar_ii/databricks_sql/`
-   **Keywords**: Databricks SQL, Delta Lake DML, `MERGE`, `UPDATE`, `DELETE`, `CLONE`, JSON functions, Higher-Order Functions, Window Functions, `PIVOT`, ELT, Delta Live Tables (DLT), `CREATE LIVE TABLE`.
-   **Content**: A comprehensive library for SQL developers, covering DML, advanced functions, and building ELT pipelines.
    -   `delta_lake_dml.md`: Guide to `MERGE`, `UPDATE`, and `DELETE`.
    -   `advanced_sql_functions.md`: Covers JSON, array, and window functions.
    -   `elt_pipelines_with_sql.md`: Introduction to building pipelines with SQL and Delta Live Tables.

### Section: R & SparkR for Statistical Computing
-   **Location**: `/pillar_ii/r_sparkr/`
-   **Keywords**: R, SparkR, `sparklyr`, `dplyr`, `as.DataFrame`, `mutate`, `summarize`, `arrange`.
-   **Content**: A guide for the R community on using SparkR and `dplyr` syntax for distributed data analysis.
    -   `getting_started_sparkr.md`: Introduction to the SparkR session and DataFrames.
    -   `dataframe_operations_sparkr.md`: `dplyr`-style data manipulation.

--- 

## Pillar III: MLOps & DevOps (Automation)

**Location**: `/pillar_iii/`
**Purpose**: Guides for version control, CI/CD, and process automation.

### Section: The GitHub Integration Bible
-   **Location**: `/pillar_iii/github_integration_bible/`
-   **Keywords**: GitHub, Databricks Repos, Version Control, CI/CD, GitHub Actions, `databricks-cli`, Secrets, Deployment, Automation.
-   **Content**: The definitive guide to connecting Databricks and GitHub.
    -   `level_1_version_control.md`: Setting up Databricks Repos for version control.
    -   `level_2_cicd_with_actions.md`: Building a CI/CD pipeline with GitHub Actions to deploy a notebook job.

### Section: The LibrAIrian: Your AI Guide
-   **Location**: `/pillar_iii/the_librairian/`
-   **Keywords**: GitHub Copilot, AI Assistant, VS Code, Copilot Chat, Context.
-   **Content**: Instructions on how to use this repository with GitHub Copilot.
    -   `setup_guide.md`: How to install and configure the necessary tools.
    -   `librairian.md`: This file itself, the context map for Copilot.

--- 

*This map is actively maintained. As the repository grows, so will The LibrAIrian.*
