import asyncio
import os
from typing import cast
from dotenv import load_dotenv

# Add references


load_dotenv()

async def main():
    # Agent instructions
    summarizer_instructions="""
    Summarize the reported issue in one short sentence. Keep it neutral and concise.
    Example output:
    Sealing unit failed on the first shift of a packaging run.
    Site team praises the new changeover procedure.
    """

    classifier_instructions="""
    Classify the feedback as one of the following: Positive, Negative, or Feature request.
    """

    action_instructions="""
    Based on the summary and classification, suggest the next action in one short sentence.
    Example output:
    Escalate as a high-priority defect for the engineering team.
    Log as positive feedback to share with the operations team.
    Log as enhancement request for the product backlog.
    """

    # Create the chat client


    # Create agents


    # Initialize the current feedback


    # Build sequential orchestration


    # Run and collect outputs


    # Display outputs



if __name__ == "__main__":
    asyncio.run(main())
