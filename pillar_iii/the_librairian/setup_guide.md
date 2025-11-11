---
title: Setup Guide
nav_order: 1
parent: The LibrAIrian Your AI Guide
grand_parent: Pillar III MLOps & DevOps
---

# Setting Up The LibrAIrian: A Step-by-Step Guide

To unlock the full power of The LibrAIrian, you need to have the right tools installed and configured. This guide will walk you through the simple, one-time setup process using **Visual Studio Code** and the **GitHub Copilot Chat** extension.

## Prerequisites

1.  **Visual Studio Code (VS Code)**: A free, powerful code editor from Microsoft. If you don't have it, [download it here](https://code.visualstudio.com/).
2.  **A GitHub Copilot Subscription**: The LibrAIrian relies on GitHub Copilot Chat, which is part of the GitHub Copilot subscription. You must have an active subscription.
3.  **This Repository Cloned**: You should have this repository (`databricks-reference`) cloned to your local machine.

## Step 1: Install the GitHub Copilot Extension

1.  Open VS Code.
2.  Go to the **Extensions** view by clicking the icon in the left-hand sidebar or by pressing `Ctrl+Shift+X`.
3.  In the search bar, type `GitHub Copilot`.
4.  You will see an extension named **GitHub Copilot** from the publisher **GitHub**. Click **Install**.
5.  This will typically install a suite of Copilot tools, including the core completion tool and **Copilot Chat**.
6.  You may need to sign in to your GitHub account to authorize the extension.

After installation, you should see a new **Chat** icon in the left-hand sidebar.

## Step 2: Open the Repository and The LibrAIrian File

1.  In VS Code, go to **File > Open Folder...** and select the `databricks-reference` repository folder that you cloned to your local machine.
2.  In the VS Code Explorer, navigate to and open the following file:

    `pillar_iii/the_librairian/librairian.md`

    This file is the "brain" of The LibrAIrian. Keeping it open in an editor tab provides the necessary context to Copilot Chat.

## Step 3: Start Interacting with The LibrAIrian

1.  Open the **Copilot Chat** view by clicking the Chat icon in the sidebar or by pressing `Ctrl+Alt+I`.
2.  You can now ask questions directly in the chat interface. Because you have the `librairian.md` file open, Copilot will use it as a primary source of context for its answers.

### Example Prompts to Get You Started:

Try asking Copilot some questions about this repository. Here are a few examples:

> "What is the Medallion Architecture? Can you point me to the file that explains it?"

> "I need a Python code example for a Pandas UDF. Where can I find one in this repo?"

> "Explain the difference between `repartition` and `coalesce` in PySpark, based on the content in this library."

> "Show me the recommended CI/CD workflow for deploying a Databricks job from this repository."

## How It Works: The Power of Context

GitHub Copilot Chat is designed to be aware of the code and files you have open in your editor. The `librairian.md` file is a highly-structured Markdown document that acts as a detailed table of contents and concept map for the entire repository. 

By having this file open, you are essentially telling Copilot: "Hey, before you answer my question, read this file first. It will tell you everything you need to know about the structure and content of this project."

This allows Copilot to provide answers that are not just general knowledge from its training data, but are specifically tailored to the best practices, code examples, and explanations contained within this exhaustive library.

You are now ready to use The LibrAIrian. Happy learning!
