// IT Support Agent client — C# / Microsoft Agent Framework port of the Python
// agent_with_functions.py sample. Connects to the agent created in the Foundry
// portal (with File search and Code interpreter already attached) and chats
// with it from the console, saving any files or charts it generates.

using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry;
using Microsoft.Extensions.AI;
using OpenAI.Containers;
using OpenAI.Responses;

LoadDotEnv();

string? projectEndpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
string agentName = Environment.GetEnvironmentVariable("AGENT_NAME") ?? "it-support-agent";

if (string.IsNullOrWhiteSpace(projectEndpoint) || projectEndpoint == "your_project_endpoint_here")
{
    Console.WriteLine("Error: PROJECT_ENDPOINT environment variable not set");
    Console.WriteLine("Please set it in your .env file or environment");
    return;
}

Console.WriteLine("Connecting to Microsoft Foundry project...");
// AzureCliCredential (rather than DefaultAzureCredential) is used here because this app is
// meant to run locally against the "az login" session from the setup steps. DefaultAzureCredential
// also tries ManagedIdentityCredential first, which can throw (instead of just being "unavailable")
// on machines without IMDS -- e.g. WSL -- aborting the credential chain before it ever reaches
// AzureCliCredential. See https://aka.ms/azsdk/net/identity/managedidentitycredential/troubleshoot
AIProjectClient projectClient = new(new Uri(projectEndpoint), new AzureCliCredential());

FoundryAgent agent;
try
{
    Console.WriteLine($"Loading agent: {agentName}");
    System.Diagnostics.Stopwatch loadStopwatch = System.Diagnostics.Stopwatch.StartNew();
    ProjectsAgentRecord agentRecord = await projectClient.AgentAdministrationClient.GetAgentAsync(agentName);
    agent = projectClient.AsAIAgent(agentRecord);
    loadStopwatch.Stop();
    Console.WriteLine($"[GetAgentAsync took {loadStopwatch.Elapsed.TotalSeconds:F1}s]");
}
catch (Exception ex)
{
    Console.WriteLine($"Error: could not find agent '{agentName}' in the project ({ex.Message})");
    Console.WriteLine("Make sure you created it in the Foundry portal and that AGENT_NAME matches its name.");
    return;
}

Console.WriteLine($"Connected to agent: {agent.Name} (id: {agent.Id})");

// Used to download files (like generated charts) that Code Interpreter writes to its sandbox.
ContainerClient containerClient = projectClient.GetProjectOpenAIClient().GetContainerClient();
DirectoryInfo outputDir = new(Path.Combine(Directory.GetCurrentDirectory(), "agent_outputs"));
HashSet<string> downloadedFiles = [];

// A session keeps the conversation (and its history) alive across turns.
AgentSession session = await agent.CreateSessionAsync();

Console.WriteLine();
Console.WriteLine(new string('=', 60));
Console.WriteLine("IT Support Agent Ready!");
Console.WriteLine("Ask questions, request data analysis, or get help.");
Console.WriteLine("Type 'exit' to quit.");
Console.WriteLine(new string('=', 60));
Console.WriteLine();

while (true)
{
    Console.Write("You: ");
    string userInput = (Console.ReadLine() ?? string.Empty).Trim();

    if (userInput.Length == 0)
    {
        continue;
    }

    if (userInput is "exit" or "quit" or "bye")
    {
        Console.WriteLine("Goodbye!");
        break;
    }

    Console.WriteLine();
    Console.WriteLine("[Agent is thinking...]");

    System.Diagnostics.Stopwatch stopwatch = System.Diagnostics.Stopwatch.StartNew();
    AgentResponse response = await agent.RunAsync(userInput, session);
    stopwatch.Stop();
    Console.WriteLine($"[RunAsync took {stopwatch.Elapsed.TotalSeconds:F1}s]");

    if (!string.IsNullOrWhiteSpace(response.Text))
    {
        Console.WriteLine();
        Console.WriteLine($"Agent: {response.Text}");
        Console.WriteLine();
    }

    await SaveGeneratedFilesAsync(response, containerClient, outputDir, downloadedFiles);
}

// Downloads any files Code Interpreter generated this turn (e.g. charts, CSVs) and
// saves them locally, printing where each one landed.
static async Task SaveGeneratedFilesAsync(
    AgentResponse response,
    ContainerClient containerClient,
    DirectoryInfo outputDir,
    HashSet<string> downloadedFiles)
{
    foreach (AIContent content in response.Messages.SelectMany(m => m.Contents))
    {
        if (content.Annotations is null)
        {
            continue;
        }

        foreach (AIAnnotation annotation in content.Annotations)
        {
            if (annotation is not CitationAnnotation { RawRepresentation: ContainerFileCitationMessageAnnotation containerCitation })
            {
                continue;
            }

            string key = $"{containerCitation.ContainerId}/{containerCitation.FileId}";
            if (!downloadedFiles.Add(key))
            {
                continue;
            }

            BinaryData fileData = await containerClient.DownloadContainerFileAsync(
                containerCitation.ContainerId,
                containerCitation.FileId);

            if (!outputDir.Exists)
            {
                outputDir.Create();
            }

            string safeFilename = Path.GetFileName(containerCitation.Filename ?? $"{containerCitation.FileId}.bin");
            string outputPath = GetUniqueOutputPath(outputDir, safeFilename);
            await File.WriteAllBytesAsync(outputPath, fileData.ToArray());

            Console.WriteLine($"[Agent generated a file - saved to: {outputPath}]");
        }
    }
}

// Avoids clobbering a file from an earlier turn that happens to share a name.
static string GetUniqueOutputPath(DirectoryInfo outputDir, string filename)
{
    string stem = Path.GetFileNameWithoutExtension(filename);
    string suffix = Path.GetExtension(filename);
    string outputPath = Path.Combine(outputDir.FullName, filename);

    int counter = 1;
    while (File.Exists(outputPath))
    {
        outputPath = Path.Combine(outputDir.FullName, $"{stem}_{counter}{suffix}");
        counter++;
    }

    return outputPath;
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
