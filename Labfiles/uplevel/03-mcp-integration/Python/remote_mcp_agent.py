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

# Configure remote MCP server
mcp_tool = MCPTool(
    server_url="https://learn.microsoft.com/api/mcp",
    server_label="mslearn"
)

print(f"Configured MCP server: mslearn")
print(f"Server URL: https://learn.microsoft.com/api/mcp\n")

# Create agent using Responses API
agent = openai_client.agents.create_version(
    agent_name="docs-research-agent",
    definition={
        "kind": "prompt",
        "model": model_deployment,
        "instructions": """You are a developer documentation assistant.
        You help developers find accurate information from Microsoft Learn documentation.
        
        Use the Microsoft Learn MCP tools to search and retrieve documentation.
        Always provide specific, accurate answers based on official documentation.
        Include relevant links when available.""",
        "tools": [{"type": "mcp", **mcp_tool.as_dict()}]
    }
)

print(f"Created agent: {agent.name} (version {agent.version})\n")

# Create a conversation with user query
user_query = "How do I deploy an Azure AI agent to production? What are the best practices?"

print(f"USER: {user_query}\n")

conversation = openai_client.conversations.create(
    items=[{"type": "message", "role": "user", "content": user_query}]
)

# Get response from agent
print("Running agent with MCP tools...\n")

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
print("\n=== Agent Response ===\n")
print("-" * 60)

if response.output:
    for item in response.output:
        if item.type == "message" and item.content:
            for content_item in item.content:
                if content_item.type == "text":
                    print(f"ASSISTANT: {content_item.text}")
                    print("-" * 60)
else:
    print("No response generated")

# Cleanup
openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
print("\nAgent deleted. Exercise complete!")
