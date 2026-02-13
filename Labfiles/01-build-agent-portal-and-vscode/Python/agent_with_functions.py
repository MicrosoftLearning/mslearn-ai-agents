import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import json
from datetime import datetime

# System status simulator
def check_system_status(system_name: str) -> str:
    """
    Check the status of a system or service.
    
    Args:
        system_name: Name of the system to check (e.g., 'email', 'vpn', 'printer')
    
    Returns:
        JSON string with status information
    """
    # Simulate system status
    systems = {
        "email": {"status": "operational", "uptime": "99.9%"},
        "vpn": {"status": "degraded", "uptime": "95.2%", "issue": "Slow connection speeds"},
        "printer": {"status": "operational", "uptime": "98.5%"},
        "network": {"status": "operational", "uptime": "99.7%"}
    }
    
    system_lower = system_name.lower()
    if system_lower in systems:
        result = {
            "system": system_name,
            "timestamp": datetime.now().isoformat(),
            **systems[system_lower]
        }
    else:
        result = {
            "system": system_name,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "message": "System not found in monitoring"
        }
    
    return json.dumps(result)


def create_support_ticket(issue_type: str, description: str, priority: str = "medium") -> str:
    """
    Create a support ticket for an IT issue.
    
    Args:
        issue_type: Type of issue (e.g., 'hardware', 'software', 'network', 'access')
        description: Detailed description of the issue
        priority: Priority level - 'low', 'medium', or 'high' (default: 'medium')
    
    Returns:
        JSON string with ticket information
    """
    # Simulate ticket creation
    import random
    ticket_id = f"TICKET-{random.randint(10000, 99999)}"
    
    result = {
        "ticket_id": ticket_id,
        "issue_type": issue_type,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "message": f"Support ticket {ticket_id} has been created successfully"
    }
    
    return json.dumps(result)


def main():
    # Initialize the project client
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
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
    agent = project_client.agents.get(agent_name=agent_name)
    print(f"Connected to agent: {agent.name} (id: {agent.id})")
    
    # Create a conversation
    conversation = openai_client.conversations.create(items=[])
    print(f"Conversation created (id: {conversation.id})")
    
    # Function map for execution
    function_map = {
        "check_system_status": check_system_status,
        "create_support_ticket": create_support_ticket
    }
    
    # Chat loop
    print("\n" + "="*60)
    print("IT Support Agent Ready!")
    print("Ask questions or request help. Type 'exit' to quit.")
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
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
            input=""
        )
        
        # Handle function calls if needed
        while True:
            # Check if response needs function execution
            needs_function_call = False
            if hasattr(response, 'output') and response.output:
                for item in response.output:
                    if hasattr(item, 'type') and item.type == 'function_call':
                        needs_function_call = True
                        function_name = item.name
                        function_args = json.loads(item.arguments) if hasattr(item, 'arguments') else {}
                        
                        print(f"\n[Calling function: {function_name}]")
                        
                        # Execute the function
                        if function_name in function_map:
                            function_result = function_map[function_name](**function_args)
                            
                            # Add function result to conversation
                            openai_client.conversations.items.create(
                                conversation_id=conversation.id,
                                items=[{
                                    "type": "function_call_output",
                                    "call_id": item.call_id if hasattr(item, 'call_id') else item.id,
                                    "output": function_result
                                }]
                            )
            
            # If function was called, get new response
            if needs_function_call:
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                    input=""
                )
            else:
                break
        
        # Display response
        if hasattr(response, 'output_text') and response.output_text:
            print(f"\nAgent: {response.output_text}\n")
        elif hasattr(response, 'output') and response.output:
            # Fallback: extract text from output items
            for item in response.output:
                if hasattr(item, 'text'):
                    print(f"\nAgent: {item.text}\n")


if __name__ == "__main__":
    main()
