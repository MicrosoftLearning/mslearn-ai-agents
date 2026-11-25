"""Foundry-backed agents and their A2A AgentCards for the title and outline servers."""

from __future__ import annotations

from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

TITLE_INSTRUCTIONS = """\
You are a helpful writing assistant.
Given a topic the user wants to write about, suggest a single clear and catchy blog post title.
Reply with the title only.
"""

OUTLINE_INSTRUCTIONS = """\
You are a helpful writing assistant.
Based on the provided title or topic, write a concise outline with 4 to 6 key sections.
Each section should be 5 to 10 words long, suitable for structuring a short blog post.
"""


def create_title_agent(client: FoundryChatClient) -> Agent:
    """Create the title agent on the Foundry-backed chat client."""
    # Create the title agent


def create_outline_agent(client: FoundryChatClient) -> Agent:
    """Create the outline agent on the Foundry-backed chat client."""
    return Agent(client=client, name="OutlineAgent", instructions=OUTLINE_INSTRUCTIONS)


_CAPABILITIES = AgentCapabilities(streaming=True, push_notifications=False)


def get_title_agent_card(url: str) -> AgentCard:
    """Return the A2A agent card that makes the title agent discoverable."""
    # Define the agent skill

    # Create the agent card



def get_outline_agent_card(url: str) -> AgentCard:
    description = "Writes a short outline (4-6 sections) for a blog post title or topic."
    return AgentCard(
        name="OutlineAgent",
        description=description,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=_CAPABILITIES,
        supported_interfaces=[AgentInterface(url=url, protocol_binding="JSONRPC", protocol_version="1.0")],
        skills=[
            AgentSkill(
                id="generate_blog_outline",
                name="Generate Blog Outline",
                description=description,
                tags=["outline", "agent-framework"],
                examples=["Write an outline for 'Why agents need a common protocol'."],
            ),
        ],
    )


AGENT_FACTORIES = {"title": create_title_agent, "outline": create_outline_agent}
AGENT_CARD_FACTORIES = {"title": get_title_agent_card, "outline": get_outline_agent_card}
