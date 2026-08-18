"""
Task 1 (Core) - Caldova site-visit expense agent, built with the Microsoft Agent Framework.

This is a single agent with one custom tool. The agent reads an engineer's site-visit expense
data, itemizes it, and uses the submit_claim tool to "email" a reimbursement claim to
the Caldova finance desk. The @tool decorator generates the tool schema from
the function signature, and agent.run() runs the whole tool-calling loop for you.
"""

import os
import asyncio
from pathlib import Path
from typing import Annotated
from dotenv import load_dotenv

# Add references
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field

load_dotenv()


async def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Load the site-visit expenses data file
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # Ask for a prompt
    user_prompt = input(f"Here is the site-visit expense data in your file:\n\n{data}\n\nWhat would you like me to do with it?\n\n")

    # Run the async agent code
    await process_expenses_data(user_prompt, data)


async def process_expenses_data(prompt, expenses_data):

    # Create a foundry chat client
    client = FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    )

    # Initialize an agent with the tool and instructions
    agent = Agent(
        client=client,
        name="SiteVisitExpenseAgent",
        instructions="""You are an AI assistant for Caldova site-visit expense claims.
                    At the user's request, create an expense claim and use the submit_claim tool to send an email to expenses@caldova.example with the subject 'Site Visit Expense Claim' and a body that contains the itemized expenses with a total.
                    Then confirm to the user that you've done so. Don't ask for any more information from the user, just use the data provided to create the email.""",
        tools=[submit_claim],
    )

    # Create a session and use the agent to process the expenses data
    try:
        # A session keeps the conversation history across the agent run
        session = agent.create_session()
        # Invoke the agent with the prompt and the site-visit expenses data
        response = await agent.run(f"{prompt}: {expenses_data}", session=session)
        # Display the response
        print(f"\n# Agent:\n{response.text}")
    except Exception as e:
        # Something went wrong
        print(e)


# Create a tool function for the email functionality
@tool(approval_mode="never_require")
def submit_claim(
    to: Annotated[str, Field(description="Who to send the email to")],
    subject: Annotated[str, Field(description="The subject of the email.")],
    body: Annotated[str, Field(description="The text body of the email.")],
):
    """Submit a Caldova site-visit expense claim by sending an email."""
    print("\nTo:", to)
    print("Subject:", subject)
    print(body, "\n")


if __name__ == "__main__":
    asyncio.run(main())
