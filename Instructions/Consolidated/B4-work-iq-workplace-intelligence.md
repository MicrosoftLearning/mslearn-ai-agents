---
title: 'Task 4 – Work IQ: bring Microsoft 365 signals into an agent'
lab:
    title: 'Task 4 – Work IQ: bring Microsoft 365 signals into an agent'
    description: 'Build an agent that accesses Microsoft 365 workplace data using Work IQ and the Model Context Protocol for meeting prep, project tracking, and action items.'
    type: 'task'
    parent: 'B'
    order: 4
    section: 'optional'
    difficulty: 4
    duration: 40
    access: 'gated'
    requires: 'A Microsoft 365 Copilot licence, IT admin consent for Work IQ, and Node.js 18 or later'
    verify: 'Run the command below. If it returns your calendar you''re ready; if it reports missing consent or no Copilot licence, skip this task.'
    verify_command: 'npm install -g @microsoft/workiq && workiq accept-eula && workiq ask -q "What meetings do I have today?"'
    level: 400
    concepts: 'Work IQ, Microsoft 365, Model Context Protocol (MCP), function tools'
    status: 'draft'
---

# Task 4 — Work IQ: bring Microsoft 365 signals into an agent

*Part of the **Integrate agents with enterprise knowledge and Microsoft 365** lab. New here? Start with [Getting started](B0-getting-started.md).*

<!-- BEGIN GENERATED: gated-notice - do not edit by hand; run: python tools/generate_lab_blocks.py -->
> ### Check your access before you start
>
> **This task needs:** A Microsoft 365 Copilot licence, IT admin consent for Work IQ, and Node.js 18 or later.
>
> Run the command below. If it returns your calendar you're ready; if it reports missing consent or no Copilot licence, skip this task.

```
npm install -g @microsoft/workiq && workiq accept-eula && workiq ask -q "What meetings do I have today?"
```

> **Don't have it?** Skip this task. Nothing else in this lab depends on it, and you can still read through the steps to see how it works.
<!-- END GENERATED: gated-notice -->

> **Set up (start here):** This task needs a Foundry project (with a deployed model) and the
> starter code. If you haven't already, complete [Getting started](B0-getting-started.md) to
> create your project, clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in
> `Python/.env`. Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 4
```

> **Continuing from a previous task?** If your project, virtual environment, and `.env` are
> already set from an earlier task, you only need to install Work IQ (below), then go straight to
> **Explore workplace intelligence scenarios**.

---

Where Tasks 1-3 grounded an agent on *documents*, this task connects an agent to **live Microsoft
365 signals** — emails, meetings, Teams messages — using **Work IQ**. You'll build a Caldova
Traders workplace intelligence agent that can prep for meetings, track projects, and extract
action items from real M365 data.

<style>
/* "Ask Anton" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
  border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Anton: "; font-weight:700;
  padding-left:1.5em;
  background:url("../Media/anton-avatar.png") left center / 1.25em 1.25em no-repeat; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>What is Work IQ?</summary>
<div class="concept-body" markdown="1">

**Work IQ** is Microsoft's contextual intelligence layer for Microsoft 365, exposed as a **Model
Context Protocol (MCP)** server. It gives an agent permission-aware access to workplace data —
emails, calendar, Teams messages, and documents — so the agent can reason over what people are
actually doing and saying. It complements **Foundry IQ** (curated knowledge) with **live
workplace signals**.

</div>
</details>

## Install Work IQ

1. Open your terminal or command prompt.

2. Install Work IQ globally via npm:

   ```
   npm install -g @microsoft/workiq
   ```

3. Accept the End User License Agreement:

   ```
   workiq accept-eula
   ```

4. Test your Work IQ installation:

   ```
   workiq ask -q "What meetings do I have today?"
   ```

5. **If the test succeeds** - You'll see meeting information from your M365 calendar. Continue to the next section.

6. **If you see "Admin consent required":**

   - The command will display a consent URL
   - Send this URL to your IT administrator with the message: "I need Work IQ access for the Microsoft Learn AI Agents lab"
   - Wait for admin approval, then retry the test command

7. **If you see "No M365 Copilot license":**

   - Unfortunately, you cannot complete this task without a Copilot license
   - You can still read through the instructions to understand the concepts

## Prepare the app

The Work IQ app is provided **complete** in the starter code — you run it as-is.

1. Open the `Python` folder and activate the virtual environment from [Getting started](B0-getting-started.md):

    ```
    .\labenv\Scripts\Activate.ps1
    ```

1. Confirm your `.env` has `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` set (Work IQ uses the model deployment to run the agent).

1. Review **workiq_lab.py**. It:
    - Validates your Work IQ installation
    - Connects to your Microsoft Foundry project
    - Initializes the Work IQ MCP client (`npx -y @microsoft/workiq mcp`)
    - Creates a `caldova-workplace-agent` with the Work IQ tools
    - Displays an interactive menu with five scenarios

## Explore workplace intelligence scenarios

1. Sign in to Azure, then run the app:

    ```
    az login
    ```

    ```
    python workiq_lab.py
    ```

The application connects to Work IQ and your Foundry project, then shows a menu of five scenarios.

### Meeting Prep scenario

1. From the main menu, select **1 - Meeting Prep**.

2. When prompted, enter a meeting topic or time, such as:
   - "my 2pm meeting"
   - "Spring Catalog Planning session"
   - "site operations standup"

3. The agent will find your meeting details, search recent emails about the topic, look for previous meetings, summarize key points, and suggest discussion points.

4. Review the output and note how sources are cited (emails, meetings, dates) and how the agent synthesizes information from multiple sources.

### Project Status scenario

1. From the main menu, select **2 - Project Status**.

2. Enter a project name you're working on, such as:
   - "Spring Catalog Launch"
   - "Capacity Review"
   - "Supplier onboarding"

3. The agent searches emails and Teams messages, finds related meetings, identifies recent decisions and blockers, and summarizes next steps and deadlines.

### Action Items scenario

1. From the main menu, select **3 - Action Items**.

2. Choose a time range (or press Enter for "this week"): "today", "last 3 days", "this month".

3. The agent searches meeting notes, task-related emails, and Teams mentions, identifies items with deadlines, and prioritizes by urgency.

### Combined Intelligence scenario

This scenario demonstrates using **both** Work IQ (workplace data) and Foundry IQ (knowledge base) together.

> **Note**: This scenario requires Foundry IQ (Azure AI Search) configured in your project with an indexed knowledge base — for example, the Caldova knowledge base from [Task 1](B1-create-a-foundry-iq-knowledge-agent.md).

1. From the main menu, select **4 - Combined Intelligence**.

2. Enter a topic that exists in both your workplace discussions and official documentation:
   - "capacity request and transfer policies"
   - "supplier lead times"
   - "contract manufacturing transfers"

3. The agent searches workplace data (Work IQ) **and** the knowledge base (Foundry IQ), compares informal discussions with official documentation, identifies gaps, and provides a comprehensive summary with labeled sources.

**Key insight:**

- **Work IQ** tells you what people are actually doing and saying
- **Foundry IQ** tells you what's officially documented
- **Together** they provide complete context for decision-making

### Custom Query scenario

1. From the main menu, select **5 - Custom Query**.

2. Try different types of workplace questions:

    ```
    Find emails about the spring catalog from my manager
    ```

    ```
    What was decided in yesterday's site operations standup?
    ```

    ```
    Show me shared documents about supplier lead times
    ```

3. Experiment with different time ranges, data sources, and follow-up questions to refine results.

### View Work IQ capabilities

From the main menu, select **6 - View Work IQ Capabilities** to review the architecture, data sources, security model, and the Work IQ vs. Foundry IQ comparison. Select **0** to exit — the app deletes the `caldova-workplace-agent` version on the way out.

## Understanding the code

Let's examine the key patterns used in `workiq_lab.py`.

### Pattern 1: Work IQ MCP client initialization

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Store server parameters for reuse
self.workiq_server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@microsoft/workiq", "mcp"]
)

# Fetch available tools from Work IQ MCP server
async def _fetch():
    async with stdio_client(self.workiq_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools

raw_tools = asyncio.run(_fetch())
```

