---
lab:
    title: 'Multi-Agent Orchestration'
    description: 'Master multi-agent coordination patterns from local to distributed to visual orchestration using a unified interactive application.'
---

# Lab 4: Multi-Agent Orchestration

In this lab, you'll master multi-agent coordination by exploring three different orchestration patterns: local coordination (agents in the same process), distributed coordination with Agent-to-Agent (A2A) protocol, and visual workflow orchestration. You'll build a complete content creation pipeline using specialized agents working together.

This lab takes approximately **75** minutes.

> **Note**: This lab builds on Labs 1-3. You should be familiar with basic agent creation, custom functions, and tool integration.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Design and implement local multi-agent coordination patterns
2. Understand the Agent-to-Agent (A2A) protocol for distributed systems
3. Compare code-based vs visual workflow orchestration
4. Apply best practices for multi-agent error handling and monitoring
5. Choose the appropriate orchestration pattern for different scenarios
6. Build production-ready multi-agent systems

## Prerequisites

Before starting this lab, ensure you have:

- Completed Labs 1-3 (or be familiar with agents, functions, and MCP)
- An Microsoft Foundry project with a deployed model
- Visual Studio Code with Foundry extension installed
- Python 3.12 or later installed
- Understanding of async/await patterns

## Scenario

You'll build a **Content Creation Pipeline** that coordinates multiple specialized agents:

- **🔍 Research Agent**: Gathers information and key findings on topics
- **📋 Outline Agent**: Creates structured outlines from research
- **✍️ Writer Agent**: Generates polished content from outlines
- **👁️ Review Agent**: (Optional) Quality checks and editorial review

These agents will work together in three different orchestration patterns, allowing you to understand the progression from simple to sophisticated multi-agent systems.

## Lab Structure

This lab uses a **unified interactive application** (`multi_agent_lab.py`) that demonstrates all orchestration patterns in one place.

```
Menu Options:
1. Exercise 1: Local Multi-Agent Coordination
2. Exercise 2: Agent-to-Agent (A2A) Communication
3. Exercise 3: Workflow Orchestration Concepts
4. Exercise 4: Interactive Content Pipeline Demo
5. View Architecture Overview
0. Exit
```

---

## Setup

### Task 1: Navigate to the lab directory

1. Open Visual Studio Code.

2. Open the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\uplevel\04-multi-agent-orchestration\Python
   ```
   
   Use **File > Open Folder** in VS Code.

### Task 2: Configure environment

1. Create a `.env` file (reuse from previous labs):

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    MODEL_DEPLOYMENT_NAME=gpt-4o
    ```
    
    **To get your endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

2. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

### Task 3: Verify setup

Ensure you have:
- ✅ `multi_agent_lab.py` - Main unified application
- ✅ `requirements.txt`
- ✅ `.env` with your project endpoint

---

## Exercise 1: Local Multi-Agent Coordination

In this exercise, you'll see how multiple specialized agents can work together sequentially in the same process to complete a complex task.

### What is Local Coordination?

**Local multi-agent coordination** means multiple agents running in the same Python process, passing data between each other through function calls or shared memory. This is the simplest orchestration pattern.

**Architecture:**
```
┌─────────────────────────────────────┐
│      Single Python Process          │
│                                     │
│  Research Agent                     │
│       ↓                             │
│  Outline Agent                      │
│       ↓                             │
│  Writer Agent                       │
│       ↓                             │
│  Final Content                      │
└─────────────────────────────────────┘
```

### Task 1: Run Exercise 1

1. **Start the unified application**:

    ```powershell
    python multi_agent_lab.py
    ```

2. **Select option 1** from the menu: "Exercise 1: Local Multi-Agent Coordination"

### Task 2: Observe the content creation pipeline

The application will demonstrate a complete multi-agent workflow:

**Phase 1: Research**
```
🔍 Research Agent working...

📊 Research Results:
• AI agents improve efficiency by automating repetitive tasks
• Cost savings of 30-40% in business automation scenarios
• 24/7 availability without human intervention
• Reduces human error in data processing
• Scales easily to handle increased workload
```

