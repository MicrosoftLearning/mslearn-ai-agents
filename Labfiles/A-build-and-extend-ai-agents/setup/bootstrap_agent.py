"""
Fast-forward setup for the Trailhead Adventure Works lab.

Task 3 needs the grounded agent you would normally build by hand in Task 1
(and extend at the start of Task 3). If you're starting at Task 3 on its own,
run this once to create that agent for you:

    python setup/bootstrap_agent.py

It reproduces, in code, exactly what Tasks 1 and 3 have you do in the portal:

  * creates an agent named 'trailhead-agent'
  * grounds it on Store_Policy.txt with the File Search tool
  * adds the Code Interpreter tool with weekly_sales.csv attached
  * writes AGENT_NAME=trailhead-agent into Python/.env

Prerequisites: PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME set in Python/.env
(run 'azd up', or fill them in from the portal), and 'az login' completed.

If you'd rather learn the portal workflow, skip this script and do Task 1
instead — the end result is the same agent.
"""

import argparse
import os
import sys
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AutoCodeInterpreterToolParam,
    CodeInterpreterTool,
    FileSearchTool,
    PromptAgentDefinition,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

AGENT_NAME = "trailhead-agent"

# The same instructions Task 1 has you paste into the portal.
INSTRUCTIONS = """You are the Trailhead Adventure Works store assistant.
You help customers and store staff with questions about products, orders, returns, rentals, and guided trips.

Guidelines:
- Always be friendly and helpful
- Use the store policy documentation to answer questions accurately
- If you don't know the answer, admit it and suggest contacting the support team directly"""

# Resolve paths relative to this file so the script works from any directory.
LAB_ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = LAB_ROOT / "Python"
ENV_PATH = PYTHON_DIR / ".env"
POLICY_FILE = PYTHON_DIR / "Store_Policy.txt"
SALES_FILE = PYTHON_DIR / "weekly_sales.csv"


def fail(message):
    print(f"\nERROR: {message}")
    sys.exit(1)


def upload_file(openai_client, path):
    """Upload a local file and return its file id."""
    if not path.exists():
        fail(f"Expected data file not found: {path}")
    print(f"  Uploading {path.name} ...")
    with open(path, "rb") as handle:
        uploaded = openai_client.files.create(file=handle, purpose="assistants")
    return uploaded.id


def build_vector_store(openai_client, file_id):
    """Create a vector store for File Search and wait until it's indexed."""
    print("  Creating vector store for Store_Policy.txt ...")
    vector_store = openai_client.vector_stores.create(
        name="trailhead-store-policy",
        file_ids=[file_id],
    )

    # Wait for the file to finish indexing so the agent can search it immediately.
    for _ in range(30):
        current = openai_client.vector_stores.retrieve(vector_store_id=vector_store.id)
        if current.status == "completed":
            break
        if current.status == "failed":
            fail("Vector store indexing failed. Check the uploaded file and try again.")
        time.sleep(2)

    return vector_store.id


def agent_exists(project_client):
    try:
        project_client.agents.get(agent_name=AGENT_NAME)
        return True
    except ResourceNotFoundError:
        return False


def set_env_value(key, value):
    """Add or update a key in Python/.env, preserving the other entries."""
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    prefix = f"{key}="
    replaced = False
    for index, line in enumerate(lines):
        if line.strip().startswith(prefix) or line.strip().startswith(f"{key} ="):
            lines[index] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        lines.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Create and ground the trailhead-agent for Task 3."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Create a new version even if the agent already exists.",
    )
    args = parser.parse_args()

    load_dotenv(ENV_PATH)
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    if not project_endpoint:
        fail("PROJECT_ENDPOINT is not set in Python/.env. Run 'azd up' or set it from the portal.")
    if not model_deployment:
        fail("MODEL_DEPLOYMENT_NAME is not set in Python/.env. Set it to your deployed model name.")

    print("Connecting to your Foundry project ...")
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        if agent_exists(project_client) and not args.force:
            print(f"\nAgent '{AGENT_NAME}' already exists — nothing to do.")
            print("Re-run with --force to add a new grounded version.")
            set_env_value("AGENT_NAME", AGENT_NAME)
            print(f"Ensured AGENT_NAME={AGENT_NAME} in {ENV_PATH}")
            return

        print("Grounding the agent (this uploads two small files):")
        policy_file_id = upload_file(openai_client, POLICY_FILE)
        vector_store_id = build_vector_store(openai_client, policy_file_id)
        sales_file_id = upload_file(openai_client, SALES_FILE)

        file_search = FileSearchTool(vector_store_ids=[vector_store_id])
        code_interpreter = CodeInterpreterTool(
            container=AutoCodeInterpreterToolParam(file_ids=[sales_file_id])
        )

        print("Creating the agent ...")
        agent = project_client.agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions=INSTRUCTIONS,
                tools=[file_search, code_interpreter],
            ),
        )
        print(f"  Created '{agent.name}' (version {agent.version}).")

    set_env_value("AGENT_NAME", AGENT_NAME)
    print(f"\nWrote AGENT_NAME={AGENT_NAME} to {ENV_PATH}")
    print("You're ready to start Task 3: run 'python agent_with_functions.py' from the Python folder.")


if __name__ == "__main__":
    main()
