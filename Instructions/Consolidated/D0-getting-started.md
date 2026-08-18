---
title: 'Getting started: set up your environment'
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Observe, evaluate, and secure your agents lab: create a Microsoft Foundry project, connect Application Insights, get the starter code, and configure your environment. Complete this once before any task.'
    type: 'task'
    parent: 'D'
    order: 0
    section: 'setup'
    access: 'open'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project, Application Insights'
    status: 'draft'
---

# Getting started

This page sets up everything the **Observe, evaluate, and secure your agents** lab needs.
**Every task begins here** — complete this page first. Each task is written so you can then
do it on its own; if you're working through the whole lab in one sitting, you only need to
do this setup once.

**Your scenario:** you work at **Caldova**, a pharmaceutical manufacturer preparing an
accelerated product launch. The supply chain assistant is live, and this lab is how you
find out what it's really doing: tracing it, scoring its answers, and attacking it.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Python

> \* Python 3.14 isn't supported yet: some dependencies have no 3.14 build.

## Create a Microsoft Foundry project

You need a Foundry project and a deployed model for every task. You can create these in the
portal (the default), or provision them with one command using the Azure Developer CLI (`azd`).

### Option A — Create the project in the portal (default)

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes, and if necessary use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

1. In the top banner, select **Start building**.

1. When prompted, create a **new** project and enter a valid name (for example, `observability-lab-project`).

1. Expand **Advanced options** and specify:
    - **Microsoft Foundry resource**: *A valid name for your Foundry resource*
    - **Region**: *Select one available near you*\*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select or create a resource group*

    > \* If you plan to do **Task 3** (red teaming), the AI Red Teaming Agent is only available
    > in **East US 2**, **France Central**, **Sweden Central**, **Switzerland West**, and
    > **North Central US**. Choosing one of those now saves you creating a second project later.

1. Select **Create** and wait for your project to be created.

1. On the project **Overview** page, note the **project endpoint** and the name of the model
    deployment that was created for you — you'll put both in your `.env`.

### Option B — Provision with azd (optional, one command)

If you'd rather not click through the portal, the lab ships an optional `azd` template that
creates the Foundry resource, a project, and a model deployment for you.

1. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).

1. From the `Labfiles/D-observe-evaluate-and-secure-agents` folder, run:

    ```
    azd auth login
    azd up
    ```

1. Answer the prompts (environment name, region). When it finishes, `azd` writes
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` into `Python/.env` for you.

    > **Note**: `azd up` does **not** create the Application Insights resource Task 1 needs —
    > connect that in the portal using the steps below. When you're done with the lab, run
    > `azd down` to delete everything it created.

## Connect Application Insights (needed for Task 1)

Foundry stores traces in an **Application Insights** resource connected to your project. Connect
one now — it takes a minute, and once it's connected Foundry starts recording server-side traces
for your agents without any code at all.

1. In the [Foundry portal](https://ai.azure.com), open your project.

1. In the left navigation, select **Agents**, then select **Traces** at the top.

1. Select **Connect**, then either pick an existing Application Insights resource or select
    **Create new** and complete the wizard.

    > If you don't see the **Connect** button, select **Manage** in the upper right, then
    > **Project details** > **Connected resources** > **Add connection** > **Application Insights**.

1. To *read* the traces you'll need the **Log Analytics Reader** role on that Application
    Insights resource. If you created it yourself, you already have it.

> **Why this matters**: your Foundry project can only hand your code a connection string if
> something is connected. Task 1 asks the project for that string, so this step has to happen
> first.

## Get the starter code

1. In VS Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-agents/Labfiles/D-observe-evaluate-and-secure-agents/Python`. This single folder holds the starter code for **every** task in this lab — you use one virtual environment and one `.env` throughout.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    > This install is larger than the other labs — it includes the evaluation SDK and, for
    > Task 3, PyRIT. Give it a few minutes.

1. Open the **.env** file and set `PROJECT_ENDPOINT` to your project endpoint and `MODEL_DEPLOYMENT_NAME` to your model deployment name. Save the file. (If you used `azd up`, these are already filled in.)

    > **Tip**: In the Foundry Toolkit VS Code extension, right-click your project deployment and select **Copy Project Endpoint** to get the endpoint URL.

## Get an agent to measure (needed for Tasks 2 and 3)

Tasks 2 and 3 measure a **grounded** agent — one that answers from the Caldova
knowledge base rather than from the model's own memory. You have two ways to get one:

- **You did [Lab B](B-integrate-agents-with-enterprise-knowledge-and-m365.md)**: set `AGENT_NAME`
  in `.env` to that agent's name (`caldova-knowledge-agent` if you kept the default) and you're
  done.
- **You didn't**: create an equivalent agent here. Sign in and run, from the `Python` folder with
  the virtual environment active:

    ```
    az login
    ```

    ```
    python ../setup/bootstrap_agent.py
    ```

    This uploads the documents in `Python/knowledge/`, grounds an agent named
    `caldova-knowledge-agent` on them with File Search, and writes `AGENT_NAME` into your `.env`.

> Task 1 doesn't need this agent — it creates and deletes its own.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check from the `Python` folder you opened in VS Code — it reads your `.env` and tells you
what (if anything) is missing:

```
python ../setup/check_env.py --task 1
```

Swap `1` for the task number you're about to start.

> **Tip**: The preflight check uses only the Python standard library, so it's safe to run
> before `pip install` and without the virtual environment active. It can't see whether
> Application Insights is connected — that's a project setting, not a `.env` value — so
> do the connection step above if you're starting at Task 1.

That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Trace your agent | [D1](D1-trace-your-agent.md) |
| Task 2 – Evaluate answer quality | [D2](D2-evaluate-answer-quality.md) |
| Task 3 – Red team your agent | [D3](D3-red-team-your-agent.md) |
