# Lab A — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Build and extend AI agents*. Use it to unblock a stuck learner, verify expected behavior,
or run the whole scenario end to end.

```
Solution/
├─ portal-agent/Python/       # Task 3 — client app (web chat + inline charts)
│  └─ agent_with_functions.py
├─ custom-functions/Python/   # Task 4 — custom function tools (web chat)
│  └─ agent.py
└─ mcp/Python/                # Task 2 — remote MCP (console) + Task 5 — your own MCP (web chat)
   ├─ agent.py                #   Task 2: Microsoft Learn Docs MCP + approval loop
   ├─ server.py               #   Task 5: your MCP server (inventory + sales tools)
   └─ client.py               #   Task 5: MCP client that drives the agent
```

`contoso_ui.py` (the shared Gradio chat shell) is included in each folder unchanged — it is
provided to learners and is **not** something they edit.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo. Do these once, then run each task.

### 1. Azure / Microsoft Foundry setup
1. Have an **Azure subscription** with access to **Microsoft Foundry (Azure AI Foundry)**.
2. Create (or open) a **Foundry project** and copy its **Project Endpoint**.
3. **Deploy a model** (for example `gpt-4o`) in that project and note the **deployment name**.
4. Make sure your signed-in identity has the **Azure AI User** role (or equivalent) on the project.

### 2. Sign in locally
```
az login
```
Sign in with the same account that has access to the project. This is the #1 cause of the
Gradio *"Connection errored out"* toast — if `az login` is missing or expired, `respond()`
throws when you send a message and the browser shows a generic error while the **real
traceback prints in the terminal**.

### 3. Create the portal agent (Task 1 — required for Task 3)
The client in `portal-agent/Python` loads an agent **by name** that you create in the portal:
1. In the Foundry portal, create an agent named **`trailhead-agent`**.
2. Ground it: upload **`Store_Policy.txt`** (from `Labfiles/A-build-and-extend-ai-agents/portal-agent/`)
   and give it instructions to answer from store policy.
3. For Task 3's chart demo, add the **Code interpreter** tool and upload
   **`weekly_sales.csv`** (from the same folder). Save the agent.

> Tasks 4 and 5 create their own agents in code (`trip-planner-agent`, `inventory-agent`)
> and delete them on exit — no portal work needed for those.

### 4. Per task: environment + secrets
In **each** task's `Python` folder:
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values:
- **portal-agent** → `PROJECT_ENDPOINT`, `AGENT_NAME=trailhead-agent`
- **custom-functions** → `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
- **mcp** → `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`

### 5. Run each task
| Task | Folder | Command | What you get |
|------|--------|---------|--------------|
| 2 | `mcp/Python` | `python agent.py` | Console output: agent calls the Learn Docs MCP and answers |
| 3 | `portal-agent/Python` | `python agent_with_functions.py` | Browser chat at `http://localhost:7860`, charts render inline |
| 4 | `custom-functions/Python` | `python agent.py` | Browser chat; agent calls your Python functions |
| 5 | `mcp/Python` | `python client.py` | Browser chat; agent calls tools from your own MCP server |

For the web tasks (3–5): the browser opens automatically. **Close the tab and press Ctrl+C**
in the terminal to stop the app. Tasks 4 and 5 delete their agent version on exit.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- From `custom-functions/Python`: `python -c "import functions; print(functions.calculate_rental_cost('premium', 5, 'priority'))"`
  should show a total cost of **$1,875** (premium $300/day × 5 × priority 1.25).
