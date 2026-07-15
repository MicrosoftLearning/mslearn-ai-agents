"""
Task 5 capstone — Microsoft Agent Framework edition (provided complete, for comparison).

This is the same capstone as client.py — one agent that combines the Task 4
trip-planner functions with your MCP inventory server — but built with the
**Microsoft Agent Framework**. Compare the two:

  client.py (raw SDK + Responses API)               client_maf.py (this file)
  ---------------------------------------------     ----------------------------------
  Hand-wire the MCP stdio client (ClientSession,    MCPStdioTool launches server.py and
  stdio_client), list its tools, wrap each as a     exposes its tools to the agent for you.
  callable, and build FunctionTool schemas.
  Route every function_call yourself: decide        agent.run() invokes whichever tool the
  local vs MCP, await MCP calls, send outputs       model picks — local @tool or MCP — and
  back with previous_response_id.                   returns the final answer.

server.py is unchanged — you still author your own MCP server. The framework only
removes the client-side wiring and the manual routing loop.
"""

import os
from contextlib import AsyncExitStack
from typing import Annotated

from dotenv import load_dotenv

# Microsoft Agent Framework references
from agent_framework import tool, Agent, MCPStdioTool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field

# The Task 4 trip-planner logic, reused so the capstone agent can plan trips AND
# check the warehouse (the tools your MCP server hosts).
import functions
from trailhead_ui import run_chat_app, AgentReply

# Load environment variables from .env file
load_dotenv()


@tool(approval_mode="never_require")
def next_available_trip(
    region: Annotated[str, Field(description="Region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')")],
) -> str:
    """Get the next available guided trip in a given region."""
    return functions.next_available_trip(region)


@tool(approval_mode="never_require")
def calculate_rental_cost(
    gear_tier: Annotated[str, Field(description="The tier of the gear rental (e.g. 'standard', 'advanced', 'premium')")],
    days: Annotated[float, Field(description="The number of days for the gear rental")],
    service_level: Annotated[str, Field(description="The service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')")],
) -> str:
    """Calculate the cost of a gear rental based on the gear tier, number of days, and service level."""
    return functions.calculate_rental_cost(gear_tier, days, service_level)


@tool(approval_mode="never_require")
def generate_booking_report(
    trip_name: Annotated[str, Field(description="The name of the guided trip being booked")],
    region: Annotated[str, Field(description="The region of the guided trip")],
    gear_tier: Annotated[str, Field(description="The tier of the gear rented for the trip (e.g. 'standard', 'advanced', 'premium')")],
    days: Annotated[float, Field(description="The number of days the gear was rented")],
    service_level: Annotated[str, Field(description="The service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')")],
    customer_name: Annotated[str, Field(description="The name of the customer making the booking")],
) -> str:
    """Generate a report summarizing a guided trip booking and gear rental."""
    return functions.generate_booking_report(trip_name, region, gear_tier, days, service_level, customer_name)


# Created once on the first message, on the same event loop the chat window uses.
exit_stack = AsyncExitStack()
agent = None
session = None
mcp_tool = None


async def setup():
    """Connect the MCP server and create the agent + session (runs once)."""
    global agent, session, mcp_tool
    if agent is not None:
        return

    # MCPStdioTool launches your MCP server and exposes its tools to the agent —
    # no ClientSession/stdio wiring and no per-tool FunctionTool schemas. It's kept
    # open for the app's lifetime so the same connection serves every message.
    mcp_tool = await exit_stack.enter_async_context(
        MCPStdioTool(name="Inventory", command="python", args=["server.py"])
    )

    client = FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    )

    # The agent holds the local trip-planner tools; the MCP tools are supplied per run.
    agent = Agent(
        client=client,
        name="trailhead-assistant",
        instructions="""
        You are the Trailhead Adventure Works assistant. You help customers plan guided
        trips and price gear rentals, and you help warehouse staff check live stock and sales.

        Trip planning and rentals:
        - Use the trip and rental tools to find guided trips, price gear, and produce booking reports.

        Warehouse inventory:
        - Recommend restock if item inventory < 10 and weekly sales > 15
        - Recommend clearance if item inventory > 20 and weekly sales < 5
        """,
        tools=[next_available_trip, calculate_rental_cost, generate_booking_report],
    )

    # A session keeps the conversation history across messages in the chat window.
    session = agent.create_session()


async def respond(user_message):
    """Handle one message from the chat window and return the agent's reply."""
    await setup()

    # Pass the MCP tools for this run alongside the agent's local tools. agent.run()
    # invokes whichever tool the model picks — a local @tool or an MCP tool — and
    # returns the final answer. No manual routing.
    result = await agent.run(user_message, tools=mcp_tool, session=session)
    return AgentReply(text=result.text)


if __name__ == "__main__":
    run_chat_app(
        respond,
        title="Trailhead Adventure Works Assistant",
        subtitle="Plan trips, price gear, and check warehouse stock (Microsoft Agent Framework edition)",
    )
