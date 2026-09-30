import os
import json
from dotenv import load_dotenv

# Add references
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from functions import next_visible_event, calculate_observation_cost, generate_observation_report


def main(): 
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Connect to the project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    

        # Define the event function tool
        event_tool = FunctionTool(
            name="next_visible_event",
            description="Get the next visible event in a given location.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')",
                    },
                },
                "required": ["location"],
                "additionalProperties": False,
            },
            strict=True,
        )
        

        # Define the observation cost function tool
        cost_tool = FunctionTool(
            name="calculate_observation_cost",
            description="Calculate the cost of an observation based on the telescope tier, number of hours, and priority level.",
            parameters={
                "type": "object",
                "properties": {
                    "telescope_tier": {
                        "type": "string",
                        "description": "the tier of the telescope (e.g. 'standard', 'advanced', 'premium')",
                    },
                    "hours": {
                        "type": "number",
                        "description": "the number of hours for the observation",
                    },
                    "priority": {
                        "type": "string",
                        "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                    },
                },
                "required": ["telescope_tier", "hours", "priority"],
                "additionalProperties": False,
            },
            strict=True,
        )
        

        # Define the observation report generation function tool
        report_tool = FunctionTool(
            name="generate_observation_report",
            description="Generate a report summarizing an astronomical observation",
            parameters={
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "description": "the name of the astronomical event being observed",
                    },
                    "location": {
                        "type": "string",
                        "description": "the location of the observer",
                    },
                    "telescope_tier": {
                        "type": "string",
                        "description": "the tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')",
                    },
                    "hours": {
                        "type": "number",
                        "description": "the number of hours the telescope was used for the observation",
                    },
                    "priority": {
                        "type": "string",
                        "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
                    },
                    "observer_name": {
                        "type": "string",
                        "description": "the name of the person who conducted the observation",
                    },                   
                },
                "required": ["event_name", "location", "telescope_tier", "hours", "priority", "observer_name"],
                "additionalProperties": False,
            },
            strict=True,
        )
                

        # Create a new agent with the function tools
        agent = project_client.agents.create_version(
            agent_name="astronomy-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions=
                    """You are an astronomy observations assistant that helps users find 
                    information about astronomical events and calculate telescope rental costs. 
                    Use the available tools to assist users with their inquiries.""",
                tools=[event_tool, cost_tool, report_tool],
            ),
        )
                
                
        # Create a thread for the chat session
        conversation = openai_client.conversations.create()
                

        while True:
            user_input = input("Enter a prompt for the astronomy agent. Use 'quit' to exit.\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("Exiting chat.")
                break

            # Create a list to hold function call outputs that will be sent back as input to the agent
            input_list: ResponseInputParam = []            

            # Send a prompt to the agent
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )
           
        
            # Retrieve the agent's response, which may include function calls
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                input=input_list,
            )

            # Check the run status for failures
            if response.status == "failed":
                print(f"Response failed: {response.error}")


            # Process function calls
            for item in response.output:
                if item.type == "function_call":
                    # Retrieve the matching function tool
                    function_name = item.name
                    result = None
                    if item.name == "next_visible_event":
                        result = next_visible_event(**json.loads(item.arguments))
                    elif item.name == "calculate_observation_cost":
                        result = calculate_observation_cost(**json.loads(item.arguments))
                    elif item.name == "generate_observation_report":
                        result = generate_observation_report(**json.loads(item.arguments))

                    # Append the output text
                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=result,
                        )
                    )
            

            # Send function call outputs back to the model and retrieve a response
            if input_list:
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=input_list,
                    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                )
            # Display the agent's response
            print(f"AGENT: {response.output_text}")            

        # Delete the agent when done
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Deleted agent.")
        

if __name__ == '__main__': 
    main()