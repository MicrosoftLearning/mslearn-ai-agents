"""
Fast-forward setup for the Caldova enterprise-knowledge lab.

Task 1 has you build an enterprise-knowledge agent and ground it on the Caldova
Traders knowledge base. If you'd rather jump straight to connecting from code (or
to an optional task), run this once to create a grounded agent for you.

Run it from the lab's starter code folder —
Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Python, the folder you
open in VS Code — with the lab virtual environment active:

    python ../setup/bootstrap_agent.py

It reproduces, in code, the grounding step Task 1 has you do in the portal:

  * creates an agent named 'caldova-knowledge-agent'
  * grounds it on the Caldova knowledge docs with the File Search tool
  * writes AGENT_NAME=caldova-knowledge-agent into Python/.env

Prerequisites: PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME set in Python/.env
(run 'azd up', or fill them in from the portal), and 'az login' completed.

If you'd rather learn the portal workflow, skip this script and do Task 1
instead — the end result is a grounded knowledge agent either way.

Note: The portal Task 1 grounds the agent with Foundry IQ (a knowledge source
with agentic retrieval and an approval step). This script uses the simpler File
Search tool so you have a working grounded agent for the code clients without the
portal steps. The code you write against it is identical.
"""

import argparse
import os
import sys
import time
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    FileSearchTool,
    PromptAgentDefinition,
)
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

AGENT_NAME = "caldova-knowledge-agent"

# The same instructions Task 1 has you give the agent in the portal.
INSTRUCTIONS = """You are the Caldova staff knowledge assistant.
You help planning and materials teams answer questions about capacity, contract manufacturers, site operations, and suppliers.

Guidelines:
- Always be friendly and helpful
- Use the Caldova knowledge base to answer questions accurately
- Cite the document you used when you can
- If you don't know the answer, admit it and suggest contacting the relevant team directly"""

# Resolve paths relative to this file so the script works from any directory.
LAB_ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIR = LAB_ROOT / "Python"
ENV_PATH = PYTHON_DIR / ".env"
DATA_DIR = PYTHON_DIR / "data"


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


def build_vector_store(openai_client, file_ids):
    """Create a vector store for File Search and wait until it's indexed."""
    print("  Creating vector store for the Caldova knowledge base ...")
    vector_store = openai_client.vector_stores.create(
        name="ks-caldovaproducts",
        file_ids=file_ids,
    )

    # Wait for the files to finish indexing so the agent can search them immediately.
    for _ in range(30):
        current = openai_client.vector_stores.retrieve(vector_store_id=vector_store.id)
        if current.status == "completed":
            break
        if current.status == "failed":
            fail("Vector store indexing failed. Check the uploaded files and try again.")
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
        description="Create and ground the caldova-knowledge-agent."
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

    data_files = sorted(DATA_DIR.glob("*.md"))
    if not data_files:
        fail(f"No knowledge documents found in {DATA_DIR}.")

    print("Connecting to your Foundry project ...")
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
        if agent_exists(project_client) and not args.force:
            print(f"\nAgent '{AGENT_NAME}' already exists - nothing to do.")
            print("Re-run with --force to add a new grounded version.")
            set_env_value("AGENT_NAME", AGENT_NAME)
            print(f"Ensured AGENT_NAME={AGENT_NAME} in {ENV_PATH}")
            return

        print(f"Grounding the agent (this uploads {len(data_files)} knowledge documents):")
        file_ids = [upload_file(openai_client, path) for path in data_files]
        vector_store_id = build_vector_store(openai_client, file_ids)

        file_search = FileSearchTool(vector_store_ids=[vector_store_id])

        print("Creating the agent ...")
        agent = project_client.agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions=INSTRUCTIONS,
                tools=[file_search],
            ),
        )
        print(f"  Created '{agent.name}' (version {agent.version}).")

    set_env_value("AGENT_NAME", AGENT_NAME)
    print(f"\nWrote AGENT_NAME={AGENT_NAME} to {ENV_PATH}")
    print("You're ready to connect from code: run 'python knowledge_agent.py' from the Python folder.")


if __name__ == "__main__":
    main()
