---
title: 'Task 2 – Evaluate answer quality'
lab:
    title: 'Task 2 – Evaluate answer quality'
    description: 'Score a grounded agent against a ground-truth dataset with the built-in groundedness, relevance and similarity evaluators, and read the row-level results.'
    type: 'task'
    parent: 'D'
    order: 2
    section: 'core'
    difficulty: 3
    duration: 35
    access: 'open'
    level: 300
    concepts: 'evaluation, groundedness, relevance, similarity, ground truth'
    islab: true
    status: 'draft'
---

# Task 2 — Evaluate answer quality

*Part of the **Observe, evaluate, and secure your agents** lab. New here? Start with [Getting started](D0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, the starter code, and a
> **grounded agent to measure**. If you haven't already, complete
> [Getting started](D0-getting-started.md) to create your project, clone the code, set
> `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`, and either point
> `AGENT_NAME` at your [Lab B](B-integrate-agents-with-enterprise-knowledge-and-m365.md) agent
> or create one with `python ../setup/bootstrap_agent.py`. Then, from the `Python` folder you
> opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished another task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — but Task 1
> didn't need `AGENT_NAME`, so check that it's set before you start.

---

The Caldova knowledge agent answers questions about capacity, contract manufacturers,
and suppliers. It sounds confident every time. That's the problem: you can read ten answers, feel
good about them, and still have no idea whether the eleventh invents a returns window that
doesn't exist.

**Evaluation** replaces that feeling with a number. You take a set of questions you already
know the right answers to, run them through the agent, and have a second model grade what
comes back.

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
<summary>What are groundedness, relevance and similarity?</summary>
<div class="concept-body" markdown="1">

They're three different ways an answer can be wrong, so they're measured separately:

- **Groundedness** — is the answer supported by the **context** it was given? A low score
  means the agent made something up, even if what it made up happens to be true.
- **Relevance** — does the answer actually address the **question**? An answer can be
  perfectly grounded and still not what was asked.
- **Similarity** — how close is the answer to the **ground truth** you wrote? This is the one
  that needs a human-authored correct answer.

Each is scored 1–5 by a model acting as a judge. Groundedness and relevance also return a
`reason`, which is usually more useful than the score.

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](D0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Look at the dataset first

Open **data/caldova_eval.jsonl**. Each line is one test case, and evaluation is only ever as
good as this file:

```json
{"query": "A planner wants to raise a capacity request with a complete program brief. How long does review take?", "context": "Standard Request Window: Requests with a complete program brief: reviewed within 5 business days ...", "ground_truth": "Five business days for a request with a complete program brief ..."}
```

- `query` — what you ask the agent.
- `context` — the source material the answer should be based on. Groundedness grades against this.
- `ground_truth` — the answer a knowledgeable human would give. Similarity grades against this.

The agent's own `response` isn't in the file: you generate it at evaluation time by pointing
the evaluation at a **target**.

Open **agent_target.py** and read it — you don't edit it. It's a callable class that takes one
`query` and returns `{"response": ...}` from your agent. That's the whole contract a target has
to meet.

### Write the evaluation

Open **evaluate_agent.py** and add code at each commented placeholder.

1. **Add references**:

    ```python
    # Add references
    from azure.ai.evaluation import (
        AzureOpenAIModelConfiguration,
        GroundednessEvaluator,
        RelevanceEvaluator,
        SimilarityEvaluator,
        evaluate,
    )
    from agent_target import CaldovaAgentTarget
    ```

1. **Configure the model that grades the answers** — the evaluators are themselves model
    calls, so they need a deployment to run on. You'll reuse the same one your agent uses:

    ```python
    # Configure the model that grades the answers
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=evaluator_endpoint(),
        azure_deployment=model_deployment,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    ```

    > No API key: with `az login` done, the evaluators authenticate as you. `evaluator_endpoint()`
    > is provided at the top of the file — it derives the resource endpoint from your
    > `PROJECT_ENDPOINT`, or uses `AZURE_OPENAI_ENDPOINT` if you set one.

1. **Create the evaluators**:

    ```python
    # Create the evaluators
    groundedness = GroundednessEvaluator(model_config)
    relevance = RelevanceEvaluator(model_config)
    similarity = SimilarityEvaluator(model_config)
    ```

1. **Run the evaluation** — `evaluate()` reads the dataset, calls the target once per row, and
    passes each evaluator exactly the columns it needs. `column_mapping` is how you say which
    column is which: `${data.x}` comes from the file, `${outputs.x}` comes back from the target:

    ```python
    # Run the evaluation
    result = evaluate(
        data=str(DATASET),
        target=CaldovaAgentTarget(),
        evaluators={
            "groundedness": groundedness,
            "relevance": relevance,
            "similarity": similarity,
        },
        evaluator_config={
            "groundedness": {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}",
                    "response": "${outputs.response}",
                }
            },
            "relevance": {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${outputs.response}",
                }
            },
            "similarity": {
                "column_mapping": {
                    "query": "${data.query}",
                    "ground_truth": "${data.ground_truth}",
                    "response": "${outputs.response}",
                }
            },
        },
        azure_ai_project=project_endpoint,
        output_path=str(OUTPUT),
    )
    ```

    > `azure_ai_project` is optional. Passing it uploads the run to your project so you can see
    > the results in the portal alongside everything else.

1. **Print the aggregate scores**:

    ```python
    # Print the aggregate scores
    print("\nAggregate scores (1-5, higher is better):")
    print(json.dumps(result["metrics"], indent=2))
    print(f"\nRow-level detail: {OUTPUT.resolve()}")
    if result.get("studio_url"):
        print(f"View in the Foundry portal: {result['studio_url']}")
    ```

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the evaluation:

    ```
    az login
    ```

    ```
    python evaluate_agent.py
    ```

1. It asks the agent all ten questions and then grades each answer three ways, so give it a
    couple of minutes. You should see something like:

    ```
    Aggregate scores (1-5, higher is better):
    {
      "groundedness.groundedness": 4.6,
      "relevance.relevance": 4.4,
      "similarity.similarity": 4.1
    }

    Row-level detail: ...\eval_results.json
    ```

    > Your numbers will differ. Exact values matter far less than being able to *reproduce*
    > them after a change.

1. Open **eval_results.json** and find the lowest-scoring row. Read its
    `groundedness_reason` or `relevance_reason` — the judge explains itself, and that
    explanation is what you'd act on.

1. Decide whether the score is the agent's fault. Sometimes a low similarity score means the
    agent gave a *better* answer than your ground truth, or that your `context` was too thin
    for the question. Evaluation grades your dataset as much as your agent.

### Make a change and prove it

This is what evaluation is actually for.

1. Add a bad test case to the end of **data/caldova_eval.jsonl** — a question whose `context`
    doesn't support the `ground_truth`, so the agent has nothing to answer from:

    ```json
    {"query": "What is the fast-track window for Halden Biologics?", "context": "Planning Desk Hours: Monday-Friday 8:00 AM - 6:00 PM.", "ground_truth": "Four months to first commercial batch."}
    ```

1. Run `python evaluate_agent.py` again and look at that row. Groundedness should drop sharply
    even if the agent's answer is correct — because the answer isn't supported by the context
    it was given. That distinction is exactly what a hallucination looks like in a metric.

1. Remove the row again when you're done.

> ✅ **Checkpoint**: You have a repeatable score for your agent's answers, row-level reasons
> for every score, and a way to tell whether tomorrow's prompt change made things better or
> worse. That's the Core of this lab — the remaining task is optional.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 3 — Red team your agent](D3-red-team-your-agent.md)
