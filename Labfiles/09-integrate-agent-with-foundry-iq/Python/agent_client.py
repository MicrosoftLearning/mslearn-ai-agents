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

# TODO: Connect to the project and create agent client
# Add your code here to:
# 1. Create DefaultAzureCredential
# 2. Create AIProjectClient using from_connection_string
# 3. Get the agent client
# 4. Create a conversation thread


# Conversation history for context
conversation_history = []


def send_message_to_agent(user_message):
    """
    Send a message to the agent and handle the response.
    """
    try:
        # TODO: Add user message to thread and run the agent
        # Add your code here to:
        # 1. Create a message with the user's input
        # 2. Create and run the agent
        # 3. Poll for completion
        # 4. Retrieve and display the response
        
        # Store in conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        print(f"You: {user_message}\n")
        print("Agent: ", end="", flush=True)
        
        # Your code will go here
        
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
