---
title: The Medallion Architecture
nav_order: 3
has_children: true
parent: Pillar I The Databricks Universe
---

# The Medallion Architecture: Structuring the Lakehouse

The Medallion Architecture is a data design pattern that provides a simple, logical framework for structuring data in a Lakehouse. It aims to incrementally and progressively improve the quality, structure, and performance of data as it flows through the system. This pattern was popularized by Databricks and is a core concept for building robust and scalable data platforms.

The architecture is named for its three distinct layers, each representing a higher state of data quality:

*   **Bronze (Raw)**: The initial landing zone for raw source data.
*   **Silver (Cleansed & Conformed)**: A validated and enriched version of the data.
*   **Gold (Aggregated & Business-Ready)**: Highly refined, aggregated data ready for analytics and reporting.

This multi-layered approach provides numerous benefits, including data lineage, auditability, and the ability to recreate downstream tables if there are errors in the pipeline. It separates concerns, allowing data engineers to focus on ingestion and validation, while analysts work with clean, reliable, business-focused data.

This section provides a deep dive into each of these three layers, explaining their purpose, characteristics, and best practices for implementation.
