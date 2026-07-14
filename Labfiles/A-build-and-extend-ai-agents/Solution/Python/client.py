import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from trailhead_ui import run_chat_app, AgentReply

# Add references
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

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
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    # Initialize the session and list the available tools
    await session.initialize()
    tools = (await session.list_tools()).tools
    print("Connected to server with tools:", [tool.name for tool in tools])

    # Build a function for each MCP tool
    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result

        tool_func.__name__ = tool_name
        return tool_func

    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}

    # Create FunctionTool definitions for the MCP tools
    mcp_function_tools = []
    for tool in tools:
        function_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            parameters={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            strict=True,
        )
        mcp_function_tools.append(function_tool)

    # Create the capstone agent with BOTH tool sets: trip planning + warehouse tools
    agent = project_client.agents.create_version(
        agent_name="trailhead-assistant",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""
            You are the Trailhead Adventure Works assistant. You help customers plan guided
            trips and price gear rentals, and you help warehouse staff check live stock and sales.

            Trip planning and rentals:
            - Use the trip and rental tools to find guided trips, price gear, and produce booking reports.

            Warehouse inventory:
            - Recommend restock if item inventory < 10 and weekly sales > 15
            - Recommend clearance if item inventory > 20 and weekly sales < 5
            """,
            tools=[*trip_planner_tools, *mcp_function_tools],
        ),
    )

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

    # Process function calls — route each one to the right place
    for item in response.output:
        if item.type == "function_call":
            kwargs = json.loads(item.arguments)

            if item.name in local_functions:
                # Task 4 trip-planner tool — a plain Python function that returns a string
                output_text = local_functions[item.name](**kwargs)
            else:
                # Task 5 warehouse tool — call it over the MCP session (async)
                result = await functions_dict[item.name](**kwargs)
                output_text = result.content[0].text

            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=output_text,
                )
            )

    # Send function call outputs back to the model and retrieve a response
    if input_list:
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)


if __name__ == "__main__":
    try:
        run_chat_app(
            respond,
            title="Trailhead Adventure Works Assistant",
            subtitle="Plan trips, price gear, and check warehouse stock",
        )
    finally:
        # Delete the agent when the app closes
        if agent is not None:
            print("Cleaning up agents:")
            project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted Trailhead assistant.")
