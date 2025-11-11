---
title: R & SparkR for Statistical Computing
nav_order: 3
has_children: true
parent: Pillar II The Developer's Toolkit
---

# R & SparkR for Statistical Computing on the Lakehouse

For decades, R has been the language of choice for statisticians, researchers, and data scientists who need a rich ecosystem for statistical modeling, data visualization, and exploratory data analysis. Databricks fully supports R as a first-class language, enabling users to leverage the power of distributed computing with Spark while staying within the familiar and powerful R environment.

This section is a dedicated guide for the R community. We will explore the two primary ways to use R with Spark in Databricks:

1.  **SparkR**: An R package that provides a light-weight frontend to use Apache Spark from R. It provides a distributed data frame implementation that supports operations like selection, filtering, and aggregation (similar to R's `data.frames`, but on large datasets).
2.  **sparklyr**: Another R interface to Spark, developed by RStudio, that provides a more `dplyr`-idiomatic interface to Spark. It's known for its compatibility with the `tidyverse` ecosystem.

This guide will provide practical examples and best practices for using both packages to perform large-scale data analysis, manipulation, and modeling on the Databricks Lakehouse Platform.

### Core Topics Covered:

*   **Getting Started with SparkR**: Setting up your environment and understanding the core concepts of using R in a distributed context.
*   **SparkR DataFrame Operations**: A guide to manipulating distributed data using SparkR's DataFrame API, drawing parallels to native R `data.frames` and `dplyr`.
*   **Distributed Machine Learning with SparkR**: Leveraging Spark's MLlib to train machine learning models on massive datasets directly from R.
*   **Using `sparklyr`**: An introduction to the `sparklyr` package and its `dplyr`-backend for a tidyverse-native experience.
