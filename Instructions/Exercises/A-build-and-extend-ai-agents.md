---
lab:
    title: 'Build and extend AI agents'
    description: 'Build the Trailhead Adventure Works assistant: ground it in store policy, then extend it with tools using remote MCP servers, custom functions, and a client app.'
    level: 300
    concepts: 'agent creation and grounding, tools, Model Context Protocol (MCP)'
    duration: 35
    islab: true
    status: 'draft'
---

<!--
PILOT NOTE (remove before publishing):
This is a pilot of the new lab template (Core + Optional tasks) applied to
"Lab A" = a consolidation of the current exercises 01, 02, and 03.
Starter code lives in a single folder — Labfiles/A-build-and-extend-ai-agents/Python/ —
shared by every task (one virtual environment, one .env). The completed reference code is
in Labfiles/A-build-and-extend-ai-agents/Solution/Python/.
Remaining follow-up tracked in the design spec: author a shared "Getting started" setup
page and link it instead of repeating setup here.
-->

# Build and extend AI agents

An agent becomes genuinely useful when it can *do* things — look up live information,
call your business logic, and act on a user's behalf. In this exercise you'll build a
grounded agent and then give it capabilities using **tools**.

**Your scenario:** you work at **Trailhead Adventure Works**, an outdoor-gear retailer that
also runs guided trips. Across this lab you'll build the staff assistant that powers the
business, adding one capability per task: first grounding it in the store's own policies,
then connecting it to live documentation, letting it analyze sales data, take trip
bookings, and check warehouse stock.

You'll start with the **Core** tasks that get you to a working, tool-using agent as
quickly as possible. From there, a set of **Optional** tasks lets you go deeper into the
areas that interest you most.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Create and ground an agent** in the Microsoft Foundry portal so it answers from your
  own data rather than guessing.
- **Extend an agent with a tool** by connecting it to a remote **Model Context Protocol
  (MCP)** server, and handle tool-approval requests in code.

The **Optional** tasks let you additionally:

- Call your agent from a **client application**.
- Give an agent **custom function tools** that run your own Python logic.
- Build and connect your **own MCP server**.
- Compare two ways to build the same agent: the **Foundry SDK + Responses API** (which you
  write) and the **Microsoft Agent Framework** (a provided, ready-to-run variant).

## Lab at a glance

Complete the **Core** tasks first (about **35 minutes**) — they're self-contained and end
with a working, tool-using agent. Then expand any **Optional** tasks that interest you.
The full lab, including all optional tasks, takes about **1 hour 55 minutes**. Use the
buttons below to auto-expand a set of tasks that match the time you have.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | Task 1 – Create and ground an agent in the portal | ★☆☆ | ~15 min |
| **Core** | Task 2 – Connect the agent to a remote MCP server in code | ★★☆ | ~20 min |
| *Optional* | Task 3 – Call your agent from a client app | ★★☆ | ~20 min |
| *Optional* | Task 4 – Add custom function tools | ★★☆ | ~25 min |
| *Optional* | Task 5 – Capstone: your own MCP server + combine every tool | ★★★ | ~35 min |

<!-- Lab-length picker. Works on the rendered GitHub Pages site; on GitHub.com's raw
     markdown view the buttons are inert, but every task can still be expanded manually.
     To change which tasks each preset opens, edit the data-tier on the task <details>. -->
<div class="lab-length-picker" role="group" aria-label="Choose your lab length">
  <span class="lab-length-label">Choose your lab length:</span>
  <button type="button" class="lab-btn is-active" data-tier="1">Core only · ~35 min</button>
  <button type="button" class="lab-btn" data-tier="2">Core + recommended · ~1h 20m</button>
  <button type="button" class="lab-btn" data-tier="3">Everything · ~1h 55m</button>
</div>

<div class="lab-length-fallback" markdown="1">

