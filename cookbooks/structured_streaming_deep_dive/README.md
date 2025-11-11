---
title: Structured Streaming Deep Dive
parent: Databricks Cookbooks
nav_order: 14
---

# Cookbook: Structured Streaming Deep Dive

## 1. Problem Statement

You need to build custom, real-time data processing applications that go beyond the declarative framework of Delta Live Tables. You require fine-grained control over the streaming logic, state management, and output sinks.

## 2. Solution Overview

This cookbook provides a deep dive into **Structured Streaming**, the core stream processing engine in Apache Spark. While DLT is recommended for most ETL pipelines, understanding Structured Streaming is essential for building advanced streaming applications.

This recipe demonstrates:

- **The Core Concepts**: Understanding the streaming DataFrame/Dataset API.
- **Windowing**: Performing aggregations over sliding or tumbling windows.
- **Watermarking**: Handling late-arriving data gracefully.
- **Multiple Output Sinks**: Writing to various sinks like Delta Lake, Kafka, or a foreach sink for custom logic.

## 3. Step-by-Step Implementation

This cookbook is a Python notebook that provides a detailed, hands-on exploration of Structured Streaming.

**Notebook**: [`01_structured_streaming_deep_dive.py`](01_structured_streaming_deep_dive.py)

### Key Concepts Demonstrated

- **Input Sources**: Reading from streaming sources like rate (for testing) or Kafka.
- **Transformations on Streaming DataFrames**: Applying standard DataFrame operations to streaming data.
- **Stateful Streaming**: Using `groupBy` and `agg` on a streaming DataFrame.
- **Output Modes**: Understanding `append`, `complete`, and `update` output modes.

## 4. How to Use This Recipe

1.  **Import the Notebook**: Import the `01_structured_streaming_deep_dive.py` notebook into your workspace.
2.  **Attach to a Cluster**: Attach the notebook to any standard Databricks cluster.
3.  **Run the Notebook**: Execute the cells to see the various Structured Streaming concepts in action. The notebook uses the built-in `rate` source, so no external data setup is required.

## 5. Best Practices & Customization

- **When to Use Structured Streaming vs. DLT**: 
    - Use **DLT** for most ETL/ELT pipelines. Its declarative nature, built-in data quality, and automatic orchestration simplify development and management.
    - Use **Structured Streaming** directly when you need custom state management, complex event-time processing, or need to write to a sink not natively supported by DLT.
- **Manage Your Checkpoints**: The checkpoint location is critical for fault tolerance and state management. Ensure it is on reliable cloud storage.
- **Monitor Your Streams**: Use the Spark UI and streaming query listener to monitor the progress, latency, and throughput of your streaming queries.
- **Attribution**: This recipe is based on the official Apache Spark Structured Streaming Programming Guide and best practices from the Databricks documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
