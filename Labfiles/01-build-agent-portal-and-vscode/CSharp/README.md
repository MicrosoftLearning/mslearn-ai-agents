# IT Support Agent client (C# / Microsoft Agent Framework)

This is a C# port of the [`Python/agent_with_functions.py`](../Python/agent_with_functions.py) client from this exercise, built with the [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/overview/) instead of a raw `azure-ai-projects` + OpenAI Responses API call. It connects to the `it-support-agent` you create in the [exercise](../../../Instructions/Exercises/01-build-agent-portal-and-vscode.md) via the Foundry portal (with **File search** and **Code interpreter** already attached) and chats with it from the console.

> **Status**: pilot / community contribution. `Microsoft.Agents.AI.Foundry` is still prerelease, so APIs may change before GA.

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download) or later
- The `it-support-agent` created in [Create a Microsoft Foundry Project](../../../Instructions/Exercises/01-build-agent-portal-and-vscode.md#create-a-microsoft-foundry-project) and [Configure your agent with instructions and grounding data](../../../Instructions/Exercises/01-build-agent-portal-and-vscode.md#configure-your-agent-with-instructions-and-grounding-data)
- The [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), signed in with `az login`

## Setup

1. Duplicate `.env.example` and rename it to `.env`.

2. In `.env`, replace `your_project_endpoint_here` with your project endpoint (copy it from the Foundry Toolkit extension or the project overview page in the Foundry portal):

    ```
   PROJECT_ENDPOINT=<your_project_endpoint>
   AGENT_NAME=it-support-agent
    ```

3. Sign in to Azure so `DefaultAzureCredential` can authenticate:

    ```bash
   az login
    ```

4. Restore and run:

    ```bash
   dotnet run
    ```

## Try it

Once the agent is ready, test both tools it was configured with in the portal:

```
What's the policy for password resets?
```

```
Create a line chart showing memory usage trends over time
```

Generated charts and cited files are saved to the `agent_outputs` folder, with the local path printed in the terminal. Type `exit` to quit.

## How it maps to the Python sample

| Python (`agent_with_functions.py`) | C# (`Program.cs`) |
| --- | --- |
| `AIProjectClient` + raw OpenAI `conversations`/`responses` calls | `AIProjectClient.AgentAdministrationClient.GetAgentAsync(name)` + `AsAIAgent(...)` from Microsoft Agent Framework, returning a `FoundryAgent` |
| Manually created `conversation` | `AgentSession` from `agent.CreateSessionAsync()` |
| `openai_client.responses.create(...)` in a loop | `agent.RunAsync(userInput, session)` |
| `download_container_file` walking `container_file_citation` annotations | `ContainerClient.DownloadContainerFileAsync` walking `CitationAnnotation` / `ContainerFileCitationMessageAnnotation` |

See [Microsoft Foundry provider docs](https://learn.microsoft.com/agent-framework/agents/providers/microsoft-foundry) for more on the `AsAIAgent` patterns used here.
