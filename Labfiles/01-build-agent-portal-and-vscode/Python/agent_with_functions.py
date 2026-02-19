from dotenv import load_dotenv
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import base64
from pathlib import Path
   
   
def save_image(image_data, filename):
    """Save base64 image data to a file."""
    output_dir = Path("agent_outputs")
    output_dir.mkdir(exist_ok=True)
       
    filepath = output_dir / filename
       
    # Decode and save the image
    image_bytes = base64.b64decode(image_data)
    with open(filepath, 'wb') as f:
        f.write(image_bytes)
       
    return str(filepath)
   
   
def main():
    # Initialize the project client
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    agent_name = os.environ.get("AGENT_NAME", "it-support-agent")
       
    if not project_endpoint:
        print("Error: PROJECT_ENDPOINT environment variable not set")
        print("Please set it in your .env file or environment")
        return
       
    print("Connecting to Microsoft Foundry project...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        credential=credential,
        endpoint=project_endpoint
    )
       
    # Get the OpenAI client for Responses API
    openai_client = project_client.get_openai_client()
       
    # Get the agent created in the portal
    print(f"Loading agent: {agent_name}")
    agent = project_client.agents.get_agent(agent_id=agent_name)
    print(f"Connected to agent: {agent.name} (id: {agent.id})")
       
    # Create a conversation
    conversation = openai_client.conversations.create(items=[])
    print(f"Conversation created (id: {conversation.id})")
       
    # Chat loop
    print("\n" + "="*60)
    print("IT Support Agent Ready!")
    print("Ask questions, request data analysis, or get help.")
    print("Type 'exit' to quit.")
    print("="*60 + "\n")
       
    while True:
        user_input = input("You: ").strip()
           
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
           
        if not user_input:
            continue
           
        # Add user message to conversation
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}]
        )
           
        # Get response from agent
        print("\n[Agent is thinking...]")
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
            input=""
        )
           
        # Display response
        if hasattr(response, 'output_text') and response.output_text:
            print(f"\nAgent: {response.output_text}\n")
        elif hasattr(response, 'output') and response.output:
            # Extract text from output items
            image_count = 0
            for item in response.output:
                if hasattr(item, 'text') and item.text:
                    print(f"\nAgent: {item.text}\n")
                elif hasattr(item, 'type'):
                    # Handle other output types like images from code interpreter
                    if item.type == 'image':
                        image_count += 1
                        filename = f"chart_{image_count}.png"
                           
                        # Download and save the image
                        if hasattr(item, 'image') and hasattr(item.image, 'data'):
                            filepath = save_image(item.image.data, filename)
                            print(f"\n[Agent generated a chart - saved to: {filepath}]")
                        else:
                            print(f"\n[Agent generated an image]")
                    elif item.type == 'file':
                        print(f"\n[Agent created a file]")
   
   
if __name__ == "__main__":
    main() 