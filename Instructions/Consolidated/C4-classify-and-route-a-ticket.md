---
title: 'Task 4 – Classify and route a support ticket'
lab:
    title: 'Task 4 – Classify and route a support ticket'
    description: 'Use the Microsoft Agent Framework to classify Caldova support tickets with a triage agent, then route each one in code based on its category and confidence.'
    type: 'task'
    parent: 'C'
    order: 4
    section: 'optional'
    difficulty: 3
    duration: 30
    access: 'open'
    level: 300
    concepts: 'Microsoft Agent Framework, structured output, classification, conditional routing'
    status: 'draft'
---

# Task 4 — Classify and route a support ticket

*Part of the **Build multi-agent solutions with the Agent Framework** lab. New here? Start with [Getting started](C0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](C0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 4
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Build the triage agent** below.

---

Not every multi-agent job needs a pipeline. Sometimes one agent does the *thinking* — reading a
message and making a decision — and your **code** acts on that decision. In this task you'll build
a Caldova **support-desk triage**: a single agent classifies each support ticket into a
category with a confidence score, and your Python code routes the ticket accordingly — escalating
billing problems, sending low-confidence tickets back for more detail, and handling the rest
automatically.

The trick that makes this work is **structured output**: you ask the agent to answer with a small
JSON object instead of prose, so your code can branch on it reliably.

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
<summary>Why route in code instead of one big prompt?</summary>
<div class="concept-body" markdown="1">

You *could* ask a single agent to both classify **and** decide what to do — but keeping the
**decision** (an agent's judgment) separate from the **routing** (your business rules) makes the
system easier to test, audit, and change. The agent returns a small, predictable classification;
your code owns what happens next. Asking the model for **structured output** (here, a JSON object
with `category` and `confidence`) is what lets code branch on the result deterministically.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/agents/overview)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](C0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Build the triage agent

Open **ticket_triage.py** and add code at each commented placeholder.

1. Review the code already in the file. Notice the `TRIAGE_INSTRUCTIONS` (which tell the agent to
    return a JSON object with `customer_issue`, `category`, and `confidence`), the
    `parse_classification` helper (which reads that JSON out of the reply), and `route_ticket`
    (your business rules). The sample tickets are loaded from `sample_tickets.json`.

    > **Tip**: As you add code, keep the indentation aligned with the comments.

1. At the top of the file, find the comment **Add references** and add the namespaces you'll need:

    ```python
    # Add references
    from agent_framework import Agent
    from agent_framework.foundry import FoundryChatClient
    from azure.identity import AzureCliCredential
    ```

1. Find the comment **Create a foundry chat client** and add the following (keep the indentation level):

    ```python
    # Create a foundry chat client
    client = FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    )
    ```

    The **AzureCliCredential** lets your code authenticate to Azure using your `az login` session, and the **FoundryChatClient** connects to your Foundry project.

1. Find the comment **Create the triage agent** and add the following:

    ```python
    # Create the triage agent
    agent = Agent(
        client=client,
        name="TicketTriageAgent",
        instructions=TRIAGE_INSTRUCTIONS,
    )
    ```

    A single agent, backed by the shared client, does all the classifying. Its behavior comes entirely from `TRIAGE_INSTRUCTIONS`.

### Classify and route each ticket

1. Inside the `for` loop, find the comment **Create a session, classify the ticket, then parse and route the result** and add the following (replace the `pass` placeholder):

    ```python
        # Create a session, classify the ticket, then parse and route the result
        session = agent.create_session()
        response = await agent.run(ticket, session=session)

        try:
            classification = parse_classification(response.text)
        except (ValueError, json.JSONDecodeError):
            print("  [review] Could not parse the classification. Send for manual review.")
            continue

        category = classification.get("category", "unknown")
        confidence = float(classification.get("confidence", 0))
        print(f"  Category:   {category} (confidence {confidence:.2f})")
        print(f"  Decision:   {route_ticket(classification)}")
    ```

    For each ticket you create a fresh session, run the agent to get its classification, parse the
    JSON, and then hand the result to `route_ticket` — the same **classify, then branch** pattern
    you'd otherwise build node-by-node in a larger workflow.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python ticket_triage.py
    ```

1. Review the output. Each ticket is classified and routed. You should see output similar to:

    ```
    Ticket 1: The batch record terminal on packaging line B keeps losing its connection even after a full restart.
      Category:   Equipment (confidence 0.95)
      Decision:   [auto] Equipment issue: send troubleshooting steps and raise a maintenance job.

    Ticket 2: Is there a way to see all of our past capacity requests and export them as a report?
      Category:   General (confidence 0.90)
      Decision:   [auto] General question: reply with a help-center answer.

    Ticket 3: We were invoiced twice for the same transfer week last Friday and the statement shows two payments. Can someone fix this?
      Category:   Billing (confidence 0.97)
      Decision:   [escalated] Billing issue routed to the Caldova orders team.
    ```

    > **Tip**: Try adding a vague ticket (for example, `"It's not working"`) to `sample_tickets.json`. A low confidence score should trip the `CONFIDENCE_THRESHOLD` and route it back for more detail instead of guessing.

> ✅ **Checkpoint**: You've used a single agent's **structured output** to drive **conditional
> routing** in code — classifying each ticket and branching on category and confidence, without a
> visual workflow designer.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next:** You've completed the optional tasks. Head back to the [lab overview](C-build-multi-agent-solutions-with-agent-framework.md) for a summary and clean-up steps.
