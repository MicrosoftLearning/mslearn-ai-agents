---
lab:
    title: 'Lab 6: Deploy Agents to Microsoft Teams'
    description: 'Deploy a production AI agent with Azure AI Search knowledge base and Microsoft Teams integration'
---

# Lab 6: Deploy Agents to Microsoft Teams

In this lab, you'll deploy a **real AI agent** to Azure using automated tools. You'll create a production-ready agent with Azure AI Search for knowledge queries, connect it via the Foundry portal, and publish it to Microsoft Teams.

This is a **hands-on deployment lab** where you'll work with real Azure resources, not simulations.

This lab takes approximately **80** minutes.

> **Note**: This lab builds on Labs 1-5. You should be familiar with agent creation, tools, and the Responses API.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Deploy AI agents to Azure using Azure Developer CLI (azd)
2. Create and configure Azure AI Search with document indexing
3. Connect agents to search using Foundry portal (Foundry IQ)
4. Publish agents to Microsoft Teams using Foundry portal
5. Manage Azure resources and costs effectively
6. Troubleshoot production deployments

## Prerequisites

Before starting this lab, ensure you have:

- **Azure subscription** with permissions to create resources
- **Azure Developer CLI (azd)** version 1.23.0 or later
- **Azure CLI** version 2.80 or later
- **Docker Desktop** installed and running
- **Python 3.10 or later** installed
- **Visual Studio Code** (recommended)
- Basic familiarity with command-line tools

> **Cost Warning**: This lab creates real Azure resources. Estimated cost: **$1-2** if you complete cleanup immediately. Always run the cleanup script when finished!

## Scenario

You'll deploy an **Enterprise Knowledge Agent** that:

- Runs in Azure AI Foundry as a hosted agent
- Searches company documentation using Azure AI Search
- Provides answers with source citations
- Can be accessed via Microsoft Teams (optional)
- Includes monitoring and logging

This represents a complete production deployment workflow.

## Lab Structure

This lab follows a progressive deployment workflow:

```
Step 0: Environment Setup (Prerequisites)
Step 1: Deploy Agent to Azure (azd up)
Step 2: Create Azure AI Search with Documents
Step 3: Connect Agent to Search (Foundry Portal)
Step 4: Publish to Microsoft Teams (Foundry Portal)
Step 5: Cleanup All Resources
```

Each step builds on the previous, creating a complete production system.

---

## Step 0: Environment Setup

Before deploying, you need to install and verify all required tools.

### Navigate to the lab directory

1. Open Visual Studio Code.

2. Open the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\uplevel\06-m365-teams-integration\Python
   ```
   
   Use **File > Open Folder** in VS Code.

### Install Azure Developer CLI

The Azure Developer CLI (azd) automates deployment to Azure.

**On Windows:**

```powershell
powershell -ex AllSigned -c "Invoke-RestMethod 'https://aka.ms/install-azd.ps1' | Invoke-Expression"
```

**On macOS/Linux:**

```bash
curl -fsSL https://aka.ms/install-azd.sh | bash
```

**Verify installation:**

```bash
azd version
```

You should see version 1.23.0 or later.

### Install Docker Desktop

Docker is required for containerizing your agent.

1. Download from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Wait for Docker to fully start (green icon in system tray/menu bar)

**Verify Docker is running:**

```bash
docker --version
docker ps
```

### Verify all prerequisites

Run the automated prerequisites checker:

```bash
python check_prerequisites.py
```

This script verifies:
- Python 3.10+
- Azure Developer CLI
- Azure CLI
- Docker (installed and running)
- Git (optional)

**Expected Output:**

```
============================================================
Lab 6: Prerequisites Check
============================================================

Prerequisites Check Results:
------------------------------------------------------------
Python: 3.12.0
Azure Developer CLI: 1.23.0
Azure CLI: Installed
Docker: 24.0.7
Docker: Running
Azure CLI: Not logged in (run 'az login')
Git: 2.42.0
------------------------------------------------------------

All required prerequisites are installed!
```

If any checks fail, follow the installation instructions provided by the script.

### Azure login

Log into Azure with both CLI tools:

```bash
# Azure CLI login
az login

