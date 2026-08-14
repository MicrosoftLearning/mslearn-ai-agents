import os
from dotenv import load_dotenv

# Add references


# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Turn on GenAI tracing


# A Saturday morning's worth of questions from the shop floor.
QUESTIONS = [
    "A customer wants to return a tent they used on one trip. What do I tell them?",
    "How much is a week's hire of a premium kayak with priority service?",
    "Which of our backpacks is best for a three-day hike in heavy rain?",
]

AGENT_NAME = "tailwind-shift-assistant"
INSTRUCTIONS = (
    "You are the Tailwind Traders shift assistant. You answer questions from store "
    "staff about products, returns, rentals, and guided trips. Keep answers short "
    "enough to read between customers."
)

# Connect to the project

    # Read the Application Insights connection string and start exporting traces


    # Get a tracer for this script


    # Create the agent staff are talking to


    # Ask each question inside its own span


    # Clean up resources by deleting the agent version

