---
title: 'Getting started: set up your environment'
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Build and extend AI agents lab: create a Microsoft Foundry project, get the starter code, and configure your environment. Complete this once before any task.'
    type: 'task'
    parent: 'A'
    order: 0
    section: 'setup'
    access: 'open'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project'
    status: 'draft'
---

# Getting started

Prepare the shared cloud resources and local Python environment for the **Build and extend
AI agents** lab. Complete this setup once before starting a task.

## The case

**Caldova** is a pharmaceutical manufacturer preparing an early product launch. Its three
factories cannot produce everything the launch requires, so you will build a supply chain
assistant to help the planning team evaluate its options.

Before you add capabilities to the assistant, you need a Microsoft Foundry project, a
deployed model, and the starter code. You reuse this setup throughout the lab, whether you
complete one task or the full sequence.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Python

> **Note**: Python 3.14 isn't supported yet because some dependencies have no 3.14 build. This lab was tested with Python 3.13.12.

## Create a Microsoft Foundry project

You need a Foundry project and a deployed model for every code task. You can create these
in the portal (the default), or provision them with one command using the Azure Developer
CLI (`azd`).

<style>
/* "Ask Anton" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
    font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
    border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Anton: "; font-weight:700;
    padding-left:1.5em;
    background:url("../Media/anton-avatar.png") left center / 1.25em 1.25em no-repeat; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
    border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
.setup-tabs { display:grid; grid-template-columns:auto auto 1fr; margin:1rem 0; }
.setup-tabs > input { position:absolute; width:1px; height:1px; overflow:hidden;
    clip:rect(0 0 0 0); white-space:nowrap; }
.setup-tabs > label { padding:.55rem .9rem; border-bottom:2px solid #d4d4d8;
    cursor:pointer; font-weight:600; color:#52525b; }
.setup-tabs > input:focus-visible + label { outline:2px solid #1a45a5; outline-offset:2px; }
.setup-tabs > input:checked + label { color:#1a45a5; border-bottom-color:#1a45a5; }
.setup-tabs .setup-panel { display:none; grid-column:1 / -1; padding-top:.75rem; }
#setup-portal:checked ~ .setup-portal-panel,
#setup-azd:checked ~ .setup-azd-panel { display:block; }
</style>

<details markdown="1" class="concept">
<summary>What is a Microsoft Foundry project?</summary>
<div class="concept-body" markdown="1">

A Microsoft Foundry project is a workspace for building and managing an AI application.
It gives you one place to work with the application's agents, models, tools, and evaluations.
In this lab, the project contains the model deployment and agents used by the Caldova
assistant.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/what-is-foundry)

</div>
</details>

<div class="setup-tabs">
<input type="radio" name="setup-method" id="setup-portal" checked="checked" />
<label for="setup-portal">Option A: Azure portal</label>
<input type="radio" name="setup-method" id="setup-azd" />
<label for="setup-azd">Option B: Azure Developer CLI</label>
<div class="setup-panel setup-portal-panel" markdown="1">

### Create the project in the portal

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

1. Set the **Agent name** to `caldova-agent` and create the agent. The playground opens with a deployed model already selected for you.

Keep this browser tab open — you'll use it in Task 1.

</div>
<div class="setup-panel setup-azd-panel" markdown="1">

### Provision with azd

Choose this option if you prefer to set up the Azure resources from the terminal. The
included `azd` template creates the Foundry resource, project, and model deployment for you.

1. Install the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd).

1. From the `Labfiles/A-build-and-extend-ai-agents` folder, run:

    ```
    azd auth login
    azd up
    ```

1. Answer the prompts (environment name, region). When it finishes, `azd` writes
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` into `Python/.env` for you.

    > **Note**: These commands create the Azure resources, but they don't create the grounded
    > agent used in Task 1. If you're starting at Task 3, run
    > `python ../setup/bootstrap_agent.py` from the `Python` folder after `azd up` to create
    > it. When you're done with the lab, run `azd down` to delete everything it created.

</div>
</div>

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
check from the `Python` folder you opened in VS Code — it reads your `.env` and
tells you what (if anything) is missing:

```
python ../setup/check_env.py --task 2
```

Swap `2` for the task number you're about to start.

> **Tip**: The preflight check uses only the Python standard library, so it's safe to run
> before `pip install` and without the virtual environment active.

That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Create and ground an agent (portal) | [A1](A1-create-and-ground-an-agent.md) |
| Task 2 – Connect a remote MCP server | [A2](A2-connect-a-remote-mcp-server.md) |
| Task 3 – Call your agent from a client app | [A3](A3-call-your-agent-from-a-client-app.md) |
| Task 4 – Add custom function tools | [A4](A4-add-custom-function-tools.md) |
| Task 5 – Capstone: build your own MCP server | [A5](A5-capstone-build-your-own-mcp-server.md) |
| Task 6 – Promote your assistant to a hosted agent | [A6](A6-promote-your-assistant-to-a-hosted-agent.md) |
