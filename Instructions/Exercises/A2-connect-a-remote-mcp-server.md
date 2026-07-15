---
lab:
    title: 'Task 2 – Connect a remote MCP server'
    description: 'Extend an agent with a tool by connecting it to a remote Model Context Protocol (MCP) server, and handle tool-approval requests in code.'
    level: 300
    concepts: 'tools, Model Context Protocol (MCP), approvals'
    islab: true
    status: 'draft'
---

# Task 2 — Connect a remote MCP server

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Starting here on its own?** First complete [Getting started](A0-getting-started.md) to
> create your Foundry project, clone the starter code, and set up your `.env`.
>
> **This task needs** `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`. From the
> `Labfiles/A-build-and-extend-ai-agents` folder, verify you're ready:
>
> ```
> python setup/check_env.py --task 2
> ```

---

The **Model Context Protocol (MCP)** lets an agent discover and call tools hosted by a
server. Behind the scenes, the Trailhead Adventure Works platform team is rebuilding the
online store on Azure — so in this task you'll connect an agent to the **Microsoft Learn
Docs** remote MCP server, giving the team an assistant that can pull trusted, up-to-date
Azure documentation on demand.

Open the shared `Python` folder and virtual environment you created in [Getting started](A0-getting-started.md), then continue below.

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
            instructions="You are a platform engineering assistant for Trailhead Adventure Works. Use the available MCP tools to look up trusted Azure documentation and help the team build and operate the online store.",
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
