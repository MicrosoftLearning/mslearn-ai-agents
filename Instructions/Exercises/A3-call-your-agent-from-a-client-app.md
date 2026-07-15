---
lab:
    title: 'Task 3 – Call your agent from a client app'
    description: 'Drive your grounded portal agent from a small web chat app using the Foundry SDK and Responses API, with inline charts.'
    level: 300
    concepts: 'Foundry SDK, Responses API, code interpreter'
    islab: true
    status: 'draft'
---

# Task 3 — Call your agent from a client app

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Starting here on its own?** First complete [Getting started](A0-getting-started.md) to set
> up your Foundry project and `.env`.
>
> Task 3 drives the **grounded agent** you build in [Task 1](A1-create-and-ground-an-agent.md).
> If you didn't do Task 1, create that agent in code with one command (from the
> `Labfiles/A-build-and-extend-ai-agents` folder):
>
> ```
> python setup/bootstrap_agent.py
> ```
>
> That creates and grounds `trailhead-agent` — including the **Code Interpreter** tool with the
> sales data already attached — and writes `AGENT_NAME` into your `.env`. If you used it, you can
> skip the portal "Set up" step below that adds Code Interpreter. Then verify you're ready:
>
> ```
> python setup/check_env.py --task 3
> ```

---

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
    you set up in [Getting started](A0-getting-started.md) (if you closed the terminal, reactivate with
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

---

**Next (optional):** [Task 4 — Add custom function tools](A4-add-custom-function-tools.md)
