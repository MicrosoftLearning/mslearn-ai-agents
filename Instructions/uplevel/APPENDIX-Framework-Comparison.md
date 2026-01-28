# Appendix: Microsoft Agent Framework vs Azure AI Projects SDK

## Overview

This appendix helps you understand the differences between the two primary approaches for building AI agents with Microsoft Foundry:

1. **Azure AI Projects SDK** (`azure-ai-projects`) - Used in Labs 1-5
2. **Microsoft Agent Framework SDK** (`agent-framework`) - Alternative approach

Both SDKs enable you to build powerful AI agents, but they take different architectural approaches. This guide will help you choose the right one for your scenario.

---

## Quick Comparison

| Aspect | Azure AI Projects SDK | Microsoft Agent Framework |
|--------|----------------------|---------------------------|
| **Used In** | Labs 1-5 (all upleveled labs) | Original Lab 04 |
| **Approach** | Portal-first, then code | Code-first |
| **Best For** | Microsoft Foundry projects | Cross-platform, framework enthusiasts |
| **Learning Curve** | Easier (portal + code) | Steeper (all code) |
| **Portal Integration** | ✅ Native | ❌ Limited |
| **Multi-Provider** | ❌ Azure only | ✅ OpenAI, Azure, Anthropic, local |
| **Plugin Ecosystem** | ❌ No | ✅ Yes (community plugins) |
| **Code Samples** | All Labs 1-5 | Lab 04 |
| **Production Ready** | ✅ Yes | ✅ Yes |

---

## What is Azure AI Projects SDK?

The **Azure AI Projects SDK** (`azure-ai-projects`) is the official Python SDK for working with Microsoft Foundry projects and the Azure AI Agent Service.

### Key Characteristics:

- **Portal-first workflow**: Create agents in the Foundry portal, enhance with code
- **Native Foundry integration**: Direct access to all Foundry features
- **VS Code extension support**: Right-click to copy endpoints, manage agents
- **Built-in tools**: CodeInterpreter, FileSearch, MCP out of the box
- **Thread-based conversations**: Simple, stateless agent interactions

### Example Code (from Labs 1-5):

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool

# Connect to your Foundry project
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.getenv("PROJECT_ENDPOINT")
)

# Create an agent with custom functions
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="You are a helpful assistant.",
    tools=[
        FunctionTool(my_custom_function)
    ]
)

# Create a thread and run
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Hello!"
)

run = project_client.agents.create_and_process_run(
    thread_id=thread.id,
    agent_id=agent.id
)

# Get response
messages = project_client.agents.list_messages(thread_id=thread.id)
```

### When to Use:

✅ **Use Azure AI Projects SDK when:**
- Building agents for Microsoft Foundry projects
- Want to leverage Foundry portal for agent management
- Need VS Code extension integration
- Working with MCP servers
- Deploying to Teams or M365
- Team includes non-developers (portal access)
- Want the simplest path to production

---

## What is Microsoft Agent Framework?

The **Microsoft Agent Framework** (`agent-framework`, formerly Semantic Kernel) is a framework for building AI agents that work across multiple AI providers.

### Key Characteristics:

- **Code-first approach**: Everything defined in code
- **Framework abstraction**: Works with multiple AI providers (OpenAI, Azure, Anthropic, local models)
- **Plugin architecture**: Reusable plugin ecosystem
- **Advanced memory**: Semantic memory, vector-based recall
- **Planning capabilities**: Automatic task decomposition

### Example Code (from Lab 04):

```python
from agent_framework import AgentThread, ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Define a custom tool function
def send_email(
    to: str,
    subject: str,
    body: str
):
    print(f"Email sent to {to}: {subject}")

# Create a chat agent
async with (
    AzureCliCredential() as credential,
    ChatAgent(
        chat_client=AzureAIAgentClient(credential=credential),
        name="expenses_agent",
        instructions="You are an expense processing assistant.",
        tools=send_email,
    ) as agent,
):
    # Run the agent
    response = await agent.run(["Submit my expense claim"])
    print(response)
```

### When to Use:

✅ **Use Microsoft Agent Framework when:**
- Need to switch between AI providers (OpenAI, Azure, local)
- Building cross-platform applications
- Want to use community plugins (Office365, GitHub, JIRA, etc.)
- Need advanced memory and semantic search
- Prefer framework-based development patterns
- Building custom plugin ecosystems
- Want planning and reasoning capabilities

---

## Side-by-Side: Creating an Agent with Custom Functions

### Scenario: IT Support Agent with System Status Function

#### Azure AI Projects SDK Approach:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool

def check_system_status(system_name: str) -> dict:
    """Check the status of a system."""
    return {
        "system": system_name,
        "status": "operational",
        "uptime": "99.9%"
    }

# Create agent in portal OR via code
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="it-support-agent",
    instructions="Help users with IT issues.",
    tools=[FunctionTool(check_system_status)]
)

# Use the agent
thread = project_client.agents.create_thread()
project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Check the email system status"
)

run = project_client.agents.create_and_process_run(
    thread_id=thread.id,
    agent_id=agent.id
)
```

