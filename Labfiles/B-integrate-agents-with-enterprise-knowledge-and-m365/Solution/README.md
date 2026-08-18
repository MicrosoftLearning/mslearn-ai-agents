# Lab B — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Integrate agents with enterprise knowledge and Microsoft 365*. Use it to unblock a stuck
learner, verify expected behavior, or run the scenario end to end.

All code tasks share a **single** `Python/` folder (one virtual environment, one `.env`),
exactly like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ knowledge_agent.py      # Task 1 (core) — console client for the Foundry IQ agent + approval loop
   ├─ knowledge_chat_app.py   # Task 1 (optional) — same agent in a web chat window (auto-approves)
   ├─ workiq_lab.py           # Task 4 — Work IQ workplace intelligence (menu-driven, 5 scenarios)
   ├─ caldova_ui.py          # shared Gradio chat shell (provided; not edited by learners)
   ├─ requirements.txt        # shared dependencies for all tasks
   ├─ .env.example            # copy to .env and fill in
   └─ data/                   # Caldova knowledge base (grounding docs)
```

Two of the four tasks are **portal publishing workflows** (Task 2: Microsoft Teams, Task 3:
Microsoft 365 Copilot). They add no new Python — you publish the Task 1 agent through the
Foundry portal — so there are no solution files for them.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Exercises/B0-getting-started.md` (shared setup)
  plus `B1`–`B4` (one page per task). Each task page tells a standalone learner exactly what it
  needs and how to fast-forward.
- **Setup scripts** in `Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/setup/`:
  - `check_env.py --task N` — preflight-checks that `.env` has the keys task *N* needs.
    Run it as `python ../setup/check_env.py --task N`.
  - `bootstrap_agent.py` — **fast-forwards the Task 1 grounding step in code**: creates and
    grounds `caldova-knowledge-agent` (File Search over the `data/` knowledge base) and writes
    `AGENT_NAME` to `.env`, so learners can start against a working agent without the portal.
    Idempotent; pass `--force` to recreate.

Both scripts run from the **starter** `Python/` folder
(`Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Python`, not `Solution/Python/`)
and use the shared virtual environment and `.env`. That's why the paths above are
`../setup/...` — `setup/` is a sibling of the starter `Python/` folder.

> **Note**: Task 1 in the portal grounds the agent with **Foundry IQ** (a knowledge source with
> agentic retrieval and an approval step). `bootstrap_agent.py` uses the simpler **File Search**
> tool so learners get a working grounded agent without the portal steps. The client code you run
> against either agent is identical.

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
Sign in with the same account that has access to the project.

### 3. Create the Foundry IQ knowledge agent (Task 1 — required for the code clients)
The Task 1 clients load an agent **by name** that you create in the portal:
1. In the Foundry portal, create an agent named **`caldova-knowledge-agent`**.
2. Add a **Foundry IQ knowledge source** and index the Caldova docs from `Python/data/`.
3. Give it instructions to answer planning and materials questions from the knowledge base. Save the agent.

> **Shortcut**: instead of the portal grounding above, run `python ../setup/bootstrap_agent.py`
> from the **starter** `Python/` folder (not `Solution/Python/`) to create and ground
> `caldova-knowledge-agent` in code (File Search) and
> write `AGENT_NAME`.

### 4. Set up the environment once (shared by all code tasks)
From this folder (`Solution/Python/`):
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values (all tasks read the same file):
- `PROJECT_ENDPOINT` — used by the code tasks
- `MODEL_DEPLOYMENT_NAME` — used by Task 4 (Work IQ)
- `AGENT_NAME=caldova-knowledge-agent` — used by the Task 1 code clients

### 5. Run each task
Code tasks run from the single `Solution/Python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python knowledge_agent.py` | Console chat: agent answers from the knowledge base; you approve the Foundry IQ tool interactively |
| 1 (web) | `python knowledge_chat_app.py` | Browser chat at `http://localhost:7860`; same agent, auto-approves the knowledge tool |
| 2 | *(portal)* | Publish the Task 1 agent to **Microsoft Teams** — no code |
| 3 | *(portal)* | Publish the Task 1 agent to **Microsoft 365 Copilot** — no code |
| 4 | `python workiq_lab.py` | Menu-driven console app: agent queries Microsoft 365 through Work IQ (5 scenarios) |

For the web variant (Task 1): the browser opens automatically. **Close the tab and press Ctrl+C**
in the terminal to stop the app. Task 4 deletes its agent version on exit.

> **Work IQ prerequisites (Task 4)**: an M365 Copilot license, admin consent, and the Work IQ CLI
> installed (`npm install -g @microsoft/workiq`, then `workiq accept-eula`). See B4 for details.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile <file>` — all solution files compile.
- The knowledge base under `Python/data/` is what the agent is grounded on; ask the running agent
  about **site headroom**, **premium tier transfer rates**, or **supplier lead times** to
  confirm grounding works.
