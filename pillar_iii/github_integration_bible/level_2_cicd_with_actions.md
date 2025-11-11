---
title: Level 2 CI/CD with GitHub Actions
nav_order: 2
parent: The GitHub Integration Bible
grand_parent: Pillar III MLOps & DevOps
---

# Level 2: Automation with CI/CD & GitHub Actions

Version control is the foundation, but **automation** is where you unlock true DevOps power. Continuous Integration (CI) and Continuous Deployment (CD) are practices that automate the testing and deployment of your code, reducing manual errors, improving quality, and accelerating your development velocity.

In the context of Databricks, a CI/CD pipeline typically means:

-   **On a Pull Request or Commit**: Automatically run tests on your notebooks and libraries.
-   **On a Merge to `main`**: Automatically deploy your project (notebooks, DLT pipelines, jobs) to a Databricks workspace (e.g., a development or staging environment).

**GitHub Actions** is a powerful and flexible CI/CD platform built directly into GitHub. We will use it to build a complete, automated deployment pipeline for our Databricks assets.

## The Goal: Automated Deployment of a Notebook Job

Our objective is to create a GitHub Actions workflow that automatically deploys a Databricks job based on a notebook from our repository. The workflow will trigger whenever code is merged into the `main` branch.

This workflow will:

1.  Trigger on a `push` to the `main` branch.
2.  Check out the repository code.
3.  Set up the Databricks CLI.
4.  Use the Databricks CLI to create or update a job in our Databricks workspace, pointing it to the notebook in the repo.

## Step 1: Storing Databricks Credentials as GitHub Secrets

You must **never** hardcode credentials like API tokens in your code or workflow files. GitHub Secrets provide a secure way to store and use sensitive information in your workflows.

1.  **Databricks Host**: This is the URL of your Databricks workspace (e.g., `https://dbc-a1b2345c-d6e7.cloud.databricks.com`).
2.  **Databricks Token**: This is a Personal Access Token (PAT) you generate from your Databricks workspace. It's recommended to create a token specifically for your CI/CD pipeline using a **Service Principal** for better security.

**To add these as secrets:**

1.  In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
2.  Click **New repository secret** for each secret:
    -   Name: `DATABRICKS_HOST`, Value: Your workspace URL.
    -   Name: `DATABRICKS_TOKEN`, Value: Your Databricks PAT.

## Step 2: Creating the GitHub Actions Workflow File

GitHub Actions are defined in YAML files located in the `.github/workflows` directory of your repository.

Create a new file: `.github/workflows/deploy_notebook_job.yml`

```yaml
# .github/workflows/deploy_notebook_job.yml

name: Deploy Databricks Notebook Job

# This action triggers on pushes to the main branch.
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install Databricks CLI
        run: |
          pip install databricks-cli

      - name: Configure Databricks CLI
        run: |
          echo "[DEFAULT]" > ~/.databrickscfg
          echo "host = ${{ secrets.DATABRICKS_HOST }}" >> ~/.databrickscfg
          echo "token = ${{ secrets.DATABRICKS_TOKEN }}" >> ~/.databrickscfg

      - name: Deploy Notebook Job to Databricks
        run: |
          databricks jobs create --json '{ 
            "name": "My Automated Notebook Job",
            "tasks": [
              {
                "task_key": "main",
                "notebook_task": {
                  "notebook_path": "/Repos/your-databricks-user/databricks-reference/path/to/your/notebook.ipynb"
                },
                "existing_cluster_id": "your-cluster-id"
              }
            ]
          }'
```

### Deconstructing the Workflow File

-   **`name`**: The name of the workflow, which appears in the GitHub Actions UI.
-   **`on`**: Defines the trigger. Here, it runs on any `push` to the `main` branch.
-   **`jobs`**: A workflow is made up of one or more jobs. We have one job named `deploy`.
-   **`runs-on`**: Specifies the type of virtual machine to run the job on. `ubuntu-latest` is a common choice.
-   **`steps`**: A sequence of tasks to be executed.
    -   `actions/checkout@v3`: A standard action to check out your repository code into the runner.
    -   `Install Databricks CLI`: A `run` step that executes shell commands to install the CLI.
    -   `Configure Databricks CLI`: This is a crucial step. It creates the `~/.databrickscfg` file that the CLI needs to authenticate with your workspace. It uses the secrets we stored earlier (`${{ secrets.DATABRICKS_HOST }}`).
    -   `Deploy Notebook Job`: This step uses the `databricks jobs create` command. The `--json` flag allows you to define the entire job configuration as a JSON object.

### Important Considerations

-   **`notebook_path`**: This path **must** be the full path to the notebook *within the Databricks workspace*. When using Databricks Repos, this typically follows the pattern `/Repos/<your-user-or-service-principal-email>/<repo-name>/<path-to-notebook>`. You need to update this to match your environment.
-   **`existing_cluster_id`**: For simplicity, this example uses an existing interactive cluster. In a production scenario, you would define a `new_cluster` configuration within the JSON to create a job cluster that runs on-demand.
-   **Idempotency**: The `databricks jobs create` command is not idempotent. If the job already exists, it will fail. A more robust workflow would use a script that checks if the job exists and then uses `databricks jobs reset --json ...` to update it, or `databricks jobs create` if it doesn't. This is a key concept for Level 3.

## Step 3: Committing and Pushing the Workflow

Commit this new YAML file to your repository and push it to GitHub. Because the file is in the `.github/workflows` directory, GitHub will automatically detect it.

Now, every time you merge a pull request into `main`, this action will automatically run, deploying your specified notebook as a job in your Databricks workspace. You have successfully created a basic, but powerful, CI/CD pipeline.

This is the second level of DevOps maturity. You have moved from manual version control to automated deployment, laying the groundwork for more advanced, enterprise-grade automation patterns.
