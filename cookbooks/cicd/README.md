---
title: CI/CD with GitHub Actions
parent: Databricks Cookbooks
nav_order: 8
---

# Cookbook: CI/CD with GitHub Actions

## 1. Problem Statement

You need to automate the testing and deployment of your Databricks notebooks and jobs. Manually deploying code is error-prone, slow, and not scalable. You want to adopt DevOps best practices for your data pipelines.

## 2. Solution Overview

This cookbook provides a production-ready recipe for setting up a Continuous Integration/Continuous Deployment (CI/CD) pipeline for your Databricks projects using **GitHub Actions**.

This recipe demonstrates how to create a workflow that automatically:

1.  **Validates** your notebooks for syntax errors and linting issues.
2.  **Deploys** your notebooks to a Databricks workspace.
3.  **Creates or updates** a Databricks Job to run your notebook.

This approach ensures that your code is always tested before deployment and that your production jobs are updated automatically and reliably.

## 3. Step-by-Step Implementation

This cookbook consists of a sample GitHub Actions workflow file that you can adapt for your own projects.

**Workflow File**: [`deploy_notebook_job.yml`](deploy_notebook_job.yml)

### Key Concepts Demonstrated

- **GitHub Actions Workflows**: Defining jobs, steps, and triggers.
- **Databricks CLI**: Using the Databricks CLI to interact with the Databricks API.
- **Environment Secrets**: Securely storing your Databricks host and token as GitHub secrets.
- **Multi-Environment Deployment**: A pattern for deploying to different environments (dev, staging, prod).
- **Automated Testing**: A basic validation step to catch errors early.

## 4. How to Use This Recipe

1.  **Create the Workflow File**: Create a file at `.github/workflows/deploy_notebook_job.yml` in your own repository and copy the contents of the [sample workflow file](deploy_notebook_job.yml).
2.  **Customize the Workflow**:
    -   Update the notebook path and job configuration to match your project.
    -   Adjust the triggers (e.g., `on: push: branches: [ main ]`) to fit your branching strategy.
3.  **Add GitHub Secrets**:
    -   In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
    -   Create secrets for `DATABRICKS_HOST` and `DATABRICKS_TOKEN`.
4.  **Push to GitHub**: Commit and push the workflow file to your repository. The workflow will run automatically on the next push to the specified branch.

## 5. Best Practices & Customization

- **Use a Service Principal**: For production workflows, it is highly recommended to use a Databricks service principal and its token instead of a personal access token.
- **Separate Dev/Prod Environments**: Use different Databricks workspaces or directories for your development and production environments. Use GitHub environments and secrets to manage the configuration for each.
- **Add More Tests**: This recipe includes a basic syntax check. For production pipelines, you should add more comprehensive tests, such as unit tests (with `pytest`) and integration tests.
- **Use Databricks Asset Bundles (DABs)**: For more complex projects, consider using Databricks Asset Bundles, which provide a more structured way to manage and deploy your assets.
- **Attribution**: This recipe is inspired by best practices from the Databricks documentation and the "GitHub Integration Bible" section of this repository.

---

**Need help?** Ask The LibrAIrian in GitHub Copilot or open an issue in this repository.
