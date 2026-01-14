import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, CodeInterpreterTool


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Display the data to be analyzed
    script_dir = Path(__file__).parent  # Get the directory of the script
    file_path = script_dir / 'data.txt'

    with file_path.open('r') as file:
        data = file.read() + "\n"
        print(data)

    # Connect to the AI Project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    ):

        # Upload the data file and create a CodeInterpreterTool
        file = project_client.files.upload_and_poll(
            file_path=file_path, purpose="agents"
        )
        print(f"Uploaded {file.filename}")

        code_interpreter = CodeInterpreterTool(file_ids=[file.id])

        # Define an agent that uses the CodeInterpreterTool
        with project_client.get_openai_client() as openai_client:
            agent = project_client.agents.create_version(
                agent_name="data-agent",
                definition=PromptAgentDefinition(
                    model=model_deployment,
                    instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
                    tools=code_interpreter.definitions,
                    tool_resources=code_interpreter.resources,
                ),
            )
            print(f"Using agent: {agent.name} (version: {agent.version})")

            # Create a conversation for the chat session
            conversation = openai_client.conversations.create()
            print(f"Created conversation (id: {conversation.id})")
        
            # Loop until the user types 'quit'
            while True:
                # Get input text
                user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
                if user_prompt.lower() == "quit":
                    break
                if len(user_prompt) == 0:
                    print("Please enter a prompt.")
                    continue

                # Send a prompt to the agent
                openai_client.conversations.items.create(
                    conversation_id=conversation.id,
                    items=[{"type": "message", "role": "user", "content": user_prompt}],
                )

                response = openai_client.responses.create(
                    conversation=conversation.id,
                    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                    input="",
                )

                # Check the response status for failures
                if response.status == "failed":
                    print(f"Response failed: {response.error}")
        
                # Show the latest response from the agent
                print(f"Agent: {response.output_text}")

            # Get the conversation history
            print("\nConversation Log:\n")
            items = openai_client.conversations.items.list(conversation_id=conversation.id)
            for item in items.data:
                if item.type == "message":
                    role = item.role.upper()
                    content = item.content[0].text.value if item.content and item.content[0].type == "text" else ""
                    print(f"{role}: {content}\n")

            # Clean up
            openai_client.conversations.delete(conversation_id=conversation.id)
            print("Conversation deleted")

        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Agent deleted")

    


if __name__ == '__main__': 
    main()