# Azure Developer CLI login
azd auth login
```

Both will open a browser for authentication. Use your Azure credentials.

**Verify login:**

```bash
az account show
```

You should see your subscription information.

---

## Step 1: Deploy Your Agent to Azure

In this step, you'll deploy a real AI agent to Azure using the automated deployment helper.

### What Gets Deployed

The deployment creates:
- **Azure AI Foundry Project** - Hosts your agent
- **Azure OpenAI** - GPT-4o model deployment
- **Container Registry** - Stores agent container images
- **Application Insights** - Monitoring and logs
- **Resource Group** - Contains all resources

**Estimated time:** 20 minutes (10-15 minutes for initial deployment)

### Review the agent configuration

Before deploying, review the agent definition in `agent.yaml`:

```yaml
name: enterprise-knowledge-agent
description: Enterprise AI agent with document search

model:
  type: azure_openai
  deployment_name: gpt-4o
  temperature: 0.7

instructions: |
  You are an Enterprise Knowledge Assistant...
  
tools: []  # Will add search tool in Step 3
```

This defines your agent's behavior and configuration.

### Run the deployment helper

Start the interactive deployment wizard:

```bash
python deploy_helper.py
```

The wizard will guide you through:

1. **Prerequisites check** - Verifies all tools are ready
2. **Azure login** - Ensures you're authenticated
3. **Project initialization** - Sets up azd project structure
4. **Configuration** - Prompts for environment name and region
5. **Deployment** - Runs `azd up` to deploy everything

**During the wizard:**

- **Environment name**: Enter something like "lab5" or "dev"
- **Azure region**: Choose "northcentralus", "eastus", or "westus"
  - (These regions have good OpenAI availability)

### Wait for deployment

The deployment process will:

```
[1/5] Creating resource group...          [2/5] Deploying Foundry project...        [3/5] Creating OpenAI deployment...       [4/5] Building agent container...         ⏳ (can take 5-10 minutes)
[5/5] Deploying agent...                  ```

**⏱️ This takes 10-15 minutes.** Go get coffee! ☕

The deployment is complete when you see:

```
========================================
  🎉 Deployment Successful!
========================================

Your agent has been deployed to Azure!
```

### Validate the deployment

Run the validation script to confirm everything worked:

```bash
python validate_deployment.py
```

**Expected output:**

```
========================================
  Lab 6: Deployment Validation
========================================

Retrieving deployment information from azd...

   Found endpoint: https://your-project.services.ai.azure.com
   Found project: your-project-name
   Found resource group: rg-lab5-xyz

Testing connection to AI Project...

   Successfully connected to project!

Checking Azure resources...

   Found 8 resources in 'rg-lab5-xyz'

🌐 Portal URLs:

   Foundry Portal: https://ai.azure.com
   Resource Group: rg-lab5-xyz

========================================
  Validation Summary
========================================

All checks passed!
Your agent is deployed and ready to use!
```

### Test in Foundry Playground

1. Open the **Foundry Portal**: https://ai.azure.com

2. Navigate to **Build** → **Agents**

3. Find your deployed agent (named "enterprise-knowledge-agent")

4. Click **Open in playground**

5. Send a test message:
   ```
   Hello! What can you help me with?
   ```

**Expected response:**

The agent should respond explaining it's an Enterprise Knowledge Assistant ready to help with company information.

**🎉 Congratulations!** You've deployed your first agent to Azure!

---

## Step 2: Add Azure AI Search with Documents

Now you'll add enterprise knowledge search capabilities by creating Azure AI Search and indexing sample documents.

### What Gets Created

- **Azure AI Search service** (Basic tier)
- **Search index** named "company-knowledge"
- **4 indexed documents**:
  - Company handbook
  - Remote work policy
  - Expense report guide
  - IT security policy

**Estimated time:** 15 minutes

### Review sample documents

The lab includes realistic company policy documents in `sample_documents/`:

```
sample_documents/
├── company_handbook.md          (2.5 KB)
├── remote_work_policy.txt       (3.3 KB)
├── expense_report_guide.md      (2.4 KB)
└── it_security_policy.txt       (9.8 KB)
```

Open one or two documents to see the content. These will be searchable by your agent.

### Run the search setup script

This script automates everything:

```bash
python setup_search.py
```

The script will:

1. Retrieve your deployment information
2. Create an Azure AI Search service
3. Create a search index with proper schema
4. Upload all documents from `sample_documents/`
5. Test search functionality
6. Save configuration to `.env`

**During setup:**

```
Step 1: Retrieving Deployment Information
Resource Group: rg-lab5-xyz
Location: northcentralus

Step 2: Creating Azure AI Search Service
Creating search service: search-abc123
⏱️  This takes 2-3 minutes...
Search service created successfully!

Step 3: Creating Search Index
Index 'company-knowledge' created successfully!

Step 4: Uploading Sample Documents
   company_handbook.md
   remote_work_policy.txt
   expense_report_guide.md
   it_security_policy.txt

