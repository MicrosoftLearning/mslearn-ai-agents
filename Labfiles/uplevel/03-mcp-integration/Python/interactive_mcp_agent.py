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
