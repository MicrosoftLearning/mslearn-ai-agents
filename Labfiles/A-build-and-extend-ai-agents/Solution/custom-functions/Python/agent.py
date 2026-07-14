import os
import json
from dotenv import load_dotenv

# Add references
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput

# Import the local functions the agent can call, and the shared chat UI
from functions import next_available_trip, calculate_rental_cost, generate_booking_report
from trailhead_ui import run_chat_app, AgentReply

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

    # Define the trip lookup function tool
    trip_tool = FunctionTool(
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
    )

    # Define the rental cost function tool
    cost_tool = FunctionTool(
        name="calculate_rental_cost",
        description="Calculate the cost of a gear rental based on the gear tier, number of days, and service level.",
        parameters={
            "type": "object",
            "properties": {
                "gear_tier": {
                    "type": "string",
                    "description": "the tier of the gear rental (e.g. 'standard', 'advanced', 'premium')",
                },
                "days": {
                    "type": "number",
                    "description": "the number of days for the gear rental",
                },
                "service_level": {
                    "type": "string",
                    "description": "the service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')",
                },
            },
            "required": ["gear_tier", "days", "service_level"],
            "additionalProperties": False,
        },
        strict=True,
    )

    # Define the booking report generation function tool
    report_tool = FunctionTool(
        name="generate_booking_report",
        description="Generate a report summarizing a guided trip booking and gear rental.",
        parameters={
            "type": "object",
            "properties": {
                "trip_name": {
                    "type": "string",
                    "description": "the name of the guided trip being booked",
                },
                "region": {
                    "type": "string",
                    "description": "the region of the guided trip",
                },
                "gear_tier": {
                    "type": "string",
                    "description": "the tier of the gear rented for the trip (e.g. 'standard', 'advanced', 'premium')",
                },
                "days": {
                    "type": "number",
                    "description": "the number of days the gear was rented",
                },
                "service_level": {
                    "type": "string",
                    "description": "the service level of the rental (e.g. 'standard', 'priority', 'express', 'rush')",
                },
                "customer_name": {
                    "type": "string",
                    "description": "the name of the customer making the booking",
                },
            },
            "required": ["trip_name", "region", "gear_tier", "days", "service_level", "customer_name"],
            "additionalProperties": False,
        },
        strict=True,
    )

    # Create a new agent with the function tools
    agent = project_client.agents.create_version(
        agent_name="trip-planner-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""You are a trip planning assistant for Trailhead Adventure Works that helps
                customers find guided trips and calculate gear rental costs.
                Use the available tools to assist users with their inquiries.""",
            tools=[trip_tool, cost_tool, report_tool],
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
                if item.name == "next_available_trip":
                    result = next_available_trip(**json.loads(item.arguments))
                elif item.name == "calculate_rental_cost":
                    result = calculate_rental_cost(**json.loads(item.arguments))
                elif item.name == "generate_booking_report":
                    result = generate_booking_report(**json.loads(item.arguments))

                input_list.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=result,
                    )
                )

        # Send function call outputs back to the model and retrieve a response
        if input_list:
            response = openai_client.responses.create(
                input=input_list,
                previous_response_id=response.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            )

        # Return the agent's final answer to display in the chat window
        return AgentReply(text=response.output_text)

    # Launch the web chat window (replaces the old console loop)
    try:
        run_chat_app(
            respond,
            title="Trailhead Adventure Works Assistant",
            subtitle="Plan a guided trip and price your gear rental.",
        )
    finally:
        # Delete the agent when the app closes
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
