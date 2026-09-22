import os
from dotenv import load_dotenv

# Add references


# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME", "caldova-knowledge-agent")

# Turn on GenAI tracing


# A morning's worth of questions from the planning desk.
QUESTIONS = [
    "How long does review take for a capacity request with a complete brief?",
    "How much is five weeks of premium contract capacity at expedited priority?",
    "Which contract manufacturers could fast-track us inside a three-month window?",
]

# Connect to the project

    # Read the Application Insights connection string and start exporting traces


    # Get a tracer for this script


    # Look up the agent so its id can be included in agent_reference


    # Ask each question inside its own span