**Choosing your lab length** (the buttons above need JavaScript, which isn't run in
GitHub's file preview) — expand the optional tasks that fit the time you have:

- **Core only (~35 min):** do Tasks 1–2 only; leave the optional tasks collapsed.
- **Core + recommended (~1h 20m):** also expand **Task 3** and **Task 4**.
- **Everything (~1h 55m):** expand **Task 3**, **Task 4**, and **Task 5** (Task 5 builds on Task 4).

</div>

<style>
.lab-length-picker { display:flex; flex-wrap:wrap; gap:.5rem; align-items:center; margin:1rem 0; }
.lab-length-label { font-weight:600; }
.lab-btn { cursor:pointer; padding:.4rem .8rem; border:1px solid #8888; border-radius:6px; background:#f3f3f3; color:#111; font:inherit; }
.lab-btn:hover { background:#e6e6e6; }
.lab-btn.is-active { background:#0969da; color:#fff; border-color:#0969da; }
details.opt-task.is-included { border-left:3px solid #0969da; padding-left:.6rem; }
details.opt-task.is-included > summary { font-weight:600; }
</style>

<script>
(function () {
  function applyTier(tier) {
    document.querySelectorAll('.lab-btn').forEach(function (b) {
      b.classList.toggle('is-active', Number(b.dataset.tier) === tier);
    });
    document.querySelectorAll('details.opt-task').forEach(function (d) {
      var included = tier >= Number(d.dataset.tier);
      d.open = included;
      d.classList.toggle('is-included', included);
    });
  }
  document.querySelectorAll('.lab-btn').forEach(function (b) {
    b.addEventListener('click', function () { applyTier(Number(b.dataset.tier)); });
  });
  var fallback = document.querySelector('.lab-length-fallback');
  if (fallback) { fallback.hidden = true; }
  applyTier(1);
})();
</script>

## Prerequisites

Before starting this exercise, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) or later installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Python

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Set up your environment

> **Note**: These setup steps are common to every lab in this path. Once the shared
> *Getting started* page exists, this section will link to it instead of repeating it.

### Create a Microsoft Foundry project

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

---

# Core

The next two tasks are the required core of this lab. Task 1 builds a grounded agent in
the portal; Task 2 extends an agent with a tool in code.

## Task 1 — Create and ground an agent (portal)

Grounding gives your agent trusted source material so it answers accurately instead of
guessing.

1. In the agent playground, set the **Instructions** to:

    ```prompt
    You are the Trailhead Adventure Works store assistant.
    You help customers and store staff with questions about products, orders, returns, rentals, and guided trips.

    Guidelines:
    - Always be friendly and helpful
    - Use the store policy documentation to answer questions accurately
    - If you don't know the answer, admit it and suggest contacting the support team directly
    ```

1. Download the sample store policy document. Open a new browser tab and navigate to:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/A-build-and-extend-ai-agents/Python/Store_Policy.txt
    ```

    Save the file to your local machine.

1. Back in the playground, in the **Tools** section, select **Add**, and add **File search**.

1. To the right of **Add**, select **Upload files**, browse to the `Store_Policy.txt` file you downloaded, and select **Attach**. Wait for the file to be indexed.

1. **Save** the agent.

### Test your grounded agent

1. In the chat pane, enter:

    ```
    What's your return policy for a tent?
    ```

    The agent should reference the store policy document in its answer.

1. Try a second question to confirm it's using the grounding data:

    ```
    How do I rent gear for a weekend trip?
    ```

> ✅ **Checkpoint**: Your agent answers store questions using the uploaded policy document.
> You've created and grounded an agent entirely in the portal.

## Task 2 — Extend an agent with a remote MCP server (code)

The **Model Context Protocol (MCP)** lets an agent discover and call tools hosted by a
server. Behind the scenes, the Trailhead Adventure Works platform team is rebuilding the
online store on Azure — so in this task you'll connect an agent to the **Microsoft Learn
Docs** remote MCP server, giving the team an assistant that can pull trusted, up-to-date
Azure documentation on demand.

### Get the starter code

1. In VS Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-agents/Labfiles/A-build-and-extend-ai-agents/Python`. This single folder holds the starter code for every task in this lab.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

1. Open the **.env** file and set `PROJECT_ENDPOINT` to your project endpoint and `MODEL_DEPLOYMENT_NAME` to your model deployment name. Save the file.

    > **Tip**: In the Foundry Toolkit VS Code extension, right-click your project deployment and select **Copy Project Endpoint** to get the endpoint URL.

### Connect the agent to the MCP server

Open **remote_mcp_agent.py** and add code at each commented placeholder.

> **Tip**: As you add code, keep the indentation aligned with the comments.

1. **Add references**:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition, MCPTool
    from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam
    ```

1. **Connect to the agents client**:

    ```python
    # Connect to the agents client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    ```

1. **Initialize agent MCP tool** — this points the agent at the Microsoft Learn Docs MCP server:

    ```python
    # Initialize agent MCP tool
    mcp_tool = MCPTool(
        server_label="api-specs",
        server_url="https://learn.microsoft.com/api/mcp",
        require_approval="always",
    )
    ```

1. **Create a new agent with the MCP tool**:

    ```python
    # Create a new agent with the MCP tool
    agent = project_client.agents.create_version(
        agent_name="platform-docs-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="You are a platform engineering assistant for Trailhead Adventure Works. Use the available MCP tools to look up trusted Azure documentation and help the team build and operate the online store.",
            tools=[mcp_tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
    ```

1. **Create a conversation thread**:

    ```python
    # Create a conversation thread
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")
    ```

1. **Send initial request that will trigger the MCP tool**:

    ```python
    # Send initial request that will trigger the MCP tool
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Give me the Azure CLI commands to deploy our product catalog API to an Azure Container App with a managed identity.",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )
    ```

1. **Process any MCP approval requests** — because the tool requires approval, the agent
    pauses and asks permission before each call. This loop auto-approves each request:

    ```python
    # Process any MCP approval requests that were generated
    while True:
        input_list: ResponseInputParam = []
        for item in response.output:
            if item.type == "mcp_approval_request":
                if item.server_label == "api-specs" and item.id:
                    input_list.append(
                        McpApprovalResponse(
                            type="mcp_approval_response",
                            approve=True,
                            approval_request_id=item.id,
                        )
                    )

        # No more approvals needed -> the agent has produced its final response
        if not input_list:
            break

        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    print(f"\nAgent response: {response.output_text}")
    ```

1. **Clean up the agent version** so you don't leave test agents behind:

    ```python
    # Clean up resources by deleting the agent version
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
    ```

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python remote_mcp_agent.py
    ```

1. Watch the agent create itself, call the MCP tool (approved automatically by your loop), and answer using live documentation. You should see output similar to:

    ```
    Agent created (id: platform-docs-agent:2, name: platform-docs-agent, version: 2)
    Created conversation (id: conv_...)

    Agent response: Here are Azure CLI commands to create an Azure Container App with a managed identity:
    ...
    Agent deleted
    ```

1. Try changing the `input` string to ask about a different Azure service, and run again.

> ✅ **Checkpoint**: You've built a grounded agent *and* extended an agent with an
> external tool via a remote MCP server, including approval handling. That's the Core of
> this lab — everything below is optional.

When you're finished, enter `deactivate` to exit the virtual environment.

---

# Optional

Tasks 3 and 4 are independent — expand either that interests you, in any order. **Task 5 is
the capstone**: it brings the lab together into one assistant and builds on **Task 4**, so do
Task 4 first. Each task begins with a **Try it first** prompt; expand **Show a solution** when
you want the full walkthrough.

> **One assistant, growing capabilities**: Tasks 3–5 all run behind the same provided web
> chat window (`trailhead_ui.py`) — the **Trailhead Adventure Works Assistant**. You focus only
> on the agent code; each task gives the same assistant a new capability (analyzing sales
> data, planning trips, and checking warehouse stock). You don't edit `trailhead_ui.py`; you
> just write a `respond()` function and hand it to `run_chat_app()`.

## Two ways to build the same agent

There's more than one way to write an agent against Microsoft Foundry, and this lab shows you
**two**:

- **The Foundry SDK with the Responses API** — the approach you'll *write* throughout this lab.
  You create the agent with `azure-ai-projects`, describe each tool with an explicit JSON
  schema, and drive the **tool-calling loop yourself**: read the model's response, run the
  tool it asked for, and send the result back. This is deliberately hands-on so you can *see*
  the mechanics every agent runtime performs under the hood.
- **The Microsoft Agent Framework (MAF)** — a higher-level framework that hides that plumbing.
  You decorate a plain Python function with `@tool` (the schema is generated for you) and call
  `await agent.run(...)`, which runs the entire tool-calling loop automatically.

Neither is "more correct" — they're different levels of abstraction. Seeing the raw mechanics
first is what makes the framework's shortcuts meaningful later. To make the contrast concrete,
**Tasks 4 and 5 each ship a ready-to-run MAF edition** of the same assistant
(`functions_agent_maf.py` and `client_maf.py`) that you can read and run alongside your own
version. The Microsoft Agent Framework is covered in depth in **Lab 07 (Agent Framework)** and
**Lab 08 (multi-agent orchestration)**.


<details markdown="1" class="opt-task" data-tier="2">
<summary><strong>Task 3 — Call your agent from a client app</strong> &middot; ★★☆ &middot; ~20 min</summary>

**Goal**: Interact with the grounded portal agent from a small **web chat app** instead of
the playground — including charts the agent produces (from code interpreter), which render
**inline** in the chat window.

**Concept reinforced**: consuming an agent programmatically with the Foundry SDK — loading
an existing agent by name and driving it with the Responses API. A provided UI shell
(`trailhead_ui.py`) turns your agent into a browser chat app, so you focus on the agent code,
not the interface.

**Set up:**

1. In the portal, open your `trailhead-agent`, add a **Code interpreter** tool, and upload
    a data file so there's something to analyze. Download and attach:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/A-build-and-extend-ai-agents/Python/weekly_sales.csv
    ```

    Save the agent.

1. Use the same `Labfiles/A-build-and-extend-ai-agents/Python` folder and virtual environment
    you set up in Task 2 (if you closed the terminal, reactivate with
    `.\labenv\Scripts\Activate.ps1`). Then open **.env** and add `AGENT_NAME=trailhead-agent`
    alongside the `PROJECT_ENDPOINT` you already set. Save the file.

> **Try it first**: The `agent_with_functions.py` file already contains a complete client
> that launches a web chat window. Before running it, predict: which SDK call loads your
> existing portal agent *by name*? How does the client tell the Responses API to use that
> agent? How does a `respond()` function turn one message into a reply the UI can show?

<details markdown="1">
<summary>Show a solution</summary>

The provided `agent_with_functions.py` already implements the client and hands its
`respond()` function to the shared `run_chat_app()` shell. The lines that matter are:

1. **Load your portal agent by name** (using `AGENT_NAME` from **.env**):

    ```python
    agent = project_client.agents.get(agent_name=agent_name)
    ```

2. **Route each request to that agent** through the Responses API (inside `respond()`):

    ```python
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input="",
    )
    ```

3. **Inline charts**: helper functions detect image outputs and `container_file_citation`
    annotations, save them under `agent_outputs/`, and return them in an `AgentReply` so the
    UI renders them **inline** in the chat.

4. **Launch the app**: the file ends by starting the browser chat window:

    ```python
    run_chat_app(respond, title="Trailhead Adventure Works Assistant")
    ```

Sign in and run it:

```
az login
python agent_with_functions.py
```

Your browser opens a chat window at `http://localhost:7860`. Ask for something that uses
code interpreter:

```
Analyze the weekly sales data and create a chart of revenue over time.
```

The agent's analysis appears in the chat and the **chart is shown inline**. Close the
browser tab and press **Ctrl+C** in the terminal to stop the app.

</details>

**Stretch**: display the agent's token usage after each response.

</details>

<details markdown="1" class="opt-task" data-tier="2">
<summary><strong>Task 4 — Add custom function tools</strong> &middot; ★★☆ &middot; ~25 min</summary>

**Goal**: Give an agent tools backed by your **own Python functions**, and process the
function calls it makes.

**Concept reinforced**: the function-calling loop — the agent decides *which* tool to
call and with *what* arguments; your code executes it and returns the result.

**Set up:**

1. Use the same `Labfiles/A-build-and-extend-ai-agents/Python` folder and virtual environment
    you set up in Task 2 (reactivate with `.\labenv\Scripts\Activate.ps1` if needed); your
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in **.env** are already set. Review
    **functions.py**, which contains the trip planner's helper functions.

> **Try it first**: Look at `next_available_trip(region)` in **functions.py**. How would
> you describe its single `region` parameter to the model so it knows when and how to
> call it? Write the JSON schema before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Work through the comments in **functions_agent.py**. Add references and connect to the project (the
same pattern as Task 2). The file is structured so your agent setup runs once, then a
`respond()` function handles each chat message and hands the reply to `run_chat_app()`:

1. **Define the three function tools.** Each schema tells the model how to call one of the
    Python functions — for example the trip lookup tool:

    ```python
    # Define the trip lookup function tool
    trip_tool = FunctionTool(
        name="next_available_trip",
        description="Get the next available guided trip in a given region.",
        parameters={
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')",
                },
            },
            "required": ["region"],
            "additionalProperties": False,
        },
        strict=True,
    )
    ```

    Define `cost_tool` (`calculate_rental_cost`) and `report_tool`
    (`generate_booking_report`) the same way, matching each function's parameters.

2. **Create the agent with all three tools:**

    ```python
    agent = project_client.agents.create_version(
        agent_name="trip-planner-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""You are a trip planning assistant for Trailhead Adventure Works that helps
                customers find guided trips and calculate gear rental costs.
                Use the available tools to assist users with their inquiries.""",
            tools=[trip_tool, cost_tool, report_tool],
        ),
    )
    ```

3. **Fill in the tool-calling loop** inside `respond()` — read each `function_call` from the
    response, run the matching Python function, and collect a `FunctionCallOutput`:

    ```python
    # Process function calls
    for item in response.output:
        if item.type == "function_call":
            result = None
            if item.name == "next_available_trip":
                result = next_available_trip(**json.loads(item.arguments))
            elif item.name == "calculate_rental_cost":
                result = calculate_rental_cost(**json.loads(item.arguments))
            elif item.name == "generate_booking_report":
                result = generate_booking_report(**json.loads(item.arguments))
            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result,
                )
            )
    ```

    The rest of `respond()` (already provided) sends the outputs back and returns the final
    answer to the chat window:

    ```python
    # Send function call outputs back to the model and retrieve a response
    if input_list:
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)
    ```

Run `python functions_agent.py`. Your browser opens the chat window — try a prompt that needs **two**
tools at once:

```
Find me the next trip I can join in Patagonia and give me the cost for 5 days of premium gear rental at priority service.
```

The agent calls both functions in one turn and combines the results, for example:

```
The next trip available in Patagonia is the Patagonia Glacier Trek on February 17th.
The cost for 5 days of premium gear rental at priority service is $1,875.
```

Close the browser tab and press **Ctrl+C** in the terminal to stop the app (the agent is
deleted automatically on exit).

</details>

**Stretch**: add a fourth function tool of your own and update the instructions to mention it.

<details markdown="1">
<summary>Compare: the same agent with the Microsoft Agent Framework</summary>

You just wrote two schemas per tool and a dispatch loop that matches each `function_call` to a
Python function. The **Microsoft Agent Framework** removes both. Open **functions_agent_maf.py**
(provided complete) and run it with `python functions_agent_maf.py` — it produces the *same*
trip-planner assistant.

The difference is the tool definition and the loop. Instead of a hand-written `FunctionTool`
schema, you decorate the function with `@tool` and describe each parameter inline:

```python
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field
from typing import Annotated

@tool(approval_mode="never_require")
def next_available_trip(
    region: Annotated[str, Field(description="Region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')")],
) -> str:
    """Get the next available guided trip in a given region."""
    return functions.next_available_trip(region)
```

Then you create the agent with the decorated functions and let `agent.run()` handle the whole
tool-calling loop — no reading `response.output`, no matching names, no sending outputs back:

```python
agent = Agent(
    client=FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    ),
    name="trip-planner-agent",
    instructions="You are a trip planning assistant for Trailhead Adventure Works...",
    tools=[next_available_trip, calculate_rental_cost, generate_booking_report],
)

# agent.run() decides which tools to call, runs them, and returns the final answer
result = await agent.run(user_message, session=session)
```

Same result, far less code — because the framework does the plumbing you wrote by hand above.
Writing it yourself first is what makes it clear *what* `agent.run()` is doing for you.

</details>

</details>

<details markdown="1" class="opt-task" data-tier="3">
<summary><strong>Task 5 — Capstone: build your own MCP server and combine everything</strong> &middot; ★★★ &middot; ~35 min</summary>

**Goal**: Host your **own** tools on an MCP server, then bring the lab together into a single
**Trailhead Adventure Works Assistant** — one agent that both **plans trips and prices gear**
(the function tools from Task 4) *and* **checks live warehouse stock and sales** (the tools
you host here).

**Concept reinforced**: the MCP server/client split — a server *registers* tools; a client
*discovers and calls* them — plus how one agent can hold **more than one kind of tool** at
once. In `respond()` you *route* each call to the right place: local Python functions run
in-process, MCP tools run over the server session.

> **Prerequisite**: This capstone builds directly on **Task 4** — complete it first. The
> trip-planner tools you wrote there (`next_available_trip`, `calculate_rental_cost`,
> `generate_booking_report`) are provided ready-made in `client.py` so you can focus on the
> new work: hosting your MCP server and *combining* both tool sets on one agent.

**Set up:**

1. Use the same `Labfiles/A-build-and-extend-ai-agents/Python` folder and virtual environment
    you set up in Task 2 (reactivate with `.\labenv\Scripts\Activate.ps1` if needed; your
    **.env** is already configured). You'll edit **server.py** and **client.py**.

> **Try it first**: Wire up **server.py** and **client.py** using the comments in each file.
> As you go, consider: why must diagnostic output go to `stderr` (or be suppressed) rather
> than `stdout`? *(Hint: MCP speaks JSON-RPC over stdio, so anything printed to stdout is
> parsed as protocol messages — a stray banner corrupts the stream. That's why the server
> starts with `show_banner=False`.)* And: once the agent has **both** tool sets, how does
> your code know whether a given `function_call` should run a local function or an MCP tool?

<details markdown="1">
<summary>Show a solution</summary>

**In `server.py`** — create the server and expose the two provided functions as tools:

```python
# Add references
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Inventory")

@mcp.tool()
def get_inventory_levels() -> dict:
    ...  # returns the sample inventory dict already in the file

@mcp.tool()
def get_weekly_sales() -> dict:
    ...  # returns the sample sales dict already in the file

# Run the MCP server
mcp.run(show_banner=False)
```

**In `client.py`** — connect to the server, discover its tools, register them **alongside**
the trip-planner tools on one agent, then route each call in `respond()`. Because the chat UI
runs on an async event loop, the connection code lives in an async `setup()` that runs once on
the first message.

1. Add the MCP references at the top of the file:

    ```python
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    ```

    The `trip_planner_tools` list and the `local_functions` dispatch dict (the Task 4 tools)
    are already provided near the top of the file — you don't need to rewrite them.

2. Inside `setup()`, start the server over stdio and open a session, then list the available
    tools and wrap each as a callable:

    ```python
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    tools = (await session.list_tools()).tools

    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            return await session.call_tool(tool_name, kwargs)
        tool_func.__name__ = tool_name
        return tool_func

    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}

    mcp_function_tools = [
        FunctionTool(
            name=tool.name,
            description=tool.description,
            parameters={"type": "object", "properties": {}, "additionalProperties": False},
            strict=True,
        )
        for tool in tools
    ]
    ```

3. Create the agent with **both** tool sets — the trip planner *and* the warehouse tools:

    ```python
    agent = project_client.agents.create_version(
        agent_name="trailhead-assistant",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""
            You are the Trailhead Adventure Works assistant. You help customers plan guided
            trips and price gear rentals, and you help warehouse staff check live stock and sales.

            Trip planning and rentals:
            - Use the trip and rental tools to find guided trips, price gear, and produce booking reports.

            Warehouse inventory:
            - Recommend restock if item inventory < 10 and weekly sales > 15
            - Recommend clearance if item inventory > 20 and weekly sales < 5
            """,
            tools=[*trip_planner_tools, *mcp_function_tools],
        ),
    )
    ```

4. In `respond()`, route each `function_call` to the right executor — local functions run
    directly (they return a string); MCP tools are awaited over the session:

    ```python
    for item in response.output:
        if item.type == "function_call":
            kwargs = json.loads(item.arguments)

            if item.name in local_functions:
                output_text = local_functions[item.name](**kwargs)          # Task 4 function
            else:
                result = await functions_dict[item.name](**kwargs)          # your MCP tool
                output_text = result.content[0].text

            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=output_text,
                )
            )

    # ...send outputs back, then:
    return AgentReply(text=response.output_text)
    ```

Run `python client.py`. Your browser opens the chat window — the server is launched for you
over stdio on the first message. Now try a prompt that exercises **both** halves of the
assistant in one conversation:

```
Plan me a trip: find the next available trip in Patagonia and price 5 days of premium gear at priority service.
```
```
Now check the warehouse — are there any products we should restock?
```

The first prompt calls your Task 4 trip-planner functions; the second calls your MCP
inventory tools — all on the **same** agent, in the **same** chat. Close the browser tab and
press **Ctrl+C** in the terminal to stop the app.

</details>

**Stretch**: add a third MCP tool (for example, `get_reorder_threshold`) and watch the agent
discover it without any other client changes — the routing already handles any tool it
doesn't recognize as a local function.

<details markdown="1">
<summary>Compare: the same capstone with the Microsoft Agent Framework</summary>

In `client.py` you hand-wired the MCP client (`ClientSession`, `stdio_client`), wrapped each
discovered tool, built `FunctionTool` schemas, and then *routed* every `function_call` yourself
— local function or MCP tool. The **Microsoft Agent Framework** collapses all of that. Open
**client_maf.py** (provided complete) and run it with `python client_maf.py` — same capstone,
same two-tool-sets-on-one-agent behavior.

Your `server.py` is unchanged — you still author the MCP server. What disappears is the client
wiring and the routing loop. An `MCPStdioTool` launches the server and exposes its tools, and
you hand it to `agent.run()` alongside the agent's own `@tool` functions:

```python
from agent_framework import tool, Agent, MCPStdioTool

agent = Agent(
    client=FoundryChatClient(...),
    name="trailhead-assistant",
    instructions="You are the Trailhead Adventure Works assistant...",
    tools=[next_available_trip, calculate_rental_cost, generate_booking_report],
)

async with MCPStdioTool(name="Inventory", command="python", args=["server.py"]) as mcp_tool:
    # One call handles either tool set — no manual "local vs MCP" routing
    result = await agent.run(user_message, tools=mcp_tool, session=session)
```

Notice there's no `if item.name in local_functions ... else ...` branch: `agent.run()` invokes
whichever tool the model picks, whether it's one of your Python functions or a tool hosted on
your MCP server. Having built the routing by hand first, you can see exactly which step the
framework is taking over.

</details>

</details>

## Summary

In this exercise you:

- Created and **grounded** an agent in the Foundry portal so it answers from your data.
- **Extended an agent with a tool** by connecting it to a remote MCP server and handling
  tool-approval requests in code.
- (Optionally) consumed an agent from a **client app**, added **custom function tools**,
  and built your **own MCP server** — then combined the function tools and your MCP tools
  into a single **capstone assistant** that routes each call to the right place.

Together these show the two big levers for making agents useful: giving them the right
**knowledge** (grounding) and the right **capabilities** (tools).

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> The code you ran in Task 2 already deletes the agent version it creates. Portal
> agents are removed when you delete the resource group.
