""" Caldova Foundry Agent that generates a tech-transfer plan outline """

import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import Agent, MessageRole, ListSortOrder
from azure.identity import DefaultAzureCredential

class OutlineAgent:

    def __init__(self):

        # Create the agents client
        self.client = AgentsClient(
            endpoint=os.environ['PROJECT_ENDPOINT'],
            credential=DefaultAzureCredential(
                exclude_environment_credential=True,
                exclude_managed_identity_credential=True
            )
        )

        self.agent: Agent | None = None

    async def create_agent(self) -> Agent:
        if self.agent:
            return self.agent

        # Create the outline agent
        self.agent = self.client.create_agent(
            model=os.environ['MODEL_DEPLOYMENT_NAME'],
            name='transfer-outline-agent',
            instructions="""
            You are a helpful tech-transfer planning assistant for Caldova.
            Based on the provided transfer title or site, write a concise plan outline with 4 to 6 key stages.
            Each stage should be 5 to 10 words long, suitable for structuring a short transfer plan.
            """,
        )
        return self.agent

    async def run_conversation(self, user_message: str) -> list[str]:
        if not self.agent:
            await self.create_agent()

        # Create a thread for the chat session
        thread = self.client.threads.create()

        # Send user message
        self.client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=user_message)

        # Create and run the agent
        run = self.client.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)

        if run.status == 'failed':
            print(f'Outline Agent: Run failed - {run.last_error}')
            return [f'Error: {run.last_error}']

        # Get response messages
        messages = self.client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        responses = []
        for msg in messages:
            # Only get the latest assistant response
            if msg.role == 'assistant' and msg.text_messages:
                for text_msg in msg.text_messages:
                    responses.append(text_msg.text.value)
                break 

        return responses if responses else ['No response received']

async def create_foundry_outline_agent() -> OutlineAgent:
    agent = OutlineAgent()
    await agent.create_agent()
    return agent
