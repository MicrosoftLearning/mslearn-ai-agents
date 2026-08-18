import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Add references
from azure.ai.evaluation import (
    AzureOpenAIModelConfiguration,
    GroundednessEvaluator,
    RelevanceEvaluator,
    SimilarityEvaluator,
    evaluate,
)
from agent_target import CaldovaAgentTarget

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
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=evaluator_endpoint(),
    azure_deployment=model_deployment,
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
)

# Create the evaluators
groundedness = GroundednessEvaluator(model_config)
relevance = RelevanceEvaluator(model_config)
similarity = SimilarityEvaluator(model_config)

# Run the evaluation
result = evaluate(
    data=str(DATASET),
    target=CaldovaAgentTarget(),
    evaluators={
        "groundedness": groundedness,
        "relevance": relevance,
        "similarity": similarity,
    },
    evaluator_config={
        "groundedness": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${outputs.response}",
            }
        },
        "relevance": {
            "column_mapping": {
                "query": "${data.query}",
                "response": "${outputs.response}",
            }
        },
        "similarity": {
            "column_mapping": {
                "query": "${data.query}",
                "ground_truth": "${data.ground_truth}",
                "response": "${outputs.response}",
            }
        },
    },
    azure_ai_project=project_endpoint,
    output_path=str(OUTPUT),
)

# Print the aggregate scores
print("\nAggregate scores (1-5, higher is better):")
print(json.dumps(result["metrics"], indent=2))
print(f"\nRow-level detail: {OUTPUT.resolve()}")
if result.get("studio_url"):
    print(f"View in the Foundry portal: {result['studio_url']}")
