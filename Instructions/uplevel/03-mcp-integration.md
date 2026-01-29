---
lab:
    title: 'Extend Agents with Model Context Protocol (MCP)'
    module: 'Module 3: Advanced Agent Integration'
---

# Lab 3: Extend Agents with Model Context Protocol (MCP)

## Lab scenario

You've learned how to create AI agents with custom functions. Now you'll discover how to dramatically extend agent capabilities using the Model Context Protocol (MCP). MCP enables agents to connect to external servers that provide specialized tools, allowing you to integrate with documentation systems, databases, APIs, and custom business logic without writing individual function wrappers for each tool.

In this lab, you'll build two types of MCP integrations: first, connecting to a remote cloud-hosted MCP server to query Microsoft Learn documentation, and second, creating your own local MCP server with custom business tools. This approach allows you to leverage both public MCP servers and build private, specialized tools for your organization.

## Lab objectives

In this lab, you will complete the following exercises:

- **Exercise 1**: Connect to a remote MCP server (Microsoft Learn Docs)
- **Exercise 2**: Build a custom local MCP server with business tools
- **Exercise 3**: Implement advanced MCP patterns and best practices

After completing this lab, you'll be able to:

- Connect AI agents to remote MCP servers
- Create custom local MCP servers with specialized tools
- Implement tool discovery and dynamic function calling
- Handle MCP authentication and error scenarios
- Apply MCP best practices for production applications

## Lab duration

- **Estimated Time**: 60 minutes

## Prerequisites

Before starting this lab, ensure you have:

