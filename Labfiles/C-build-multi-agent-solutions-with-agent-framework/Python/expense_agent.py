import os
import asyncio
from pathlib import Path
from typing import Annotated
from dotenv import load_dotenv

# Add references


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


    # Initialize an agent with the tool and instructions


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



if __name__ == "__main__":
    asyncio.run(main())
