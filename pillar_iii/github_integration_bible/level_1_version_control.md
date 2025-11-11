---
title: Level 1 Version Control with Repos
nav_order: 1
parent: The GitHub Integration Bible
grand_parent: Pillar III MLOps & DevOps
---

# Level 1: Version Control with Databricks Repos

The first and most fundamental step in bringing DevOps practices to your Databricks workspace is versioning your code. **Databricks Repos** is a feature that provides a direct, visual integration between your Databricks workspace and a remote Git repository, such as one hosted on GitHub.

This integration allows you to treat your notebooks, Python files, and SQL scripts as first-class citizens in your version control system. It enables collaborative development, feature branching, and a full audit history of your code, right from the Databricks UI.

## Why Use Databricks Repos?

-   **Single Source of Truth**: Your GitHub repository becomes the single source of truth for your project code.
-   **Collaboration**: Multiple developers can work on the same project, each in their own branch, and then merge changes, just like in traditional software development.
-   **Version History**: Every change is tracked. You can easily revert to previous versions of a notebook if a bug is introduced.
-   **Code Reviews**: By pushing changes to a feature branch and opening a pull request in GitHub, you can enforce code reviews for your notebooks, improving code quality and knowledge sharing.

## Setting Up Your First Repo

Connecting a GitHub repository to your Databricks workspace is a straightforward, one-time setup process.

### Step 1: Configure Git Integration in User Settings

1.  In your Databricks workspace, click on your username in the top-right corner and select **User Settings**.
2.  Go to the **Git Integration** tab.
3.  For the Git provider, select **GitHub**.
4.  You will need to provide a **GitHub Personal Access Token (PAT)** with `repo` scope. Follow the GitHub documentation to create one.
    -   **Important**: Use a token with an expiration date and treat it like a password. Store it securely.
5.  Enter your GitHub username or email and paste the PAT into the **Token** field. Click **Save**.

![Git Integration Setup](https://docs.databricks.com/_images/git-integ-azure.png)
*Source: Databricks Documentation*

### Step 2: Clone a Remote Repository

1.  In the left-hand navigation pane of your workspace, right-click on your username and select **Create > Repo**.
2.  In the dialog box:
    -   **Git repository URL**: Paste the HTTPS URL of the GitHub repository you want to clone (e.g., `https://github.com/your-username/your-repo.git`).
    -   **Repo Name**: This will be the name of the folder in your Databricks workspace. It defaults to the repository name.
3.  Click **Create**. Databricks will clone the repository into a folder under your user directory.

## The Development Workflow in Databricks Repos

Once the repo is cloned, you can work with it using a simple, Git-based workflow directly within the Databricks UI.

### 1. Create a New Branch

**Best Practice**: Never commit directly to the `main` branch. Always create a new feature branch for your work.

1.  Click on the Git branch button at the top-left of your notebook editor (it will likely say `main`).
2.  In the dialog, click the **Create Branch** button.
3.  Give your branch a descriptive name (e.g., `feature/add-new-aggregation`).

### 2. Make and Commit Changes

Now, you can edit your notebooks or files as you normally would. As you make changes, the Git dialog will show you the diffs.

1.  When you are ready to save your work, go to the Git dialog.
2.  Add a concise and descriptive **commit message** (e.g., "Add daily sales summary to reporting notebook").
3.  Click **Commit & Push**. This will commit the changes to your feature branch and push the branch to the remote GitHub repository.

### 3. Create a Pull Request

1.  After you push your changes, a link will appear in the Databricks UI to **Create a Pull Request**.
2.  Clicking this link will take you to GitHub, where you can open a PR to merge your feature branch into the `main` branch.
3.  This is where your team can review your code, suggest changes, and ultimately approve the merge.

### 4. Pulling Latest Changes

To update your repo with the latest changes from the remote repository (e.g., after a teammate merges their PR), simply click the **Pull** button in the Git dialog. This ensures your branch is up-to-date.

## Best Practices for Using Databricks Repos

-   **Branching Strategy**: Adopt a consistent branching strategy, such as GitFlow or a simplified feature-branching model.
-   **Small, Frequent Commits**: Make small, logical commits with clear messages. This makes your history easier to read and code reviews easier to perform.
-   **Pull Requests for Everything**: Enforce a policy that all changes to the `main` branch must come through a pull request. Protect the `main` branch in your GitHub repository settings.
-   **Separate Code and Notebooks**: While you can do everything in notebooks, a best practice is to put reusable Python code into `.py` files and import them into your notebooks. This makes the code more modular and easier to test.

By mastering this foundational level of integration, you have already made a massive leap forward in professionalizing your data development lifecycle. You have a versioned, collaborative, and auditable process for managing your Databricks code.
