import os
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, ConnectedAgentTool



# Clear the console
os.system('cls' if os.name=='nt' else 'clear')

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


# Connect to the AI Project client
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
):

    # Create an agent to prioritize support tickets
    priority_agent_name = "priority_agent"
    priority_agent_instructions = """
    Assess how urgent a ticket is based on its description.

    Respond with one of the following levels:
    - High: User-facing or blocking issues
    - Medium: Time-sensitive but not breaking anything
    - Low: Cosmetic or non-urgent tasks

    Only output the urgency level and a very brief explanation.
    """

    priority_agent = project_client.agents.create_version(
        agent_name=priority_agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=priority_agent_instructions
        ),
    )

    # Create an agent to assign tickets to the appropriate team
    team_agent_name = "team_agent"
    team_agent_instructions = """
    Decide which team should own each ticket.

    Choose from the following teams:
    - Frontend
    - Backend
    - Infrastructure
    - Marketing

    Base your answer on the content of the ticket. Respond with the team name and a very brief explanation.
    """

    team_agent = project_client.agents.create_version(
        agent_name=team_agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=team_agent_instructions
        ),
    )

    # Create an agent to estimate effort for a support ticket
    effort_agent_name = "effort_agent"
    effort_agent_instructions = """
    Estimate how much work each ticket will require.

    Use the following scale:
    - Small: Can be completed in a day
    - Medium: 2-3 days of work
    - Large: Multi-day or cross-team effort

    Base your estimate on the complexity implied by the ticket. Respond with the effort level and a brief justification.
    """

    effort_agent = project_client.agents.create_version(
        agent_name=effort_agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=effort_agent_instructions
        ),
    )

    # Create connected agent tools for the support agents
    priority_agent_tool = ConnectedAgentTool(
        id=priority_agent.id, 
        name=priority_agent_name, 
        description="Assess the priority of a ticket"
    )
    
    team_agent_tool = ConnectedAgentTool(
        id=team_agent.id, 
        name=team_agent_name, 
        description="Determines which team should take the ticket"
    )
    
    effort_agent_tool = ConnectedAgentTool(
        id=effort_agent.id, 
        name=effort_agent_name, 
        description="Determines the effort required to complete the ticket"
    )
    
    # Create an agent to triage support ticket processing by using connected agents
    triage_agent_name = "triage-agent"
    triage_agent_instructions = """
    Triage the given ticket. Use the connected tools to determine the ticket's priority, 
    which team it should be assigned to, and how much effort it may take.
    """

    triage_agent = project_client.agents.create_version(
        agent_name=triage_agent_name,
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=triage_agent_instructions,
            tools=[
                priority_agent_tool.definitions[0],
                team_agent_tool.definitions[0],
                effort_agent_tool.definitions[0]
            ]
        ),
    )
    
    # Use the agents to triage a support issue
    with project_client.get_openai_client() as openai_client:
        print("Creating conversation.")
        conversation = openai_client.conversations.create()

        # Create the ticket prompt
        prompt = input("\nWhat's the support problem you need to resolve?: ")
        
        # Send a prompt to the agent
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": prompt}],
        )
        
        # Run the conversation using the primary agent
        print("\nProcessing agent response. Please wait.")
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": triage_agent.name, "type": "agent_reference"}},
            input="",
        )
            
        if response.status == "failed":
            print(f"Response failed: {response.error}")

        # Fetch and display messages
        items = openai_client.conversations.items.list(conversation_id=conversation.id)
        for item in items.data:
            if item.type == "message":
                role = item.role.upper()
                content = item.content[0].text.value if item.content and item.content[0].type == "text" else ""
                print(f"{role}:\n{content}\n")
        
        # Clean up conversation
        openai_client.conversations.delete(conversation_id=conversation.id)
        print("Conversation deleted")

    # Clean up
    print("Cleaning up agents:")
    project_client.agents.delete_version(agent_name=triage_agent.name, agent_version=triage_agent.version)
    print("Deleted triage agent.")
    project_client.agents.delete_version(agent_name=priority_agent.name, agent_version=priority_agent.version)
    print("Deleted priority agent.")
    project_client.agents.delete_version(agent_name=team_agent.name, agent_version=team_agent.version)
    print("Deleted team agent.")
    project_client.agents.delete_version(agent_name=effort_agent.name, agent_version=effort_agent.version)
    print("Deleted effort agent.")

