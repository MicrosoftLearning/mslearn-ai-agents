---
lab:
    title: 'Task 1 – Create and ground an agent'
    description: 'Create an agent in the Microsoft Foundry portal and ground it in Trailhead Adventure Works store policy so it answers from your data.'
    level: 300
    concepts: 'agent creation, grounding, file search'
    islab: true
    status: 'draft'
---

# Task 1 — Create and ground an agent

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Starting here on its own?** You need a Microsoft Foundry project with a deployed model.
> If you don't have one yet, complete [Getting started](A0-getting-started.md) first
> (Option A creates it in the portal). Task 1 is completed entirely in the portal — no local
> code or `.env` file is required.

---

Grounding gives your agent trusted source material so it answers accurately instead of
guessing.

1. In the agent playground, set the **Instructions** to:

    ```prompt
    You are the Trailhead Adventure Works store assistant.
    You help customers and store staff with questions about products, orders, returns, rentals, and guided trips.

    Guidelines:
    - Always be friendly and helpful
    - Use the store policy documentation to answer questions accurately
    - If you don't know the answer, admit it and suggest contacting the support team directly
    ```

1. Download the sample store policy document. Open a new browser tab and navigate to:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/A-build-and-extend-ai-agents/Python/Store_Policy.txt
    ```

    Save the file to your local machine.

1. Back in the playground, in the **Tools** section, select **Add**, and add **File search**.

1. To the right of **Add**, select **Upload files**, browse to the `Store_Policy.txt` file you downloaded, and select **Attach**. Wait for the file to be indexed.

1. **Save** the agent.

### Test your grounded agent

1. In the chat pane, enter:

    ```
    What's your return policy for a tent?
    ```

    The agent should reference the store policy document in its answer.

1. Try a second question to confirm it's using the grounding data:

    ```
    How do I rent gear for a weekend trip?
    ```

> ✅ **Checkpoint**: Your agent answers store questions using the uploaded policy document.
> You've created and grounded an agent entirely in the portal.

---

**Next:** [Task 2 — Connect a remote MCP server](A2-connect-a-remote-mcp-server.md)
