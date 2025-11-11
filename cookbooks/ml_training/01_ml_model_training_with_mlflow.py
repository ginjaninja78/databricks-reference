_# Databricks notebook source

# DBTITLE 1,ML Model Training with MLflow
# MAGIC %md
# MAGIC # Cookbook: ML Model Training with MLflow
# MAGIC 
# MAGIC ## 1. Problem Statement
# MAGIC 
# MAGIC You need a systematic and reproducible way to train, track, and manage machine learning models. This includes logging model parameters, metrics, and artifacts, as well as managing the model lifecycle from experimentation to production.
# MAGIC 
# MAGIC ## 2. Solution Overview
# MAGIC 
# MAGIC This cookbook provides a comprehensive recipe for using **MLflow**, an open-source platform for the end-to-end machine learning lifecycle, on Databricks. MLflow is seamlessly integrated into the Databricks platform, providing a managed and collaborative environment for ML development.
# MAGIC 
# MAGIC This recipe demonstrates:
# MAGIC 
# MAGIC - **Experiment Tracking**: Logging model parameters, metrics, and artifacts using `mlflow.autolog()`.
# MAGIC - **Model Registration**: Registering the best model to the MLflow Model Registry.
# MAGIC - **Model Versioning**: Managing different versions of the model.
# MAGIC - **Model Staging**: Transitioning models between stages (e.g., Staging, Production).
# MAGIC 
# MAGIC ## 3. How to Use This Recipe
# MAGIC 
# MAGIC 1.  **Attach to a Cluster**: Attach this notebook to a cluster with a Databricks ML runtime (e.g., DBR ML 13.3 LTS).
# MAGIC 2.  **Run the Notebook**: Run the cells in this notebook to train a model, track it with MLflow, and register it to the Model Registry.

# COMMAND ----------

# DBTITLE 1,Import Libraries
import mlflow
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# COMMAND ----------

# DBTITLE 1,Generate Sample Data
# Generate some sample data for a binary classification problem
np.random.seed(42)
X = np.random.rand(100, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# COMMAND ----------

# DBTITLE 1,Enable MLflow Autologging
# MLflow autologging will automatically log parameters, metrics, and the model
mlflow.autolog()

# COMMAND ----------

# DBTITLE 1,Train the Model
with mlflow.start_run() as run:
  # Create and train the model
  model = LogisticRegression()
  model.fit(X_train, y_train)

  # Make predictions
  y_pred = model.predict(X_test)

  # Calculate accuracy
  accuracy = accuracy_score(y_test, y_pred)
  print(f"Accuracy: {accuracy}")

  # The accuracy will be automatically logged by MLflow

# COMMAND ----------

# DBTITLE 1,Register the Model
# Get the run ID from the last run
run_id = run.info.run_id

# Construct the model URI
model_uri = f"runs:/{run_id}/model"

# Register the model to the MLflow Model Registry
model_name = "my-classification-model"
registered_model = mlflow.register_model(model_uri, model_name)

print(f"Model registered with name: {model_name}, version: {registered_model.version}")

# COMMAND ----------

# DBTITLE 1,Load the Registered Model for Inference
# Load the model from the Model Registry
model_version = registered_model.version
loaded_model = mlflow.pyfunc.load_model(f"models:/{model_name}/{model_version}")

# Perform inference
predictions = loaded_model.predict(X_test)
print(predictions)

# COMMAND ----------

# DBTITLE 1,Next Steps & Best Practices
# MAGIC %md
# MAGIC ### Next Steps
# MAGIC 
# MAGIC - **Transition Model Stage**: Go to the **Models** tab in the Databricks workspace, find your model, and transition it to "Staging" or "Production".
# MAGIC - **Serve the Model**: Use Databricks Model Serving to deploy your model as a REST API.
# MAGIC - **Automate with CI/CD**: Use the MLflow API to automate model registration and deployment as part of a CI/CD pipeline.
# MAGIC 
# MAGIC ### Best Practices Demonstrated
# MAGIC 
# MAGIC - **Use ML Runtimes**: Using a Databricks ML runtime simplifies dependency management.
# MAGIC - **Autologging**: `mlflow.autolog()` is the easiest way to ensure comprehensive experiment tracking.
# MAGIC - **Model Registry**: The Model Registry is the source of truth for production models.
# MAGIC - **Separation of Training and Inference**: The notebook separates the training logic from the inference logic, which is a best practice for productionizing models.
# MAGIC 
# MAGIC ### Attribution
# MAGIC 
# MAGIC This recipe is based on best practices from the official MLflow and Databricks documentation. It provides a foundational workflow for most ML projects.