**Phase 2: Outline**
```
📋 Outline Agent working...

📝 Outline:
1. Introduction to AI Agents in Business
2. Key Benefits
   2.1 Efficiency Improvements
   2.2 Cost Reduction
   2.3 Error Reduction
3. Implementation Considerations
4. Conclusion
```

**Phase 3: Writing**
```
✍️ Writer Agent working...

📄 Final Article:
AI agents are revolutionizing business automation by providing
intelligent, autonomous capabilities that transform how organizations
operate. These digital assistants bring unprecedented efficiency...
[complete article generated]
```

### Task 3: Understand the coordination flow

**Sequential Coordination Pattern:**
```python
# From multi_agent_lab.py (simplified)

# Step 1: Research
research_results = research_agent.run(topic)

# Step 2: Create outline from research
outline = outline_agent.run(research_results)

# Step 3: Write content from outline
final_content = writer_agent.run(outline)
```

**Key Characteristics:**
- ✅ **Simple**: Easy to understand and debug
- ✅ **Fast**: No network latency between agents
- ✅ **Reliable**: All agents in same process
- ❌ **Limited Scalability**: Bound to single process
- ❌ **No Isolation**: One agent failure affects all

### Task 4: Key concepts

**When to Use Local Coordination:**
- Prototyping and development
- Simple workflows with 2-4 agents
- Low-volume processing
- When latency is critical
- Single-machine deployment

**Agent Specialization Benefits:**
- Each agent has clear, focused responsibility
- Easier to test individual agents
- Can optimize each agent independently
- Reusable agents for different workflows

**Coordination Patterns:**
```
Sequential:  A → B → C → D
Parallel:    A → [B, C, D] → E
Conditional: A → (B or C) → D
Iterative:   A → B → C → (back to A if needed)
```

---

## Exercise 2: Agent-to-Agent (A2A) Communication

In this exercise, you'll learn about distributed agent architectures using the Agent-to-Agent protocol, where agents run as independent services.

### What is A2A Protocol?

**Agent-to-Agent (A2A)** is a protocol that enables agents to communicate as independent HTTP services. Each agent runs in its own process, container, or even different machines.

**Architecture:**
```
┌──────────────┐
│ Coordinator  │
│   Agent      │
└──────┬───────┘
       │ HTTP
       ├─────────────┬───────────────┐
       │             │               │
┌──────▼──────┐ ┌───▼────────┐ ┌───▼────────┐
│  Research   │ │  Outline   │ │   Writer   │
│  Service    │ │  Service   │ │  Service   │
│  :5001      │ │  :5002     │ │  :5003     │
└─────────────┘ └────────────┘ └────────────┘
```

### Task 1: Run Exercise 2

1. If not already running, start the application:
   ```powershell
   python multi_agent_lab.py
   ```

2. **Select option 2** from the menu: "Exercise 2: Agent-to-Agent (A2A) Communication"

### Task 2: Understand A2A components

The exercise explains the four key components of A2A:

**1. Agent Registration**
Each agent registers its capabilities:
```python
agent_info = {
    "name": "research-agent",
    "description": "Gathers research on topics",
    "endpoint": "http://localhost:5001/invoke",
    "capabilities": ["research", "fact-checking"]
}
```

**2. Agent Discovery**
Coordinator finds available agents:
```python
available_agents = registry.list_agents()
research_agent = registry.find_agent('research-agent')
```

**3. Agent Invocation**
HTTP POST to agent endpoint:
```python
response = requests.post(
    research_agent.endpoint,
    json={'task': 'Research AI benefits'},
    headers={'Authorization': f'Bearer {token}'}
)
```

**4. Response Handling**
Structured JSON responses:
```python
result = response.json()
if result['status'] == 'success':
    next_step(result['data'])
else:
    handle_error(result['error'])
```

### Task 3: Observe the simulation

The application simulates a distributed workflow:

```
[Coordinator] Sending task to Research Agent (HTTP POST)
[Research Agent] Processing research request...
[Research Agent] Returning results to Coordinator
[Coordinator] Sending outline task to Outline Agent
[Outline Agent] Creating structured outline...
[Outline Agent] Returning outline to Coordinator
[Coordinator] Workflow complete!
```