**Pros:**
- ✅ Can create agent in portal first
- ✅ Simple thread-based conversation
- ✅ Clear, straightforward API

**Cons:**
- ❌ Azure-only
- ❌ Less flexibility in execution patterns

---

#### Agent Framework Approach:

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from pydantic import Field
from typing import Annotated

def check_system_status(
    system_name: Annotated[str, Field(description="Name of the system to check")]
) -> dict:
    """Check the status of a system."""
    return {
        "system": system_name,
        "status": "operational",
        "uptime": "99.9%"
    }

# Create agent (code-only)
async with (
    AzureCliCredential() as credential,
    ChatAgent(
        chat_client=AzureAIAgentClient(credential=credential),
        name="it-support-agent",
        instructions="Help users with IT issues.",
        tools=check_system_status,
    ) as agent,
):
    response = await agent.run(["Check the email system status"])
    print(response)
```

**Pros:**
- ✅ Provider-agnostic (can swap to OpenAI easily)
- ✅ Framework patterns (async, context managers)
- ✅ Plugin architecture for reusability

**Cons:**
- ❌ No portal integration
- ❌ More boilerplate code
- ❌ Requires async/await understanding

---

## Decision Matrix

### Choose **Azure AI Projects SDK** if:

| Criteria | Why |
|----------|-----|
| **Starting with portal** | Portal provides visual agent builder |
| **Team has non-developers** | Portal access for testing/configuration |
| **Using VS Code extension** | Native integration with Foundry extension |
| **Need MCP servers** | Built-in MCP support |
| **Deploying to Teams/M365** | Seamless Foundry → Teams deployment |
| **Want simplest approach** | Less code, more portal configuration |

### Choose **Microsoft Agent Framework** if:

| Criteria | Why |
|----------|-----|
| **Multi-provider requirement** | Need to work with OpenAI, Anthropic, local models |
| **Framework preference** | Prefer framework patterns (plugins, DI, etc.) |
| **Using community plugins** | Want Office365, GitHub, JIRA integrations |
| **Complex memory needs** | Semantic memory, vector search |
| **Planning/reasoning** | Need automatic task decomposition |
| **Code-first culture** | Team prefers all configuration in code |

---

## Can You Mix Both?

**Yes, but carefully.**

You can use both SDKs in the same project, but they serve different purposes:

### Hybrid Approach:

```python
# Use Azure AI Projects SDK for Foundry agents
from azure.ai.projects import AIProjectClient

# Use Agent Framework for local processing
from agent_framework import ChatAgent

# Example: Foundry agent for production, Framework agent for development
if os.getenv("ENVIRONMENT") == "production":
    # Use Foundry agent
    agent = project_client.agents.create_agent(...)
else:
    # Use local Agent Framework for testing
    agent = ChatAgent(...)
```

**When to mix:**
- Development: Use Agent Framework locally with OpenAI
- Production: Deploy to Foundry with Azure AI Projects SDK
- Testing: Framework for unit tests, Projects SDK for integration tests

**When NOT to mix:**
- Don't try to convert agents between frameworks (incompatible)
- Don't mix in same execution path (confusing)
- Don't duplicate functionality (choose one approach)

---

## Migration Guidance

### From Agent Framework → Azure AI Projects SDK

**Why migrate:**
- Want Foundry portal integration
- Need Teams deployment
- Team prefers visual tools

**Migration steps:**
1. Create Foundry project in portal
2. Recreate agents using `AIProjectClient.agents.create_agent()`
3. Convert custom functions to `FunctionTool` format
4. Replace async agent execution with thread-based pattern
5. Test in Foundry portal

**Compatibility:**
- ✅ Custom functions translate directly
- ✅ Instructions/prompts work the same
- ❌ Plugins need rewriting as functions
- ❌ Memory patterns differ

---

### From Azure AI Projects SDK → Agent Framework

**Why migrate:**
- Need multi-provider support
- Want framework plugin ecosystem
- Require advanced memory/planning

**Migration steps:**
1. Extract agent instructions and functions from Foundry
2. Create `ChatAgent` with equivalent configuration
3. Rewrite tool calls using Agent Framework patterns
4. Replace thread management with agent execution
5. Implement memory if needed

**Compatibility:**
- ✅ Instructions work the same
- ✅ Custom functions translate directly
- ❌ MCP servers not directly supported
- ❌ Code interpreter requires separate implementation

---

## Common Patterns Comparison

### Pattern 1: Async Custom Functions

#### Azure AI Projects SDK:
```python
async def analyze_data(data_id: str) -> dict:
    # Async operation
    result = await external_api.analyze(data_id)
    return result

# Use in agent
agent = project_client.agents.create_agent(
    tools=[FunctionTool(analyze_data)]
)
```

#### Agent Framework:
```python
async def analyze_data(
    data_id: Annotated[str, Field(description="Data ID")]
) -> dict:
    # Same async operation
    result = await external_api.analyze(data_id)
    return result

