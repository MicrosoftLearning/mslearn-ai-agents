import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPServerTool
import json

def main():
    # Initialize the project client
    project_connection_string = os.environ.get("PROJECT_CONNECTION_STRING")
    
    if not project_connection_string:
        print("Error: PROJECT_CONNECTION_STRING environment variable not set")
        print("Please set it in your .env file or environment")
        return
    
    print("Connecting to Microsoft Foundry project...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=project_connection_string,
        credential=credential
    )
    
    # Configure MCP server connection
    mcp_tool = MCPServerTool(
        name="it-support-mcp-server",
        command="python",
        args=["mcp_server.py"]
    )
    
    # Create agent with MCP tools
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="it-support-agent-mcp",
        instructions="""You are an IT Support Agent for Contoso Corporation.
        You help employees with technical issues and global office information.
        
        You have access to MCP tools that provide:
        - Current time in different timezones
        - Office hours and contact information for global offices
        
        Use these tools to help employees contact the right office or schedule support.""",
        tools=[mcp_tool]
    )
    
    print(f"Agent created with MCP integration!")
    print(f"Agent ID: {agent.id}")
    
    # Create a thread for conversation
    thread = project_client.agents.create_thread()
    print(f"Thread ID: {thread.id}\n")
    
    # Chat loop
    print("="*60)
    print("IT Support Agent with MCP Ready!")
    print("Ask about office hours or timezone information.")
    print("Type 'exit' to quit.")
    print("="*60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        # Run the agent
        run = project_client.agents.create_run(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        # Wait for completion
        while run.status in ["queued", "in_progress"]:
            run = project_client.agents.get_run(
                thread_id=thread.id,
                run_id=run.id
            )
            import time
            time.sleep(1)
        
        # Get the response
        messages = project_client.agents.list_messages(thread_id=thread.id)
        
        # Display the latest assistant message
        for message in messages:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, 'text'):
                        print(f"\nAgent: {content.text.value}\n")
                break

if __name__ == "__main__":
    main()
