"""
Tailwind Traders - Support Triage workflow, web chat edition (optional).

This is the same workflow invocation as `workflow.py`, but instead of printing to
the console it runs behind the shared Gradio chat shell (`tailwind_ui.py`). Type any
message in the browser (for example, "Start processing support tickets") and the
assistant runs the portal workflow and shows the classified, routed tickets inline.

You focus on the workflow code; you don't edit `tailwind_ui.py`.
"""

import os, json, re
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from tailwind_ui import run_chat_app

# The workflow you built and saved in the Foundry portal
workflow = {
    "name": "Tailwind-Traders-Support-Triage"
}

_openai_client = None


def get_openai_client():
    """Create the OpenAI client lazily so the module can be imported without Azure."""
    global _openai_client
    if _openai_client is None:
        load_dotenv()
        endpoint = os.environ["PROJECT_ENDPOINT"]
        credential = DefaultAzureCredential()
        project_client = AIProjectClient(endpoint=endpoint, credential=credential)
        _openai_client = project_client.get_openai_client()
    return _openai_client


def format_workflow_output(output_text):
    """Turn the raw workflow output into readable markdown for the chat window."""
    tickets = re.findall(r"(\{.*?\})(.*?)(?=\{|$)", output_text, re.DOTALL)

    if not tickets:
        return output_text

    lines = []
    for ticket_number, (ticket_json, response_text) in enumerate(tickets, start=1):
        ticket = json.loads(ticket_json)
        lines.append(f"### Ticket {ticket_number}: {ticket['category']} ({ticket['confidence']:.0%} confidence)")
        lines.append(f"**Issue:** {ticket['customer_issue']}")
        lines.append(f"**Response:** {response_text.strip()}")
        lines.append("")
    return "\n".join(lines).strip()


def respond(user_message):
    """Run the portal workflow once and return its formatted output."""
    openai_client = get_openai_client()
    conversation = openai_client.conversations.create()
    try:
        stream = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": workflow["name"], "type": "agent_reference"}},
            input="Start",
            stream=True,
        )

        replies = []
        for event in stream:
            if event.type == "response.completed":
                response = openai_client.responses.retrieve(event.response.id)
                replies.append(format_workflow_output(response.output_text))

        return "\n\n".join(replies) if replies else "The workflow did not return any output."
    finally:
        openai_client.conversations.delete(conversation_id=conversation.id)


if __name__ == "__main__":
    run_chat_app(respond, title="Tailwind Traders Support Triage")
