import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPTool

# Load environment variables
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1")

if not project_endpoint:
    print("Error: PROJECT_ENDPOINT not set in .env file")
    exit(1)

print("Connecting to Microsoft Foundry project...")
credential = DefaultAzureCredential()

# Create the project client with new pattern
project_client = AIProjectClient(
    credential=credential,
    endpoint=project_endpoint
)

# Get OpenAI client for Responses API
openai_client = project_client.get_openai_client()

# Configure local MCP server (stdio connection)
mcp_tool = MCPTool(
    name="business-tools-mcp-server",
    command="python",
    args=["mcp_server.py"]
)

print(f"Configured local MCP server: business-tools-mcp-server\n")

# Create agent with local MCP tools using Responses API
agent = openai_client.agents.create_version(
    agent_name="business-operations-agent",
    definition={
        "kind": "prompt",
        "model": model_deployment,
        "instructions": """You are a business operations assistant for Contoso Corporation.
        You help with inventory management and provide global office information.
        
        You have access to tools that can:
        - Check inventory levels for products
        - Provide restock recommendations
        - Get current time in any timezone
        - Retrieve office hours and contact information
        
        Use these tools to help with operational queries.
        Be specific and actionable in your recommendations.""",
        "tools": [{"type": "mcp", **mcp_tool.as_dict()}]
    }
)

print(f"Created agent: {agent.name} (version {agent.version})\n")

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
    
    # Create conversation
    conversation = openai_client.conversations.create(
        items=[{"type": "message", "role": "user", "content": query}]
    )
    
    print("Processing...\n")
    
    # Get response
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={
            "agent": {
                "type": "agent_reference",
                "name": agent.name,
                "version": agent.version
            }
        }
    )
    
    # Display response
    if response.output:
        for item in response.output:
            if item.type == "message" and item.content:
                for content_item in item.content:
                    if content_item.type == "text":
                        print(f"AGENT: {content_item.text}\n")
    
    print("-" * 70)

# Cleanup
openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
print("\n✅ All tests complete! Agent deleted.")
