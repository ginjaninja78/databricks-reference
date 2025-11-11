---
title: ML Model Training with MLflow
parent: Databricks Cookbooks
nav_order: 3
---

# Cookbook: ML Model Training with MLflow

## 1. Problem Statement

You need a systematic and reproducible way to train, track, and manage machine learning models. This includes logging model parameters, metrics, and artifacts, as well as managing the model lifecycle from experimentation to production.

## 2. Solution Overview

This cookbook provides a comprehensive recipe for using **MLflow**, an open-source platform for the end-to-end machine learning lifecycle, on Databricks. MLflow is seamlessly integrated into the Databricks platform, providing a managed and collaborative environment for ML development.

This recipe demonstrates:

- **Experiment Tracking**: Logging model parameters, metrics, and artifacts using `mlflow.autolog()`.
- **Model Registration**: Registering the best model to the MLflow Model Registry.
- **Model Versioning**: Managing different versions of the model.
- **Model Staging**: Transitioning models between stages (e.g., Staging, Production).

## 3. Step-by-Step Implementation

This cookbook is implemented as a Python notebook that you can run directly in your Databricks workspace.

**Notebook**: [`01_ml_model_training_with_mlflow.py`](01_ml_model_training_with_mlflow.py)

### Key Concepts Demonstrated

- **Automatic Logging**: Using `mlflow.autolog()` to automatically log everything from your training session.
- **MLflow Runs**: Each training execution is captured as an MLflow Run.
- **MLflow Model Registry**: A centralized model store to manage the full lifecycle of MLflow Models.
- **Loading Models**: Loading a registered model for inference.

## 4. How to Use This Recipe

1.  **Import the Notebook**: Import the `01_ml_model_training_with_mlflow.py` notebook into your Databricks workspace.
2.  **Attach to a Cluster**: Attach the notebook to a cluster with a Databricks ML runtime (e.g., DBR ML 13.3 LTS).
3.  **Run the Notebook**: Run the cells in the notebook to train a model, track it with MLflow, and register it to the Model Registry.
4.  **Explore the MLflow UI**:
    - Click the **Experiment** icon in the notebook to view the MLflow runs.
    - Go to the **Models** tab in the Databricks workspace to see the registered model.

## 5. Best Practices & Customization

- **Use ML Runtimes**: Always use a Databricks ML runtime for machine learning workloads. They come pre-installed with all the necessary libraries (MLflow, scikit-learn, TensorFlow, PyTorch, etc.).
- **Autologging is Your Friend**: `mlflow.autolog()` is the easiest way to get started with experiment tracking. It supports most popular ML libraries.
- **Tag Your Runs**: Use `mlflow.set_tag()` to add custom tags to your runs for better organization and searchability.
- **CI/CD for Models**: Use the MLflow API to automate model registration and deployment as part of a CI/CD pipeline.
- **Attribution**: This recipe is based on best practices from the official MLflow and Databricks documentation.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