# Use in agent
async with ChatAgent(tools=analyze_data) as agent:
    response = await agent.run(["Analyze data 123"])
```

**Similarity:** Both support async functions natively

---

### Pattern 2: File Upload and Analysis

#### Azure AI Projects SDK:
```python
# Upload file
file = project_client.agents.upload_file(
    file_path="data.csv",
    purpose=FilePurpose.AGENTS
)

# Use code interpreter
agent = project_client.agents.create_agent(
    tools=[CodeInterpreterTool()],
    tool_resources={
        "code_interpreter": {
            "file_ids": [file.id]
        }
    }
)
```

#### Agent Framework:
```python
# No built-in code interpreter
# Must implement file handling manually or use plugins

def analyze_csv(file_path: str) -> dict:
    import pandas as pd
    df = pd.read_csv(file_path)
    return {"summary": df.describe().to_dict()}

async with ChatAgent(tools=analyze_csv) as agent:
    response = await agent.run(["Analyze data.csv"])
```

**Difference:** Azure SDK has built-in CodeInterpreter, Framework requires custom implementation

---

### Pattern 3: Multi-Agent Coordination

#### Azure AI Projects SDK (from Lab 4):
```python
# Create specialized agents
research_agent = project_client.agents.create_agent(
    name="research-agent",
    instructions="Research topics thoroughly."
)

writer_agent = project_client.agents.create_agent(
    name="writer-agent",
    instructions="Write engaging content."
)

# Coordinate manually
research_thread = project_client.agents.create_thread()
research_run = project_client.agents.create_and_process_run(
    thread_id=research_thread.id,
    agent_id=research_agent.id
)

# Pass results to writer
writer_thread = project_client.agents.create_thread()
# ... coordinate manually
```

#### Agent Framework:
```python
# Framework has built-in multi-agent patterns
from agent_framework import AgentGroup

async with AgentGroup([
    ChatAgent(name="research-agent", ...),
    ChatAgent(name="writer-agent", ...)
]) as group:
    # Framework coordinates automatically
    result = await group.execute("Write article about AI")
```

**Difference:** Framework has more advanced orchestration patterns built-in

---

## Labs 1-5 Coverage with Azure AI Projects SDK

Here's what you learned in the upleveled labs using Azure AI Projects SDK:

| Lab | Capabilities Covered |
|-----|---------------------|
| **Lab 1** | Agent creation (portal + code), custom functions, FunctionTool |
| **Lab 2** | CodeInterpreter, async functions, file operations, data analysis |
| **Lab 3** | MCP integration (remote + local servers), external tool integration |
| **Lab 4** | Multi-agent coordination, A2A protocol, visual workflows |
| **Lab 5** | Foundry IQ, Teams deployment, M365 Graph API, production patterns |

**Result:** You have comprehensive production-ready skills with Azure AI Projects SDK.

---

## When to Learn Agent Framework

Consider learning Microsoft Agent Framework if:

1. **After completing Labs 1-5**, you want to explore alternative approaches
2. **Multi-cloud strategy**: Your organization uses multiple AI providers
3. **Open-source preference**: You prefer framework-based development
4. **Plugin ecosystem**: You need community plugins (Office365, GitHub, etc.)
5. **Local development**: You want to develop with local models (Ollama, etc.)

---

## Resources

### Azure AI Projects SDK
- **Documentation**: https://learn.microsoft.com/azure/ai-services/agents/
- **SDK Reference**: https://aka.ms/azsdk/python/ai-projects/docs
- **Samples**: Labs 1-5 in this repository
- **VS Code Extension**: Microsoft Foundry (marketplace)

### Microsoft Agent Framework
- **Documentation**: https://learn.microsoft.com/semantic-kernel/
- **GitHub**: https://github.com/microsoft/semantic-kernel
- **Samples**: Lab 04 in this repository
- **Community**: https://aka.ms/sk-discord

---

## Summary

**For most learners completing Labs 1-5:**
- ✅ **Azure AI Projects SDK** is the right choice
- ✅ You have all the skills needed for production agents
- ✅ No need to learn Agent Framework unless specific requirements

**Agent Framework is valuable when:**
- 🔄 Need multi-provider support
- 🔌 Want plugin ecosystem
- 🎯 Require advanced planning/memory
- 💻 Prefer code-first, framework patterns

**Both SDKs are production-ready and Microsoft-supported.** Your choice depends on your requirements, not quality or capability.

---

## Conclusion

The upleveled labs (Labs 1-5) teach you the **Azure AI Projects SDK** approach, which is:
- Simpler to learn (portal + code)
- Native to Microsoft Foundry
- Ideal for Teams and M365 deployment
- Perfect for most enterprise scenarios

**Microsoft Agent Framework** is a powerful alternative for developers who need cross-platform capabilities or prefer framework-based patterns.

**You don't need to learn both.** Choose based on your requirements, and the skills from Labs 1-5 will serve you well in production agent development.

---

*This appendix is supplementary material for the Microsoft Foundry Upleveled Labs (Labs 1-5). It is not required reading but provides context for developers curious about alternative approaches.*
