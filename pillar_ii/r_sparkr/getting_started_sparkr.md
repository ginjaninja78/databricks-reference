---
title: Getting Started with SparkR
nav_order: 1
parent: R & SparkR for Statistical Computing
grand_parent: Pillar II The Developer's Toolkit
---

# Getting Started with SparkR

SparkR is an R package from the Apache Spark project that allows R users to run jobs on a Spark cluster. It provides a distributed DataFrame implementation that mirrors the concepts of the PySpark and Scala APIs, allowing you to leverage the full power of Spark's distributed engine from within a familiar R environment.

Databricks notebooks provide a seamless experience for using SparkR. When you create an R notebook, the Spark session is automatically initialized and connected for you.

## The SparkR Session

In a Databricks R notebook, the `spark` object is pre-configured and available for you to use. This is your gateway to the Spark cluster. You can use it to read data, create DataFrames, and configure your Spark session.

```R
# The spark object is already available in a Databricks R notebook
# You can view its configuration
sparkR.session()
```

## Creating a SparkR DataFrame

Similar to PySpark, the most common way to create a SparkR DataFrame is by reading from a data source. SparkR's `read.df` function is the primary tool for this.

### Reading from a Data Source

```R
# Reading a CSV file into a SparkR DataFrame
df <- read.df("/path/to/your/data.csv",
              source = "csv",
              header = "true",
              inferSchema = "true")

# The best practice is to read from a Delta Lake table
delta_df <- tableToDF("your_catalog.your_schema.your_table")

# Display the first few rows of the DataFrame
head(df)
```

### Creating from a Local R `data.frame`

For testing and examples, you can convert a local R `data.frame` into a distributed SparkR DataFrame using `as.DataFrame()` or `createDataFrame()`.

```R
# Create a local R data.frame
local_df <- data.frame(
  first_name = c("James", "Maria", "Robert"),
  last_name = c("Smith", "Garcia", "Jones"),
  age = c(30, 45, 25)
)

# Convert the local data.frame to a SparkR DataFrame
spark_df <- as.DataFrame(local_df)

# Show the structure of the SparkR DataFrame
printSchema(spark_df)

# Display the content
showDF(spark_df)
```

## Key Concepts: Lazy Evaluation

Just like in PySpark, operations in SparkR are **lazy**. When you apply a transformation (like a filter or select), SparkR does not execute the job immediately. Instead, it builds up a query plan. The computation is only triggered when an **action** is called.

-   **Transformations**: `select()`, `filter()`, `mutate()`, `groupBy()`
-   **Actions**: `head()`, `count()`, `collect()`, `write.df()`

```R
# Transformation 1: Select two columns
selected_df <- select(spark_df, "first_name", "age")

# Transformation 2: Filter for age > 28
filtered_df <- filter(selected_df, selected_df$age > 28)

# At this point, no work has been done. The query plan is built.

# Action: Collect the results back to the R driver as a local data.frame
results <- collect(filtered_df)

# The collect() action triggers the execution of the entire plan.
print(results)
```

Understanding this lazy evaluation model is crucial for writing efficient SparkR code. It allows Spark to optimize the entire query before execution.

## Interoperability with `dplyr`

SparkR has built-in support for many verbs from the popular `dplyr` package, allowing you to write more idiomatic R code. You can use `mutate()`, `filter()`, `select()`, `arrange()`, and `summarize()` directly on SparkR DataFrames.

```R
# Load the SparkR library which includes dplyr-like functions
library(SparkR)

# Use dplyr verbs to chain operations
result_df <- spark_df %>%
  filter(.$age > 28) %>%
  mutate(full_name = paste(.$first_name, .$last_name)) %>%
  select("full_name", "age") %>%
  arrange(desc(.$age))

# Trigger the computation with an action
head(result_df)
```

This `dplyr` integration provides a more natural and expressive way for R users to interact with distributed data, bridging the gap between familiar R syntax and the power of the Spark engine.
