// Local MCP client -- C# / Microsoft Agent Framework port of the Python client.py sample.
// Spawns InventoryServer as a subprocess over stdio, discovers its tools, and hands them
// straight to an agent as local MCP tools.
//
// Compare with Agent/Program.cs: that project uses a *hosted* MCP tool (Foundry calls the
// remote server directly). Here, this client owns the MCP session and the Agent Framework
// invokes each tool call locally -- there's no manual "wrap each tool in a function, build a
// FunctionTool JSON schema, walk response.output for function_call items" like client.py does;
// McpClientTool already implements AITool, so the discovered tools can be passed to the agent
// as-is.

using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

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

// Start the MCP server. In a standard production setup the server would run separately from
// the client, but for this lab the client is responsible for starting it, using stdio as a
// lightweight communication channel -- same tradeoff client.py makes with StdioServerParameters.
await using McpClient mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new()
{
    Name = "Inventory",
    Command = "dotnet",
    Arguments = ["run", "--project", "../InventoryServer"],
}));

// List available tools
IList<McpClientTool> mcpTools = await mcpClient.ListToolsAsync();
Console.WriteLine($"\nConnected to server with tools: {string.Join(", ", mcpTools.Select(t => t.Name))}");

// AzureCliCredential talks to the "az login" session directly. DefaultAzureCredential also tries
// ManagedIdentityCredential first, which can throw (instead of just being "unavailable") on
// machines without IMDS -- e.g. WSL -- aborting the credential chain before it ever reaches
// AzureCliCredential.
AIProjectClient projectClient = new(new Uri(projectEndpoint), new AzureCliCredential());

// McpClientTool already implements AITool, so the tools discovered from the MCP session can be
// handed to the agent directly -- no per-tool JSON schema or dispatch function needed.
AIAgent agent = projectClient.AsAIAgent(
    modelDeployment,
    instructions: """
        You are an inventory assistant. Here are some general guidelines:
        - Recommend restock if item inventory < 10 and weekly sales > 15
        - Recommend clearance if item inventory > 20 and weekly sales < 5
        """,
    name: "inventory-agent",
    tools: [.. mcpTools.Cast<AITool>()]);

AgentSession session = await agent.CreateSessionAsync();

while (true)
{
    Console.Write("Enter a prompt for the inventory agent. Use 'quit' to exit.\nUSER: ");
    string userInput = (Console.ReadLine() ?? string.Empty).Trim();

    if (userInput.Equals("quit", StringComparison.OrdinalIgnoreCase))
    {
        Console.WriteLine("Exiting chat.");
        break;
    }

    if (userInput.Length == 0)
    {
        continue;
    }

    AgentResponse response = await agent.RunAsync(userInput, session);
    Console.WriteLine($"Agent response: {response.Text}");
}

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