### Task 4: Key concepts

**A2A Benefits:**

| Benefit | Description |
|---------|-------------|
| **Scalability** | Each agent scales independently (horizontal scaling) |
| **Resilience** | Agent failures don't crash entire system |
| **Flexibility** | Mix languages and technologies (polyglot) |
| **Deployment** | Deploy to containers, serverless, cloud |
| **Security** | Network policies, authentication per service |
| **Monitoring** | Track each agent separately |

**Deployment Options:**
- **Azure Container Apps** ⭐ (Recommended - serverless containers)
- **Azure Kubernetes Service** (AKS - full orchestration)
- **Azure App Service** (Simple web apps)
- **Azure Functions** (Serverless, event-driven)

**Security Considerations:**
```python
# Use managed identities
credential = DefaultAzureCredential()

# Implement authentication
headers = {
    'Authorization': f'Bearer {get_token()}',
    'X-API-Key': os.getenv('API_KEY')
}

# Enable network policies
# VNet integration in Azure Container Apps
```

**Error Handling:**
```python
@retry(max_attempts=3, backoff=exponential)
async def invoke_agent(agent_endpoint, task):
    try:
        response = await http_client.post(
            agent_endpoint,
            json=task,
            timeout=30
        )
        return response.json()
    except TimeoutError:
        logger.error(f"Agent timeout: {agent_endpoint}")
        return fallback_response()
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise
```

### Task 5: A2A vs Local comparison

| Aspect | Local | A2A Distributed |
|--------|-------|-----------------|
| **Complexity** | Low | Medium-High |
| **Scalability** | Limited | High |
| **Resilience** | Low | High |
| **Latency** | Very Low | Higher (network) |
| **Cost** | Low | Medium-High |
| **Use Case** | Dev/prototyping | Production |

---

## Exercise 3: Workflow Orchestration Concepts

In this exercise, you'll learn about visual workflow orchestration and when to use code vs visual tools.

### What is Workflow Orchestration?

**Workflow orchestration** provides visual, low-code/no-code coordination of multi-agent systems. Tools like Microsoft Foundry Workflow Designer let you drag-and-drop agents into workflows.

### Task 1: Run Exercise 3

1. **Select option 3** from the menu: "Exercise 3: Workflow Orchestration Concepts"

### Task 2: Understand visual workflows

The exercise displays a visual workflow canvas:

```
┌─────────────────────────────────────────────────────┐
│              Workflow Canvas                        │
│                                                     │
│  [Start] ──► [Research] ──► [Outline] ──► [Write] │
│                   │             │            │      │
│                   │             │            ▼      │
│                   │             │        [Review]   │
│                   │             │            │      │
│                   │             │        ┌───┴───┐  │
│                   │             │        │ Good? │  │
│                   │             │        └───┬───┘  │
│                   │             │            │      │
│                   │             │        Yes │  No  │
│                   │             │            │   │  │
│                   │             │            ▼   └──┘
│                   │             │        [Publish]  │
└─────────────────────────────────────────────────────┘
```

### Task 3: Learn workflow components

**1. Triggers**
- Manual start button
- HTTP endpoint (webhook)
- Schedule (cron: "0 9 * * MON")
- Event-driven (Azure Event Grid)

**2. Agent Steps**
- Call local agents
- Invoke A2A agents
- Execute custom code snippets
- External API calls

**3. Control Flow**
- **Sequential**: One step after another
- **Parallel**: Multiple steps simultaneously
- **Conditional**: If-else branching
- **Loop**: Iterate until condition met

**4. Error Handling**
- Try-catch blocks around steps
- Retry policies (exponential backoff)
- Fallback agents for failures
- Alert notifications to teams

**5. Data Flow**
- Pass outputs as inputs to next step
- Transform data (JSON manipulation)
- Store intermediate results
- Aggregate final outputs

### Task 4: Code vs Visual comparison

**Code-Based Orchestration:**
```python
# Sequential coordination
research = await research_agent.run(topic)
outline = await outline_agent.run(research)
content = await writer_agent.run(outline)

# Error handling
try:
    result = await process_step()
except Exception:
    result = await fallback_step()

# Conditional logic
if quality_check(content):
    publish(content)
else:
    revise(content)
```

