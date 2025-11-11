# The Ultimate Databricks Reference Library

**A comprehensive, exhaustive guide for developers migrating to and mastering Databricks.**

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://ginjaninja78.github.io/databricks-reference/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

**📖 [Quick Reference Cheat Sheet](QUICK_REFERENCE.md)** • **🎨 [Visual Banner](BANNER.md)** • **🤖 [Meet The LibrAIrian](.github/LibrAIrian.agent.md)**

---

## 🎯 Purpose

This repository is designed as a **portfolio-grade, enterprise-ready resource** for data engineers, data scientists, and developers at all levels who are:

- **Migrating** from traditional SQL databases, data warehouses, or Snowflake to Databricks
- **Onboarding** to the Databricks Lakehouse platform
- **Mastering** advanced Databricks features, Delta Lake, and the Medallion Architecture
- **Integrating** Databricks with Power BI, Power Platform, GitHub, and enterprise tooling
- **Building** production-grade data pipelines with best practices

This is not a quick-start guide. This is an **exhaustive library** with deep explainers, massive code samples, and real-world enterprise patterns.

---

## 🤖 Meet "The LibrAIrian" - Your AI-Powered Guide

This repository features **"The LibrAIrian"**, an innovative AI-assisted navigation system designed to work with **GitHub Copilot** in VS Code.

The LibrAIrian helps you:
- **Navigate** this massive repository intelligently
- **Find** exactly the code examples, notebooks, or documentation you need
- **Generate** Databricks-specific code following this project's conventions
- **Learn** interactively by asking questions grounded in the repository's content

### How to Use The LibrAIrian

1. **Open this repository in VS Code** with GitHub Copilot enabled
2. **Open the Copilot Chat panel** (Ctrl+Shift+I or Cmd+Shift+I)
3. **Ask questions** referencing The LibrAIrian's knowledge base:

```
@workspace #file:.librAIrian/navigator.md Where can I find examples of connecting Power BI to Databricks?
```

```
@workspace #file:.librAIrian/manifest.md I need to migrate a stored procedure from SQL Server. Which documents should I read?
```

```
@workspace #file:.librAIrian/code_conventions.md Generate a PySpark script to read a CSV file and write it to a Delta table, following the project's coding standards.
```

**Learn more:** [The LibrAIrian Documentation](.librAIrian/README.md)

---

## 📚 Repository Structure

This repository is organized into **Four Pillars**, each representing a major domain of Databricks expertise:

### **Pillar I: The Databricks Universe** - Core Concepts
Foundational knowledge about the Lakehouse architecture, Databricks workspaces, notebooks, and the Medallion (Bronze/Silver/Gold) data model.

📂 [`pillar_i/`](pillar_i/)

### **Pillar II: The Developer's Toolkit** - Code & Languages
Deep dives into PySpark, SQL, R, and Scala with massive libraries of code examples and notebooks for developers at all levels.

📂 [`pillar_ii/`](pillar_ii/)

### **Pillar III: MLOps & DevOps** - GitHub Integration & Automation
The complete guide to integrating Databricks with GitHub, CI/CD pipelines, GitHub Actions, and the GitHub Copilot prompt library.

📂 [`pillar_iii/`](pillar_iii/)

### **Pillar IV: Enterprise Readiness** - Advanced Topics
Power BI/Power Platform integration, Delta Lake internals, Unity Catalog, security, governance, and cost optimization.

📂 [`pillar_iv/`](pillar_iv/)

---

## 🚀 Quick Start

### For Beginners
Start with [Pillar I: Introduction to Databricks](pillar_i/introduction/README.md) to understand the fundamentals.

### For Migrators
Jump to the [SQL Migration Guide](pillar_ii/sql_on_lakehouse/migration_guides/README.md) for your specific source system (SQL Server, Oracle, Teradata, etc.).

### For Advanced Users
Explore [Delta Lake Deep Dive](pillar_iv/delta_lake/README.md) or [CI/CD with GitHub Actions](pillar_iii/github_integration/cicd_github_actions.md).

### For Power Platform Users
See [Power BI Integration](pillar_iv/bi_power_platform/power_bi_integration.md) and [Power Automate with Databricks](pillar_iv/bi_power_platform/power_automate_integration.md).

