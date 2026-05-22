""" Azure AI Foundry Agent that generates a title """

import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import Agent, ListSortOrder, MessageRole

class TitleAgent:

    def __init__(self):

        # Create the agents client


        self.agent: Agent | None = None

    async def create_agent(self) -> Agent:
        if self.agent:
            return self.agent

        # Create the title agent


        return self.agent
        
    async def run_conversation(self, user_message: str) -> list[str]:
        # Add a message to the thread, process it, and retrieve the response

        if not self.agent:
            await self.create_agent()

        # Create a thread for the chat session


        # Send user message
        

        # Create and run the agent


        if run.status == 'failed':
            print(f'Title Agent: Run failed - {run.last_error}')
            return [f'Error: {run.last_error}']

        # Get response messages
        messages = self.client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        responses = []
        for msg in messages:
            # Only get the latest assistant response
            if msg.role == MessageRole.AGENT and msg.text_messages:
                for text_msg in msg.text_messages:
                    responses.append(text_msg.text.value)
                break 

        return responses if responses else ['No response received']

async def create_foundry_title_agent() -> TitleAgent:
    agent = TitleAgent()
    await agent.create_agent()
    return agent
