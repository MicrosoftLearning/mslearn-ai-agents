---
lab:
    title: 'Work IQ - Workplace Intelligence for AI Agents (Optional)'
    description: 'Build AI agents that access Microsoft 365 workplace data using Work IQ and the Model Context Protocol for meeting prep, project tracking, and action items.'
    level: 300
    duration: 40
---

# Work IQ - Workplace Intelligence for AI Agents

In this lab, you'll build an AI agent that accesses your Microsoft 365 workplace data using **Work IQ** - Microsoft's contextual intelligence layer built on the Model Context Protocol (MCP). You'll create a workplace intelligence agent that can prepare for meetings, track projects, extract action items, and answer workplace questions using real M365 data.

This lab takes approximately **40** minutes.

> **Note:** This is an **optional/advanced lab** that requires a Microsoft 365 Copilot license. It's designed for enterprise learners, Microsoft employees, or those with M365 Copilot access. Standard M365 accounts without Copilot will not work.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Understand Work IQ architecture and how it integrates with Microsoft 365
2. Connect AI agents to Work IQ using the Model Context Protocol (MCP)
3. Build workplace intelligence scenarios (meeting prep, project tracking, action items)
4. Combine Work IQ (workplace signals) with Foundry IQ (knowledge base)
5. Design effective queries for workplace data
6. Handle authentication, permissions, and privacy correctly

## Prerequisites

Before starting this lab, ensure you have:

- Basic understanding of AI agents and the Model Context Protocol (MCP)
- **Microsoft 365 with Copilot License**
- IT admin approval for Work IQ (organizational accounts only)
- Node.js 18 or higher installed
- Python 3.10 or higher installed
- Azure CLI (authenticated with `az login`)
- Active M365 data (emails, meetings, Teams chats) to query

> **Important:** Work IQ **only works** with Microsoft 365 Copilot-enabled accounts. You cannot complete this lab without Copilot.

## Scenario

You'll build a **Workplace Intelligence Agent** that helps you:

- **Meeting Prep**: Gather context from emails, previous meetings, and shared documents
- **Project Status**: Track updates across emails, Teams, and files
- **Action Items**: Extract tasks from meetings, emails, and Teams mentions
- **Combined Intelligence**: Use both workplace data (Work IQ) and knowledge base (Foundry IQ)
- **Custom Queries**: Answer any workplace question using M365 data

## Architecture

This lab demonstrates Work IQ integration with AI agents:

```
┌─────────────────────────────────────────┐
│         Your AI Agent                   │
│   (Microsoft Foundry Project)           │
└────────┬────────────────────────────────┘
         │
         │ StdioMCPClient
         │
┌────────▼────────────────────────────────┐
│  Work IQ MCP Server                     │
│  (npx @microsoft/workiq mcp)            │
└────────┬────────────────────────────────┘
         │
         │ M365 APIs (Copilot license)
         │
┌────────▼────────────────────────────────┐
│  Microsoft 365 Data Sources             │
│  • Emails (Outlook)                     │
│  • Calendar & Meetings                  │
│  • Teams Messages & Chats               │
│  • OneDrive & SharePoint Docs          │
│  • People & Org Data                    │
└─────────────────────────────────────────┘
```

---

## Setup

### Install Work IQ

1. Open your terminal or command prompt.

2. Install Work IQ globally via npm:

   ```bash
   npm install -g @microsoft/workiq
   ```

3. Accept the End User License Agreement:

   ```bash
   workiq accept-eula
   ```

4. Test your Work IQ installation:

   ```bash
   workiq ask -q "What meetings do I have today?"
   ```

5. **If the test succeeds** - You'll see meeting information from your M365 calendar. Continue to the next task!

6. **If you see "Admin consent required":**

   - The command will display a consent URL
   - Send this URL to your IT administrator with the message: "I need Work IQ access for the Microsoft Learn AI Agents lab"
   - Wait for admin approval, then retry the test command

7. **If you see "No M365 Copilot license":**

   - Unfortunately, you cannot complete this lab without a Copilot license
   - You can still read through the instructions to understand the concepts
   - Consider this lab optional and return to it when you have Copilot access

### Prepare the lab environment

1. Open Visual Studio Code.

