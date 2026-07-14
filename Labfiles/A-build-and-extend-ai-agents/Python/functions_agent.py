import os
import json
from dotenv import load_dotenv

# Add references


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


    # Define the rental cost function tool


    # Define the booking report generation function tool


    # Create a new agent with the function tools


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