**Visual Workflow (JSON Export):**
```json
{
  "workflow": {
    "name": "content-pipeline",
    "steps": [
      {"id": 1, "type": "agent", "agent": "research"},
      {"id": 2, "type": "agent", "agent": "outline"},
      {"id": 3, "type": "agent", "agent": "writer"},
      {"id": 4, "type": "condition", "check": "quality"},
      {"id": 5, "type": "agent", "agent": "publish"}
    ],
    "error_handling": {
      "retry": 3,
      "fallback": "alert-admin"
    }
  }
}
```

### Task 5: When to use each approach

**✅ Use Code When:**
- Need fine-grained control
- Complex custom logic required
- Version control is critical
- Frequent debugging expected
- Dev team is technical

**✅ Use Visual Workflows When:**
- Non-technical stakeholders involved
- Rapid prototyping needed
- Standard patterns apply
- Visual documentation helps
- Business users design workflows

**🎯 Best Practice: Use Both!**
```
1. Prototype visually in workflow designer
2. Export workflow to code
3. Add custom logic and error handling
4. Deploy code to production
5. Keep visual diagram updated for docs
```

---

## Exercise 4: Interactive Content Pipeline Demo

In this exercise, you'll interact with a live multi-agent content creation pipeline.

### Task 1: Run Exercise 4

1. **Select option 4** from the menu: "Exercise 4: Interactive Content Pipeline Demo"

2. The application creates a Research + Writer agent team.

### Task 2: Create content interactively

**Try these topics:**

1. **Technical Topics:**
   - "Benefits of microservices architecture"
   - "Getting started with Kubernetes"
   - "Introduction to GraphQL APIs"

2. **Business Topics:**
   - "Improving customer retention strategies"
   - "Digital transformation in healthcare"
   - "Sustainable business practices"

3. **Custom Topics:**
   - Enter your own topic of interest

### Task 3: Observe the workflow

For each topic, you'll see:

```
📍 Creating content about: 'Your Topic'
══════════════════════════════════════════════════════

🔍 Step 1: Research Agent working...
   ✓ Research complete

✍️ Step 2: Writer Agent working...
   ✓ Writing complete

══════════════════════════════════════════════════════
📄 GENERATED CONTENT
══════════════════════════════════════════════════════

[Your generated article appears here]

══════════════════════════════════════════════════════
```

### Task 4: Experiment with different approaches

**Sequential (Current):**
```
Research → Write
(Simple, fast)
```

**Extended Pipeline (Concept):**
```
Research → Outline → Write → Review → Publish
(More sophisticated, higher quality)
```

**Parallel Research (Advanced):**
```
[Research Topic 1]  \
[Research Topic 2]  → Synthesize → Outline → Write
[Research Topic 3]  /
(Comprehensive, slower)
```

### Task 5: Key observations

**Agent Collaboration:**
- Research agent provides raw data
- Writer agent transforms data into polished content
- Each agent has clear responsibility
- Output quality depends on coordination

**Production Considerations:**
- Add retry logic for failed agents
- Implement timeout handling
- Cache research results
- Monitor agent performance
- Log all interactions

---

## Exercise 5: Architecture Overview

### Task 1: View the overview

**Select option 5** from the menu to see the complete architecture evolution.

### Understanding the progression

**1️⃣ Local Coordination** (Labs 1-3)
```
Single Process → Simple → Fast → Limited Scale
Good for: Development, prototyping, simple workflows
```

**2️⃣ Distributed A2A** (Production)
```
Multiple Services → Complex → Scalable → Resilient
Good for: Production, high-volume, enterprise
```

**3️⃣ Visual Workflows** (Low-Code)
```
Visual Design → Accessible → Exportable → Documented
Good for: Business users, rapid prototyping, documentation
```

### Comparison matrix

| Pattern | Complexity | Scalability | Resilience | Cost | Best For |
|---------|-----------|-------------|------------|------|----------|
| **Local** | Low | Low | Low | Low | Development |
| **A2A** | High | High | High | Medium | Production |
| **Visual** | Medium | High | High | Low | Business Users |

