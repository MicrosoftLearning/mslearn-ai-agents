"""Interactive chat with a Foundry routing agent that delegates to remote agents over A2A.

The routing agent discovers each remote agent from its AgentCard, wraps it as a tool, and
decides per request which remote agent(s) to call.
"""

import asyncio
import os
from contextlib import AsyncExitStack

import httpx
from a2a.client import A2ACardResolver
from agent_framework import Agent
from agent_framework.a2a import A2AAgent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

ROUTING_INSTRUCTIONS = """\
You are an expert routing delegator that helps users write blog posts.

- Delegate to the specialized remote agents available as tools. Do not write titles or outlines yourself.
- For a request that needs both a title and an outline, call the title agent first, then pass the
  chosen title to the outline agent.
- Reply to the user with the results, clearly labelled.
"""


def remote_agent_urls() -> list[str]:
    host = os.environ["SERVER_URL"]
    return [
        f"http://{host}:{os.environ['TITLE_AGENT_PORT']}/",
        f"http://{host}:{os.environ['OUTLINE_AGENT_PORT']}/",
    ]


async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

    async with AsyncExitStack() as stack:
        tools = []
        async with httpx.AsyncClient(timeout=60.0) as http_client:
            for url in remote_agent_urls():
                # Discover the remote agent by fetching its agent card

                print(f"Discovered remote agent: {card.name} - {card.description}")

                # Connect to the remote agent over A2A

                # Give the routing agent the remote agent as a tool it can call

        routing_agent = Agent(
            client=client,
            name="RoutingAgent",
            instructions=ROUTING_INSTRUCTIONS,
            tools=tools,
        )
        session = routing_agent.create_session()

        print("\nEnter a prompt for the routing agent. Type 'quit' to exit.")
        while True:
            user_input = await asyncio.to_thread(input, "User: ")
            if user_input.strip().lower() == "quit":
                print("Goodbye!")
                break
            if not user_input.strip():
                continue
            response = await routing_agent.run(user_input, session=session)
            print(f"Agent: {response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
