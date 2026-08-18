---
title: 'Task 2 – Connect a remote MCP server'
lab:
    title: 'Task 2 – Connect a remote MCP server'
    description: 'Extend an agent with a tool by connecting it to a remote Model Context Protocol (MCP) server, and handle tool-approval requests in code.'
    type: 'task'
    parent: 'A'
    order: 2
    section: 'core'
    difficulty: 3
    duration: 20
    access: 'open'
    level: 300
    concepts: 'tools, Model Context Protocol (MCP), approvals'
    status: 'draft'
---

# Task 2 — Connect a remote MCP server

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](A0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 2
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Connect the agent to the MCP server** below.

---

The **Model Context Protocol (MCP)** lets an agent discover and call tools hosted by a
server. Behind the scenes, the Caldova platform team is rebuilding the
supply chain platform on Azure — so in this task you'll connect an agent to the **Microsoft Learn
Docs** remote MCP server, giving the team an assistant that can pull trusted, up-to-date
Azure documentation on demand.

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
<summary>What is MCP?</summary>
<div class="concept-body" markdown="1">

The **Model Context Protocol (MCP)** solves this by letting an agent discover tools at
runtime. With MCP, tools live on a **server** that acts as a live catalog. Your agent
(through a **client**) asks the server what tools are available and calls them on demand.

[Learn more →](https://review.learn.microsoft.com/en-us/training/modules/build-extend-ai-agents/5-connect-agents-to-mcp?branch=pr-en-us-55509)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](A0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Connect the agent to the MCP server

Open **remote_mcp_agent.py** and add code at each commented placeholder.

> **Tip**: As you add code, keep the indentation aligned with the comments.

1. **Add references**:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition, MCPTool
    from openai.types.responses.response_input_param import McpApprovalResponse, ResponseInputParam
    ```

1. **Connect to the agents client**:

    ```python
    # Connect to the agents client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    ```

1. **Initialize agent MCP tool** — this points the agent at the Microsoft Learn Docs MCP server:

    ```python
    # Initialize agent MCP tool
    mcp_tool = MCPTool(
        server_label="api-specs",
        server_url="https://learn.microsoft.com/api/mcp",
        require_approval="always",
    )
    ```

1. **Create a new agent with the MCP tool**:

    ```python
    # Create a new agent with the MCP tool
    agent = project_client.agents.create_version(
        agent_name="platform-docs-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="You are a platform engineering assistant for Caldova. Use the available MCP tools to look up trusted Azure documentation and help the team build and operate the supply chain platform.",
            tools=[mcp_tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
    ```

1. **Create a conversation thread**:

    ```python
    # Create a conversation thread
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")
    ```

1. **Send initial request that will trigger the MCP tool**:

    ```python
    # Send initial request that will trigger the MCP tool
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Give me the Azure CLI commands to deploy our product catalog API to an Azure Container App with a managed identity.",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )
    ```

1. **Process any MCP approval requests** — because the tool requires approval, the agent
    pauses and asks permission before each call. This loop auto-approves each request:

    ```python
    # Process any MCP approval requests that were generated
    while True:
        input_list: ResponseInputParam = []
        for item in response.output:
            if item.type == "mcp_approval_request":
                if item.server_label == "api-specs" and item.id:
                    input_list.append(
                        McpApprovalResponse(
                            type="mcp_approval_response",
                            approve=True,
                            approval_request_id=item.id,
                        )
                    )

        # No more approvals needed -> the agent has produced its final response
        if not input_list:
            break

        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    print(f"\nAgent response: {response.output_text}")
    ```

1. **Clean up the agent version** so you don't leave test agents behind:

    ```python
    # Clean up resources by deleting the agent version
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
    ```

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python remote_mcp_agent.py
    ```

1. Watch the agent create itself, call the MCP tool (approved automatically by your loop), and answer using live documentation. You should see output similar to:

    ```
    Agent created (id: platform-docs-agent:2, name: platform-docs-agent, version: 2)
    Created conversation (id: conv_...)

    Agent response: Here are Azure CLI commands to create an Azure Container App with a managed identity:
    ...
    Agent deleted
    ```

1. Try changing the `input` string to ask about a different Azure service, and run again.

> ✅ **Checkpoint**: You've built a grounded agent *and* extended an agent with an
> external tool via a remote MCP server, including approval handling. That's the Core of
> this lab — everything below is optional.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 3 — Call your agent from a client app](A3-call-your-agent-from-a-client-app.md) · [Task 4 — Add custom function tools](A4-add-custom-function-tools.md)
