import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool, ToolSet
from user_functions import user_functions

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


    # Connect to the AI Project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    ):

        # Define an agent that can use the custom functions
        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)

        with project_client.get_openai_client() as openai_client:
            project_client.enable_auto_function_calls(toolset)
            
            agent = project_client.agents.create_version(
                agent_name="support-agent",
                definition=PromptAgentDefinition(
                    model=model_deployment,
                    instructions="""You are a technical support agent.
                                    When a user has a technical issue, you get their email address and a description of the issue.
                                    Then you use those values to submit a support ticket using the function available to you.
                                    If a file is saved, tell the user the file name.
                                 """,
                    toolset=toolset
                ),
            )
            print(f"You're chatting with: {agent.name} ({agent.id})")

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
