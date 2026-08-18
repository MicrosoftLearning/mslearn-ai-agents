import os
from dotenv import load_dotenv

# Add references


# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Turn on GenAI tracing


# A morning's worth of questions from the planning desk.
QUESTIONS = [
    "How long does review take for a capacity request with a complete brief?",
    "How much is five weeks of premium contract capacity at expedited priority?",
    "Which contract manufacturers could fast-track us inside a three-month window?",
]

AGENT_NAME = "caldova-planning-assistant"
INSTRUCTIONS = (
    "You are the Caldova planning assistant. You answer questions from planning "
    "and materials teams about capacity, contract manufacturers, and suppliers. "
    "Keep answers short enough to read between meetings."
)

# Connect to the project

    # Read the Application Insights connection string and start exporting traces


    # Get a tracer for this script


    # Create the agent staff are talking to


    # Ask each question inside its own span


    # Clean up resources by deleting the agent version

