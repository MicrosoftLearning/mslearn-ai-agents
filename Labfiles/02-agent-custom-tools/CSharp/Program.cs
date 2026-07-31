// Astronomy agent client -- C# / Microsoft Agent Framework port of the Python agent.py sample.
// Defines an agent with custom function tools (see Functions.cs) and chats with it from the
// console. Unlike the Python sample, the Agent Framework generates each tool's JSON schema
// from the C# method signature and [Description] attributes, and handles the function-call /
// function-result loop automatically -- there's no manual "walk response.output, dispatch by
// name, resend as function_call_output" loop here.

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

// AzureCliCredential (rather than DefaultAzureCredential) talks to the "az login" session
// directly. DefaultAzureCredential also tries ManagedIdentityCredential first, which can throw
// (instead of just being "unavailable") on machines without IMDS -- e.g. WSL -- aborting the
// credential chain before it ever reaches AzureCliCredential.
AIProjectClient projectClient = new(new Uri(projectEndpoint), new AzureCliCredential());

// Wrap each local method as a tool. AIFunctionFactory reads the method signature and
// [Description] attributes to build the tool's JSON schema -- no hand-written schema needed.
AITool[] tools =
[
    AIFunctionFactory.Create(Functions.NextVisibleEvent),
    AIFunctionFactory.Create(Functions.CalculateObservationCost),
    AIFunctionFactory.Create(Functions.GenerateObservationReport),
];

AIAgent agent = projectClient.AsAIAgent(
    modelDeployment,
    instructions: """
        You are an astronomy observations assistant that helps users find
        information about astronomical events and calculate telescope rental costs.
        Use the available tools to assist users with their inquiries.
        """,
    name: "astronomy-agent",
    tools: tools);

AgentSession session = await agent.CreateSessionAsync();

while (true)
{
    Console.Write("Enter a prompt for the astronomy agent. Use 'quit' to exit.\nUSER: ");
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
    Console.WriteLine($"AGENT: {response.Text}");
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