Uploaded 4 documents successfully!

Step 5: Testing Search
   Remote Work Policy - Contoso Corporation
      Category: Policy
      Source: remote_work_policy.txt

Search is working correctly!

Step 6: Saving Configuration
Configuration saved to .env
```

### Verify search in Azure Portal

1. Open **Azure Portal**: https://portal.azure.com

2. Navigate to your resource group (e.g., "rg-lab5-xyz")

3. Find the **Azure AI Search** service (named "search-abc123")

4. Click on the search service

5. Go to **Indexes** → **company-knowledge**

6. Click **Search** and try a query like "remote work"

You should see results from your indexed documents!

---

## Step 3: Connect Agent to Search (Foundry Portal)

Now you'll connect your agent to the Azure AI Search service using the Foundry portal. This enables your agent to search company documents and provide knowledge-based answers.

**No code required** - everything is done in the portal UI!

**Estimated time:** 10 minutes

### Open Foundry portal

1. Go to: **https://ai.azure.com**

2. Sign in with your Azure credentials

3. Ensure you're in the correct subscription and project

### Navigate to Management Center

1. In the Foundry portal, click **Management Center** in the bottom left corner

2. Click on **Connected Resources** in the left navigation

This is where you manage connections to external services like Azure AI Search.

### Add Azure AI Search connection

1. Click **+ New Connection** button

2. In the connection type list, select **Azure AI Search**

3. In the connection details:
   - **Subscription**: Select your subscription
   - **Resource**: Find and select your search service (starts with "search-")
   - **Authentication**: Select **API Key**

4. Click **Add Connection**

5. Wait for the connection to be validated (should take a few seconds)

6. You should see a success message: "Connection created successfully"

### Update agent with search tool

Now add the search tool to your agent:

1. Navigate back to **Build** → **Agents**

2. Find your agent ("enterprise-knowledge-agent")

3. Click on the agent to open its details

4. Click the **Edit** button (or **Configure** tab)

5. Scroll down to the **Tools** section

6. Click **+ Add Tool**

7. Select **Azure AI Search** from the tool types

8. Configure the tool:
   - **Connection**: Select the connection you just created
   - **Index Name**: Enter `company-knowledge`
   - **Top K**: Enter `5` (number of search results to return)

9. Click **Save** to save the tool configuration

10. Click **Save** again to save the agent changes

**Your agent now has search capabilities!** 🎉

### Test in playground with knowledge queries

1. Click **Open in playground** on your agent

2. Try these knowledge-based queries:

   **Query 1: Remote work policy**
   ```
   What is our remote work policy?
   ```
   
   **Expected**: Agent searches documents and provides details about eligibility, equipment, work hours, etc.

   **Query 2: Expense reports**
   ```
   How do I submit expense reports?
   ```
   
   **Expected**: Agent explains the submission process, limits, approval workflow.

   **Query 3: Security guidelines**
   ```
   What are the laptop security requirements?
   ```
   
   **Expected**: Agent provides information about encryption, passwords, VPN usage.

### Observe search behavior

As you test, notice:

**Grounding**: Agent responses include information from your documents  
**Citations**: (In production) Agent shows which documents were used  
**Relevance**: Semantic search finds relevant content even without exact keyword matches  
**Context**: Agent understands the question and finds appropriate information

### Troubleshooting

**Agent doesn't find information:**
- Wait 30 seconds after adding the tool (indexing delay)
- Verify index name is exactly "company-knowledge"
- Check connection is active in Management Center
- Try more specific questions

**Connection failed:**
- Ensure search service is running (check Azure Portal)
- Verify you have permissions on the search service
- Try recreating the connection with API Key authentication

**No results in search:**
- Documents may still be indexing (wait 1-2 minutes)
- Test search directly in Azure Portal first
- Verify documents were uploaded successfully

---

## Step 4: Publish to Microsoft Teams (Foundry Portal)

Now you'll publish your agent to Microsoft Teams so employees can access it as a custom app.

**No code required** - the Foundry portal handles everything!

**Estimated time:** 15 minutes

### What You'll Create

The Foundry portal will automatically:
- Create Azure Bot Service resources
- Generate Teams app manifest
- Package app icons and configuration
- Provide downloadable `manifest.zip`

### Prepare app information

Before publishing, gather this information:

- **App Name**: "Enterprise Knowledge Agent" (or your choice)
- **Short Description**: "AI agent with company knowledge"
- **Full Description**: "Enterprise AI agent with access to company documentation and search"
- **Developer Name**: Your name or "Contoso Corp"
- **Website URL**: https://contoso.com (or your company URL)
- **Privacy Policy URL**: https://contoso.com/privacy
- **Terms of Use URL**: https://contoso.com/terms

> **Note**: For this lab, placeholder URLs are fine. In production, these should be real policy pages.

### Create app icons

You'll need two simple icons:

1. **Color icon** (192x192 pixels):
   - Full color version of your app logo
   - PNG format
   - Can create in PowerPoint/Slides, Canva, or Figma

2. **Outline icon** (32x32 pixels):
   - Simple white outline on transparent background
   - PNG format
   - Used in Teams sidebar

**Quick option**: Use a solid color square with your initials or a simple emoji as the icon for this lab.

### Publish from Foundry portal

1. Go to your agent in Foundry portal (**Build** → **Agents**)

2. Click on your agent to open details

3. Click the **Publish** button at the top

4. Select deployment target: **Microsoft Teams**

5. Click **Continue**

### Configure Teams app details

Fill in the Teams app configuration form:

**Basic Information:**
- **App Name**: Enterprise Knowledge Agent
- **Short Description**: AI agent with company knowledge
- **Full Description**: Enterprise AI agent with access to company documentation

**Developer Information:**
- **Developer Name**: Your name
- **Website**: https://contoso.com
- **Privacy Policy**: https://contoso.com/privacy
- **Terms of Use**: https://contoso.com/terms

**App Icons:**
- Upload your **color icon** (192x192 px)
- Upload your **outline icon** (32x32 px)

**App Scope:**
- Choose **Shared** for personal testing
- Or **Organization** for company-wide (requires admin approval)

**Permissions** (pre-selected):
- Identity
- Message team members

Click **Generate Package**

### Download manifest package

After generation completes:

1. The portal displays: "App package created successfully"

2. You'll see your Bot ID and other details

3. Click **Download** to get `manifest.zip`

4. Save the file to your computer

**What just happened:**
- Azure Bot Service was created automatically
- Bot authentication was configured
- Teams manifest was generated
- App package was created

### Upload to Microsoft Teams

Now install the app in Teams:

1. **Open Microsoft Teams** (desktop app or web)

2. Click **Apps** in the left sidebar

3. Click **Manage your apps** (bottom left)

4. Click **Upload an app**

5. Select **Upload a custom app**

6. Browse and select your downloaded `manifest.zip`

7. Click **Add** to install for yourself
   - Or **Add to a team** to install for a team

8. The app installs and opens automatically

### Test your agent in Teams!

1. Find your agent in Teams (should open automatically after install)

2. Start a conversation with a test query:
   ```
   Hello! What can you help me with?
   ```

3. Try knowledge queries:
   ```
   What is our remote work policy?
   ```
   
   ```
   How do I submit expense reports?
   ```

4. Observe the agent responding with information from your knowledge base!

**🎉 Congratulations!** Your agent is now deployed to Teams!

### What You've Accomplished

Published agent to Teams via Foundry portal  
Created Azure Bot Service automatically  
Generated Teams app manifest  
Installed custom app in Teams  
Tested knowledge queries in production environment

### Troubleshooting

**Can't upload app to Teams:**
- Ensure manifest.zip is not corrupted (re-download if needed)
- Check Teams admin hasn't blocked custom apps
- Try uploading for yourself first (not team-wide)
- Verify icons are correct size (192x192 and 32x32)

**Agent doesn't respond:**
- Check Bot Service is running (Azure Portal → Resource Group)
- Verify agent is deployed and active in Foundry
- Check Application Insights for errors
- Test agent in Foundry playground first

**Permission denied:**
- "Organization" scope requires Teams admin approval
- Use "Shared" scope for personal testing
- Contact your Teams admin if needed

**Wrong information returned:**
- Agent uses search connection from Foundry
- Verify search is working in playground first
- Check that documents are properly indexed

---

## Step 5: Cleanup All Resources

**IMPORTANT**: Always clean up resources to avoid ongoing charges!

**Estimated time:** 5 minutes

### Why Cleanup Matters

Leaving resources running incurs charges:
- Azure OpenAI: ~$0.50/day
- Azure AI Search: ~$0.25-0.50/hour
- Container Registry: ~$0.10/day
- **Total**: ~$1-2/day if left running

Cleaning up now saves money! 💰

### Run the cleanup script

The cleanup script safely removes all Azure resources:

```bash
python cleanup_all.py
```

### Confirm deletion

The script will:

1. **Show what will be deleted:**
   ```
   Resources to be deleted:
   • AI Foundry Project (1 resource)
   • Azure OpenAI (1 resource)
   • Azure AI Search (1 resource)
   • Container Registry (1 resource)
   • Application Insights (1 resource)
   • Bot Service (1 resource)
   
   Total: 8 resources
   ```

2. **Estimate cost savings:**
   ```
   By cleaning up resources, you avoid:
   ~$1-2/day in ongoing charges
   ```

3. **Ask for confirmation:**
   ```
   Are you sure you want to delete everything? Type 'yes' to confirm:
   ```

4. Type **yes** and press Enter

### Wait for cleanup

The cleanup process:

```
Running azd down...
⏱️  This may take 3-5 minutes...

