import argparse
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME", "caldova-knowledge-agent")

SEED_PROMPTS = Path("data/attack_objectives.json")
OUTPUT = Path("redteam_scan.json")

credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
openai_client = project_client.get_openai_client()


# Build the callback that sends one attack prompt to your agent
def caldova_agent(query: str) -> str:
    """The target. The Red Teaming Agent calls this once per attack prompt."""
    try:
        response = openai_client.responses.create(
            input=query,
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )
        return response.output_text
    except Exception as error:  # a blocked prompt is a result, not a crash
        return f"The agent did not answer: {error}"


async def main():
    parser = argparse.ArgumentParser(description="Red team the Caldova agent.")
    parser.add_argument(
        "--seed-prompts",
        action="store_true",
        help="Attack with data/attack_objectives.json instead of the Microsoft-curated objectives.",
    )
    args = parser.parse_args()

    # Create the AI Red Teaming Agent
    if args.seed_prompts:
        red_team = RedTeam(
            azure_ai_project=project_endpoint,
            credential=credential,
            custom_attack_seed_prompts=str(SEED_PROMPTS),
        )
    else:
        red_team = RedTeam(
            azure_ai_project=project_endpoint,
            credential=credential,
            risk_categories=[
                RiskCategory.Violence,
                RiskCategory.HateUnfairness,
                RiskCategory.SelfHarm,
            ],
            num_objectives=2,
        )

    # Run the scan
    print("Scanning. This sends adversarial prompts to your agent and takes a few minutes ...")
    await red_team.scan(
        target=caldova_agent,
        scan_name="caldova-knowledge-agent",
        attack_strategies=[
            AttackStrategy.Base64,
            AttackStrategy.Flip,
            AttackStrategy.Compose([AttackStrategy.Base64, AttackStrategy.ROT13]),
        ],
        output_path=str(OUTPUT),
    )

    # Read the scorecard back and show the headline numbers
    scan = json.loads(OUTPUT.read_text(encoding="utf-8"))
    scorecard = scan.get("redteaming_scorecard", {})
    print("\nAttack success rate by risk category:")
    print(json.dumps(scorecard.get("risk_category_summary", []), indent=2))
    print("\nAttack success rate by technique:")
    print(json.dumps(scorecard.get("attack_technique_summary", []), indent=2))
    print(f"\nFull scorecard: {OUTPUT.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
