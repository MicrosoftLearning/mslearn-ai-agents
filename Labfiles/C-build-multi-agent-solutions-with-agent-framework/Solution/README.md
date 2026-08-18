# Lab C — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Build multi-agent solutions with the Agent Framework*. Use it to unblock a stuck learner,
verify expected behavior, or run the whole scenario end to end.

All tasks share a **single** `Python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ expense_agent.py        # Task 1 — single agent with a tool (Microsoft Agent Framework)
   ├─ data.txt                #   Task 1 — Caldova site-visit expense data
   ├─ feedback_agents.py      # Task 2 — sequential orchestration of three agents (MAF)
   ├─ run_all.py              # Task 3 — launches the three A2A agent servers
   ├─ client.py               # Task 3 — chat client that talks to the routing agent
   ├─ title_agent/            #   Task 3 — remote agent: suggests a transfer brief title
   ├─ outline_agent/          #   Task 3 — remote agent: drafts a transfer plan outline
   ├─ routing_agent/          #   Task 3 — orchestrator that delegates to the remote agents via A2A
   ├─ ticket_triage.py        # Task 4 — single agent classifies a ticket; code routes on the result
   └─ sample_tickets.json     #   Task 4 — sample Caldova support tickets
```

The whole lab is built on the **Microsoft Agent Framework (MAF)**. Task 1 and Task 2 use the
native MAF path — `FoundryChatClient` + `@tool` + `Agent` + `agent.create_session()` +
`agent.run(..., session=)` -> `result.text`. Task 3 keeps the Foundry SDK inner agents and
adds the **A2A** protocol so agents in separate processes can call each other. Task 4 returns to a
single MAF agent, but uses its **structured (JSON) output** to drive **conditional routing** in code.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Exercises/C0-getting-started.md` (shared setup)
  plus `C1`–`C4` (one page per task). Each task page tells a standalone learner exactly what it
  needs and how to fast-forward.
- **Setup scripts** in `Labfiles/C-build-multi-agent-solutions-with-agent-framework/setup/`:
  - `check_env.py --task N` — preflight-checks that `.env` has the keys task *N* needs.
    Run it as `python ../setup/check_env.py --task N`.

The script runs from the **starter** `Python/` folder
(`Labfiles/C-build-multi-agent-solutions-with-agent-framework/Python`, not `Solution/Python/`)
and uses the shared virtual environment and `.env`. That's why the path above is
`../setup/...` — `setup/` is a sibling of the starter `Python/` folder.

### Optional: provision infrastructure with azd

Instead of creating the project by hand, `azure.yaml` + `infra/` let you provision a Foundry
project and model deployment with one command:

```
azd up      # create the project + model deployment, writes Python/.env
azd down    # remove everything when you're done
```

The manual portal path is still the default — azd is offered as **Option B** in Getting started
for learners who prefer infrastructure as code.

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
Sign in with the same account that has access to the project. Every task authenticates with
`DefaultAzureCredential`, so a missing or expired `az login` is the most common reason a task
fails at run time.

### 3. Set up the environment once (shared by all tasks)
From this folder (`Solution/Python/`):
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values (all tasks read the same file):
- `PROJECT_ENDPOINT` — used by every task
- `MODEL_DEPLOYMENT_NAME` — used by every task
- `SERVER_URL`, `TITLE_AGENT_PORT`, `OUTLINE_AGENT_PORT`, `ROUTING_AGENT_PORT` — used by Task 3
  (these ship pre-filled in `.env.example`)

### 4. Run each task
All commands run from the single `Solution/Python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python expense_agent.py` | Console output: the agent reads `data.txt`, then calls the `submit_claim` tool to email an expense claim |
| 2 | `python feedback_agents.py` | Console output: three agents summarize, classify, and recommend an action on site feedback, in sequence |
| 3 | `python run_all.py` (leave running), then in a second terminal `python client.py` | The three A2A agent servers start; the routing agent delegates your request to the transfer-title and transfer-outline agents |
| 4 | `python ticket_triage.py` | Console output: the triage agent classifies three sample tickets; code routes each by category and confidence |

For Task 3, `run_all.py` starts the `title_agent`, `outline_agent`, and `routing_agent`
servers. Wait for all three to report ready, then run `client.py` in another terminal and chat.
Press Ctrl+C in the `run_all.py` terminal to stop every server.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- From `Solution/Python/`: `python -c "print(open('data.txt').read())"` prints the Caldova
  site-visit expense data that Task 1's agent reads.