Deleting resource group...
Removing Azure Bot Service...
Purging OpenAI resources...

All resources deleted successfully!
```

### Verify cleanup

The script automatically verifies resources were deleted:

```
Verifying cleanup...

Resource group 'rg-lab5-xyz' deleted
All resources removed successfully!
```

### Remove Teams app (optional)

If you installed the agent in Teams, uninstall it:

1. Open Microsoft Teams

2. Go to **Apps**

3. Click **Manage your apps**

4. Find "Enterprise Knowledge Agent"

5. Click the **...** menu → **Uninstall**

6. Confirm deletion

The Azure Bot Service backend is already deleted, so the app won't work anymore anyway.

### Verify in Azure Portal

Double-check everything is gone:

1. Go to https://portal.azure.com

2. Navigate to **Resource Groups**

3. Your lab resource group (e.g., "rg-lab5-xyz") should be gone

4. Check **All Resources** view - no lab resources should appear

### Manual Cleanup (if script fails)

If automatic cleanup failed, delete manually:

```bash
# Delete via Azure CLI
az group delete --name rg-lab5-xyz --yes --no-wait

# Or use Azure Portal:
# 1. Go to Resource Groups
# 2. Find your lab resource group
# 3. Click "Delete resource group"
# 4. Type the name to confirm
```

---

## Lab Summary

**Congratulations!** 🎉 You've completed Lab 6!

### What You Accomplished

**Deployed a real AI agent to Azure** using Azure Developer CLI  
**Created Azure AI Search** with indexed company documents  
**Connected agent to search** using Foundry portal (Foundry IQ)  
**Published to Microsoft Teams** using Foundry portal automation  
**Tested in production** with real knowledge queries  
**Cleaned up resources** to manage costs

### Skills You Learned

**Azure AI Foundry:**
- Deploy agents to production with `azd`
- Configure agent models and instructions
- Use Foundry portal for connections and publishing
- Monitor with Application Insights

**Azure AI Search:**
- Create search services and indexes
- Index documents for semantic search
- Connect search to agents (RAG pattern)
- Test and verify search functionality

**Microsoft Teams Integration:**
- Publish agents to Teams via Foundry portal
- Understand bot architecture
- Install custom apps in Teams
- Troubleshoot Teams deployments

**Azure Resource Management:**
- Use Azure Developer CLI for deployments
- Manage resource groups and services
- Monitor costs and usage
- Clean up resources properly

### Production Best Practices

From this lab, you learned:

**Automate deployments** - Use scripts and tools like `azd`  
**Use portal UIs** - When available, portals simplify complex tasks  
**Monitor resources** - Application Insights tracks agent behavior  
**Manage costs** - Always clean up when done  
**Test thoroughly** - Validate at each step before proceeding  
**Document setup** - Keep track of endpoints and configuration

### Next Steps

To build on this lab:

1. **Add more documents** to your search index
2. **Customize agent instructions** for your use case
3. **Add more tools** (e.g., Microsoft Graph API)
4. **Implement authentication** for sensitive data
5. **Set up monitoring** and alerts
6. **Create CI/CD pipeline** for automated deployments

### Resources

**Documentation:**
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
- [Publish to Teams](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/publish-copilot)

**Tools:**
- [Azure Portal](https://portal.azure.com)
- [Foundry Portal](https://ai.azure.com)
- [Teams](https://teams.microsoft.com)

---

**Lab Complete!** 🎉

You've successfully deployed a production AI agent with knowledge search and Teams integration!
    "text": "Found 5 documents matching your query",
    "wrap": true
  }],
  "actions": [{
    "type": "Action.Submit",
    "title": "View Details",
    "data": { "action": "details" }
  }]
}
```

