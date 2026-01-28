# Lab 3: Extend Agents with Model Context Protocol (MCP)

This lab demonstrates how to extend AI agents with the Model Context Protocol (MCP), enabling connections to both remote cloud-hosted MCP servers and custom local MCP servers.

## Prerequisites

- Completed Lab 1 (you'll reuse the same Microsoft Foundry project)
- Python 3.10 or higher
- VS Code with Microsoft Foundry extension
- Active Azure subscription

## Lab Structure

### Exercise 1: Remote MCP Integration
Connect to Microsoft Learn Docs MCP server to query official documentation.

**File**: `remote_mcp_agent.py`

### Exercise 2: Custom Local MCP Server
Build your own MCP server with business tools (inventory, office hours).

**Files**: 
- `mcp_server.py` - Custom MCP server with 4 business tools
- `local_mcp_agent.py` - Agent that connects to local MCP server

### Exercise 3: Advanced Patterns
Implement production-ready MCP patterns with error handling and hybrid architectures.

**Files**:
- `interactive_mcp_agent.py` - Interactive hybrid agent (remote + local MCP)
- `robust_mcp_agent.py` - Production-ready error handling patterns

## Setup

1. **Navigate to the lab directory**:
   ```powershell
   cd C:\repos\mslearn-ai-agents\Labfiles\uplevel\03-mcp-integration\Python
   ```

2. **Create environment file**:
   ```powershell
   cp .env.example .env
   ```

3. **Configure your project endpoint**:
   - Open `.env` in VS Code
   - In Microsoft Foundry extension, right-click your project > Copy Endpoint
   - Paste into `.env` file

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Exercises

### Exercise 1: Remote MCP
```powershell
python remote_mcp_agent.py
```

### Exercise 2: Local MCP
```powershell
python local_mcp_agent.py
```

### Exercise 3: Advanced Patterns

**Interactive hybrid agent**:
```powershell
python interactive_mcp_agent.py
```

**Robust error handling**:
```powershell
python robust_mcp_agent.py
```

## Key Concepts

### Remote MCP Servers
- **Use case**: Public data sources, documentation, external APIs
- **Connection**: HTTPS endpoints
- **Example**: Microsoft Learn Docs (`https://learn.microsoft.com/api/mcp`)

### Local MCP Servers
- **Use case**: Private data, custom business logic
- **Connection**: Stdio (local process communication)
- **Example**: Custom inventory and office information tools

### Hybrid Architecture
Combine remote and local MCP servers in a single agent for maximum capability.

## Architecture

```
┌─────────────────────────────────┐
│      Your AI Agent              │
│  (Microsoft Foundry Project)     │
└────────┬────────────┬───────────┘
         │            │
         │ Remote     │ Local
         │ MCP        │ MCP
         │            │
┌────────▼─────┐  ┌──▼──────────┐
│ MS Learn MCP │  │ Custom MCP  │
│ (HTTPS)      │  │ (stdio)     │
│              │  │             │
│ • Search     │  │ • Inventory │
│ • Docs       │  │ • Offices   │
└──────────────┘  └─────────────┘
```

## MCP Tools in This Lab

### Remote MCP Tools (Microsoft Learn)
- `search_documentation` - AI-powered doc search
- `get_article` - Retrieve full article content
- `get_code_samples` - Find code examples

### Local MCP Tools (Custom)
- `check_inventory` - Check product stock levels
- `get_restock_recommendations` - Identify low-stock items
- `get_time_in_timezone` - Get current time in any timezone
- `get_office_hours` - Retrieve office contact information

## Troubleshooting

### MCP Server Won't Start
- Verify `mcp` package is installed: `pip list | grep mcp`
- Check Python version: `python --version` (need 3.10+)
- Ensure `mcp_server.py` is in the current directory

### Connection Errors
- Verify PROJECT_ENDPOINT in `.env` file
- Ensure you're signed in to Azure: `az login`
- Check Microsoft Foundry project is active

### Tool Discovery Failures
- MCP server must be running before agent connects
- Check stdout/stderr for MCP server errors
- Verify tool schemas in `mcp_server.py`

## Production Best Practices

1. **Error Handling**: Implement retries and graceful degradation
2. **Timeouts**: Set appropriate timeouts for MCP calls
3. **Monitoring**: Log MCP tool usage and performance
4. **Security**: Validate all tool inputs, use authentication
5. **Testing**: Test with valid and invalid inputs

## Additional Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Microsoft Foundry MCP Docs](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/model-context-protocol)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Public MCP Servers](https://modelcontextprotocol.io/servers)

## Next Steps

Continue to **Lab 4: Multi-Agent Orchestration** to learn how to coordinate multiple specialized agents.