2. Navigate to the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\05b-work-iq-integration\Python
   ```
   
   Use **File > Open Folder** in VS Code.

3. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

5. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Configure your `.env` file:

   In the lab folder, open the `.env` file and update it with your Foundry project endpoint:

   ```env
   PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-id
   MODEL_DEPLOYMENT_NAME=gpt-4.1
   ```

   > **Tip:** To get your endpoint: In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

### Verify setup

Ensure you have:
- Work IQ installed and accessible (`workiq --version` works)
- Admin consent approved (or personal M365 account with Copilot)
- `workiq_lab.py` - Main interactive application
- `requirements.txt` - Python dependencies installed
- `.env` file configured with your project endpoint

---

## Explore Workplace Intelligence Scenarios

In this exercise, you'll run a unified interactive application that demonstrates five workplace intelligence scenarios using a single AI agent with Work IQ tools.

### Launch the lab application

1. Ensure you're in the lab directory with your virtual environment activated.

2. Run the lab application:

   ```bash
   python workiq_lab.py
   ```

3. The application will:
   - Validate Work IQ setup
   - Connect to your Microsoft Foundry project
   - Initialize the Work IQ MCP client
   - Create a workplace intelligence agent
   - Display an interactive menu with 5 scenarios

### Meeting Prep scenario

This scenario helps you prepare for meetings by gathering relevant context.

1. From the main menu, select **1 - Meeting Prep**.

2. When prompted, enter a meeting topic or time, such as:
   - "my 2pm meeting"
   - "Q4 Planning session"
   - "team standup"

3. The agent will:
   - Find your meeting details (time, attendees, agenda)
   - Search recent emails about the topic
   - Look for previous meetings on this subject
   - Summarize key points and decisions
   - Suggest discussion points

4. Review the output and note:
   - How sources are cited (emails, meetings, dates)
   - How the agent synthesizes information from multiple sources
   - The time saved compared to manual searching

**Reflection:** How does this differ from manually searching your email and calendar?

### Project Status scenario

This scenario tracks project updates across your workplace tools.

1. From the main menu, select **2 - Project Status**.

2. Enter a project name you're working on, such as:
   - "Website redesign"
   - "Q1 OKRs"
   - "Customer onboarding"

3. The agent will:
   - Search emails and Teams messages about the project
   - Find related meetings and their outcomes
   - Identify recent decisions and changes
   - List blockers or issues mentioned
   - Summarize next steps and deadlines

4. Analyze the results:
   - How comprehensive is the status update?
   - What sources did the agent use?
   - Could this be built with traditional APIs? What's the development effort difference?

### Action Items scenario

This scenario extracts your open tasks from various sources.

1. From the main menu, select **3 - Action Items**.

2. Choose a time range (or press Enter for "this week"):
   - "today"
   - "last 3 days"
   - "this month"

3. The agent will:
   - Search meeting notes for assigned action items
   - Look for task-related emails sent to you
   - Check Teams messages where you were mentioned
   - Identify items with deadlines
   - Prioritize by urgency if possible

4. Examine the output:
   - Are all your action items captured?
   - How accurate is the prioritization?
   - Where were action items found (meetings, emails, Teams)?

### Combined Intelligence scenario

This scenario demonstrates using **both** Work IQ (workplace data) and Foundry IQ (knowledge base) together.

> **Note:** This scenario requires Azure AI Search configured in your Foundry project with an indexed knowledge base.

1. From the main menu, select **4 - Combined Intelligence**.

2. Enter a topic that exists in both your workplace discussions and official documentation:
   - "remote work policy"
   - "expense reporting"
   - "security guidelines"

3. The agent will:
   - Search workplace data (Work IQ): emails, meetings, Teams discussions
   - Search knowledge base (Foundry IQ): official docs, policies, procedures
   - Compare workplace discussions with official documentation
   - Identify gaps or inconsistencies
   - Provide a comprehensive summary with labeled sources

4. Compare the two perspectives:
   - What's documented officially vs. discussed informally?
   - Are there any contradictions?
   - Which source is more up-to-date?

**Key Insight:** 
- **Work IQ** tells you what people are actually doing and saying
- **Foundry IQ** tells you what's officially documented
- **Together** they provide complete context for decision-making

### Custom Query scenario

This scenario lets you explore your workplace data with your own questions.

1. From the main menu, select **5 - Custom Query**.

2. Try different types of workplace questions:

   **Email searches:**
   ```
   Find emails about the budget from my manager
   ```

   **Meeting summaries:**
   ```
   What was decided in yesterday's standup?
   ```

   **Team activity:**
   ```
   What did the engineering team discuss this week?
   ```

   **Document discovery:**
   ```
   Show me shared documents about security policies
   ```

3. Experiment with:
   - Different time ranges
   - Different data sources (emails vs. meetings vs. Teams)
   - Different levels of specificity
   - Follow-up questions to refine results

4. Note what works well:
   - Specific queries usually work better than vague ones
   - Including time ranges improves relevance
   - Names and keywords help narrow results

---

## Explore and Experiment

Now that you've completed all scenarios, take 5-10 minutes to explore on your own.

### Test edge cases

1. Try queries about data you don't have - how does the agent respond?

2. Ask ambiguous questions - how does the agent handle them?

3. Search for very old information - what are the limits?

### Explore different query styles

1. **Very specific**: "Find the email from John about Q3 budget sent on January 15th"

2. **Very broad**: "Tell me about recent developments"

3. **Comparative**: "Compare this week's discussions to last week's"

### View Work IQ capabilities

From the main menu, select **6 - View Work IQ Capabilities** to review:
- Architecture overview
- Data sources available
- Security and privacy model
- Work IQ vs. Foundry IQ comparison
- Common use cases

---

## Understanding the Code

Let's examine the key patterns used in this lab.

### Pattern 1: Work IQ MCP Client Initialization

```python
from azure.ai.projects.mcp import StdioMCPClient

