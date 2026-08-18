import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Add references


# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

DATASET = Path("data/caldova_eval.jsonl")
OUTPUT = Path("eval_results.json")


def evaluator_endpoint():
    """The Azure OpenAI endpoint the evaluator model runs on.

    Provided. AZURE_OPENAI_ENDPOINT wins if you set it; otherwise this strips
    the '/api/projects/<name>' suffix off PROJECT_ENDPOINT to get the endpoint
    of the Foundry resource underneath.
    """
    configured = os.getenv("AZURE_OPENAI_ENDPOINT")
    if configured:
        return configured
    return project_endpoint.split("/api/projects/")[0]


# Configure the model that grades the answers


# Create the evaluators


# Run the evaluation


# Print the aggregate scores

