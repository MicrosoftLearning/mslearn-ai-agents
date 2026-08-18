---
title: 'Task 1 – Create and ground an agent'
lab:
    title: 'Task 1 – Create and ground an agent'
    description: 'Create an agent in the Microsoft Foundry portal and ground it in Caldova supply chain policy so it answers from your data.'
    type: 'task'
    parent: 'A'
    order: 1
    section: 'core'
    difficulty: 2
    duration: 15
    access: 'open'
    level: 200
    concepts: 'agent creation, grounding, file search'
    status: 'draft'
---

# Task 1 — Create and ground an agent

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a deployed model**. Don't have one
> yet? Complete [Getting started](A0-getting-started.md) first (Option A creates it in the
> portal). This task is completed entirely in the portal — no local code or `.env` file is
> required, so there's nothing to carry over from other tasks.

---

Grounding gives your agent trusted source material so it answers accurately instead of
guessing.

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
<summary>What is grounding?</summary>
<div class="concept-body" markdown="1">

The single most important capability for the Caldova agent is **grounding**.
Grounding attaches trusted source material — such as the supply chain policy document — so the
agent answers *from that data* instead of inventing a response.

[Learn more →](https://review.learn.microsoft.com/en-us/training/modules/build-extend-ai-agents/2-understand-agents-foundry?branch=pr-en-us-55509)

</div>
</details>

1. In the agent playground, set the **Instructions** to:

    ```prompt
    You are the Caldova supply chain assistant.
    You help planning and materials teams with questions about capacity, contract manufacturers, and materials.

    Guidelines:
    - Always be clear and concise
    - Use the supply chain policy documentation to answer questions accurately
    - If you don't know the answer, admit it and suggest contacting the planning desk directly
    ```

1. Download the sample supply chain policy document. Open a new browser tab and navigate to:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/A-build-and-extend-ai-agents/Python/Supply_Chain_Policy.txt
    ```

    Save the file to your local machine.

1. Back in the playground, in the **Tools** section, select **Add**, and add **File search**.

1. To the right of **Add**, select **Upload files**, browse to the `Supply_Chain_Policy.txt` file you downloaded, and select **Attach**. Wait for the file to be indexed.

1. **Save** the agent.

### Test your grounded agent

1. In the chat pane, enter:

    ```
    How long does review take for a standard capacity request?
    ```

    The agent should reference the supply chain policy document in its answer.

1. Try a second question to confirm it's using the grounding data:

    ```
    How much is five weeks of premium contract capacity at expedited priority?
    ```

> ✅ **Checkpoint**: Your agent answers supply chain questions using the uploaded policy document.
> You've created and grounded an agent entirely in the portal.

---

**Next:** [Task 2 — Connect a remote MCP server](A2-connect-a-remote-mcp-server.md)
