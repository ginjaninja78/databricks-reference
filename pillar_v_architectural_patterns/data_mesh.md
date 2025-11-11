---
title: Data Mesh on Databricks
parent: Pillar V: Architectural Patterns
nav_order: 1
---

# Architectural Pattern: Data Mesh on Databricks

## 1. What is Data Mesh?

Data Mesh is a sociotechnical paradigm for managing data at scale. It challenges the traditional, centralized data platform model (like a monolithic data warehouse or data lake) and advocates for a decentralized, domain-oriented approach.

The four core principles of Data Mesh are:

1.  **Domain-Oriented Ownership**: Data is owned and managed by the business domains that produce it.
2.  **Data as a Product**: Data should be treated as a product, with a focus on quality, discoverability, and usability.
3.  **Self-Serve Data Platform**: A central platform team provides the tools and infrastructure to enable domain teams to manage their own data products.
4.  **Federated Computational Governance**: A set of global rules and standards are defined and enforced across all data products.

## 2. Implementing Data Mesh on Databricks

The Databricks Lakehouse Platform is uniquely suited to implementing a Data Mesh architecture. Here’s how Unity Catalog and other Databricks features map to the four principles:

### Domain-Oriented Ownership

- **Unity Catalog**: Create a separate catalog for each business domain (e.g., `sales`, `marketing`, `finance`).
- **Permissions**: Delegate ownership of each catalog to the corresponding domain team, giving them full control over the schemas and tables within their domain.

### Data as a Product

- **Delta Lake**: The foundation for creating high-quality, reliable data products with ACID transactions, schema enforcement, and time travel.
- **Unity Catalog**: Provides a centralized place to discover, search, and understand data products across all domains.
- **Data Lineage**: Automatically captures and visualizes lineage, helping consumers understand the origin and transformations of the data.

### Self-Serve Data Platform

- **Databricks Workspaces**: Provide domain teams with their own workspaces, pre-configured with the necessary tools and libraries.
- **Cluster Policies**: Define and enforce standards for cluster configurations, ensuring cost control and governance.
- **Databricks CLI/API & Terraform**: Enable automation and infrastructure-as-code for managing the platform.

### Federated Computational Governance

- **Unity Catalog**: The central hub for defining and enforcing global governance policies.
- **Access Control**: Use Unity Catalog to manage permissions on data products.
- **Tags and ABAC**: Use tags to classify data and implement attribute-based access control for scalable governance.
- **Audit Logs**: Monitor access and activities across the entire platform.

## 3. Example Data Mesh Structure in Unity Catalog

```
unity_catalog
├── sales_catalog
│   ├── silver_schema
│   │   └── transactions
│   └── gold_schema
│       └── daily_sales_agg
├── marketing_catalog
│   ├── silver_schema
│   │   └── campaign_data
│   └── gold_schema
│       └── campaign_performance
└── finance_catalog
    ├── silver_schema
    │   └── financial_statements
    └── gold_schema
        └── quarterly_revenue
```

In this example:

- Each business domain (`sales`, `marketing`, `finance`) has its own catalog.
- The domain teams are responsible for creating and managing the data products (tables) within their catalog.
- Data consumers from other domains can discover and request access to these data products through Unity Catalog.

## 4. Best Practices

- **Start Small**: Begin with one or two domains and gradually expand your Data Mesh implementation.
- **Invest in Platform Engineering**: A strong central platform team is essential for providing the self-serve tools and infrastructure that domain teams need.
- **Focus on Data Products**: Encourage domain teams to think of their data as a product, with a focus on quality, documentation, and usability.
- **Establish a Governance Council**: Create a cross-functional governance council to define and evolve your global rules and standards.