- Completed Lab 1 (you'll reuse the same Microsoft Foundry project)
- Python 3.10 or higher installed
- Visual Studio Code with Microsoft Foundry extension
- Azure CLI installed and configured
- Active Azure subscription with Foundry access

## Architecture

This lab demonstrates two MCP integration patterns:

```
┌─────────────────────────────────────────┐
│         Your AI Agent                   │
│   (Microsoft Foundry Project)            │
└────────┬─────────────────┬──────────────┘
         │                  │
         │ Exercise 1       │ Exercise 2
         │ (Remote MCP)     │ (Local MCP)
         │                  │
┌────────▼────────────┐  ┌──▼──────────────────┐
│  Microsoft Learn    │  │  Custom MCP Server  │
│  Docs MCP Server    │  │  (Local stdio)      │
│  (HTTPS)            │  │                     │
│                     │  │  • Inventory tools  │
│  • Search docs      │  │  • Office info      │
│  • Get content      │  │  • Timezone tools   │
└─────────────────────┘  └─────────────────────┘
```

---

## Exercise 1: Connect to a remote MCP server

In this exercise, you'll connect your agent to Microsoft's Learn documentation MCP server. This public server provides AI-powered search capabilities across official Microsoft documentation, making it perfect for building developer support agents.

### Task 1: Set up the project

1. **Open VS Code** and ensure the **Microsoft Foundry** extension is installed and signed in.

2. **Navigate to the lab directory**:
   - Open a terminal in VS Code
   - Navigate to `C:\repos\mslearn-ai-agents\Labfiles\uplevel\03-mcp-integration\Python`

3. **Install dependencies**:

    ```powershell
    pip install -r requirements.txt
    ```

    This will install the required packages:
    - `azure-ai-projects` - Microsoft Foundry SDK
    - `azure-identity` - Azure authentication
    - `mcp` - Model Context Protocol SDK
    - `python-dotenv` - Environment variable management
    - `pytz` - Timezone support

4. **Configure environment file**:
   - In the lab folder, locate the provided `.env` file
   - Open the `.env` file and replace `your_project_endpoint_here` with your actual project endpoint
   - **To get your project endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project (created in Lab 1), and select **Copy Endpoint**

    The `.env` file should contain:
    ```
    PROJECT_ENDPOINT=<paste_your_endpoint_here>
    MODEL_DEPLOYMENT_NAME=gpt-4.1
    ```

### Task 2: Run the unified MCP lab application

Instead of creating multiple separate files, you'll use a single interactive application that guides you through all MCP concepts.

1. **Create `mcp_lab.py`** - The main lab application:

   > **Note**: This file is provided in the lab files. If you need to create it, the complete code is available in the lab repository.

2. **Run the application**:

    ```powershell
    python mcp_lab.py
    ```

3. **Select Exercise 1** from the menu to explore remote MCP.

The application provides a menu-driven interface for all exercises. Here's what happens when you run Exercise 1:

    ```python
    # The agent connects to the remote MCP server
    # Discovers available tools automatically
    # Queries Microsoft Learn documentation
    # Returns accurate, sourced information
    ```

### Task 3: Explore the results

The application will show you:
- MCP server connection details
- Sample queries being processed
- Tool calls made to the remote MCP server  
- Responses with documentation excerpts

**Key observations**:
- Agent automatically discovers MCP tools
- No manual function definitions needed
- Real-time documentation queries
- Sources are official Microsoft Learn content

Try modifying the queries in the code to explore different documentation topics!

### Key concepts

**Remote MCP servers** provide:
- **Zero infrastructure**: No need to host or maintain servers
- **Automatic updates**: Documentation stays current
- **Specialized tools**: Purpose-built for specific domains
- **HTTPS connectivity**: Secure, authenticated access

---

## Exercise 2: Build a custom local MCP server

While remote MCP servers are convenient, many scenarios require custom tools that access private data or implement proprietary business logic. In this exercise, you'll use a pre-built local MCP server and connect your agent to it.

### Task 1: Understand the MCP server

The `mcp_server.py` file (provided in lab files) implements 4 custom business tools:

1. **check_inventory** - Check product stock levels
2. **get_restock_recommendations** - Identify low-stock items
3. **get_time_in_timezone** - Get current time anywhere
4. **get_office_hours** - Retrieve office contact information

The server uses **stdio** (standard input/output) for local communication with your agent.

### Task 2: Run Exercise 2 from the unified application

1. **Ensure `mcp_server.py` is in your directory**:

    ```powershell
    ls mcp_server.py
    ```

2. **Run the main application** (if not already running):

    ```powershell
    python mcp_lab.py
    ```

3. **Select Exercise 2** from the menu.

### Task 3: Observe the local MCP integration

The application will automatically:
- Start the local MCP server as a background process
- Connect your agent to it via stdio
- Discover the 4 available tools
- Test each tool with sample queries

**Sample interactions you'll see**:
- Inventory check for specific products
- Restock recommendations (shows low-stock items)
- Timezone queries (Tokyo, London, etc.)
- Office contact information

**Key observations**:
- Local MCP server runs as subprocess
- Agent discovers tools automatically
- Tools access private business data
- Fast stdio communication

Try modifying the inventory data in `mcp_server.py` to see how the agent adapts!

### Key concepts

**Local MCP servers** provide:
- **Custom business logic**: Implement proprietary tools
- **Private data access**: Connect to internal databases
- **Stdio communication**: Fast, local process communication
- **Dynamic tool discovery**: Agent automatically learns available tools
- **Full control**: You manage the server lifecycle

---

## Exercise 3: Advanced MCP patterns

Now that you've connected to both remote and local MCP servers, let's explore advanced patterns for production use.

### Task 1: Interactive MCP agent

Create an interactive agent that lets users ask questions and automatically routes to the appropriate MCP tools.

1. **Create `interactive_mcp_agent.py`**:

    ```python
    import os
    import time
    from dotenv import load_dotenv
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects.models import MCPServerTool
    
    # Load environment variables
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
    
    if not project_endpoint:
        print("Error: PROJECT_ENDPOINT not set in .env file")
        exit(1)
    
    print("Connecting to Microsoft Foundry project...")
    credential = DefaultAzureCredential()
    
    # Create the project client
    with AIProjectClient.from_connection_string(
        conn_str=project_endpoint,
        credential=credential
    ) as agents_client:
        
        # Configure both remote and local MCP tools
        remote_mcp = MCPServerTool(
            server_url="https://learn.microsoft.com/api/mcp",
            server_label="mslearn"
        )
        
        local_mcp = MCPServerTool(
            name="business-tools-mcp-server",
            command="python",
            args=["mcp_server.py"]
        )
        
        # Create hybrid agent with both MCP servers
        agent = agents_client.create_agent(
            model=model_deployment,
            name="hybrid-assistant",
            instructions="""You are a comprehensive assistant for Contoso Corporation.
            
            You have access to two sets of tools:
            1. Microsoft Learn documentation (for technical questions)
            2. Business operations tools (inventory, office information)
            
            Choose the appropriate tools based on the user's question:
            - Use Microsoft Learn tools for Azure, development, or technical questions
            - Use business tools for inventory, office hours, or operational questions
            
            Always be helpful and provide accurate, actionable information.""",
            tools=[remote_mcp, local_mcp]
        )
        
        print(f"✅ Created hybrid agent: {agent.name}")
        print(f"   • Remote MCP: Microsoft Learn Documentation")
        print(f"   • Local MCP: Business Operations Tools\n")
        
        # Create thread
        thread = agents_client.create_thread()
        
        print("=" * 70)
        print("INTERACTIVE MCP AGENT")
        print("Ask technical questions or business operations questions.")
        print("Type 'quit' to exit.")
        print("=" * 70 + "\n")
        
        while True:
            # Get user input
            user_input = input("YOU: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            # Create message
            message = agents_client.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run agent
            print("\nProcessing...\n")
            run = agents_client.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            # Wait for completion
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = agents_client.runs.get(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            # Display response
            messages = agents_client.messages.list(thread_id=thread.id)
            
            for msg in messages:
                if msg.role == "assistant":
                    if msg.text_messages:
                        response = msg.text_messages[-1].text.value
                        print(f"AGENT: {response}\n")
                    break
            
            print("-" * 70 + "\n")
        
        # Cleanup
        agents_client.delete_agent(agent.id)
        print("Agent deleted.")
    ```

2. **Run the interactive agent**:

    ```powershell
    python interactive_mcp_agent.py
    ```

3. **Try different question types**:
   - Technical: "How do I implement semantic caching in Azure AI?"
   - Business: "Show me inventory recommendations"
   - Mixed: "What time is it in our Tokyo office, and do they have any technical docs on Azure Functions?"

### Task 2: MCP error handling and best practices

Create a robust MCP agent with comprehensive error handling.

1. **Create `robust_mcp_agent.py`**:

    ```python
    import os
    import time
    from dotenv import load_dotenv
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects.models import MCPServerTool
    
    load_dotenv()
    
    def create_mcp_agent_with_error_handling():
        """Create an MCP agent with comprehensive error handling."""
        
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")
        
        if not project_endpoint:
            raise ValueError("PROJECT_ENDPOINT not set in .env file")
        
        try:
            print("Initializing Microsoft Foundry client...")
            credential = DefaultAzureCredential()
            
            agents_client = AIProjectClient.from_connection_string(
                conn_str=project_endpoint,
                credential=credential
            )
            
            print("✅ Connected to Microsoft Foundry")
            
            # Configure MCP with validation
            try:
                mcp_tool = MCPServerTool(
                    name="business-tools-mcp-server",
                    command="python",
                    args=["mcp_server.py"]
                )
                print("✅ Configured local MCP server")
            except Exception as e:
                print(f"❌ Failed to configure MCP server: {e}")
                raise
            
            # Create agent with error handling instructions
            try:
                agent = agents_client.create_agent(
                    model=model_deployment,
                    name="robust-mcp-agent",
                    instructions="""You are a reliable business operations assistant.
                    
                    Error Handling Guidelines:
                    - If a tool fails, acknowledge the error and suggest alternatives
                    - If data is unavailable, provide general guidance
                    - Always maintain a helpful tone even when errors occur
                    - Suggest manual steps when automated tools fail
                    
                    Use your tools to help with operational queries, but gracefully
                    handle any issues that arise.""",
                    tools=[mcp_tool]
                )
                print(f"✅ Created agent: {agent.name} (ID: {agent.id})")
                return agents_client, agent
                
            except Exception as e:
                print(f"❌ Failed to create agent: {e}")
                raise
                
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            raise
    
    def query_agent_safely(agents_client, agent, thread, query, max_retries=3):
        """Query agent with retry logic and error handling."""
        
        for attempt in range(max_retries):
            try:
                # Create message
                message = agents_client.create_message(
                    thread_id=thread.id,
                    role="user",
                    content=query
                )
                
                # Run agent
                print(f"Attempt {attempt + 1}: Running agent...")
                run = agents_client.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=agent.id
                )
                
                # Wait for completion with timeout
                timeout = 30  # seconds
                elapsed = 0
                
                while run.status in ["queued", "in_progress"] and elapsed < timeout:
                    time.sleep(1)
                    elapsed += 1
                    run = agents_client.runs.get(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                
                # Check status
                if run.status == "completed":
                    messages = agents_client.messages.list(thread_id=thread.id)
                    
                    for msg in messages:
                        if msg.role == "assistant":
                            if msg.text_messages:
                                return msg.text_messages[-1].text.value
                    
                    return "No response generated"
                
                elif run.status == "failed":
                    print(f"⚠️  Run failed: {run.last_error}")
                    if attempt < max_retries - 1:
                        print(f"   Retrying... ({attempt + 2}/{max_retries})")
                        continue
                    else:
                        return f"Agent failed after {max_retries} attempts: {run.last_error}"
                
                elif elapsed >= timeout:
                    print("⚠️  Request timed out")
                    return "Request timed out. Please try again with a simpler query."
                
            except Exception as e:
                print(f"⚠️  Error during query: {e}")
                if attempt < max_retries - 1:
                    print(f"   Retrying... ({attempt + 2}/{max_retries})")
                    continue
                else:
                    return f"Query failed after {max_retries} attempts: {str(e)}"
        
        return "Maximum retries exceeded"
    
    def main():
        """Main execution with comprehensive error handling."""
        
        try:
            # Initialize
            agents_client, agent = create_mcp_agent_with_error_handling()
            
            # Create thread
            thread = agents_client.create_thread()
            print(f"✅ Created conversation thread\n")
            
            # Test queries with error handling
            test_queries = [
                "Check inventory for laptop-dell-5000",
                "What products need restocking?",
                "Check inventory for invalid-product-xyz",  # Will trigger error handling
                "Get office info for the Paris office"      # Will trigger error handling
            ]
            
            print("=" * 70)
            print("ROBUST MCP AGENT WITH ERROR HANDLING")
            print("=" * 70 + "\n")
            
            for query in test_queries:
                print(f"USER: {query}\n")
                
                response = query_agent_safely(
                    agents_client,
                    agent,
                    thread,
                    query
                )
                
                print(f"AGENT: {response}\n")
                print("-" * 70 + "\n")
            
            # Cleanup
            agents_client.delete_agent(agent.id)
            print("✅ Agent deleted. Exercise complete!")
            
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            print("Please check your configuration and try again.")
    
    if __name__ == "__main__":
        main()
    ```

2. **Run the robust agent**:

    ```powershell
    python robust_mcp_agent.py
    ```

3. **Observe error handling**:
   - Invalid product queries are handled gracefully
   - Network timeouts trigger retries
   - Agent provides helpful feedback even when tools fail

### Best practices summary

**MCP Production Checklist**:

1. **Error Handling**
   - ✅ Implement retry logic for transient failures
   - ✅ Validate tool inputs before calling
   - ✅ Provide graceful degradation when tools fail
   - ✅ Log errors for debugging

2. **Performance**
   - ✅ Set appropriate timeouts
   - ✅ Cache MCP tool discoveries
   - ✅ Use async patterns for concurrent tool calls
   - ✅ Monitor MCP server health

3. **Security**
   - ✅ Authenticate MCP connections
   - ✅ Validate all tool parameters
   - ✅ Limit tool execution scope
   - ✅ Audit tool usage

4. **Testing**
   - ✅ Test with valid and invalid inputs
   - ✅ Simulate server failures
   - ✅ Verify error messages
   - ✅ Load test with multiple concurrent requests

---

## Summary

Congratulations! You've completed Lab 3 and learned how to extend AI agents with the Model Context Protocol.

### What you've learned

- **Remote MCP Integration**: Connected to cloud-hosted MCP servers (Microsoft Learn Docs)
- **Custom Local MCP Servers**: Built specialized business tools with MCP
- **Tool Discovery**: Enabled agents to dynamically discover and use MCP tools
- **Hybrid Architectures**: Combined remote and local MCP servers in one agent
- **Production Patterns**: Implemented error handling, retries, and best practices

### Key takeaways

1. **MCP Extends Capabilities**: Dramatically expand agent functionality without writing individual function wrappers
2. **Remote + Local Pattern**: Combine public MCP servers with private tools for powerful hybrid solutions
3. **Dynamic Discovery**: Agents automatically learn available tools from MCP servers
4. **Production Ready**: Proper error handling and monitoring are essential for reliable MCP integrations

### Architecture patterns

You've learned three MCP integration patterns:

1. **Remote only**: Connect to public MCP servers (Exercise 1)
2. **Local only**: Build custom MCP servers (Exercise 2)
3. **Hybrid**: Combine remote and local MCP tools (Exercise 3)

### Next steps

In **Lab 4: Multi-Agent Orchestration**, you'll learn how to coordinate multiple specialized agents using local coordination, distributed A2A protocol, and visual workflow designers.

**Continue to**: [Lab 4 - Multi-Agent Orchestration](./04-multi-agent-orchestration.md)

---

## Clean up

To avoid incurring charges:

1. All agents created in this lab were automatically deleted
2. Your Microsoft Foundry project remains for use in subsequent labs
3. No additional cleanup required

## Additional resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Microsoft Foundry MCP Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/model-context-protocol)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Public MCP Servers Directory](https://modelcontextprotocol.io/servers)
