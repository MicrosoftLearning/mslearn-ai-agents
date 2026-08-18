"""
Task 2 (Optional) - Multi-agent sequential orchestration with the Microsoft Agent Framework.

Three Caldova agents work together in a pipeline to triage a piece of site
feedback: a Summarizer condenses it, a Classifier labels it, and an Action agent recommends
the next step. SequentialBuilder runs them in order and collects every agent's output.
"""

import asyncio
import os
from typing import cast
from dotenv import load_dotenv

# Add references
from agent_framework import Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

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
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
    )

    # Create agents
    summarizer_agent = chat_client.as_agent(
        name="summarizer",
        instructions=summarizer_instructions,
    )

    classifier_agent = chat_client.as_agent(
        name="classifier",
        instructions=classifier_instructions,
    )

    action_agent = chat_client.as_agent(
        name="action",
        instructions=action_instructions,
    )

    # Initialize the current feedback
    feedback="""
    I use the line-scheduling app before every changeover, and it works well overall.
    But when I'm checking the schedule at night on the floor, the bright screen is really harsh on my eyes.
    If you added a dark mode option, it would make it much more comfortable to use in low light.
    """

    # Build sequential orchestration
    workflow = SequentialBuilder(
        participants=[summarizer_agent, classifier_agent, action_agent],
        output_from="all",
    ).build()

    # Run and collect outputs
    result = await workflow.run(f"Site feedback: {feedback}")
    outputs = result.get_outputs()

    # Display outputs
    i = 1
    for response in outputs:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            i += 1


if __name__ == "__main__":
    asyncio.run(main())
