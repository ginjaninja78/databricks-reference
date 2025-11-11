_# Databricks notebook source

# DBTITLE 1,Graph Analytics with GraphFrames
# MAGIC %md
# MAGIC # Cookbook: Graph Analytics with GraphFrames
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need to analyze relationships and connections within your data. This could be for use cases like social network analysis, fraud detection, or recommendation engines.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a recipe for performing graph analytics in Databricks using **GraphFrames**.
# MAGIC 
# MAGIC ## 3. How to Use This Recipe
# MAGIC 
# MAGIC 1.  **Install GraphFrames**: Install the `graphframes:graphframes` package from Maven on your cluster.
# MAGIC 2.  **Run this Notebook**: Execute the cells to create a sample graph and run various analyses.

# COMMAND ----------

# DBTITLE 1,Create Vertices and Edges
# Create a DataFrame for the vertices (nodes)
vertices = spark.createDataFrame([
    ("a", "Alice", 34),
    ("b", "Bob", 36),
    ("c", "Charlie", 30),
    ("d", "David", 29),
    ("e", "Esther", 32),
    ("f", "Fanny", 36)
], ["id", "name", "age"])

# Create a DataFrame for the edges (relationships)
edges = spark.createDataFrame([
    ("a", "b", "friend"),
    ("b", "c", "follow"),
    ("c", "b", "follow"),
    ("f", "c", "follow"),
    ("e", "f", "friend"),
    ("e", "d", "friend"),
    ("d", "a", "friend")
], ["src", "dst", "relationship"])

# COMMAND ----------

# DBTITLE 1,Create the GraphFrame
from graphframes import *

# Create a GraphFrame from the vertices and edges
g = GraphFrame(vertices, edges)

# COMMAND ----------

# DBTITLE 1,Basic Graph Queries
# Display the vertices and edges
display(g.vertices)
display(g.edges)

# Get the in-degree and out-degree of each vertex
display(g.inDegrees)
display(g.outDegrees)

# COMMAND ----------

# DBTITLE 1,PageRank Algorithm
# Run PageRank to determine the importance of each vertex
results = g.pageRank(resetProbability=0.15, tol=0.01)

# Display the results
display(results.vertices.select("id", "pagerank").orderBy(desc("pagerank")))

# COMMAND ----------

# DBTITLE 1,Breadth-First Search (BFS)
# Find the shortest path from "a" to all other vertices
results = g.bfs("id = \'a\'"))

display(results)

# COMMAND ----------

# DBTITLE 1,Triangle Counting
# Count the number of triangles passing through each vertex
# This is often used for community detection
results = g.triangleCount()

display(results.select("id", "count").orderBy(desc("count")))

# COMMAND ----------

# DBTITLE 1,Best Practices
# MAGIC %md
# MAGIC ### When to Use GraphFrames
# MAGIC 
# MAGIC - When your data has a natural graph structure (e.g., social networks, transaction data, network logs).
# MAGIC - When you need to answer questions about relationships, paths, and communities.
# MAGIC 
# MAGIC ### Performance Considerations
# MAGIC 
# MAGIC - Graph algorithms can be computationally expensive. Make sure your cluster is sized appropriately.
# MAGIC - For very large graphs, consider using a dedicated graph database.
# MAGIC 
# MAGIC ### Visualization
# MAGIC 
# MAGIC - For smaller graphs, you can convert the GraphFrame to a NetworkX graph and use `matplotlib` to visualize it.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on the official GraphFrames documentation.
