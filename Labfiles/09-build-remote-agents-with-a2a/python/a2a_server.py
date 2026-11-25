"""Host a Foundry-backed Agent Framework agent (title or outline) as an A2A server.

Usage:
  python a2a_server.py --agent-type title
  python a2a_server.py --agent-type outline
"""

import argparse
import os
import sys

import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from agent_definitions import AGENT_CARD_FACTORIES, AGENT_FACTORIES
from agent_executor import AgentFrameworkExecutor
from agent_framework.foundry import FoundryChatClient
from agent_framework_hosting import AgentState
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

load_dotenv()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A2A agent server")
    parser.add_argument("--agent-type", choices=sorted(AGENT_FACTORIES), required=True)
    parser.add_argument("--host", default=os.getenv("SERVER_URL", "localhost"))
    parser.add_argument("--port", type=int, default=None, help="Defaults to TITLE_AGENT_PORT / OUTLINE_AGENT_PORT")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    port = args.port or int(os.environ[f"{args.agent_type.upper()}_AGENT_PORT"])

    for var in ("FOUNDRY_PROJECT_ENDPOINT", "FOUNDRY_MODEL"):
        if not os.getenv(var):
            print(f"Error: {var} environment variable is not set.")
            sys.exit(1)

    # Create the Foundry-backed agent and its A2A agent card
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )
    agent = AGENT_FACTORIES[args.agent_type](client)

    url = f"http://{args.host}:{port}/"
    agent_card = AGENT_CARD_FACTORIES[args.agent_type](url)

    # The request handler connects the A2A protocol to the executor that runs the agent
    request_handler = DefaultRequestHandler(
        agent_executor=AgentFrameworkExecutor(AgentState(agent)),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    async def health(request: Request) -> PlainTextResponse:
        return PlainTextResponse(f"{agent_card.name} is running!")

    app = Starlette(
        routes=[
            # Serve the agent card so other agents can discover this one

            # Accept A2A messages (JSON-RPC) and pass them to the request handler
            Route("/health", health, methods=["GET"]),
        ]
    )

    print(f"Starting {agent_card.name} at {url} (agent card: {url}.well-known/agent-card.json)")
    uvicorn.run(app, host=args.host, port=port)


if __name__ == "__main__":
    main()
