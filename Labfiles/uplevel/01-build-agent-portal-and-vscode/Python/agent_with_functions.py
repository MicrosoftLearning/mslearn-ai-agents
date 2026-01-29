import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool
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


# Function definitions for the agent
functions = [
    FunctionTool(
        name="check_system_status",
        description="Check the status of a system or service",
        parameters={
            "type": "object",
            "properties": {
                "system_name": {
                    "type": "string",
                    "description": "Name of the system to check (e.g., 'email', 'vpn', 'printer')"
                }
            },
            "required": ["system_name"]
        }
    ),
    FunctionTool(
        name="create_support_ticket",
        description="Create a support ticket for an IT issue",
        parameters={
            "type": "object",
            "properties": {
                "issue_type": {
                    "type": "string",
                    "description": "Type of issue",
                    "enum": ["hardware", "software", "network", "access"]
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue"
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level",
                    "enum": ["low", "medium", "high"],
                    "default": "medium"
                }
            },
            "required": ["issue_type", "description"]
        }
    )
]


def main():
    # Initialize the project client
    project_endpoint = os.environ.get("PROJECT_ENDPOINT")
    
    if not project_endpoint:
        print("Error: PROJECT_ENDPOINT environment variable not set")
        print("Please set it in your .env file or environment")
        return
    
    print("Connecting to Microsoft Foundry project...")
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=project_endpoint,
        credential=credential
    )
    
    # Get the agent
    agent_name = "it-support-agent"
    print(f"Loading agent: {agent_name}")
    
    # Create agent with functions
    agent = project_client.agents.create_agent(
        model="gpt-4.1",
        name=agent_name,
        instructions="""You are an IT Support Agent for Contoso Corporation.
        You help employees with technical issues and IT policy questions.
        
        You have access to these tools:
        - check_system_status: Check if systems are operational
        - create_support_ticket: Create support tickets for issues
        
        Use these tools when appropriate to help users.""",
        tools=functions
    )
    
    print(f"Agent created with ID: {agent.id}")
    
    # Create a thread for conversation
    thread = project_client.agents.create_thread()
    print(f"Thread created with ID: {thread.id}")
    
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
        
        # Add user message to thread
        project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        
        # Run the agent
        run = project_client.agents.create_run(
            thread_id=thread.id,
            agent_id=agent.id
        )
        
        # Wait for completion and handle function calls
        while run.status in ["queued", "in_progress", "requires_action"]:
            run = project_client.agents.get_run(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run.status == "requires_action":
                tool_outputs = []
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"\n[Calling function: {function_name}]")
                    
                    # Execute the function
                    if function_name in function_map:
                        function_result = function_map[function_name](**function_args)
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": function_result
                        })
                
                # Submit tool outputs
                project_client.agents.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            
            import time
            time.sleep(1)
        
        # Get the response
        messages = project_client.agents.list_messages(thread_id=thread.id)
        
        # Display the latest assistant message
        for message in messages:
            if message.role == "assistant":
                for content in message.content:
                    if hasattr(content, 'text'):
                        print(f"\nAgent: {content.text.value}\n")
                break


if __name__ == "__main__":
    main()
