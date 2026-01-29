---
lab:
    title: 'M365 & Teams Integration'
    description: 'Deploy AI agents to production with Microsoft 365 and Teams integration using a unified interactive application.'
---

# Lab 5: M365 & Teams Integration

In this lab, you'll learn how to deploy AI agents to production environments by integrating with Microsoft 365 and Microsoft Teams. You'll explore Foundry IQ for enterprise knowledge search, Teams deployment patterns, and Microsoft Graph API integration.

This lab takes approximately **75** minutes.

> **Note**: This lab builds on Labs 1-4. You should be familiar with agent creation, tools, MCP, and multi-agent patterns.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Configure Foundry IQ for enterprise knowledge search
2. Understand Microsoft Teams deployment architecture
3. Integrate agents with Microsoft Graph API (M365 services)
4. Apply production deployment best practices
5. Design secure, scalable enterprise agent solutions
6. Navigate the production deployment lifecycle

## Prerequisites

Before starting this lab, ensure you have:

- Completed Labs 1-4 (or be familiar with agent fundamentals)
- An Microsoft Foundry project with a deployed model
- Visual Studio Code with Foundry extension installed
- Python 3.12 or later installed
- Understanding of REST APIs and authentication

## Scenario

You'll explore deploying an **Enterprise Knowledge Agent** that:

- Searches company documentation using Foundry IQ
- Runs in Microsoft Teams for employee access
- Integrates with Microsoft 365 (SharePoint, Calendar, Email)
- Follows production security and monitoring patterns

This represents a complete, real-world enterprise AI agent deployment.

## Lab Structure

This lab uses a **unified interactive application** (`m365_teams_lab.py`) that demonstrates all production deployment patterns.

```
Menu Options:
1. Exercise 1: Foundry IQ Knowledge Agent
2. Exercise 2: Microsoft Teams Deployment Concepts
3. Exercise 3: Microsoft 365 (Graph API) Integration
4. Exercise 4: Production Enterprise Agent Demo
5. View Architecture & Deployment Guide
0. Exit
```

---

## Setup

### Task 1: Navigate to the lab directory

1. Open Visual Studio Code.

2. Open the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\uplevel\05-m365-teams-integration\Python
   ```
   
   Use **File > Open Folder** in VS Code.

### Task 2: Configure environment

1. In the lab folder, locate the provided `.env` and `requirements.txt` files.

1. Open the `.env` file and replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    MODEL_DEPLOYMENT_NAME=gpt-4o
    ```
    
    **To get your endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

1. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

### Task 3: Verify setup

Ensure you have:
- ✅ `m365_teams_lab.py` - Main unified application
- ✅ `requirements.txt`
- ✅ `.env` with your project endpoint

---

## Exercise 1: Foundry IQ Knowledge Agent

In this exercise, you'll learn about Foundry IQ, which connects AI agents to enterprise knowledge bases using Azure AI Search.

### What is Foundry IQ?

**Foundry IQ** is Microsoft Foundry's solution for grounding agents in enterprise data. It connects your agent to Azure AI Search, enabling semantic search across company documents with automatic citations.

**Architecture:**
```
User Query
    ↓
AI Agent
    ↓
Foundry IQ Connection
    ↓
Azure AI Search Index
    ↓
Enterprise Documents (PDFs, Word, SharePoint, etc.)
```

### Task 1: Run Exercise 1

1. **Start the unified application**:

    ```powershell
    python m365_teams_lab.py
    ```

2. **Select option 1** from the menu: "Exercise 1: Foundry IQ Knowledge Agent"

### Task 2: Understand Foundry IQ architecture

The application displays the complete architecture:

```
┌─────────────────────────────────────────┐
│        Your AI Agent                    │
│   (Microsoft Foundry Project)            │
└────────┬────────────────────────────────┘
         │
         │ Foundry IQ Connection
         ▼
┌─────────────────────────────────────────┐
│      Azure AI Search                    │
│   (Enterprise Knowledge Base)           │
│                                         │
│  • Company documents                    │
│  • Product documentation                │
│  • Internal wikis                       │
│  • SharePoint content                   │
└─────────────────────────────────────────┘
```

### Task 3: Observe knowledge agent demonstration

The application creates a knowledge agent and demonstrates enterprise search:

