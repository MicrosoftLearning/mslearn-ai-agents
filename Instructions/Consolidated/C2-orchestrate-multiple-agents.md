---
title: 'Task 2 – Orchestrate multiple agents in sequence'
lab:
    title: 'Task 2 – Orchestrate multiple agents in sequence'
    description: 'Use the Microsoft Agent Framework to orchestrate several agents in a sequence: a summarizer, a classifier, and an action agent triage a piece of site feedback, each building on the last.'
    type: 'task'
    parent: 'C'
    order: 2
    section: 'optional'
    difficulty: 3
    duration: 30
    access: 'open'
    level: 300
    concepts: 'Microsoft Agent Framework, multi-agent orchestration, sequential workflow'
    status: 'draft'
---

# Task 2 — Orchestrate multiple agents in sequence

*Part of the **Build multi-agent solutions with the Agent Framework** lab. New here? Start with [Getting started](C0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](C0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Create the agents** below.

---

Some jobs are best done by a **team** of specialists, each handling one step and passing its
result to the next. The Microsoft Agent Framework's **sequential orchestration** does exactly
that: it runs a list of agents in order and collects each one's output. In this task you'll build
a Caldova **feedback triage** pipeline — a *summarizer* condenses a site comment, a
*classifier* labels it, and an *action* agent recommends the next step.

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
<summary>What is sequential orchestration?</summary>
<div class="concept-body" markdown="1">

**Sequential orchestration** runs several agents one after another, feeding the running
conversation from each agent into the next. It's a good fit when a task breaks cleanly into
ordered stages — summarize, then classify, then decide — and each stage benefits from the output
of the one before it. In the Agent Framework you build one with `SequentialBuilder`, listing the
participant agents in the order they should run.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/agents/overview)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](C0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Create the agents

Open **feedback_agents.py** and add code at each commented placeholder.

1. Review the code already in the file. In the `main` function, take a moment to read the three
    sets of agent **instructions** (summarizer, classifier, action) — these define what each agent
    does.

    > **Tip**: As you add code, keep the indentation aligned with the comments.

1. At the top of the file, find the comment **Add references** and add the namespaces you'll need:

    ```python
    # Add references
    from agent_framework import Message
    from agent_framework.foundry import FoundryChatClient
    from agent_framework.orchestrations import SequentialBuilder
    from azure.identity import AzureCliCredential
    ```

1. Find the comment **Create the chat client** and add the following (keep the indentation level):

    ```python
    # Create the chat client
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    )
    ```

    The **AzureCliCredential** lets your code authenticate to Azure using your `az login` session, and the **FoundryChatClient** connects to your Foundry project. All three agents share this one client.

1. Find the comment **Create agents** and add the following to create the three agents from the shared client:

    ```python
    # Create agents
    summarizer_agent = chat_client.as_agent(
        name="summarizer",
        instructions=summarizer_instructions,
    )

    classifier_agent = chat_client.as_agent(
        name="classifier",
        instructions=classifier_instructions,
    )

    action_agent = chat_client.as_agent(
        name="action",
        instructions=action_instructions,
    )
    ```

1. Find the comment **Initialize the current feedback** and add a sample piece of site feedback for the pipeline to triage:

    ```python
    # Initialize the current feedback
    feedback="""
    I use the line-scheduling app before every changeover, and it works well overall.
    But when I'm checking the schedule at night on the floor, the bright screen is really harsh on my eyes.
    If you added a dark mode option, it would make it much more comfortable to use in low light.
    """
    ```

### Create a sequential orchestration

1. Find the comment **Build sequential orchestration** and add the following to define the pipeline:

    ```python
    # Build sequential orchestration
    workflow = SequentialBuilder(
        participants=[summarizer_agent, classifier_agent, action_agent],
        output_from="all",
    ).build()
    ```

    The agents process the feedback in the order they're listed. `output_from="all"` ensures the outputs from *every* agent are collected, not just the last one.

1. Find the comment **Run and collect outputs** and add the following:

    ```python
    # Run and collect outputs
    result = await workflow.run(f"Site feedback: {feedback}")
    outputs = result.get_outputs()
    ```

    This runs the orchestration and collects the output from each participating agent.

1. Find the comment **Display outputs** and add the following:

    ```python
    # Display outputs
    i = 1
    for response in outputs:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            i += 1
    ```

    This formats and prints each message collected from the orchestration, labeled with the agent that produced it.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python feedback_agents.py
    ```

1. Review the output. Each agent contributes one step, and you should see output similar to:

    ```
    Site team requests a dark mode option for comfortable night-shift use.
    Feature request
    Log as an enhancement request to add a dark mode for night-shift use.
    ------------------------------------------------------------
    01 [summarizer]
    Site team requests a dark mode option for comfortable night-shift use.
    ------------------------------------------------------------
    02 [classifier]
    Feature request
    ------------------------------------------------------------
    03 [action]
    Log as an enhancement request to add a dark mode for night-shift use.
    ```

    > **Tip**: If the app fails because the rate limit is exceeded, wait a few seconds and try again. Try editing the `feedback` string to a complaint or a compliment and run again to see the classification and recommended action change.

> ✅ **Checkpoint**: You've orchestrated three agents in a sequence with the Microsoft Agent
> Framework, passing work from one specialist to the next and collecting every agent's output.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 3 — Connect remote agents with A2A](C3-connect-remote-agents-with-a2a.md)
