---
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Build and extend AI agents lab: create a Microsoft Foundry project, get the starter code, and configure your environment. Complete this once before any task.'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project'
    status: 'draft'
---

# Getting started

This page sets up everything the **Build and extend AI agents** lab needs. Complete it
**once**, then do any task — [Task 1](A1-create-and-ground-an-agent.md) through
[Task 5](A5-capstone-build-your-own-mcp-server.md) — on its own or in order.

**Your scenario:** you work at **Trailhead Adventure Works**, an outdoor-gear retailer that
also runs guided trips. Across the lab you'll build the staff assistant that powers the
business, adding one capability per task.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) or later installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Python

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Create a Microsoft Foundry project

You need a Foundry project and a deployed model for every code task. You can create these
in the portal (the default), or provision them with one command using the Azure Developer
CLI (`azd`).

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

1. Select **Create** and wait for your project to be created. When prompted, continue through the welcome dialog and select **Create agent**.

1. Set the **Agent name** to `trailhead-agent` and create the agent. The playground opens with a deployed model already selected for you.

Keep this browser tab open — you'll use it in Task 1.

### Option B — Provision with azd (optional, one command)

If you'd rather not click through the portal, the lab ships an optional `azd` template that
creates the Foundry resource, a project, and a model deployment for you.

1. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).

1. From the `Labfiles/A-build-and-extend-ai-agents` folder, run:

    ```
    azd auth login
    azd up
    ```

1. Answer the prompts (environment name, region). When it finishes, `azd` writes
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` into `Python/.env` for you.

    > **Note**: This provisions the resources but does **not** create the grounded portal
    > agent — Task 1 does that. If you're starting at Task 3, run
    > `python setup/bootstrap_agent.py` after `azd up` to create it. When you're done with
    > the lab, run `azd down` to delete everything it created.

## Get the starter code

1. In VS Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-agents/Labfiles/A-build-and-extend-ai-agents/Python`. This single folder holds the starter code for **every** task in this lab — you use one virtual environment and one `.env` throughout.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

1. Open the **.env** file and set `PROJECT_ENDPOINT` to your project endpoint and `MODEL_DEPLOYMENT_NAME` to your model deployment name. Save the file. (If you used `azd up`, these are already filled in.)

    > **Tip**: In the Foundry Toolkit VS Code extension, right-click your project deployment and select **Copy Project Endpoint** to get the endpoint URL.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check from the `Labfiles/A-build-and-extend-ai-agents` folder — it reads your `.env` and
tells you what (if anything) is missing:

```
python setup/check_env.py --task 2
```

Swap `2` for the task number you're about to start. That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Create and ground an agent (portal) | [A1](A1-create-and-ground-an-agent.md) |
| Task 2 – Connect a remote MCP server | [A2](A2-connect-a-remote-mcp-server.md) |
| Task 3 – Call your agent from a client app | [A3](A3-call-your-agent-from-a-client-app.md) |
| Task 4 – Add custom function tools | [A4](A4-add-custom-function-tools.md) |
| Task 5 – Capstone: build your own MCP server | [A5](A5-capstone-build-your-own-mcp-server.md) |
