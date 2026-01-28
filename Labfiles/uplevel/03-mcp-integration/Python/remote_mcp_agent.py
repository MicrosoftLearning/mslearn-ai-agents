import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPServerTool, ListSortOrder

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
    
    # Configure remote MCP server
    mcp_tool = MCPServerTool(
        server_url="https://learn.microsoft.com/api/mcp",
        server_label="mslearn"
    )
    
    print(f"Configured MCP server: {mcp_tool.server_label}")
    print(f"Server URL: {mcp_tool.server_url}\n")
    
    # Create agent with MCP tool
    agent = agents_client.create_agent(
        model=model_deployment,
        name="docs-research-agent",
        instructions="""You are a developer documentation assistant.
        You help developers find accurate information from Microsoft Learn documentation.
        
        Use the Microsoft Learn MCP tools to search and retrieve documentation.
        Always provide specific, accurate answers based on official documentation.
        Include relevant links when available.""",
        tools=[mcp_tool]
    )
    
    print(f"Created agent: {agent.name} (ID: {agent.id})")
    
    # Create thread for conversation
    thread = agents_client.create_thread()
    print(f"Created conversation thread (ID: {thread.id})\n")
    
    # Create a message with a documentation query
    user_query = "How do I deploy an Azure AI agent to production? What are the best practices?"
    
    print(f"USER: {user_query}\n")
    
    message = agents_client.create_message(
        thread_id=thread.id,
        role="user",
        content=user_query
    )
    
    # Run the agent with automatic tool approval
    print("Running agent with MCP tools...\n")
    
    run = agents_client.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id
    )
    
    # Check run status
    print(f"Run completed with status: {run.status}")
    
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
    else:
        # Display run steps to see tool calls
        run_steps = agents_client.run_steps.list(
            thread_id=thread.id,
            run_id=run.id
        )
        
        print("\n=== Agent Execution Steps ===\n")
        for step in run_steps:
            print(f"Step {step.id}: {step.status}")
            
            step_details = step.get("step_details", {})
            tool_calls = step_details.get("tool_calls", [])
            
            if tool_calls:
                print("  MCP Tool Calls:")
                for call in tool_calls:
                    print(f"    - {call.get('type')}: {call.get('name', 'N/A')}")
                    print(f"      Call ID: {call.get('id')}")
            print()
        
        # Fetch and display messages
        messages = agents_client.messages.list(
            thread_id=thread.id,
            order=ListSortOrder.ASCENDING
        )
        
        print("\n=== Conversation ===\n")
        print("-" * 60)
        for msg in messages:
            if msg.text_messages:
                last_text = msg.text_messages[-1]
                print(f"{msg.role.upper()}: {last_text.text.value}")
                print("-" * 60)
    
    # Cleanup
    agents_client.delete_agent(agent.id)
    print("\nAgent deleted. Exercise complete!")
