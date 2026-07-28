# Lab D — Solution (complete code)

This folder contains a **finished, working version** of the optional client-app task
(**D4**) in *Design agent workflows in Microsoft Foundry*. The core of this lab is built in
the Foundry **visual workflow designer** (portal), so there's only a small amount of code —
the client that invokes your saved workflow.

```
Solution/
└─ Python/
   ├─ workflow.py       # Task D4 — invoke the workflow from code (console output)
   ├─ workflow_ui.py    #   Task D4 — same invocation behind the shared Gradio web chat
   ├─ tailwind_ui.py    # shared Gradio chat shell (provided; not edited by learners)
   ├─ requirements.txt
   └─ .env.example
```

The workflow itself — the **Set variable**, **For each**, **Invoke agent**, and **If/Else**
nodes — lives in the Foundry portal, not in this repo. Build it by following instruction
pages **D1–D3**. The prompts, JSON schema, and node messages you paste into the portal are in
`../assets/agent-prompts.md`.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo.

### 1. Build the workflow in the Foundry portal
Follow **D1** (and optionally **D2**/**D3**) to create and **Save** a workflow named
**`Tailwind-Traders-Support-Triage`**. The client loads the workflow **by name**, so the name
must match exactly (or update the `workflow["name"]` value in `workflow.py`).

### 2. Sign in locally
```
az login
```
Sign in with the same account that has access to your Foundry project. A missing or expired
`az login` is the #1 cause of runtime errors when the client calls the project.

### 3. Set up the environment
From the `Python/` folder:
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and set:
- `PROJECT_ENDPOINT` — your Foundry project endpoint (Code > **.env variables** in the
  workflow visualizer shows it as `AZURE_EXISTING_AIPROJECT_ENDPOINT`).

### 4. Run it
| Command | What you get |
|---------|--------------|
| `python workflow.py` | Console output: each ticket's category, confidence, and drafted response |
| `python workflow_ui.py` | Browser chat at `http://localhost:7860`; type a message to run the workflow, results render inline |

For the web version, the browser opens automatically. **Close the tab and press Ctrl+C** in
the terminal to stop the app. When you're finished, enter `deactivate` to exit the virtual
environment.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile workflow.py workflow_ui.py tailwind_ui.py` — all solution files compile.
- `python -c "import workflow_ui; print(workflow_ui.format_workflow_output('{\"customer_issue\":\"x\",\"category\":\"Gear\",\"confidence\":0.92}Try a factory reset.'))"`
  formats one ticket into readable markdown without contacting Azure.
