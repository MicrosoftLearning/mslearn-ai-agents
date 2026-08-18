---
title: 'Getting started: set up your environment'
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Build multi-agent solutions with the Agent Framework lab: create a Microsoft Foundry project, get the starter code, and configure your environment. Complete this once before any task.'
    type: 'task'
    parent: 'C'
    order: 0
    section: 'setup'
    access: 'open'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project'
    status: 'draft'
---

# Getting started

This page sets up everything the **Build multi-agent solutions with the Agent Framework** lab
needs. **Every task begins here** — complete this page first. Each task is written so you can then
do it on its own; if you're working through the whole lab in one sitting, you only need to do this
setup once.

**Your scenario:** you work at **Caldova**, a pharmaceutical manufacturer preparing an
accelerated product launch. Across the lab you'll build the automation behind Caldova
operations, starting with one agent and growing to a coordinated team of them.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Python

> \* Python 3.14 isn't supported yet: some dependencies have no 3.14 build. This lab was tested with Python 3.13.12.

## Create a Microsoft Foundry project

You need a Foundry project and a deployed model for every task. You can create these in the
portal (the default), or provision them with one command using the Azure Developer CLI (`azd`).

### Option A — Create the project in the portal (default)

Microsoft Foundry uses projects to organize models, resources, data, and other assets.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes, and if necessary use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

1. In the top banner, select **Start building**.

1. When prompted, create a **new** project and enter a valid name (for example, `agents-lab-project`).

1. Expand **Advanced options** and specify:
    - **Microsoft Foundry resource**: *A valid name for your Foundry resource*
    - **Region**: *Select one available near you*\*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select or create a resource group*

    > \* Some Azure AI resources are constrained by regional model quotas. If you hit a quota limit later, you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created. When prompted, continue through the welcome dialog.

1. When prompted to deploy a model, deploy a **gpt-4o** model (or another available chat model). Note the **deployment name** — you'll set it as `MODEL_DEPLOYMENT_NAME` in your `.env`.

1. From the project overview, copy the **Project endpoint** — you'll set it as `PROJECT_ENDPOINT`.

### Option B — Provision with azd (optional, one command)

If you'd rather not click through the portal, the lab ships an optional `azd` template that
creates the Foundry resource, a project, and a model deployment for you.

1. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).

1. From the `Labfiles/C-build-multi-agent-solutions-with-agent-framework` folder, run:

    ```
    azd auth login
    azd up
    ```

1. Answer the prompts (environment name, region). When it finishes, `azd` writes
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` into `Python/.env` for you.

    > **Note**: When you're done with the lab, run `azd down` to delete everything it created.

## Get the starter code

1. In VS Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-agents/Labfiles/C-build-multi-agent-solutions-with-agent-framework/Python`. This single folder holds the starter code for **every** task in this lab — you use one virtual environment and one `.env` throughout.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

1. Open the **.env** file and set `PROJECT_ENDPOINT` to your project endpoint and `MODEL_DEPLOYMENT_NAME` to your model deployment name. Save the file. (If you used `azd up`, these are already filled in.)

    > **Tip**: In the Foundry Toolkit VS Code extension, right-click your project deployment and select **Copy Project Endpoint** to get the endpoint URL.

    > The `.env` also ships with `SERVER_URL` and three `*_PORT` values pre-filled — those are only used by **Task 3** (remote agents), and you normally don't need to change them.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check from the `Python` folder you opened in VS Code — it reads
your `.env` and tells you what (if anything) is missing:

```
python ../setup/check_env.py --task 1
```

Swap `1` for the task number you're about to start.

> **Tip**: The preflight check uses only the Python standard library, so it's safe to run
> before `pip install` and without the virtual environment active.

That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Build an agent with a tool | [C1](C1-create-an-agent-with-a-tool.md) |
| Task 2 – Orchestrate multiple agents in sequence | [C2](C2-orchestrate-multiple-agents.md) |
| Task 3 – Connect remote agents with A2A | [C3](C3-connect-remote-agents-with-a2a.md) |
| Task 4 – Classify and route a support ticket | [C4](C4-classify-and-route-a-ticket.md) |