### Deployment walkthrough

The application walks through the 9-step deployment process:

1. **Install Teams Toolkit** - VS Code extension
2. **Create Teams App Project** - Use template
3. **Configure Bot Registration** - Azure Bot Service
4. **Connect to AI Agent** - Link backend logic
5. **Design Adaptive Cards** - Create rich UI
6. **Test Locally** - Debug in Teams with tunnel
7. **Deploy to Azure** - Publish to App Service
8. **Publish to Teams** - Submit to admin center
9. **Users Install App** - Teams App Store

### Teams capabilities

**What agents can do in Teams:**

| Capability | Description | Use Case |
|------------|-------------|----------|
| **Personal Chat** | 1-on-1 with agent | Individual queries |
| **Team Channels** | Agent in channels | Team collaboration |
| **Message Extensions** | Search and share | Quick lookups |
| **Tabs** | Embedded UI | Rich dashboards |
| **Adaptive Cards** | Interactive responses | Forms, approvals |
| **SSO** | Single Sign-On | Seamless auth |
| **Notifications** | Proactive messages | Alerts, updates |

### Security and compliance

**Built-in security features:**
- Azure AD authentication
- Respects Teams data policies
- Audit logging enabled
- Data residency compliance
- Admin controls and policies
- User consent and permissions

