import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import CodeInterpreterTool

def main():
    # Initialize the project client
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    if not project_endpoint:
        print("Error: PROJECT_ENDPOINT environment variable not set")
        print("Please set it in your .env file")
        return
    
    print("Connecting to Azure AI Foundry project...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=project_endpoint,
        credential=credential
    )
    
    print("Creating Sales Analytics Agent with code interpreter...")
    
    # Create agent with code interpreter tool
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="sales-analytics-agent",
        instructions="""You are a Sales Analytics Agent for Contoso Corporation.
        You help sales teams analyze data, generate insights, and create visualizations.
        
        When analyzing data:
        - Always examine the data structure first
        - Provide clear explanations of your findings
        - Create visualizations when appropriate
        - Highlight key trends and anomalies
        - Suggest actionable recommendations
        
        You have access to Python code interpreter for data analysis.""",
        tools=[CodeInterpreterTool()]
    )
    
    print(f"✅ Agent created with ID: {agent.id}")
    
    # Create a thread for conversation
    thread = project_client.agents.create_thread()
    print(f"✅ Thread created with ID: {thread.id}\n")
    
    # Interactive chat loop
    print("="*70)
    print("Sales Analytics Agent Ready!")
    print("Upload data files and ask analysis questions.")
    print("Type 'exit' to quit.")
    print("="*70 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nThank you for using Sales Analytics Agent!")
            break
        
        if not user_input:
            continue
        
        # Add user message to thread
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        # Run the agent
        print("\n🔄 Analyzing...")
        run = project_client.agents.create_run(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        # Wait for completion
        import time
        while run.status in ["queued", "in_progress"]:
            time.sleep(1)
            run = project_client.agents.get_run(
                thread_id=thread.id,
                run_id=run.id
            )
        
        # Check for errors
        if run.status == "failed":
            print(f"❌ Error: {run.last_error}")
            continue
        
        # Get the response
        messages = project_client.agents.list_messages(thread_id=thread.id)
        
        # Display the latest assistant message
        for message in messages:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, 'text'):
                        print(f"\nAgent: {content.text.value}\n")
                    # Display images if generated
                    elif hasattr(content, 'image_file'):
                        print(f"📊 Chart generated: {content.image_file.file_id}")
                break

if __name__ == "__main__":
    main()
