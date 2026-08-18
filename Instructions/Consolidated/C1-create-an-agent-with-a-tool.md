---
title: 'Task 1 – Build an agent with a tool'
lab:
    title: 'Task 1 – Build an agent with a tool'
    description: 'Use the Microsoft Agent Framework to build a single agent that calls a custom tool: decorate a Python function with @tool, attach it to an Agent, and let agent.run() drive the tool-calling loop.'
    type: 'task'
    parent: 'C'
    order: 1
    section: 'core'
    difficulty: 3
    duration: 30
    access: 'open'
    level: 300
    concepts: 'Microsoft Agent Framework, tools, agents'
    status: 'draft'
---

# Task 1 — Build an agent with a tool

*Part of the **Build multi-agent solutions with the Agent Framework** lab. New here? Start with [Getting started](C0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](C0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 1
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Build the agent with a custom tool** below.

---

Every useful agent can *do* something beyond chatting. With the **Microsoft Agent Framework
(MAF)**, you give an agent a capability by writing an ordinary Python function, marking it with
`@tool`, and handing it to the agent — the framework generates the tool's schema and runs the
whole tool-calling loop for you. In this task you'll build the Caldova **site-visit expense
agent**: it reads an engineer's site-visit expense data, itemizes it, and calls a tool to "email" a
reimbursement claim to the finance desk.

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
<summary>What is a tool?</summary>
<div class="concept-body" markdown="1">

A **tool** is a function you give an agent so it can take action or fetch information beyond the
model's own knowledge. In the Agent Framework you write a normal Python function and add the
`@tool` decorator; the framework reads the function signature (including the parameter
descriptions) to build the schema the model needs. When the model decides a tool is needed,
`agent.run()` calls your function, feeds the result back to the model, and continues — all
automatically.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/agents/overview)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](C0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Build the agent with a custom tool

Open **expense_agent.py** and add code at each commented placeholder.

1. Review the code already in the file. It contains:
    - Some **import** statements.
    - A `main` function that loads `data.txt` (the site-visit expense data), asks you what to do with it, and then calls...
    - A `process_expenses_data` function where you'll create and run your agent.

    > **Tip**: As you add code, keep the indentation aligned with the comments.

1. At the top of the file, find the comment **Add references** and add the namespaces you'll need:

    ```python
    # Add references
    from agent_framework import tool, Agent
    from agent_framework.foundry import FoundryChatClient
    from azure.identity import AzureCliCredential
    from pydantic import Field
    ```

1. Near the bottom of the file, find the comment **Create a tool function for the email functionality** and add the tool the agent will use to send the claim:

    ```python
    # Create a tool function for the email functionality
    @tool(approval_mode="never_require")
    def submit_claim(
        to: Annotated[str, Field(description="Who to send the email to")],
        subject: Annotated[str, Field(description="The subject of the email.")],
        body: Annotated[str, Field(description="The text body of the email.")],
    ):
        """Submit a Caldova site-visit expense claim by sending an email."""
        print("\nTo:", to)
        print("Subject:", subject)
        print(body, "\n")
    ```

    > **Note**: The function *simulates* sending an email by printing it to the console. In a real application, you'd use an SMTP service or similar to actually send the email. `approval_mode="never_require"` lets the agent call the tool without pausing to ask you for approval each time.

1. Back up in the `process_expenses_data` function, find the comment **Create a foundry chat client** and add the following (keep the indentation level):

    ```python
    # Create a foundry chat client
    client = FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    )
    ```

    The **AzureCliCredential** object lets your code authenticate to Azure using your `az login` session. The **FoundryChatClient** connects to your Foundry project using the endpoint and model deployment name from `.env`.

1. Find the comment **Initialize an agent with the tool and instructions** and add the following:

    ```python
    # Initialize an agent with the tool and instructions
    agent = Agent(
        client=client,
        name="SiteVisitExpenseAgent",
        instructions="""You are an AI assistant for Caldova site-visit expense claims.
                    At the user's request, create an expense claim and use the submit_claim tool to send an email to expenses@caldova.example with the subject 'Site Visit Expense Claim' and a body that contains the itemized expenses with a total.
                    Then confirm to the user that you've done so. Don't ask for any more information from the user, just use the data provided to create the email.""",
        tools=[submit_claim],
    )
    ```

    The **Agent** object is initialized with the client, instructions that tell it how to behave, and the `submit_claim` tool it's allowed to call.

1. Review the code that follows the agent (already provided). It creates a **session** to hold the conversation and calls `await agent.run(...)`, which runs the entire tool-calling loop and returns the final response as `response.text`:

    ```python
    # Create a session and use the agent to process the expenses data
    try:
        # A session keeps the conversation history across the agent run
        session = agent.create_session()
        # Invoke the agent with the prompt and the site-visit expenses data
        response = await agent.run(f"{prompt}: {expenses_data}", session=session)
        # Display the response
        print(f"\n# Agent:\n{response.text}")
    except Exception as e:
        # Something went wrong
        print(e)
    ```

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python expense_agent.py
    ```

    `az login` lets the `AzureCliCredential` authenticate to your Azure account.

1. When asked what to do with the expenses data, enter:

    ```
    Submit an expense claim
    ```

1. Review the output. The agent should compose an itemized expense-claim email — printed by the `submit_claim` tool — and then confirm it's done. You'll see output similar to:

    ```
    To: expenses@caldova.example
    Subject: Site Visit Expense Claim
    ...itemized expenses with a total...

    # Agent:
    I've submitted your site-visit expense claim to expenses@caldova.example.
    ```

    > **Tip**: If the app fails because the rate limit is exceeded, wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

> ✅ **Checkpoint**: You've built a single agent with a custom tool using the Microsoft Agent
> Framework — the model decided when to call your tool, and `agent.run()` handled the loop.
> That's the Core of this lab. The optional tasks below grow this into a multi-agent solution.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 2 — Orchestrate multiple agents in sequence](C2-orchestrate-multiple-agents.md) · [Task 3 — Connect remote agents with A2A](C3-connect-remote-agents-with-a2a.md)
