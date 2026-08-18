---
title: 'Task 6 – Promote your assistant to a hosted agent'
lab:
    title: 'Task 6 – Promote your assistant to a hosted agent'
    description: 'Take the Caldova assistant you built as a prompt agent and deploy it as a hosted agent - your own code running in a Foundry-managed container - with the Azure Developer CLI.'
    type: 'task'
    parent: 'A'
    order: 6
    section: 'optional'
    difficulty: 3
    duration: 30
    access: 'open'
    level: 300
    concepts: 'hosted agents, deployment, Azure Developer CLI'
    status: 'draft'
---

# Task 6 — Promote your assistant to a hosted agent

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task deploys code, so it needs a Foundry project, a deployed
> model, and the **Azure Developer CLI (`azd`)**. If you haven't already, complete
> [Getting started](A0-getting-started.md) to create your project and set `PROJECT_ENDPOINT`
> and `MODEL_DEPLOYMENT_NAME` in `Python/.env`. Then, from the `Python` folder you opened in
> VS Code, verify:

```
python ../setup/check_env.py --task 6
```

> You also need **`azd` 1.25.3 or later** and the Foundry extension. Install it once with:
>
> ```
> azd ext install microsoft.foundry
> ```

> **Continuing from a previous task?** The hosted agent lives in its own folder
> (`Python/hosted_agent/`) with its own dependencies, so it doesn't reuse the shared
> `labenv`. Everything you need is below — you can start here without having finished the
> earlier tasks.

---

**Goal**: take the **same Caldova assistant** you've been building and run it as a
**hosted agent** — your own code, packaged and deployed to Foundry Agent Service, invokable by
reference just like the prompt agents you built earlier.

**Prompt agent vs. hosted agent** — in every earlier task you built a *prompt agent*: you
described the agent with a `PromptAgentDefinition` (a model, instructions, and tools) and let
Foundry run it. That's fast and declarative, but the logic has to fit in a prompt-and-tools
definition. A *hosted agent* is **your own code** — any framework or plain Python — packaged as
a container and run on Foundry-managed infrastructure. You choose the runtime behavior, and the
platform handles scaling, session state, identity, and an endpoint. It's the natural next step
when an assistant outgrows a prompt definition, and it's how you'd operationalize the assistant
for Teams or Microsoft 365 delivery later.

In this task you use the **Responses protocol**, so your hosted agent stays OpenAI-compatible —
the same client code that called your prompt agents can call this one.

## Review the agent code

1. In the `Labfiles/A-build-and-extend-ai-agents/Python/hosted_agent` folder, open **main.py**.
    The `azure-ai-agentserver-responses` hosting library runs the web server, health checks,
    and conversation history for you — you only write the **handler** that answers one turn.

1. Two blocks are marked `TODO`: create the Responses client, and call the model from the
    handler. Fill them in.

> **Try it first**: the handler already has the user's message (`user_input`) and the
> conversation history assembled into `input_items`. How would you send that to your model
> deployment and return the reply? *(Hint: the Responses client's `create(...)` is synchronous,
> so the sample runs it off the event loop with `run_in_executor` to avoid blocking the
> server.)*

<details markdown="1">
<summary>Show a solution</summary>

Create the Responses client near the top of the file:

```python
_responses_client = (
    AIProjectClient(endpoint=_endpoint, credential=DefaultAzureCredential())
    .get_openai_client()
    .responses
)
```

Then complete the handler to call the model with the Caldova system prompt and return the reply:

```python
response = await asyncio.get_running_loop().run_in_executor(
    None,
    lambda: _responses_client.create(
        model=_model,
        instructions=_SYSTEM_PROMPT,
        input=input_items,
        store=False,
    ),
)
return TextResponse(context, request, text=response.output_text)
```

The complete file is in `Solution/Python/hosted_agent/main.py`.

</details>

## Configure the model

1. Copy `hosted_agent/.env.example` to `hosted_agent/.env` and set
    `AZURE_AI_MODEL_DEPLOYMENT_NAME` to your deployed model name (for example, `gpt-4o`). In a
    hosted container `FOUNDRY_PROJECT_ENDPOINT` is injected for you; `azd ai agent run` sets it
    automatically when you test locally.

## Initialize the azd project

1. From the `hosted_agent` folder, scaffold the agent definition. This generates an
    `azure.yaml` describing a hosted **`azure.ai.agent`** service:

    ```
    azd ai agent init --protocol responses --deploy-mode code
    ```

    Answer the prompts: pick an **agent name** (for example, `caldova-hosted-agent`), select
    **Use an existing Foundry project** (the one from Getting started), and choose your
    subscription and location.

> A completed `azure.yaml` is included in `Solution/Python/hosted_agent/` so you can see what
> the tool produces. `--deploy-mode code` means Foundry builds the container for you (a **remote
> build**) — you don't need Docker installed locally.

## Provision and test locally

1. Provision the supporting resources (such as Application Insights):

    ```
    azd provision
    ```

1. Run the agent locally. This creates a virtual environment, installs
    `requirements.txt`, launches your handler, and opens the agent inspector in your browser:

    ```
    azd ai agent run
    ```

1. Chat with it in the inspector, or invoke it from a second terminal:

    ```
    azd ai agent invoke --local "How long does review take for a capacity request?"
    ```

## Deploy to Foundry Agent Service

1. Build and deploy the container to Foundry:

    ```
    azd deploy
    ```

    When it finishes, the output includes an **agent playground** link and an **agent
    endpoint**. Your hosted agent now has its own dedicated endpoint and identity.

1. Invoke the deployed agent:

    ```
    azd ai agent invoke "A planner needs five weeks of premium contract capacity. What will it cost at expedited priority?"
    ```

> **Same reference, your code now**: a hosted agent is invoked exactly like the prompt agents
> you built — by name, through the OpenAI-compatible client. Any app that used
> `agent_reference` against a prompt agent can point at this hosted agent instead; the
> difference is that the logic answering each turn is now **your code** running in a container,
> not a prompt definition.

> ✅ **Checkpoint**: You promoted the Caldova assistant from a prompt agent to a hosted
> agent, tested it locally with `azd ai agent run`, deployed it with `azd deploy`, and invoked
> the deployed agent by name.

## Clean up

When you're done, remove everything this task created:

```
azd down
```

> **Warning**: `azd down` deletes every resource in the resource group, including the Foundry
> project and hosted agent. If the group holds other resources, those are deleted too.

---

**Back to the** [lab overview](A-build-and-extend-ai-agents.md).