# Connect to Work IQ MCP server
self.workiq_client = StdioMCPClient(
    command="npx",
    args=["-y", "@microsoft/workiq", "mcp"]
)
```

This launches Work IQ as an MCP server subprocess and connects via stdio (standard input/output).

### Pattern 2: Creating Agent with Work IQ Tools

```python
# Get Work IQ tools
workiq_tools = [tool.model_dump() for tool in self.workiq_client.tools]

# Create agent using Responses API
self.agent = self.openai_client.agents.create_version(
    agent_name="workplace-intelligence-agent",
    definition={
        "kind": "prompt",
        "model": self.model_deployment,
        "instructions": "You are a workplace intelligence assistant...",
        "tools": workiq_tools  # Work IQ tools added here
    }
)
```

The agent is given all available Work IQ tools for querying M365 data.

### Pattern 3: Executing Queries with Responses API

```python
# Create conversation
conversation = self.openai_client.conversations.create(
    items=[{"type": "message", "role": "user", "content": query}]
)

# Create response with agent
response = self.openai_client.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent": {
            "type": "agent_reference",
            "name": self.agent.name,
            "version": self.agent.version
        }
    }
)
```

This uses the Responses API pattern (not the old Runs/Threads pattern) for cleaner agent execution.

---

## Clean Up

The lab automatically cleans up the agent when you exit:

```python
self.openai_client.agents.delete_version(
    agent_name=self.agent.name,
    version=self.agent.version
)
```

No Azure resources are created in this lab (Work IQ uses your M365 license), so no additional cleanup is needed.

---

## Troubleshooting

### "Work IQ command not found"

**Solution:** Install Work IQ:
```bash
npm install -g @microsoft/workiq
```

### "Admin consent required"

**Solution:** 
1. Run `workiq mcp` to get the consent URL
2. Send to your IT admin for approval
3. Or use a personal M365 account with Copilot

### "No M365 Copilot license"

**Solution:** This lab requires Copilot. Either:
- Purchase M365 Copilot license ($30/month)
- Use organizational account with Copilot
- Read through the lab to understand concepts without hands-on

### "MCP server not responding"

**Solution:** Test Work IQ directly:
```bash
workiq ask -q "What meetings do I have?"
```

If this fails, reinstall:
```bash
npm install -g @microsoft/workiq
```

### "No data returned"

**Solution:**
- Ensure your M365 account has emails, meetings, Teams activity
- Try broader queries
- Check if your query matches your actual data

---

## Summary

In this lab, you:

* Installed and configured Work IQ MCP server
* Built an AI agent that accesses Microsoft 365 workplace data
* Explored 5 workplace intelligence scenarios (meeting prep, project status, action items, combined intelligence, custom queries)
* Combined Work IQ with Foundry IQ for comprehensive context
* Learned MCP architecture and integration patterns
* Understood security, privacy, and authentication models

### Key Takeaways

1. **Work IQ enables workplace context** - Agents can access the rich signals in M365 data that inform real work

2. **MCP provides a standard interface** - Work IQ uses the Model Context Protocol, making it easy to integrate with agents

3. **Responses API simplifies agent execution** - The new pattern is cleaner than the older Runs/Threads approach

4. **Combined intelligence is powerful** - Work IQ (workplace signals) + Foundry IQ (knowledge base) = complete context

5. **Security is built-in** - Work IQ respects M365 permissions and requires appropriate authentication

### Next Steps

Consider building your own workplace intelligence solutions:
- Specialized meeting assistant
- Automated status reporter
- Task tracking agent
- Communication analyzer
- Decision history tracker

---

## Additional Resources

* [Model Context Protocol Specification](https://modelcontextprotocol.io/)
* [Azure AI Foundry Agents Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/)
* [Work IQ on npm](https://www.npmjs.com/package/@microsoft/workiq)
* [Microsoft 365 Copilot](https://www.microsoft.com/microsoft-365/copilot)
* [Microsoft Graph API](https://learn.microsoft.com/graph/) (alternative approach)