**Production considerations:**
- Implement rate limiting
- Monitor token usage
- Log all interactions
- Handle errors gracefully
- Provide user feedback mechanisms

---

## Microsoft 365 (Graph API) Integration

In this exercise, you'll learn how to integrate agents with Microsoft 365 services using Microsoft Graph API.

### What is Microsoft Graph API?

**Microsoft Graph** is the unified REST API for accessing Microsoft 365 data and services. It enables agents to interact with SharePoint, Outlook, Calendar, Teams, and more.

**Unified Access:**
```
One API → All M365 Services
```

### Run the application

1. **Select option 3** from the menu: "Task 3: Microsoft 365 (Graph API) Integration"

### Understand Graph API architecture

```
┌─────────────────────────────────┐
│        Your AI Agent            │
└────────┬────────────────────────┘
         │
         │ Microsoft Graph API
         │ (REST - HTTPS)
         │
┌────────▼────────────────────────┐
│   Microsoft 365 Services        │
│                                 │
│  [SharePoint] [Outlook] [Teams] │
│  [OneDrive]   [Calendar][Users] │
└─────────────────────────────────┘
```

### Common integrations

The application shows 4 common integration patterns:

**1. SharePoint Search**
```python
@agent_function
def search_sharepoint(query: str) -> dict:
    endpoint = 'https://graph.microsoft.com/v1.0/search/query'
    body = {
        'requests': [{
            'entityTypes': ['driveItem'],
            'query': {'queryString': query}
        }]
    }
    response = requests.post(endpoint, headers=auth_headers, json=body)
    return response.json()
```

**Use cases:**
- Search for company documents
- Find specific files or folders
- Locate SharePoint sites

**2. Calendar Operations**
```python
@agent_function
def get_calendar_events(days: int = 7) -> list:
    endpoint = 'https://graph.microsoft.com/v1.0/me/events'
    params = {
        '$select': 'subject,start,end,organizer',
        '$top': 10
    }
    response = requests.get(endpoint, headers=auth_headers, params=params)
    return response.json()['value']
```

**Use cases:**
- Check availability
- Schedule meetings
- Get upcoming events
- Send meeting invites

**3. Email Operations**
```python
@agent_function
def send_email(to: str, subject: str, body: str) -> bool:
    endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'
    message = {
        'message': {
            'subject': subject,
            'body': {'contentType': 'Text', 'content': body},
            'toRecipients': [{'emailAddress': {'address': to}}]
        }
    }
    response = requests.post(endpoint, headers=auth_headers, json=message)
    return response.status_code == 202
```

**Use cases:**
- Send notifications
- Email reports
- Forward information
- Automate communications

**4. User Profile**
```python
@agent_function
def get_user_profile() -> dict:
    endpoint = 'https://graph.microsoft.com/v1.0/me'
    response = requests.get(endpoint, headers=auth_headers)
    return response.json()
```

**Use cases:**
- Personalize responses
- Check user department
- Get manager info
- Access user preferences

### Authentication flow

**OAuth 2.0 Process:**

1. User signs in with Microsoft account
2. App requests permissions (scopes)
3. User consents to permissions
4. App receives access token
5. Token used for API calls

**Required Scopes:**
```python
scopes = [
    'Calendars.Read',      # Read calendars
    'Mail.Send',           # Send email
    'Files.Read.All',      # Read files
    'User.Read',           # Read profile
    'Sites.Read.All'       # Search SharePoint
]
```