### Best practices summary

**🎯 Agent Design:**
- Single responsibility principle
- Clear input/output contracts
- Stateless when possible
- Idempotent operations

**🔄 Coordination Patterns:**
- Sequential: A → B → C
- Parallel: A + B → C
- Conditional: A → (B or C) → D
- Loop: A → B → (repeat if needed)

**🛡️ Error Handling:**
- Retry with exponential backoff
- Circuit breakers for failing agents
- Fallback agents for critical paths
- Dead letter queues for failed tasks

**📊 Monitoring:**
- Log all agent interactions
- Track execution time per agent
- Monitor error rates and success rates
- Alert on workflow failures

**🔐 Security:**
- Authenticate all agent-to-agent calls
- Encrypt data in transit (HTTPS/TLS)
- Validate all inputs (prevent injection)
- Audit all operations (compliance)

---

## Summary

Congratulations! You've completed Lab 4 and mastered multi-agent orchestration patterns.

### What You've Learned

1. **Local Multi-Agent Coordination**
   - Sequential agent execution
   - Simple coordination patterns
   - In-process communication

2. **A2A Protocol**
   - Distributed agent architecture
   - HTTP-based communication
   - Scalable, resilient systems

3. **Visual Orchestration**
   - Workflow designer concepts
   - Code vs visual tradeoffs
   - Low-code/no-code patterns

4. **Production Patterns**
   - Error handling strategies
   - Monitoring and logging
   - Security best practices

### Key Takeaways

| Concept | Key Learning |
|---------|--------------|
| **Specialization** | Each agent should have one clear purpose |
| **Coordination** | Choose pattern based on scale and complexity |
| **Resilience** | Distributed systems are more fault-tolerant |
| **Flexibility** | Visual + code approaches complement each other |
| **Production** | Error handling and monitoring are critical |

### Evolution Path

```
Development → Testing → Staging → Production
    ↓            ↓          ↓          ↓
  Local      → Local    → A2A      → A2A
  (Prototype)  (Test)    (Staging)  (Scale)
```

### Production Deployment Checklist

Before deploying multi-agent systems to production:

- ✅ **Testing**
  - Unit test each agent independently
  - Integration test agent interactions
  - Load test expected volume
  - Chaos engineering (failure scenarios)

- ✅ **Monitoring**
  - Application Insights or similar
  - Custom metrics per agent
  - Distributed tracing
  - Alert rules for failures

- ✅ **Security**
  - Managed identities for authentication
  - Network isolation (VNets)
  - Input validation on all agents
  - Audit logging

- ✅ **Scalability**
  - Auto-scaling rules
  - Load balancing
  - Rate limiting
  - Caching strategies

- ✅ **Operations**
  - CI/CD pipelines
  - Blue-green deployments
  - Rollback procedures
  - Incident response plan

### Real-World Applications

**Content Creation** (This Lab):
- Research → Outline → Write → Review → Publish

**Customer Support**:
- Triage → Route → Resolve → Follow-up

**Data Processing**:
- Ingest → Validate → Transform → Analyze → Report

**Order Fulfillment**:
- Receive → Validate → Process → Ship → Notify

### Next Steps

In **Lab 5: M365 & Teams Integration**, you'll learn how to deploy your agents to production environments, integrate with Microsoft 365, and create Teams-based agent experiences.

**Continue to**: [Lab 5 - M365 & Teams Integration](./05-m365-teams-integration.md)

---

## Clean Up

All agents created in this lab were automatically deleted after each exercise. No additional cleanup required.

## Additional Resources

- [Multi-Agent Systems Architecture](https://learn.microsoft.com/azure/ai-foundry/agents/multi-agent)
- [Azure Container Apps for Agent Deployment](https://learn.microsoft.com/azure/container-apps/)
- [Agent-to-Agent Protocol Specification](https://learn.microsoft.com/azure/ai-foundry/agents/a2a-protocol)
- [Workflow Designer Documentation](https://learn.microsoft.com/azure/ai-foundry/workflows)
- [Production Deployment Best Practices](https://learn.microsoft.com/azure/ai-foundry/agents/production)
