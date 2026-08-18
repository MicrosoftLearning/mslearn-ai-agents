import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from caldova_ui import run_chat_app, AgentReply

# Add references


# The capacity-planner functions you built in Task 4, reused here so the capstone agent can
# both plan capacity (local functions) AND check materials (your MCP server tools).
from functions import next_available_slot, calculate_transfer_cost, generate_capacity_report

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client (kept open for the app's lifetime)
credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
openai_client = project_client.get_openai_client()

# --- Capacity-planner tools (from Task 4), provided here so you can focus on the combination ---
# The tool schemas the model sees...
capacity_planner_tools = [
    FunctionTool(
        name="next_available_slot",
        description="Get the next open production slot at a given site.",
        parameters={
            "type": "object",
            "properties": {
                "site": {
                    "type": "string",
                    "description": "site to find the next open production slot at (e.g. 'ashford', 'brightwater', 'calderwood')",
                },
            },
            "required": ["site"],
            "additionalProperties": False,
        },
        strict=True,
    ),
    FunctionTool(
        name="calculate_transfer_cost",
        description="Calculate the cost of transferring production to a contract manufacturer, based on the CMO tier, number of weeks, and priority.",
        parameters={
            "type": "object",
            "properties": {
                "cmo_tier": {"type": "string", "description": "the CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')"},
                "weeks": {"type": "number", "description": "the number of weeks of contract capacity"},
                "priority": {"type": "string", "description": "the priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')"},
            },
            "required": ["cmo_tier", "weeks", "priority"],
            "additionalProperties": False,
        },
        strict=True,
    ),
    FunctionTool(
        name="generate_capacity_report",
        description="Draft a capacity request summarizing an open production slot and a contract manufacturing estimate.",
        parameters={
            "type": "object",
            "properties": {
                "slot_name": {"type": "string", "description": "the name of the production slot being requested"},
                "site": {"type": "string", "description": "the site the production slot belongs to"},
                "cmo_tier": {"type": "string", "description": "the CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')"},
                "weeks": {"type": "number", "description": "the number of weeks of contract capacity"},
                "priority": {"type": "string", "description": "the priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')"},
                "requested_by": {"type": "string", "description": "the team or role requesting the capacity"},
            },
            "required": ["slot_name", "site", "cmo_tier", "weeks", "priority", "requested_by"],
            "additionalProperties": False,
        },
        strict=True,
    ),
]

# ...and how to actually run each one (these are plain synchronous Python functions).
local_functions = {
    "next_available_slot": next_available_slot,
    "calculate_transfer_cost": calculate_transfer_cost,
    "generate_capacity_report": generate_capacity_report,
}

# Shared state, set up once on the first message so the MCP session is created
# on the same event loop the chat window uses.
exit_stack = AsyncExitStack()
session = None
agent = None
conversation = None
functions_dict = {}


async def setup():
    """Connect to the MCP server, discover its tools, and create the combined agent (runs once)."""
    global session, agent, conversation, functions_dict
    if session is not None:
        return

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None,
    )

    # Start the MCP server and create a client session


    # Initialize the session and list the available tools


    # Build a function for each MCP tool


    # Create FunctionTool definitions for the MCP tools


    # Create the capstone agent with BOTH tool sets: capacity_planner_tools + your MCP tools


    # Create a thread for the chat session
    conversation = openai_client.conversations.create()


async def respond(user_message):
    """Handle one message from the chat window and return the agent's reply."""
    await setup()

    # Send the user's prompt to the agent
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )

    # Retrieve the agent's response, which may include function calls to either tool set
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input=[],
    )

    if response.status == "failed":
        return AgentReply(text=f"Response failed: {response.error}")

    # Create an input list to hold function call outputs to send back to the model
    input_list: ResponseInputParam = []

    # Process function calls — route each one: local Python function or MCP server tool


    # Send function call outputs back to the model and retrieve a response.
    # Attach them to the same conversation so the tool calls are resolved in
    # conversation state — otherwise the next turn fails with "No tool output
    # found for function call".
    if input_list:
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=input_list,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)


if __name__ == "__main__":
    try:
        run_chat_app(
            respond,
            title="Caldova Assistant",
            subtitle="Find capacity, estimate transfers, and check material stock",
        )
    finally:
        # Delete the agent when the app closes
        if agent is not None:
            print("Cleaning up agents:")
            project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted Caldova assistant.")
