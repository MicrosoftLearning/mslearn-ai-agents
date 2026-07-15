"""
Task 4 — Microsoft Agent Framework edition (provided complete, for comparison).

This file does exactly what functions_agent.py does — it gives the agent three
trip-planner tools — but it's built with the **Microsoft Agent Framework** instead
of the raw azure-ai-projects SDK + Responses API. Compare the two side by side:

  functions_agent.py (raw SDK + Responses API)     functions_agent_maf.py (this file)
  ---------------------------------------------     ----------------------------------
  Hand-write a FunctionTool JSON schema for         The @tool decorator generates the
  every function.                                   schema from the signature + Field text.
  Loop over response.output yourself, match         agent.run() runs the whole tool-calling
  each function_call, execute it, and send the      loop for you and returns the final answer.
  output back with previous_response_id.

You author the same three tools and the same instructions; the framework hides the
plumbing. Labs 07 and 08 explore the Agent Framework in more depth.
"""

import os
from typing import Annotated

from dotenv import load_dotenv

# Microsoft Agent Framework references
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field

# Reuse the same trip-planner logic from Task 4, plus the shared chat UI
import functions
from trailhead_ui import run_chat_app, AgentReply

# Load environment variables from .env file
load_dotenv()


# Expose each helper as a tool. @tool builds the schema the model sees from the
# function signature plus the Annotated/Field descriptions — no JSON to hand-write.
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


# Create the Foundry chat client and the agent once, at startup. FoundryChatClient
# wraps your model deployment; Agent adds the instructions and tools on top of it.
client = FoundryChatClient(
    project_endpoint=os.getenv("PROJECT_ENDPOINT"),
    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="trip-planner-agent",
    instructions="""You are a trip planning assistant for Trailhead Adventure Works that helps
        customers find guided trips and calculate gear rental costs.
        Use the available tools to assist users with their inquiries.""",
    tools=[next_available_trip, calculate_rental_cost, generate_booking_report],
)

# A session keeps the conversation history across messages in the chat window.
session = agent.create_session()


async def respond(user_message):
    """Handle one message from the chat window and return the agent's reply."""
    # agent.run() runs the entire tool-calling loop for you: it decides which tools
    # to call, invokes them, feeds the results back, and returns the final answer.
    result = await agent.run(user_message, session=session)
    return AgentReply(text=result.text)


if __name__ == "__main__":
    run_chat_app(
        respond,
        title="Trailhead Adventure Works Assistant",
        subtitle="Plan a guided trip and price your gear rental. (Microsoft Agent Framework edition)",
    )