---

## 📖 Documentation Site

This repository is published as a **GitHub Pages site** for easy navigation and reading:

🌐 **[https://ginjaninja78.github.io/databricks-reference/](https://ginjaninja78.github.io/databricks-reference/)**

---

## 🧪 Sample Code & Notebooks

This repository includes hundreds of ready-to-use examples:

- **Sample Notebooks**: [`sample_notebooks/`](sample_notebooks/) - Jupyter/Databricks notebooks for Bronze, Silver, Gold layers and advanced scenarios
- **Python Code**: [`sample_code/python/`](sample_code/python/) - Standalone Python scripts and modules
- **R Code**: [`sample_code/r/`](sample_code/r/) - SparkR and sparklyr examples
- **Scala Code**: [`sample_code/scala/`](sample_code/scala/) - High-performance Scala examples
- **SQL Scripts**: [`sample_code/sql/`](sample_code/sql/) - Databricks SQL queries and migration patterns

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing a typo, adding a new example, or writing an entire section, your input is valued.

Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request.

---

## 📋 Table of Contents

### Pillar I: The Databricks Universe
- [Introduction to the Lakehouse](pillar_i/introduction/lakehouse_philosophy.md)
- [Databricks Architecture](pillar_i/introduction/databricks_architecture.md)
- [Mastering Notebooks](pillar_i/workspace_and_notebooks/mastering_notebooks.md)
- [The Medallion Architecture](pillar_i/medallion_architecture/README.md)
  - [Bronze Layer Deep Dive](pillar_i/medallion_architecture/bronze_layer.md)
  - [Silver Layer Deep Dive](pillar_i/medallion_architecture/silver_layer.md)
  - [Gold Layer Deep Dive](pillar_i/medallion_architecture/gold_layer.md)

### Pillar II: The Developer's Toolkit
- [PySpark Mastery](pillar_ii/pyspark_mastery/README.md)
  - [Foundations](pillar_ii/pyspark_mastery/foundations.md)
  - [Advanced Techniques](pillar_ii/pyspark_mastery/advanced_techniques.md)
  - [Code Library](pillar_ii/pyspark_mastery/code_library/README.md)
- [SQL on the Lakehouse](pillar_ii/sql_on_lakehouse/README.md)
  - [Databricks SQL Deep Dive](pillar_ii/sql_on_lakehouse/databricks_sql_deep_dive.md)
  - [Migration Guides](pillar_ii/sql_on_lakehouse/migration_guides/README.md)
  - [Query Optimization](pillar_ii/sql_on_lakehouse/query_optimization.md)
- [R and Scala for Specialists](pillar_ii/r_and_scala/README.md)

### Pillar III: MLOps & DevOps
- [The GitHub Integration Bible](pillar_iii/github_integration/README.md)
  - [Databricks Repos Setup](pillar_iii/github_integration/databricks_repos_setup.md)
  - [CI/CD with GitHub Actions](pillar_iii/github_integration/cicd_github_actions.md)
  - [GitHub Actions Cookbook](pillar_iii/github_integration/github_actions_cookbook/README.md)
  - [GitHub Copilot Prompt Library](pillar_iii/github_integration/copilot_prompts/README.md)

### Pillar IV: Enterprise Readiness
- [Power BI Integration](pillar_iv/bi_power_platform/power_bi_integration.md)
- [Power Platform Integration](pillar_iv/bi_power_platform/power_platform_integration.md)
- [Delta Lake Deep Dive](pillar_iv/delta_lake/README.md)
- [Unity Catalog & Governance](pillar_iv/governance_security/unity_catalog.md)
- [Security Best Practices](pillar_iv/governance_security/security_best_practices.md)
- [Databricks Workflows](pillar_iv/workflows/databricks_workflows.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This repository is a community-driven effort to democratize Databricks knowledge and accelerate enterprise adoption of the Lakehouse paradigm.

Special thanks to all contributors, reviewers, and the Databricks community.

---

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/ginjaninja78/databricks-reference/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ginjaninja78/databricks-reference/discussions)
- **Pull Requests**: [Contributing Guide](CONTRIBUTING.md)

---

**Built with ❤️ for the data community**
