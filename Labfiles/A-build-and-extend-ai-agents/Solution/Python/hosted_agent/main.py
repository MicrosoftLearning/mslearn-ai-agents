"""Caldova assistant - hosted agent edition (complete reference).

Everywhere else in this lab you built *prompt agents*: you described the agent
with a PromptAgentDefinition (model + instructions + tools) and let Foundry run
it for you. This file is the same assistant packaged as a *hosted agent* - your
own code, running in a Foundry-managed container.

The azure-ai-agentserver-responses library turns this file into a web service
that speaks the Responses protocol: it provides the HTTP server, health checks,
and conversation history, so you only write the handler. Inside the handler you
forward the user's message to a Foundry model with the Caldova system prompt.

Run and deploy it with the Azure Developer CLI (see A6 in the instructions):
    azd ai agent run          # test locally
    azd deploy                # deploy to Foundry Agent Service
"""

import asyncio
import logging
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    ResponsesServerOptions,
    TextResponse,
)
from azure.ai.agentserver.responses.models import (
    MessageContentInputTextContent,
    MessageContentOutputTextContent,
)

logger = logging.getLogger(__name__)

# In a hosted container these are injected for you. Locally, `azd ai agent run`
# sets FOUNDRY_PROJECT_ENDPOINT; set the model name in .env (see .env.example).
_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
_model = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

# The Responses client that calls your Foundry model deployment.
_responses_client = (
    AIProjectClient(endpoint=_endpoint, credential=DefaultAzureCredential())
    .get_openai_client()
    .responses
)

# The hosting library. It runs the web server and manages conversation history.
app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(default_fetch_history_count=20),
)

# The same assistant instructions you used for your prompt agents.
_SYSTEM_PROMPT = (
    "You are the Caldova supply chain assistant. You help planning and "
    "materials teams with questions about capacity, contract manufacturers, and materials. "
    "Always be friendly and concise. If you don't know the answer, say so and suggest "
    "contacting the support team directly."
)

_ROLE_MAP = {
    MessageContentOutputTextContent: "assistant",
    MessageContentInputTextContent: "user",
}


def _build_input(current_input: str, history: list) -> list:
    """Convert platform history + the current message into Responses API input."""
    items = []
    for item in history:
        for content in getattr(item, "content", None) or []:
            role = _ROLE_MAP.get(type(content))
            if role and content.text:
                items.append({"role": role, "content": content.text})
    items.append({"role": "user", "content": current_input})
    return items


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    _cancellation_signal: asyncio.Event,
):
    """Handle one turn: forward the user's message to the model and reply."""
    user_input = await context.get_input_text() or "Hello!"
    history = await context.get_history()
    input_items = _build_input(user_input, history)

    # The Responses client is synchronous, so run it off the event loop.
    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda: _responses_client.create(
            model=_model,
            instructions=_SYSTEM_PROMPT,
            input=input_items,
            store=False,
        ),
    )

    return TextResponse(context, request, text=response.output_text)


app.run()
