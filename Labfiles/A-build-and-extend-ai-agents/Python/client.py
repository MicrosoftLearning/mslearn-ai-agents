import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from tailwind_ui import run_chat_app, AgentReply

# Add references


# The trip-planner functions you built in Task 4, reused here so the capstone agent can
# both plan trips (local functions) AND check the warehouse (your MCP server tools).
from functions import next_available_trip, calculate_rental_cost, generate_booking_report

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client (kept open for the app's lifetime)
credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
openai_client = project_client.get_openai_client()

# --- Trip-planner tools (from Task 4), provided here so you can focus on the combination ---
# The tool schemas the model sees...
trip_planner_tools = [
    FunctionTool(
        name="next_available_trip",
        description="Get the next available guided trip in a given region.",
        parameters={
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')",
                },
            },
            "required": ["region"],
            "additionalProperties": False,
        },
        strict=True,
    ),
    FunctionTool(
        name="calculate_rental_cost",
        description="Calculate the cost of a gear rental based on the gear tier, number of days, and service level.",
        parameters={
            "type": "object",
            "properties": {
                "gear_tier": {"type": "string", "description": "the tier of the gear rental (e.g. 'standard', 'advanced', 'premium')"},
                "days": {"type": "number", "description": "the number of days for the gear rental"},
                "service_level": {"type": "string", "description": "the service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')"},
            },
            "required": ["gear_tier", "days", "service_level"],
            "additionalProperties": False,
        },
        strict=True,
    ),
    FunctionTool(
        name="generate_booking_report",
        description="Generate a report summarizing a guided trip booking and gear rental.",
        parameters={
            "type": "object",
            "properties": {
                "trip_name": {"type": "string", "description": "the name of the guided trip being booked"},
                "region": {"type": "string", "description": "the region of the guided trip"},
                "gear_tier": {"type": "string", "description": "the tier of the gear rented for the trip (e.g. 'standard', 'advanced', 'premium')"},
                "days": {"type": "number", "description": "the number of days the gear was rented"},
                "service_level": {"type": "string", "description": "the service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')"},
                "customer_name": {"type": "string", "description": "the name of the customer making the booking"},
            },
            "required": ["trip_name", "region", "gear_tier", "days", "service_level", "customer_name"],
            "additionalProperties": False,
        },
        strict=True,
    ),
]

# ...and how to actually run each one (these are plain synchronous Python functions).
local_functions = {
    "next_available_trip": next_available_trip,
    "calculate_rental_cost": calculate_rental_cost,
    "generate_booking_report": generate_booking_report,
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


    # Create the capstone agent with BOTH tool sets: trip_planner_tools + your MCP tools


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
            title="Tailwind Traders Assistant",
            subtitle="Plan trips, price gear, and check warehouse stock",
        )
    finally:
        # Delete the agent when the app closes
        if agent is not None:
            print("Cleaning up agents:")
            project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted Tailwind assistant.")
