# Lab 1: Build AI Agents with Portal and VS Code

This directory contains the lab files for Lab 1 - Building AI Agents using both Microsoft Foundry portal and the VS Code extension.

## Contents

### Python Files

- **`agent_with_functions.py`** - Agent implementation with custom functions (check_system_status, create_support_ticket)
- **`requirements.txt`** - Python package dependencies
- **`.env.example`** - Template for environment configuration

### Data Files

- **`IT_Policy.txt`** - Sample IT policy document for grounding data

### Archived Files

- **`ARCHIVED_FOR_LAB_3/`** - MCP server code archived for use in Lab 3

## Setup Instructions

### 1. Prerequisites

- Python 3.12 or later
- Azure subscription with AI Foundry access
- Visual Studio Code with Microsoft Foundry extension
- Azure CLI or Azure authentication configured

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Microsoft Foundry project endpoint:
   ```
   PROJECT_ENDPOINT=<your_project_endpoint>
   ```

   **To get your endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

### 4. Authenticate with Azure

Ensure you're authenticated with Azure. You can use:

```bash
az login
```

Or configure environment variables for service principal authentication.

## Running the Examples

### Agent with Custom Functions

```bash
python agent_with_functions.py
```

This will:
- Connect to your Microsoft Foundry project
- Create an agent with custom functions
- Start an interactive chat session

Try prompts like:
- "Is the email system working?"
- "Create a ticket for a printer issue"
- "Check VPN status and create a ticket if there's a problem"

## File Descriptions

### agent_with_functions.py

Demonstrates:
- Creating an agent with custom function tools
- Defining function schemas
- Handling function calls in the agent run loop
- Interactive chat with function execution

Functions available:
- `check_system_status(system_name)` - Check if a system is operational
- `create_support_ticket(issue_type, description, priority)` - Create IT support tickets

## Architecture

```
┌─────────────────┐
│  Your Python    │
│  Application    │
└────────┬────────┘
         │
         │ Azure AI SDK
         ▼
┌─────────────────┐
│ Microsoft Foundry│
│  Agent Service  │
└────────┬────────┘
         │
         └──────────► Custom Functions (in-process)
```

## Troubleshooting

### "Module not found" errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Authentication failures

1. Verify you're logged into Azure: `az login`
2. Check that your account has access to the AI Foundry project
3. Verify the connection string is correct in `.env`

### Agent creation fails

1. Ensure the model (gpt-4o) is deployed in your project
2. Check you have sufficient quota in your region
3. Verify the project connection string is correct

## Next Steps

After completing this lab, continue with:
- **Lab 2**: Advanced Tool Calling - Code interpreter, async functions, data processing
- **Lab 3**: MCP Integration - Connect agents to external tools (includes the archived MCP code from this lab)
- **Lab 5**: M365 & Teams Integration - Deploy agents to production

## Learn More

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [Microsoft Foundry VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-ai)

## Next Steps

After completing this lab, consider:
- Moving to Lab 2 for advanced tool calling patterns
- Exploring Lab 3 for MCP integration (uses the archived code from this lab)
- Building multi-agent systems in Lab 4
- Deploying to Microsoft Teams in Lab 5

## License

This code is provided as part of Microsoft Learn training materials.
