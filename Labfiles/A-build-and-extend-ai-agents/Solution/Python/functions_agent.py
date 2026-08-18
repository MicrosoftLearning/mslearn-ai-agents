import os
import json
from dotenv import load_dotenv

# Add references
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput

# Import the local functions the agent can call, and the shared chat UI
from functions import next_available_slot, calculate_transfer_cost, generate_capacity_report
from caldova_ui import run_chat_app, AgentReply

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Define the slot lookup function tool
    slot_tool = FunctionTool(
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
    )

    # Define the transfer cost function tool
    cost_tool = FunctionTool(
        name="calculate_transfer_cost",
        description="Calculate the cost of transferring production to a contract manufacturer, based on the CMO tier, number of weeks, and priority.",
        parameters={
            "type": "object",
            "properties": {
                "cmo_tier": {
                    "type": "string",
                    "description": "the CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')",
                },
                "weeks": {
                    "type": "number",
                    "description": "the number of weeks of contract capacity",
                },
                "priority": {
                    "type": "string",
                    "description": "the priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')",
                },
            },
            "required": ["cmo_tier", "weeks", "priority"],
            "additionalProperties": False,
        },
        strict=True,
    )

    # Define the capacity request function tool
    report_tool = FunctionTool(
        name="generate_capacity_report",
        description="Draft a capacity request summarizing an open production slot and a contract manufacturing estimate.",
        parameters={
            "type": "object",
            "properties": {
                "slot_name": {
                    "type": "string",
                    "description": "the name of the production slot being requested",
                },
                "site": {
                    "type": "string",
                    "description": "the site the production slot belongs to",
                },
                "cmo_tier": {
                    "type": "string",
                    "description": "the CMO tier for the transfer (e.g. 'standard', 'advanced', 'premium')",
                },
                "weeks": {
                    "type": "number",
                    "description": "the number of weeks of contract capacity",
                },
                "priority": {
                    "type": "string",
                    "description": "the priority of the transfer (e.g. 'standard', 'expedited', 'fast_track', 'emergency')",
                },
                "requested_by": {
                    "type": "string",
                    "description": "the team or role requesting the capacity",
                },
            },
            "required": ["slot_name", "site", "cmo_tier", "weeks", "priority", "requested_by"],
            "additionalProperties": False,
        },
        strict=True,
    )

    # Create a new agent with the function tools
    agent = project_client.agents.create_version(
        agent_name="capacity-planner-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""You are a capacity planning assistant for Caldova that helps
                planners find open production slots and estimate contract manufacturing costs.
                Use the available tools to assist users with their inquiries.""",
            tools=[slot_tool, cost_tool, report_tool],
        ),
    )

    # Create a thread for the chat session
    conversation = openai_client.conversations.create()

    def respond(user_message):
        """Handle one message from the chat window and return the agent's reply."""

        # Send the user's prompt to the agent
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_message}],
        )

        # Retrieve the agent's response, which may include function calls
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            input="",
        )

        # Create a list to hold function call outputs to send back to the agent
        input_list = []

        # Process function calls
        for item in response.output:
            if item.type == "function_call":
                result = None
                if item.name == "next_available_slot":
                    result = next_available_slot(**json.loads(item.arguments))
                elif item.name == "calculate_transfer_cost":
                    result = calculate_transfer_cost(**json.loads(item.arguments))
                elif item.name == "generate_capacity_report":
                    result = generate_capacity_report(**json.loads(item.arguments))

                input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=result,
                    )
                )

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

        # Return the agent's final answer to display in the chat window
        return AgentReply(text=response.output_text)

    # Launch the web chat window (replaces the old console loop)
    try:
        run_chat_app(
            respond,
            title="Caldova Assistant",
            subtitle="Find an open production slot and estimate contract capacity.",
        )
    finally:
        # Delete the agent when the app closes
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
