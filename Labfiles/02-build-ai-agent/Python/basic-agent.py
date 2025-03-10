import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, BingGroundingTool, ToolSet
from azure.identity import DefaultAzureCredential
from pathlib import Path

def initialize_tools():
    



load_dotenv()
deployed_model = os.getenv("MODEL_DEPLOYMENT")
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(exclude_environment_credential=True, exclude_managed_identity_credential=True), conn_str=os.getenv("PROJECT_CONNECTION")
)

with project_client:
    # Get the toolset
    toolset = initialize_tools()

    # Create an agent
    

    # Run the agent
    
    
    # Uncomment to see the raw messages JSON
    # print(f"Messages: {messages}")

    # Get the last message from the sender
    last_msg = messages.get_last_text_message_by_role("assistant")
    if last_msg:
        print(f"Last agent message: {last_msg.text.value}")

    # Generate an image file for the chart
    for image_content in messages.image_contents:
        print(f"Image File ID: {image_content.image_file.file_id}")
        file_name = f"{image_content.image_file.file_id}_image_file.png"
        project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
        print(f"Saved image file to: {Path.cwd() / file_name}")

    # Delete the agent once done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