**Sample Queries:**
- "What is our remote work policy?"
- "How do I submit expense reports?"
- "What are the company's security guidelines?"

**What you'll see:**
1. Agent is created with knowledge search capabilities
2. Queries are processed against the knowledge base
3. Responses include information from company documents
4. (In production) Citations show source documents

### Task 4: Key components

**1. Azure AI Search Index**

The foundation of enterprise search:
```
Documents → Upload → Index → Embeddings → Search-ready
```

Supports:
- PDF, Word, Excel, PowerPoint
- HTML pages and SharePoint sites
- Custom data sources via connectors
- Semantic ranking for relevance

**2. Foundry IQ Connection**

Bridges agent to search:
```python
# Simplified configuration
agent = agents_client.create_agent(
    model='gpt-4o',
    name='knowledge-agent',
    instructions='Search and answer from knowledge base',
    tools=[
        AzureAISearchTool(
            search_endpoint='https://your-search.search.windows.net',
            index_name='company-knowledge'
        )
    ]
)
```

**3. Automatic Grounding**

Agent responses include:
- ✅ Information from indexed documents
- ✅ Source citations (document names, pages)
- ✅ Confidence scores
- ✅ Semantic relevance ranking

### Task 5: Production setup steps

**To implement in production:**

1. **Create Azure AI Search resource**
   ```powershell
   az search service create \
     --name company-search \
     --resource-group your-rg \
     --sku standard
   ```

2. **Index your documents**
   - Upload documents to Azure Blob Storage
   - Configure AI Search indexer
   - Enable semantic ranking
   - Test search queries

3. **Create Foundry IQ connection**
   - In AI Foundry portal: Settings → Connections
   - Add Azure AI Search connection
   - Specify index name and endpoint
   - Test connection

4. **Configure agent**
   - Add Azure AI Search tool
   - Specify index and search parameters
   - Define grounding behavior
   - Test with sample queries

5. **Refine and optimize**
   - Adjust search relevance
   - Configure semantic ranker
   - Add custom skills if needed
   - Monitor query performance

### Task 6: Key concepts

**Semantic Search vs Keyword Search:**

| Aspect | Keyword Search | Semantic Search |
|--------|---------------|-----------------|
| **Matching** | Exact text matches | Meaning-based |
| **Relevance** | Frequency-based | Context-aware |
| **Ranking** | TF-IDF | Neural embeddings |
| **Results** | Literal matches | Conceptually similar |

**Best Practices:**
- ✅ Index documents regularly (daily/weekly)
- ✅ Use semantic ranking for better results
- ✅ Configure synonyms for domain terms
- ✅ Monitor search performance and costs
- ✅ Implement access control (document-level)

---

## Exercise 2: Microsoft Teams Deployment

In this exercise, you'll learn how to deploy AI agents to Microsoft Teams for enterprise-wide access.

### What is Teams Deployment?

**Microsoft Teams** integration allows employees to interact with AI agents directly in their collaboration platform. Agents appear as bots in Teams chat, channels, and meetings.

**User Experience:**
```
Employee opens Teams
    ↓
Starts chat with Knowledge Agent
    ↓
Agent responds with information
    ↓
Rich Adaptive Cards display results
    ↓
Employee takes action (approve, search more, etc.)
```

### Task 1: Run Exercise 2

1. **Select option 2** from the menu: "Exercise 2: Microsoft Teams Deployment Concepts"

### Task 2: Understand Teams architecture

The application displays the complete deployment architecture:

```
┌──────────────────────────────────┐
│   Microsoft Teams Client         │
│  (Desktop, Web, Mobile)          │
└────────┬─────────────────────────┘
         │ Secure Channel
         ▼
┌──────────────────────────────────┐
│   Teams App (Your Agent)         │
│  • Adaptive Cards UI             │
│  • Bot conversation              │
│  • Message extensions            │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│   Microsoft Foundry Agent         │
│   (Backend Logic)                │
└──────────────────────────────────┘
```

### Task 3: Learn deployment components

**1. Teams Toolkit (VS Code Extension)**

Your deployment tool:
- Project scaffolding and templates
- Local debugging with ngrok tunnels
- One-click Azure deployment
- App manifest configuration

**Install:**
```
VS Code Extensions → Search "Teams Toolkit" → Install
```

