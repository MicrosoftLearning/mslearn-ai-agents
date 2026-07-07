import os
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv
from outline_agent.agent_executor import create_foundry_agent_executor
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

load_dotenv()

host = os.environ["SERVER_URL"]
port = os.environ["TITLE_AGENT_PORT"]

# Define agent skills
skills = [
    AgentSkill(
        id='generate_outline',
        name='Generate Outline',
        description='Generates an outline based on a topic',
        tags=['outline'],
        examples=[
            'Can you give me an outline for this article?',
        ],
    ),
]

# Create agent card
agent_card = AgentCard(
    name='AI Foundry Outline Agent',
    description='An intelligent outline generator agent powered by Azure AI Foundry. '
    'I can help you generate outlines for your articles.',
    url=f'http://{host}:{port}/',
    version='1.0.0',
    default_input_modes=['text'],
    default_output_modes=['text'],
    capabilities=AgentCapabilities(streaming=True),
    skills=skills,
)

# Create agent executor
agent_executor = create_foundry_agent_executor(agent_card)

# Create request handler
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor, task_store=InMemoryTaskStore()
)

# Create A2A application
a2a_app = A2AStarletteApplication(
    agent_card=agent_card, http_handler=request_handler
)

# Get routes
routes = a2a_app.routes()

# Add health check endpoint
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse('AI Foundry Outline Agent is running!')

routes.append(Route(path='/health', methods=['GET'], endpoint=health_check))

# Create Starlette app
app = Starlette(routes=routes)

def main():
    # Run the server
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()
