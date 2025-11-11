---
title: SparkR DataFrame Operations
nav_order: 2
parent: R & SparkR for Statistical Computing
grand_parent: Pillar II The Developer's Toolkit
---

# SparkR DataFrame Operations: A `dplyr`-like Approach

Manipulating SparkR DataFrames will feel familiar to any R user comfortable with `dplyr`. SparkR implements many of the same verbs and uses a similar chaining syntax with the `%>%` pipe operator. This allows you to write clean, readable, and expressive code to transform distributed data.

This guide covers the most common DataFrame operations using `dplyr`-style syntax.

### Our Sample Data

We'll use the same sales data as in the PySpark examples, now created as a SparkR DataFrame.

```R
# Create a local data.frame first
sales_data <- data.frame(
  order_id = c(101, 102, 103, 104, 105, 106, 107, 108),
  customer_id = c(1, 2, 1, 3, 2, 1, 4, 3),
  product_id = c(10, 20, 30, 10, 20, 40, 10, 20),
  quantity = c(2, 1, 5, 10, 2, 1, 3, 4),
  unit_price = c(12.50, 25.00, 2.75, 12.00, 24.50, 150.00, 12.50, 24.00),
  country = c("USA", "USA", "Canada", "Mexico", "USA", "Canada", "USA", "Mexico")
)

# Convert to a SparkR DataFrame
sales_df <- as.DataFrame(sales_data)
```

## 1. Selecting Columns: `select()`

Use `select()` to choose a subset of columns.

```R
# Select product_id and country
product_country_df <- select(sales_df, "product_id", "country")

head(product_country_df)
```

## 2. Creating New Columns: `mutate()`

Use `mutate()` to add new columns. The new column is defined as an expression of existing columns.

```R
# Create a new column 'total_price'
sales_with_total_df <- mutate(sales_df, total_price = sales_df$quantity * sales_df$unit_price)

head(sales_with_total_df)
```

## 3. Filtering Rows: `filter()`

Use `filter()` to select rows based on a logical condition.

```R
# Filter for sales in the USA with quantity > 1
usa_large_orders_df <- filter(sales_df, sales_df$country == "USA" & sales_df$quantity > 1)

head(usa_large_orders_df)
```

## 4. Aggregating Data: `groupBy()` and `summarize()`

This is a two-step process, just like in `dplyr`.

1.  `groupBy()`: Groups the DataFrame by one or more columns.
2.  `summarize()` (or `agg()`): Applies aggregation functions to the grouped data.

```R
# First, group by country
grouped_data <- groupBy(sales_df, sales_df$country)

# Then, summarize each group
country_summary_df <- summarize(
  grouped_data,
  total_sales = sum(sales_df$quantity * sales_df$unit_price),
  avg_quantity = avg(sales_df$quantity),
  num_orders = n(sales_df$order_id)
)

head(country_summary_df)
```

## 5. Sorting Data: `arrange()`

Use `arrange()` to sort the DataFrame by one or more columns. Use the `desc()` function for descending order.

```R
# Sort the summary by total_sales in descending order
sorted_summary_df <- arrange(country_summary_df, desc(country_summary_df$total_sales))

head(sorted_summary_df)
```

## 6. Joining DataFrames: `join()`

SparkR's `join()` function supports all standard join types.

```R
# Create a customers DataFrame
customer_data <- data.frame(
  customer_id = c(1, 2, 3, 5),
  customer_name = c("Alice", "Bob", "Charlie", "Eve")
)
customers_df <- as.DataFrame(customer_data)

# Perform an inner join
sales_with_customers_df <- join(
  sales_df,
  customers_df,
  sales_df$customer_id == customers_df$customer_id, # Join condition
  joinType = "inner"
)

head(sales_with_customers_df)
```

## Chaining Operations with `%>%`

These operations become even more powerful when chained together with the pipe operator.

**Question**: "What are the total sales for each customer, for customers in the USA, sorted from highest to lowest?"

```R
# Ensure the library is loaded to use the pipe
library(SparkR)

customer_sales_usa_df <- sales_df %>%
  # 1. Filter for USA
  filter(.$country == "USA") %>%
  # 2. Create total_price column
  mutate(total_price = .$quantity * .$unit_price) %>%
  # 3. Group by customer
  groupBy(.$customer_id) %>%
  # 4. Summarize to get total sales
  summarize(total_sales_usd = sum(.$total_price)) %>%
  # 5. Arrange by sales in descending order
  arrange(desc(.$total_sales_usd))

# Action: Show the final result
head(customer_sales_usa_df)
```

This example shows how you can write complex, distributed data transformations using the same elegant and readable syntax that has made `dplyr` a favorite in the R community. SparkR effectively translates these familiar R commands into a high-performance Spark execution plan.
