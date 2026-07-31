# Astronomy agent client (C# / Microsoft Agent Framework)

This is a C# port of the [`Python/agent.py`](../Python/agent.py) client from this exercise, built with the [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/overview/) instead of hand-written `azure-ai-projects` calls. It creates an astronomy assistant agent with three custom function tools (see [`Functions.cs`](Functions.cs), ported from [`Python/functions.py`](../Python/functions.py)) and chats with it from the console.

> **Status**: pilot / community contribution. `Microsoft.Agents.AI.Foundry` is still prerelease, so APIs may change before GA.

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download) or later
- A Foundry project with a deployed model, per [Create a Foundry project with the Foundry Toolkit for VS Code extension](../../../Instructions/Exercises/02-agent-custom-tools.md#create-a-foundry-project-with-the-foundry-toolkit-for-vs-code-extension) and [Deploy a model](../../../Instructions/Exercises/02-agent-custom-tools.md#deploy-a-model)
- The [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), signed in with `az login`

## Setup

1. Duplicate `.env.example` and rename it to `.env`.

2. In `.env`, replace the placeholders with your project endpoint and model deployment name:

    ```
   PROJECT_ENDPOINT=<your_project_endpoint>
   MODEL_DEPLOYMENT_NAME=<your_model_deployment_name>
    ```

3. Sign in to Azure so `AzureCliCredential` can authenticate:

    ```bash
   az login
    ```

4. Restore and run:

    ```bash
   dotnet run
    ```

## Try it

```
What's the next visible event in Europe?
```

```
How much would 3 hours on an advanced telescope with high priority cost?
```

```
Generate a report for observing the Geminids Meteor Shower from Europe on a premium telescope, 2 hours, normal priority, for observer Alex Chen.
```

The generated report is written to the current directory, matching the Python sample's behavior. Type `quit` to exit.

## How it maps to the Python sample

| Python (`agent.py` / `functions.py`) | C# (`Program.cs` / `Functions.cs`) |
| --- | --- |
| Hand-written JSON schema for each `FunctionTool` | `[Description]` attributes + `AIFunctionFactory.Create(...)`, which reads the method signature via reflection |
| `project_client.agents.create_version(...)` (persists a versioned agent server-side) | `AIProjectClient.AsAIAgent(model, instructions, name, tools)` (a code-owned, ephemeral agent -- no server-side agent resource) |
| Manually walking `response.output` for `function_call` items, dispatching by name, and resending results as `function_call_output` | `agent.RunAsync(...)` -- the framework invokes the matching local method and continues automatically |
| Manually created `conversation` + `previous_response_id` chaining | `AgentSession` from `agent.CreateSessionAsync()` |
| `project_client.agents.delete_version(...)` cleanup at the end | Not needed -- nothing is persisted server-side |

See [Function Tools](https://learn.microsoft.com/agent-framework/tools/function-tools) and [Microsoft Foundry provider docs](https://learn.microsoft.com/agent-framework/agents/providers/microsoft-foundry) for more on the patterns used here.
