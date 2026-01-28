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