**2. App Manifest (manifest.json)**

Defines your Teams app:
```json
{
  "name": { "short": "Knowledge Agent" },
  "description": { 
    "short": "Enterprise knowledge assistant",
    "full": "Search company docs and get answers"
  },
  "bots": [{
    "botId": "${{BOT_ID}}",
    "scopes": ["personal", "team", "groupchat"]
  }],
  "permissions": ["identity", "messageTeamMembers"]
}
```

**3. Adaptive Cards**

Rich, interactive UI:
```json
{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "body": [{
    "type": "TextBlock",
    "text": "Search Results",
    "weight": "bolder",
    "size": "large"
  }, {
    "type": "TextBlock",
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

### Task 4: Deployment walkthrough

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

### Task 5: Teams capabilities

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

### Task 6: Security and compliance

**Built-in security features:**
- ✅ Azure AD authentication
- ✅ Respects Teams data policies
- ✅ Audit logging enabled
- ✅ Data residency compliance
- ✅ Admin controls and policies
- ✅ User consent and permissions

**Production considerations:**
- Implement rate limiting
- Monitor token usage
- Log all interactions
- Handle errors gracefully
- Provide user feedback mechanisms

---

## Exercise 3: Microsoft 365 (Graph API) Integration

In this exercise, you'll learn how to integrate agents with Microsoft 365 services using Microsoft Graph API.

### What is Microsoft Graph API?

**Microsoft Graph** is the unified REST API for accessing Microsoft 365 data and services. It enables agents to interact with SharePoint, Outlook, Calendar, Teams, and more.

**Unified Access:**
```
One API → All M365 Services
```

### Task 1: Run Exercise 3

1. **Select option 3** from the menu: "Exercise 3: Microsoft 365 (Graph API) Integration"

### Task 2: Understand Graph API architecture

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

### Task 3: Common integrations

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

### Task 4: Authentication flow

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

### Task 5: Implementation pattern

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

### Task 6: Benefits and considerations

**✅ Benefits:**
- Unified API for all M365 services
- Strong authentication and security
- Respects user permissions (no elevation)
- Rich data access across services
- Webhooks for real-time events
- Well-documented with SDKs

**⚠️ Considerations:**
- Requires proper permission scopes
- Rate limiting (throttling)
- Token expiration and refresh
- Data privacy and compliance
- User consent requirements

---

## Exercise 4: Production Enterprise Agent Demo

In this exercise, you'll interact with a complete enterprise agent demonstrating all integration concepts.

### Task 1: Run Exercise 4

1. **Select option 4** from the menu: "Exercise 4: Production Enterprise Agent Demo"

2. The application creates an interactive enterprise assistant.

### Task 2: Try the enterprise agent

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

### Task 3: Observe agent behavior

**The agent demonstrates:**
- ✅ Natural language understanding
- ✅ Context retention across messages
- ✅ Professional, helpful tone
- ✅ Graceful handling of unknown information
- ✅ Suggestions for further help

**In production, this agent would:**
- Search actual SharePoint/documents
- Access real calendar data via Graph API
- Send emails and create tickets
- Personalize based on user profile
- Log all interactions for compliance

### Task 4: Production enhancements

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

## Exercise 5: Architecture & Deployment Guide

### Task 1: View the complete architecture

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

**📊 Monitoring:**
- Application Insights for telemetry
- Custom metrics (response time, success rate)
- Error tracking and alerting
- User feedback collection
- Cost monitoring (token usage)

**⚡ Performance:**
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

**🔧 Operations:**
- CI/CD pipelines
- Automated testing
- Blue-green deployments
- Rollback procedures
- Incident response plan

---

## Summary

Congratulations! You've completed Lab 5 and learned production deployment patterns for AI agents.

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

- ✅ **Security**: Auth, permissions, encryption
- ✅ **Compliance**: Data residency, audit logs, policies
- ✅ **Performance**: Caching, scaling, optimization
- ✅ **Monitoring**: Telemetry, alerts, dashboards
- ✅ **Testing**: Unit, integration, load, security tests
- ✅ **Documentation**: User guides, admin docs, runbooks
- ✅ **Training**: User training, admin training
- ✅ **Support**: Help desk, escalation procedures

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
