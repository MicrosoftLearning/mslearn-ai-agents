import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole, MessageTextContent

# Load environment variables
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_id = os.getenv("AGENT_ID")

# Validate configuration
if not project_endpoint or not agent_id:
    raise ValueError("PROJECT_ENDPOINT and AGENT_ID must be set in .env file")

print(f"Connecting to project: {project_endpoint}")
print(f"Using agent: {agent_id}\n")

# Connect to the project and agent
credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    credential=credential,
    conn_str=project_endpoint
)

# Create an agent client
agent_client = project_client.agents

# Create a thread for the conversation
thread = agent_client.create_thread()
print(f"Created conversation thread: {thread.id}\n")

# Conversation history for context
conversation_history = []


def send_message_to_agent(user_message):
    """
    Send a message to the agent and handle the response.
    """
    try:
        # Store in conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        print(f"You: {user_message}\n")
        print("Agent: ", end="", flush=True)
        
        # Add user message to thread
        message = agent_client.create_message(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=user_message
        )
        
        # Run the agent
        run = agent_client.create_run(
            thread_id=thread.id,
            agent_id=agent_id
        )
        
        # Poll for completion
        while run.status in ["queued", "in_progress", "requires_action"]:
            run = agent_client.get_run(thread_id=thread.id, run_id=run.id)
            
        # Check for errors
        if run.status == "failed":
            print(f"\n\nError: Run failed - {run.last_error}\n")
            return None
        
        # Retrieve the agent's response
        messages = agent_client.list_messages(thread_id=thread.id)
        
        # Get the latest assistant message
        latest_message = None
        for msg in messages:
            if msg.role == MessageRole.ASSISTANT:
                latest_message = msg
                break
        
        if latest_message and latest_message.content:
            # Extract text content
            response_text = ""
            for content_item in latest_message.content:
                if isinstance(content_item, MessageTextContent):
                    response_text = content_item.text.value
                    break
            
            print(f"{response_text}\n")
            
            # Check for citations/annotations
            if latest_message.content[0].text.annotations:
                print("\nSources:")
                for annotation in latest_message.content[0].text.annotations:
                    if hasattr(annotation, 'file_citation'):
                        print(f"  - {annotation.file_citation.file_id}")
            
            # Store in conversation history
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text
        else:
            print("No response received.\n")
            return None
            
    except Exception as e:
        print(f"\n\nError: {str(e)}\n")
        return None


def display_conversation_history():
    """
    Display the full conversation history.
    """
    print("\n" + "="*60)
    print("CONVERSATION HISTORY")
    print("="*60 + "\n")
    
    for turn in conversation_history:
        role = turn["role"].upper()
        content = turn["content"]
        print(f"{role}: {content}\n")
    
    print("="*60 + "\n")


def main():
    """
    Main interaction loop.
    """
    print("Contoso Product Expert Agent")
    print("Ask questions about our outdoor and camping products.")
    print("Type 'history' to see conversation history, or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == 'quit':
                print("\nEnding conversation...")
                break
                
            if user_input.lower() == 'history':
                display_conversation_history()
                continue
            
            # Send message and get response
            send_message_to_agent(user_input)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}\n")
    
    # Cleanup
    try:
        agent_client.delete_thread(thread_id=thread.id)
        print("Thread cleaned up successfully.")
    except:
        pass


if __name__ == "__main__":
    main()