### Implementation pattern

**Complete example:**
```python
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient

# Initialize Graph client
credential = DefaultAzureCredential()
scopes = ['https://graph.microsoft.com/.default']
graph_client = GraphServiceClient(credential, scopes)

# Use in agent function
@agent_function
def search_company_docs(query: str):
    """Search SharePoint using Graph API"""
    results = graph_client.search.query(query)
    return format_results(results)
```

### Benefits and considerations

**Benefits:**
- Unified API for all M365 services
- Strong authentication and security
- Respects user permissions (no elevation)
- Rich data access across services
- Webhooks for real-time events
- Well-documented with SDKs

**Considerations:**
- Requires proper permission scopes
- Rate limiting (throttling)
- Token expiration and refresh
- Data privacy and compliance
- User consent requirements

---

## Production Enterprise Agent Demo

In this exercise, you'll interact with a complete enterprise agent demonstrating all integration concepts.

### Run the application

1. **Select option 4** from the menu: "Task 4: Production Enterprise Agent Demo"

2. The application creates an interactive enterprise assistant.

### Try the enterprise agent

**Suggested Queries:**

**Knowledge Search:**
- "Find documents about remote work policy"
- "Search for Q4 sales reports"
- "What's our code of conduct?"

**Calendar/Schedule:**
- "Check my calendar for tomorrow"
- "Do I have any meetings this week?"
- "When is my next team meeting?"

**IT Support:**
- "How do I submit an IT ticket?"
- "What's the VPN setup process?"
- "Who do I contact for laptop issues?"

**Company Info:**
- "What are our company values?"
- "Where can I find the employee handbook?"
- "What's the org chart for my department?"

### Observe agent behavior

**The agent demonstrates:**
- Natural language understanding
- Context retention across messages
- Professional, helpful tone
- Graceful handling of unknown information
- Suggestions for further help

**In production, this agent would:**
- Search actual SharePoint/documents
- Access real calendar data via Graph API
- Send emails and create tickets
- Personalize based on user profile
- Log all interactions for compliance

### Production enhancements

**To make this production-ready:**

1. **Add Real Integrations**
   - Connect to Azure AI Search
   - Implement Graph API calls
   - Add custom business functions
   - Integrate with ticketing systems

2. **Enhance Security**
   - Implement proper authentication
   - Add authorization checks
   - Validate all inputs
   - Encrypt sensitive data

3. **Improve Monitoring**
   - Log all queries and responses
   - Track performance metrics
   - Monitor error rates
   - Alert on failures

4. **Optimize Performance**
   - Cache frequent queries
   - Implement rate limiting
   - Use async operations
   - Optimize token usage

5. **Enhance UX**
   - Add typing indicators
   - Use rich Adaptive Cards
   - Provide quick actions
   - Enable feedback collection

---

## Architecture & Deployment Guide

### View the complete architecture

**Select option 5** from the menu to see the production architecture.

### Complete Production Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    End Users                             │
│  (Employees via Teams, Web, Mobile)                      │
└────────┬─────────────────────────────────────────────────┘
         │ HTTPS
         ▼
┌──────────────────────────────────────────────────────────┐
│              Microsoft Teams                             │
│  • Chat Interface  • Adaptive Cards  • Extensions        │
└────────┬─────────────────────────────────────────────────┘
         │ Bot Framework
         ▼
┌──────────────────────────────────────────────────────────┐
│         Azure Bot Service (App Service)                  │
│  • Conversation routing  • Authentication  • Handling    │
└────────┬─────────────────────────────────────────────────┘
         │
         ├──────────────────┬────────────────────┐
         │                  │                    │
         ▼                  ▼                    ▼
