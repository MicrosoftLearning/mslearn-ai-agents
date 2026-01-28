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
    
    # Configure local MCP server (stdio connection)
    mcp_tool = MCPServerTool(
        name="business-tools-mcp-server",
        command="python",
        args=["mcp_server.py"]
    )
    
    print(f"Configured local MCP server: {mcp_tool.name}\n")
    
    # Create agent with local MCP tools
    agent = agents_client.create_agent(
        model=model_deployment,
        name="business-operations-agent",
        instructions="""You are a business operations assistant for Contoso Corporation.
        You help with inventory management and provide global office information.
        
        You have access to tools that can:
        - Check inventory levels for products
        - Provide restock recommendations
        - Get current time in any timezone
        - Retrieve office hours and contact information
        
        Use these tools to help with operational queries.
        Be specific and actionable in your recommendations.""",
        tools=[mcp_tool]
    )
    
    print(f"Created agent: {agent.name} (ID: {agent.id})")
    
    # Create thread
    thread = agents_client.create_thread()
    print(f"Created conversation thread (ID: {thread.id})\n")
    
    # Test queries
    test_queries = [
        "What's the current inventory status for laptop-dell-5000?",
        "Which products need restocking?",
        "What time is it in Tokyo right now? Are they in business hours?",
        "Give me contact information for the London office"
    ]
    
    print("=" * 70)
    print("TESTING LOCAL MCP TOOLS")
    print("=" * 70 + "\n")
    
    for query in test_queries:
        print(f"\nUSER: {query}\n")
        
        # Create message
        message = agents_client.create_message(
            thread_id=thread.id,
            role="user",
            content=query
        )
        
        # Run agent
        print("Processing...\n")
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
        
        # Get latest assistant message
        messages = agents_client.messages.list(thread_id=thread.id)
        
        for msg in messages:
            if msg.role == "assistant":
                if msg.text_messages:
                    response = msg.text_messages[-1].text.value
                    print(f"AGENT: {response}\n")
                break
        
        print("-" * 70)
    
    # Cleanup
    agents_client.delete_agent(agent.id)
    print("\n✅ All tests complete! Agent deleted.")