Rather than maintaining a persistent connection, a new MCP session is opened per operation. `StdioServerParameters` stores the command and arguments used to launch the Work IQ MCP server subprocess each time.

### Pattern 2: Creating the agent with Work IQ tools

```python
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool

# Convert MCP tools to FunctionTool objects
workiq_tools = [
    FunctionTool(
        name=tool.name,
        description=tool.description,
        parameters=tool.inputSchema,
    )
    for tool in raw_tools
]

# Create agent with Work IQ tools
self.agent = self.project_client.agents.create_version(
    agent_name="caldova-workplace-agent",
    definition=PromptAgentDefinition(
        model=self.model_deployment,
        instructions="You are a workplace intelligence assistant for Caldova staff...",
        tools=workiq_tools  # Work IQ tools added here
    )
)
```

Each MCP tool is wrapped in a `FunctionTool` and passed to a `PromptAgentDefinition`.

### Pattern 3: Tool call loop

After the initial response, the agent may request one or more Work IQ tool calls. These are executed and fed back to continue the conversation:

```python
from openai.types.responses.response_input_param import FunctionCallOutput

while True:
    if response.status == "failed":
        break

    input_list = []
    for item in response.output:
        if item.type == "function_call":
            kwargs = json.loads(item.arguments)
            result = self._call_workiq_tool(item.name, kwargs)
            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result.content[0].text,
                )
            )

    if input_list:
        response = self.openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": self.agent.name, "type": "agent_reference"}}
        )
    else:
        break  # No more tool calls - final response ready
```

The loop continues until the agent produces a response with no pending function calls, at which point `response.output_text` contains the final answer.

> ✅ **Checkpoint**: You've built an agent that brings **live Microsoft 365 signals** into its
> reasoning through Work IQ, and seen how it complements the document-grounded agent from Task 1.

## Clean up

The app deletes the `caldova-workplace-agent` version when you exit. Work IQ uses your M365 license rather than creating Azure resources, so there's nothing else to remove for this task. When you're finished, enter `deactivate` to exit the virtual environment.

## Troubleshooting

**"Work IQ command not found"** — Install Work IQ: `npm install -g @microsoft/workiq`

**"Admin consent required"** — Run `workiq mcp` to get the consent URL and send it to your IT admin, or use a personal M365 account with Copilot.

**"No M365 Copilot license"** — This task requires Copilot. Use an account with an M365 Copilot license, or read through the lab to understand the concepts.

**"MCP server not responding"** — Test Work IQ directly with `workiq ask -q "What meetings do I have?"`. If it fails, reinstall with `npm install -g @microsoft/workiq`.

**"No data returned"** — Ensure your M365 account has emails, meetings, and Teams activity, and try broader queries.

---

**Back to the [lab overview](B-integrate-agents-with-enterprise-knowledge-and-m365.md).**
