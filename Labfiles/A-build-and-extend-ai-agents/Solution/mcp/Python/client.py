import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from contoso_ui import run_chat_app, AgentReply

# Add references
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client (kept open for the app's lifetime)
credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
openai_client = project_client.get_openai_client()

# Shared state, set up once on the first message so the MCP session is created
# on the same event loop the chat window uses.
exit_stack = AsyncExitStack()
session = None
agent = None
conversation = None
functions_dict = {}


async def setup():
    """Connect to the MCP server, discover its tools, and create the agent (runs once)."""
    global session, agent, conversation, functions_dict
    if session is not None:
        return

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None,
    )

    # Start the MCP server and create a client session
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    # Initialize the session and list the available tools
    await session.initialize()
    tools = (await session.list_tools()).tools
    print("Connected to server with tools:", [tool.name for tool in tools])

    # Build a function for each tool
    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result

        tool_func.__name__ = tool_name
        return tool_func

    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}

    # Create FunctionTool definitions for the agent
    mcp_function_tools = []
    for tool in tools:
        function_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            parameters={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            strict=True,
        )
        mcp_function_tools.append(function_tool)

    # Create the agent
    agent = project_client.agents.create_version(
        agent_name="inventory-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""
            You are an inventory assistant. Here are some general guidelines:
            - Recommend restock if item inventory < 10 and weekly sales > 15
            - Recommend clearance if item inventory > 20 and weekly sales < 5
            """,
            tools=mcp_function_tools,
        ),
    )

    # Create a thread for the chat session
    conversation = openai_client.conversations.create()


async def respond(user_message):
    """Handle one message from the chat window and return the agent's reply."""
    await setup()

    # Send the user's prompt to the agent
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )

    # Retrieve the agent's response, which may include function calls to the MCP server tools
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input=[],
    )

    if response.status == "failed":
        return AgentReply(text=f"Response failed: {response.error}")

    # Create an input list to hold function call outputs to send back to the model
    input_list: ResponseInputParam = []

    # Process function calls
    for item in response.output:
        if item.type == "function_call":
            # Retrieve the matching function tool
            function_name = item.name
            kwargs = json.loads(item.arguments)
            required_function = functions_dict.get(function_name)

            # Invoke the function
            output = await required_function(**kwargs)

            # Append the output text
            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=output.content[0].text,
                )
            )

    # Send function call outputs back to the model and retrieve a response
    if input_list:
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)


if __name__ == "__main__":
    try:
        run_chat_app(
            respond,
            title="Contoso Adventure Works Assistant",
            subtitle="Warehouse inventory & weekly sales",
        )
    finally:
        # Delete the agent when the app closes
        if agent is not None:
            print("Cleaning up agents:")
            project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
            print("Deleted inventory agent.")
