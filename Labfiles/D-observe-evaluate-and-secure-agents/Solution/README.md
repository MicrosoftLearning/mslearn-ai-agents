# Lab D — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Observe, evaluate, and secure your agents*. Use it to unblock a stuck learner, verify
expected behavior, or run the whole scenario end to end.

All tasks share a **single** `Python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ Python/
   ├─ traced_agent.py     # Task 1 — OpenTelemetry + Azure Monitor tracing, with custom spans
   ├─ evaluate_agent.py   # Task 2 — groundedness, relevance and similarity against ground truth
   ├─ red_team_agent.py   # Task 3 — AI Red Teaming Agent scan of the deployed agent
   ├─ agent_target.py     # provided; wraps the knowledge agent as an evaluation target
   ├─ data/
   │  ├─ caldova_eval.jsonl      # Task 2 — 10 questions with context and ground truth
   │  └─ attack_objectives.json   # Task 3 — custom adversarial seed prompts
   └─ knowledge/          # grounding docs used by ../setup/bootstrap_agent.py
```

`agent_target.py` is provided complete in the starter folder too — learners don't write it.
It exists so the evaluation code stays about *evaluation* rather than about calling an agent,
which they already did in Labs A and B.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** — `Instructions/Consolidated/D0-getting-started.md` (shared
  setup) plus `D1`–`D3` (one page per task).
- **Setup scripts** in `Labfiles/D-observe-evaluate-and-secure-agents/setup/`:
  - `check_env.py --task N` — preflight-checks that `.env` has the keys task *N* needs.
    Run it as `python ../setup/check_env.py --task N`.
  - `bootstrap_agent.py` — creates and grounds `caldova-knowledge-agent` (File Search over
    the docs in `Python/knowledge/`) and writes `AGENT_NAME` to `.env`, so Tasks 2 and 3
    have something to measure without doing Lab B first. Idempotent; pass `--force` to
    recreate.

Both scripts run from the **starter** `Python/` folder
(`Labfiles/D-observe-evaluate-and-secure-agents/Python`, not `Solution/Python/`).

### Optional: provision infrastructure with azd

`azure.yaml` and `infra/` are generated from `Labfiles/_shared/` — don't edit them here.
They provision a Foundry project and model deployment:

```
azd up      # create the project + model deployment, writes Python/.env
azd down    # remove everything when you're done
```

They do **not** create the Application Insights resource Task 1 needs. That is a *connection*
on the Foundry project, and the lab has learners make it in the portal (Agents > Traces >
Connect) because that is where they will then read the traces.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo.

### 1. Azure / Microsoft Foundry setup
1. A **Foundry project** with a **deployed chat model** (for example `gpt-4o`).
2. An **Application Insights** resource connected to the project (Task 1).
3. Your signed-in identity needs **Azure AI User** (or equivalent) on the project, and
   **Log Analytics Reader** on the Application Insights resource to read traces.
4. For Task 3, the project must be in a region the AI Red Teaming Agent supports:
   East US 2, France Central, Sweden Central, Switzerland West, or North Central US.

### 2. Sign in locally
```
az login
```

### 3. Create the agent Tasks 2 and 3 measure
Either reuse the Lab B knowledge agent (set `AGENT_NAME` to its name), or from the
**starter** `Python/` folder run:
```
python ../setup/bootstrap_agent.py
```

### 4. Set up the environment once (shared by all tasks)
From this folder (`Solution/Python/`):
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
and `AGENT_NAME`.

> **Python version**: use 3.10–3.13. The `[redteam]` extra pulls in PyRIT, which does not
> support 3.14 yet.

### 5. Run each task

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python traced_agent.py` | Three answers in the terminal, and a trace per question in the Foundry portal's **Traces** tab |
| 2 | `python evaluate_agent.py` | Aggregate groundedness/relevance/similarity scores, `eval_results.json`, and a portal link |
| 3 | `python red_team_agent.py` | An attack-success-rate scorecard in `redteam_scan.json` |
| 3 (custom prompts) | `python red_team_agent.py --seed-prompts` | The same scan driven by `data/attack_objectives.json` |

Task 3 takes several minutes and sends deliberately harmful prompts to your own agent.

---

## Quick sanity checks that DON'T need Azure
- `python -m py_compile traced_agent.py evaluate_agent.py red_team_agent.py agent_target.py`
- `python -c "import json;[json.loads(l) for l in open('data/caldova_eval.jsonl',encoding='utf-8')];print('dataset ok')"`
- `python -c "import json;print(len(json.load(open('data/attack_objectives.json',encoding='utf-8'))),'seed prompts')"`

> **Note**: this lab's code has been import- and syntax-verified against
> `azure-ai-projects==2.3.0` and `azure-ai-evaluation==1.18.3`, but it has **not** been run
> end to end against a live Foundry project in this repo.
