# MCP integration clients (C# / Microsoft Agent Framework)

C# ports of the Python samples in this exercise, built with the [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/overview/) instead of hand-written `azure-ai-projects` calls. There are three projects, matching the three Python files:

| Project | Python equivalent | What it does |
| --- | --- | --- |
| [`Agent/`](Agent) | [`agent.py`](../Python/agent.py) | Connects an agent to the remote Microsoft Learn Docs MCP server (a **hosted** MCP tool -- Foundry calls the remote server directly) and auto-approves each tool call |
| [`InventoryServer/`](InventoryServer) | [`server.py`](../Python/server.py) | A custom MCP server exposing inventory/sales tools over stdio |
| [`InventoryClient/`](InventoryClient) | [`client.py`](../Python/client.py) | Spawns `InventoryServer`, discovers its tools, and hands them to an agent as **local** MCP tools |

> **Status**: pilot / community contribution. `Microsoft.Agents.AI.Foundry` is still prerelease, so APIs may change before GA.

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download) or later
- A Foundry project with a deployed model, per [Create a Foundry project with the Foundry Toolkit for VS Code extension](../../../Instructions/Exercises/03-mcp-integration.md#create-a-foundry-project-with-the-foundry-toolkit-for-vs-code-extension) and [Deploy a model](../../../Instructions/Exercises/03-mcp-integration.md#deploy-a-model)
- The [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), signed in with `az login`

## Running the remote MCP server sample

1. In `Agent/`, duplicate `.env.example` as `.env` and fill in `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`.
2. `az login`
3. From `Agent/`, run:

    ```bash
   dotnet run
    ```

   It sends one fixed prompt (matching `agent.py`), auto-approves the MCP tool calls it triggers, and prints the response.

## Running the custom MCP server + client sample

1. In `InventoryClient/`, duplicate `.env.example` as `.env` and fill in `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`. `InventoryServer` doesn't need its own `.env` -- it has no Azure dependency at all, only `InventoryClient` does.
2. `az login`
3. From `InventoryClient/`, run:

    ```bash
   dotnet run
    ```

   This spawns `InventoryServer` as a subprocess automatically (via `dotnet run --project ../InventoryServer`) -- you don't need to start it separately. Try prompts like:

    ```
   Show me the current inventory levels for all products.
    ```

    ```
   Are there any products that should be restocked?
    ```

   Type `quit` to exit.

   You can also run `InventoryServer` on its own (`dotnet run` from that folder) to sanity-check it starts without errors, though it won't print anything useful to a terminal since it's speaking the MCP protocol over stdio.

## How it maps to the Python sample

| Python | C# |
| --- | --- |
| `MCPTool(server_label=..., server_url=..., require_approval="always")` | `new HostedMcpServerTool(serverName:, serverAddress:) { ApprovalMode = HostedMcpServerToolApprovalMode.AlwaysRequire }` |
| Manually walking `response.output` for `mcp_approval_request` items and resending `McpApprovalResponse`s | `response.Messages...OfType<ToolApprovalRequestContent>()` + `request.CreateResponse(approved: true)`, resent via `agent.RunAsync(approvals, session)` |
| `FastMCP` + `@mcp.tool()` | `[McpServerToolType]` on the class, `[McpServerTool]` on each method (official [ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol) SDK) |
| `StdioServerParameters(command="python", args=["server.py"])` + `stdio_client(...)` | `McpClient.CreateAsync(new StdioClientTransport(new() { Command = "dotnet", Arguments = ["run", "--project", "../InventoryServer"] }))` |
| Manually wrapping each MCP tool in a Python function, hand-writing a `FunctionTool` JSON schema for it, and dispatching `function_call` items by name | `mcpTools.Cast<AITool>()` -- `McpClientTool` already implements `AITool`, so the discovered tools go straight to the agent |
| `project_client.agents.create_version(...)` (persists a versioned agent server-side) | `AIProjectClient.AsAIAgent(model, instructions, name, tools)` (a code-owned, ephemeral agent -- no server-side agent resource, so no `delete_version` cleanup either) |

See [Hosted MCP Tools](https://learn.microsoft.com/agent-framework/tools/hosted-mcp-tools), [Local MCP Tools](https://learn.microsoft.com/agent-framework/tools/local-mcp-tools), and the [ModelContextProtocol C# SDK](https://github.com/modelcontextprotocol/csharp-sdk) for more on the patterns used here.
