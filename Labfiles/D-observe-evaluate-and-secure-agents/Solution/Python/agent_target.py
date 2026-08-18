"""
The application under evaluation: the Caldova knowledge agent.

This file is PROVIDED - you don't edit it. It wraps the agent you already have
(from Lab B, or from `python ../setup/bootstrap_agent.py`) in the shape the
evaluate() API expects for a *target*: something callable that takes a row of
your dataset and returns the application's output for that row.

evaluate() calls this once per line of caldova_eval.jsonl, passing the columns
of that line as keyword arguments, and merges the returned dictionary back into
the row as `outputs.*`. So returning {"response": ...} makes `${outputs.response}`
available to every evaluator.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class CaldovaAgentTarget:
    """Sends one question to the knowledge agent and returns its answer."""

    def __init__(self):
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        self.agent_name = os.getenv("AGENT_NAME", "caldova-knowledge-agent")

        if not project_endpoint:
            raise ValueError("PROJECT_ENDPOINT must be set in .env")

        self.credential = DefaultAzureCredential()
        self.project_client = AIProjectClient(
            endpoint=project_endpoint, credential=self.credential
        )
        self.openai_client = self.project_client.get_openai_client()

        # Fail early with a useful message rather than once per dataset row.
        self.project_client.agents.get(agent_name=self.agent_name)

    def __call__(self, *, query: str, **kwargs) -> dict:
        """Answer one question. Extra dataset columns arrive in kwargs and are ignored."""
        response = self.openai_client.responses.create(
            input=query,
            extra_body={
                "agent_reference": {"name": self.agent_name, "type": "agent_reference"}
            },
        )
        return {"response": response.output_text}
