"""
Task 4 — Microsoft Agent Framework edition (provided complete, for comparison).

This file does exactly what functions_agent.py does — it gives the agent three
capacity-planner tools — but it's built with the **Microsoft Agent Framework** instead
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

# Reuse the same capacity-planner logic from Task 4, plus the shared chat UI
import functions
from caldova_ui import run_chat_app, AgentReply

# Load environment variables from .env file
load_dotenv()


# Expose each helper as a tool. @tool builds the schema the model sees from the
# function signature plus the Annotated/Field descriptions — no JSON to hand-write.
@tool(approval_mode="never_require")
def next_available_slot(
    site: Annotated[str, Field(description="Site to find the next open production slot at (e.g. 'ashford', 'brightwater', 'calderwood')")],
) -> str:
    """Get the next open production slot at a given site."""
    return functions.next_available_slot(site)


@tool(approval_mode="never_require")
def calculate_transfer_cost(
    cmo_tier: Annotated[str, Field(description="The CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')")],
    weeks: Annotated[float, Field(description="The number of weeks of contract capacity")],
    priority: Annotated[str, Field(description="The priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')")],
) -> str:
    """Calculate the cost of transferring production to a contract manufacturer, based on the CMO tier, number of weeks, and priority."""
    return functions.calculate_transfer_cost(cmo_tier, weeks, priority)


@tool(approval_mode="never_require")
def generate_capacity_report(
    slot_name: Annotated[str, Field(description="The name of the production slot being requested")],
    site: Annotated[str, Field(description="The site the production slot belongs to")],
    cmo_tier: Annotated[str, Field(description="The CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')")],
    weeks: Annotated[float, Field(description="The number of weeks of contract capacity")],
    priority: Annotated[str, Field(description="The priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')")],
    requested_by: Annotated[str, Field(description="The team or role requesting the capacity")],
) -> str:
    """Draft a capacity request summarizing an open production slot and a contract manufacturing estimate."""
    return functions.generate_capacity_report(slot_name, site, cmo_tier, weeks, priority, requested_by)


# Create the Foundry chat client and the agent once, at startup. FoundryChatClient
# wraps your model deployment; Agent adds the instructions and tools on top of it.
client = FoundryChatClient(
    project_endpoint=os.getenv("PROJECT_ENDPOINT"),
    model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    credential=AzureCliCredential(),
)

agent = Agent(
    client=client,
    name="capacity-planner-agent",
    instructions="""You are a capacity planning assistant for Caldova that helps
        planners find open production slots and estimate contract manufacturing costs.
        Use the available tools to assist users with their inquiries.""",
    tools=[next_available_slot, calculate_transfer_cost, generate_capacity_report],
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
        title="Caldova Assistant",
        subtitle="Find an open production slot and estimate contract capacity. (Microsoft Agent Framework edition)",
    )
