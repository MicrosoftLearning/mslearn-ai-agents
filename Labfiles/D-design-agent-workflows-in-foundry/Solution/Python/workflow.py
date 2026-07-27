import os, json, re
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def print_workflow_output(output_text):
    tickets = re.findall(r"(\{.*?\})(.*?)(?=\{|$)", output_text, re.DOTALL)

    if not tickets:
        print(output_text)
        return

    for ticket_number, (ticket_json, response_text) in enumerate(tickets, start=1):
        ticket = json.loads(ticket_json)

        print("\n" + "=" * 80)
        print(f"Ticket {ticket_number}: {ticket['category']} ({ticket['confidence']:.0%} confidence)")
        print("-" * 80)
        print(f"Issue: {ticket['customer_issue']}")
        print("\nResponse:")
        print(response_text.strip())
    print("=" * 80 + "\n")

load_dotenv()
endpoint = os.environ["PROJECT_ENDPOINT"]

# Connect to the AI Project client
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # Specify the workflow
    workflow = {
        "name": "Tailwind-Traders-Support-Triage"
    }

    # Create a conversation and run the workflow
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    stream = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": workflow["name"], "type": "agent_reference"}},
        input="Start",
        stream=True,
    )

    # Process events from the workflow run
    for event in stream:
        if (event.type == "response.completed"):
            print("\nResponse completed:")
            response = openai_client.responses.retrieve(event.response.id)
            print_workflow_output(response.output_text)

    # Clean up resources
    openai_client.conversations.delete(conversation_id=conversation.id)
    print("\nConversation deleted")