┌────────────────┐  ┌──────────────┐  ┌────────────────┐
│ AI Foundry     │  │ Azure AI     │  │ Microsoft      │
│ Agent          │  │ Search       │  │ Graph API      │
│ • Logic        │  │ • Knowledge  │  │ • M365 Data    │
│ • Functions    │  │ • Semantic   │  │ • SharePoint   │
│ • Tools        │  │   search     │  │ • Calendar     │
└────────────────┘  └──────────────┘  └────────────────┘
```

### 6-Week Deployment Timeline

**Phase 1: Development (Weeks 1-2)**
- □ Create AI Foundry project and agent
- □ Develop and test agent functions
- □ Set up Azure AI Search index
- □ Test locally with portal

**Phase 2: Teams Integration (Week 3)**
- □ Install Teams Toolkit
- □ Create Teams app project
- □ Configure bot registration
- □ Design Adaptive Cards
- □ Test locally in Teams

**Phase 3: M365 Integration (Week 4)**
- □ Register app in Azure AD
- □ Configure Graph API permissions
- □ Implement authentication
- □ Add SharePoint/Calendar functions
- □ Test with real M365 data

**Phase 4: Production Deployment (Week 5)**
- □ Deploy to Azure App Service
- □ Configure production settings
- □ Set up monitoring/logging
- □ Publish to Teams Admin Center
- □ Pilot with small user group

**Phase 5: Rollout (Week 6)**
- □ Train users
- □ Publish to Teams App Store
- □ Monitor usage
- □ Gather feedback
- □ Iterate and improve

### Production Best Practices

**🔒 Security:**
- Use managed identities (no secrets in code)
- Implement least-privilege access
- Enable audit logging
- Encrypt data at rest and in transit
- Regular security reviews

**Monitoring:**
- Application Insights for telemetry
- Custom metrics (response time, success rate)
- Error tracking and alerting
- User feedback collection
- Cost monitoring (token usage)

**Performance:**
- Cache frequent queries
- Optimize token usage
- Use async operations
- Implement rate limiting
- Auto-scale based on demand

**👥 User Experience:**
- Clear onboarding messages
- Helpful error messages
- Typing indicators
- Rich Adaptive Cards
- Feedback mechanisms

**Operations:**
- CI/CD pipelines
- Automated testing
- Blue-green deployments
- Rollback procedures
- Incident response plan

---

## Summary

Congratulations! You've completed Lab 6 and learned production deployment patterns for AI agents.

### What You've Learned

1. **Foundry IQ**
   - Enterprise knowledge search
   - Azure AI Search integration
   - Automatic grounding and citations

2. **Microsoft Teams Deployment**
   - Teams Toolkit usage
   - Bot configuration
   - Adaptive Cards UI
   - App manifest and permissions

3. **Microsoft Graph API**
   - SharePoint search
   - Calendar and email operations
   - Authentication flows
   - M365 service integration

4. **Production Architecture**
   - Complete deployment topology
   - Security and monitoring
   - Performance optimization
   - Operational best practices

### Key Takeaways

| Concept | Key Learning |
|---------|--------------|
| **Foundry IQ** | Enterprise knowledge grounding at scale |
| **Teams** | Brings agents to where employees work |
| **Graph API** | Unified access to M365 services |
| **Security** | Authentication, authorization, compliance |
| **Architecture** | Multi-tier, scalable, resilient design |

### Real-World Applications

**IT Support Bot:**
- Knowledge base search
- Ticket creation
- Status tracking
- Escalation workflows

**HR Assistant:**
- Policy questions
- Benefits information
- Time-off requests
- Employee onboarding

**Sales Assistant:**
- CRM queries
- Product information
- Quote generation
- Lead tracking

**Knowledge Agent:**
- Document search
- Expert finding
- Training resources
- Best practices

### Production Deployment Checklist

Before going live:

- **Security**: Auth, permissions, encryption
- **Compliance**: Data residency, audit logs, policies
- **Performance**: Caching, scaling, optimization
- **Monitoring**: Telemetry, alerts, dashboards
- **Testing**: Unit, integration, load, security tests
- **Documentation**: User guides, admin docs, runbooks
- **Training**: User training, admin training
- **Support**: Help desk, escalation procedures

### Congratulations!

🎉 **You've completed all 5 core labs!**

You now have the skills to:
- Build AI agents from scratch
- Implement advanced tools and capabilities
- Extend agents with MCP
- Coordinate multiple agents
- Deploy to production environments

**Total Learning**: 315 minutes (5.25 hours) of hands-on experience

### Next Steps

**Continue Learning:**
- Explore Lab 6 (Agent Framework - Optional)
- Build your own production agent
- Join the AI agent community
- Share your experiences

**Stay Updated:**
- Follow Microsoft Foundry updates
- Try new features as they release
- Contribute to open-source agent projects
- Attend AI conferences and webinars

---

## Clean Up

All agents created in this lab were automatically deleted after each exercise. No additional cleanup required.

## Additional Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Foundry IQ Guide](https://learn.microsoft.com/azure/ai-foundry/foundry-iq)
- [Teams Toolkit Documentation](https://learn.microsoft.com/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)
- [Microsoft Graph API Reference](https://learn.microsoft.com/graph/overview)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [Azure AI Search](https://learn.microsoft.com/azure/search/)
