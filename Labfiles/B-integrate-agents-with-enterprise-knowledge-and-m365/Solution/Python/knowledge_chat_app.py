"""
Caldova Staff Knowledge Assistant - web chat variant (provided complete).

This is an optional, friendlier version of knowledge_agent.py. Instead of a console
loop, it serves the same Foundry IQ enterprise-knowledge agent through the shared
Caldova web chat window (caldova_ui.py).

To keep the browser experience smooth, this variant AUTO-APPROVES the Foundry IQ
knowledge tool when the agent asks for approval. The console client
(knowledge_agent.py) shows the interactive yes/no approval flow instead.
"""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from caldova_ui import run_chat_app

# Load environment variables
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME")

if not project_endpoint or not agent_name:
    raise ValueError("PROJECT_ENDPOINT and AGENT_NAME must be set in .env file")

# Connect to the project and agent
credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_managed_identity_credential=True
)
project_client = AIProjectClient(
    credential=credential,
    endpoint=project_endpoint
)
openai_client = project_client.get_openai_client()
agent = project_client.agents.get(agent_name=agent_name)

# One shared conversation for the browser session
conversation = openai_client.conversations.create(items=[])


def respond(user_message):
    """Route a chat message to the Foundry IQ agent and return the reply text."""
    # Add the user's message to the conversation
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )

    # Ask the agent to respond
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input=""
    )

    # Auto-approve any Foundry IQ knowledge-tool approval request
    approval_request = None
    if getattr(response, "output", None):
        for item in response.output:
            if getattr(item, "type", None) == "mcp_approval_request":
                approval_request = item
                break

    if approval_request:
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{
                "type": "mcp_approval_response",
                "approval_request_id": approval_request.id,
                "approve": True,
            }],
        )
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            input=""
        )

    return response.output_text or "No response received."


if __name__ == "__main__":
    run_chat_app(
        respond,
        title="Caldova Staff Knowledge Assistant",
        subtitle="Grounded on plant capacity, CMO directory, tech transfer, and supplier docs.",
        placeholder="Ask about capacity, contract manufacturers, or suppliers...",
    )
