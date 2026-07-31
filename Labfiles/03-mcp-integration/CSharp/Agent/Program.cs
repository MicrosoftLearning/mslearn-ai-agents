// Remote MCP server client -- C# / Microsoft Agent Framework port of the Python agent.py sample.
// Connects an agent to the Microsoft Learn Docs remote MCP server (a *hosted* MCP tool: Foundry
// itself calls the remote server, not this client) and automatically approves each tool call the
// agent wants to make, matching agent.py's require_approval="always" + auto-approve loop.

using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

LoadDotEnv();

string? projectEndpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
string? modelDeployment = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");

if (string.IsNullOrWhiteSpace(projectEndpoint) || projectEndpoint == "your_project_endpoint_here")
{
    Console.WriteLine("Error: PROJECT_ENDPOINT environment variable not set");
    Console.WriteLine("Please set it in your .env file or environment");
    return;
}

if (string.IsNullOrWhiteSpace(modelDeployment))
{
    Console.WriteLine("Error: MODEL_DEPLOYMENT_NAME environment variable not set");
    Console.WriteLine("Please set it in your .env file or environment");
    return;
}

// AzureCliCredential talks to the "az login" session directly. DefaultAzureCredential also tries
// ManagedIdentityCredential first, which can throw (instead of just being "unavailable") on
// machines without IMDS -- e.g. WSL -- aborting the credential chain before it ever reaches
// AzureCliCredential.
AIProjectClient projectClient = new(new Uri(projectEndpoint), new AzureCliCredential());

// This connects to the Microsoft Learn Docs remote MCP server -- a cloud-hosted service that
// enables clients to access trusted and up-to-date information directly from Microsoft's
// official documentation. Because Foundry calls this server directly (a "hosted" MCP tool),
// there's no local MCP client/session here -- compare with InventoryClient, which uses a *local*
// MCP tool instead.
var mcpTool = new HostedMcpServerTool(serverName: "api-specs", serverAddress: "https://learn.microsoft.com/api/mcp")
{
    ApprovalMode = HostedMcpServerToolApprovalMode.AlwaysRequire,
};

AIAgent agent = projectClient.AsAIAgent(
    modelDeployment,
    instructions: "You are a helpful agent that can use MCP tools to assist users. Use the available MCP tools to answer questions and perform tasks.",
    name: "MyAgent",
    tools: [mcpTool]);

Console.WriteLine($"Agent created (name: {agent.Name})");

AgentSession session = await agent.CreateSessionAsync();

AgentResponse response = await agent.RunAsync(
    "Give me the Azure CLI commands to create an Azure Container App with a managed identity.",
    session);

// The agent may issue several tool calls, each needing its own approval, so we loop until
// there are none left -- mirroring the Python sample's "while True" approval loop.
List<ToolApprovalRequestContent> approvalRequests = response.Messages.SelectMany(m => m.Contents).OfType<ToolApprovalRequestContent>().ToList();

while (approvalRequests.Count > 0)
{
    // Automatically approve every MCP request to allow the agent to proceed.
    List<ChatMessage> approvals = approvalRequests
        .Select(request => new ChatMessage(ChatRole.User, [request.CreateResponse(approved: true)]))
        .ToList();

    response = await agent.RunAsync(approvals, session);
    approvalRequests = response.Messages.SelectMany(m => m.Contents).OfType<ToolApprovalRequestContent>().ToList();
}

Console.WriteLine($"\nAgent response: {response.Text}");

// No cleanup step here -- AsAIAgent(model, instructions, name, tools) doesn't persist a
// server-side agent resource the way the Python sample's agents.create_version(...) does, so
// there's nothing in the Foundry project to delete (see the CSharp/README.md for details).

// Minimal ".env" loader so this project can reuse the same .env file format as
// the Python sample, without adding a NuGet dependency just for that.
static void LoadDotEnv()
{
    string envPath = Path.Combine(Directory.GetCurrentDirectory(), ".env");
    if (!File.Exists(envPath))
    {
        return;
    }

    foreach (string rawLine in File.ReadAllLines(envPath))
    {
        string line = rawLine.Trim();
        if (line.Length == 0 || line.StartsWith('#'))
        {
            continue;
        }

        int separatorIndex = line.IndexOf('=');
        if (separatorIndex <= 0)
        {
            continue;
        }

        string key = line[..separatorIndex].Trim();
        string value = line[(separatorIndex + 1)..].Trim().Trim('"');

        if (Environment.GetEnvironmentVariable(key) is null)
        {
            Environment.SetEnvironmentVariable(key, value);
        }
    }
}
