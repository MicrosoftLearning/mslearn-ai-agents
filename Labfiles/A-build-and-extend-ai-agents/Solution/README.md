# Lab A — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Build and extend AI agents*. Use it to unblock a stuck learner, verify expected behavior,
or run the whole scenario end to end.

All tasks share a **single** `Python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ remote_mcp_agent.py     # Task 2 — remote MCP (Microsoft Learn Docs) + approval loop
   ├─ agent_with_functions.py # Task 3 — client app (web chat + inline charts)
   ├─ functions_agent.py      # Task 4 — custom function tools (web chat)
   ├─ functions_agent_maf.py  #   Task 4 — same agent, Microsoft Agent Framework edition
   ├─ functions.py            #   Task 4: trip-planner helper functions
   ├─ server.py               # Task 5 — your MCP server (inventory + sales tools)
   ├─ client.py               # Task 5 — capstone: MCP client that combines Task 4 + Task 5 tools
   ├─ client_maf.py           #   Task 5 — same capstone, Microsoft Agent Framework edition
   ├─ trailhead_ui.py         # shared Gradio chat shell (provided; not edited by learners)
   ├─ Store_Policy.txt        # Task 1 grounding doc (uploaded to the portal agent)
   ├─ weekly_sales.csv        # Task 3 code-interpreter data (uploaded to the portal agent)
   └─ data/                   #   Task 4 lookup data (trips, rental rates, service multipliers)
```

Because everything lives in one folder, the two `agent.py` files from the source labs were
renamed to avoid a collision: **`remote_mcp_agent.py`** (Task 2) and **`functions_agent.py`**
(Task 4). `trailhead_ui.py` (the shared Gradio chat shell) appears once and is **not**
something learners edit.

---

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Exercises/A0-getting-started.md` (shared setup)
  plus `A1`–`A5` (one page per task). Each task page tells a standalone learner exactly what it
  needs and how to fast-forward.
- **Setup scripts** in `Labfiles/A-build-and-extend-ai-agents/setup/`:
  - `check_env.py --task N` — preflight-checks that `.env` has the keys task *N* needs.
  - `bootstrap_agent.py` — **fast-forwards Task 1 in code**: creates and grounds
    `trailhead-agent` (File Search on `Store_Policy.txt` + Code Interpreter on `weekly_sales.csv`)
    and writes `AGENT_NAME` to `.env`, so learners can start at **Task 3** without the portal.
    Idempotent; pass `--force` to recreate.

Both scripts run from the **starter** `Python/` folder and use the shared virtual environment
and `.env`.

### Optional: provision infrastructure with azd

Instead of creating the project by hand, `azure.yaml` + `infra/` let you provision a Foundry
project and model deployment with one command:

```
azd up      # create the project + model deployment, writes Python/.env
azd down    # remove everything when you're done
```

The manual portal path (Task 1) is still the default — azd is offered as **Option B** in
Getting started for learners who prefer infrastructure as code.

> **Note**: the azd path is bicep-validated but has not been deployment-tested in this repo yet.

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
The Task 3 client loads an agent **by name** that you create in the portal:
1. In the Foundry portal, create an agent named **`trailhead-agent`**.
2. Ground it: upload **`Store_Policy.txt`** (from `Python/`) and give it instructions to
   answer from store policy.
3. For Task 3's chart demo, add the **Code interpreter** tool and upload **`weekly_sales.csv`**
   (from the same folder). Save the agent.

> Tasks 4 and 5 create their own agents in code (`trip-planner-agent`, `trailhead-assistant`)
> and delete them on exit — no portal work needed for those.

> **Shortcut**: instead of the portal steps above, run `python setup/bootstrap_agent.py` from
> the `Python/` folder to create and ground `trailhead-agent` in code and write `AGENT_NAME`.

### 4. Set up the environment once (shared by all tasks)
From the `Python/` folder:
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values (all tasks read the same file):
- `PROJECT_ENDPOINT` — used by every task
- `MODEL_DEPLOYMENT_NAME` — used by Tasks 2, 4, and 5
- `AGENT_NAME=trailhead-agent` — used by Task 3

### 5. Run each task
All commands run from the single `Python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 2 | `python remote_mcp_agent.py` | Console output: agent calls the Learn Docs MCP and answers |
| 3 | `python agent_with_functions.py` | Browser chat at `http://localhost:7860`, charts render inline |
| 4 | `python functions_agent.py` | Browser chat; agent calls your Python functions |
| 4 (MAF) | `python functions_agent_maf.py` | Same agent built with the Microsoft Agent Framework (`@tool` + `agent.run()`) |
| 5 | `python client.py` | Browser chat; **capstone** — one agent that plans trips (Task 4 functions) *and* checks the warehouse (your MCP server). Do Task 4 first. |
| 5 (MAF) | `python client_maf.py` | Same capstone built with the Microsoft Agent Framework (`MCPStdioTool` + `agent.run()`) |

For the web tasks (3–5): the browser opens automatically. **Close the tab and press Ctrl+C**
in the terminal to stop the app. Tasks 4 and 5 delete their agent version on exit. The `_maf.py`
variants are provided complete as a framework comparison — see the "Two ways to build the same
agent" section in the exercise instructions.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- From `Python/`: `python -c "import functions; print(functions.calculate_rental_cost('premium', 5, 'priority'))"`
  should show a total cost of **$1,875** (premium $300/day × 5 × priority 1.25).
