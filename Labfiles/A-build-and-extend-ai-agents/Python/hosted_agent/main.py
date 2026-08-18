"""Caldova assistant - hosted agent edition (starter).

Everywhere else in this lab you built *prompt agents*: you described the agent
with a PromptAgentDefinition (model + instructions + tools) and let Foundry run
it for you. Here you package the same assistant as a *hosted agent* - your own
code, running in a Foundry-managed container.

The azure-ai-agentserver-responses library provides the HTTP server, health
checks, and conversation history, so you only write the handler. Fill in the two
blocks marked TODO, then run it with `azd ai agent run` (see A6 in the
instructions). The complete version is in Solution/Python/hosted_agent/main.py.
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

# TODO: Create the Responses client that calls your Foundry model deployment.
#   Build an AIProjectClient(endpoint=_endpoint, credential=DefaultAzureCredential()),
#   then call .get_openai_client().responses on it.
_responses_client = None

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

    # TODO: Call the model with the Caldova system prompt and the input items,
    #   then return the reply. The Responses client is synchronous, so run it off
    #   the event loop with run_in_executor:
    #
    #   response = await asyncio.get_running_loop().run_in_executor(
    #       None,
    #       lambda: _responses_client.create(
    #           model=_model,
    #           instructions=_SYSTEM_PROMPT,
    #           input=input_items,
    #           store=False,
    #       ),
    #   )
    #   return TextResponse(context, request, text=response.output_text)
    raise NotImplementedError("Complete the handler to call the model and return a reply.")


app.run()
