import os
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from title_agent.agent_executor import create_foundry_agent_executor

load_dotenv()

host = os.environ["SERVER_URL"]
port = os.environ["TITLE_AGENT_PORT"]

# Define agent skills


# Create agent card


# Create agent executor


# Create request handler


# Create A2A application


# Get routes
routes = a2a_app.routes()

# Add health check endpoint
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse('AI Foundry Title Agent is running!')

routes.append(Route(path='/health', methods=['GET'], endpoint=health_check))

# Create Starlette app
app = Starlette(routes=routes)

def main():
    # Run the server
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()

