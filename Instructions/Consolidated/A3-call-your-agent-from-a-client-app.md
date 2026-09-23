---
title: 'Task 3 – Call your agent from a client app'
lab:
    title: 'Task 3 – Call your agent from a client app'
    description: 'Drive your grounded portal agent from a small web chat app using the Foundry SDK and Responses API, with inline charts.'
    type: 'task'
    parent: 'A'
    order: 3
    section: 'optional'
    difficulty: 3
    duration: 20
    access: 'open'
    level: 300
    concepts: 'Foundry SDK, Responses API, code interpreter'
    status: 'draft'
---

# Task 3 — Call your agent from a client app

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](A0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` in `Python/.env`.

This task drives a **grounded agent**. The quickest way to get one is to create it in code —
from the `Python` folder you opened in VS Code, run:

```
python ../setup/bootstrap_agent.py
```

That creates and grounds `caldova-agent` — including the **Code Interpreter** tool with the
output data already attached — and writes `AGENT_NAME` into your `.env`. Then verify you're ready:

```
python ../setup/check_env.py --task 3
```

> **Already built the agent in [Task 1](A1-create-and-ground-an-agent.md)?** Use it instead
> of the script: open your `caldova-agent` in the portal, add the **Code interpreter** tool
> with the output data (step 1 below), and set `AGENT_NAME=caldova-agent` in `.env`.

---

**Goal**: Interact with the grounded portal agent from a small **web chat app** instead of
the playground — including charts the agent produces (from code interpreter), which render
**inline** in the chat window.

You load the existing agent by name and send messages to it from a provided web interface.

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
</style>

<details markdown="1" class="concept">
<summary>How does an app call a Foundry agent?</summary>
<div class="concept-body" markdown="1">

The **Foundry SDK** gives your Python code access to projects and agents. The **Responses
API** sends a user's input and returns the agent's response, including tool output. An
`agent_reference` tells the API which saved agent should handle the request, while a
conversation keeps messages together across turns.

</div>
</details>

<details markdown="1" class="concept">
<summary>What does Code Interpreter do?</summary>
<div class="concept-body" markdown="1">

Code Interpreter gives the agent a managed environment where it can run code against
attached files. Here, the agent reads `weekly_output.csv`, calculates results, and creates
a chart. The client detects the generated image and displays it in the chat.

</div>
</details>

**Set up:**

If you ran `python ../setup/bootstrap_agent.py` above, your agent, its **Code Interpreter** tool,
and `AGENT_NAME` are already configured — activate your virtual environment
(`.\labenv\Scripts\Activate.ps1`) and skip to **Try it first**.

**If you built the agent yourself in Task 1**, finish wiring it up:

1. In the portal, open your `caldova-agent`, add a **Code interpreter** tool, and upload
    a data file so there's something to analyze. Download and attach:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/A-build-and-extend-ai-agents/Python/weekly_output.csv
    ```

    Save the agent.

1. In the `Labfiles/A-build-and-extend-ai-agents/Python` folder, activate the virtual
    environment (`.\labenv\Scripts\Activate.ps1`). Then open **.env** and add
    `AGENT_NAME=caldova-agent` alongside the `PROJECT_ENDPOINT` you already set. Save the file.

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
    run_chat_app(respond, title="Caldova Supply Chain Assistant")
    ```

Sign in and run it:

```
az login
python agent_with_functions.py
```

Your browser opens a chat window at `http://localhost:7860`. Ask for something that uses
code interpreter:

```
Analyze the weekly production output data and create a chart of output over time.
```

The agent's analysis appears in the chat and the **chart is shown inline**. Close the
browser tab and press **Ctrl+C** in the terminal to stop the app.

</details>

**Stretch**: display the agent's token usage after each response.

---

**Next (optional):** [Task 4 — Add custom function tools](A4-add-custom-function-tools.md)
