import os
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Turn on GenAI tracing
os.environ.setdefault("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING", "true")
os.environ.setdefault("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "true")

# A morning's worth of questions from the planning desk.
QUESTIONS = [
    "How long does review take for a capacity request with a complete brief?",
    "How much is five weeks of premium contract capacity at expedited priority?",
    "Which contract manufacturers could fast-track us inside a three-month window?",
]

AGENT_NAME = "caldova-planning-assistant"
INSTRUCTIONS = (
    "You are the Caldova planning assistant. You answer questions from planning "
    "and materials teams about capacity, contract manufacturers, and suppliers. "
    "Keep answers short enough to read between meetings."
)

# Connect to the project
with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Read the Application Insights connection string and start exporting traces
    try:
        connection_string = project_client.telemetry.get_application_insights_connection_string()
    except Exception as error:
        raise SystemExit(
            "Could not read an Application Insights connection string from this project.\n"
            "In the Foundry portal, open your project, select Agents > Traces, and select\n"
            f"Connect to create or connect an Application Insights resource.\n\nDetails: {error}"
        )
    configure_azure_monitor(connection_string=connection_string)

    # Get a tracer for this script
    tracer = trace.get_tracer(__name__)

    # Create the agent staff are talking to
    agent = project_client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=INSTRUCTIONS,
        ),
    )
    print(f"Agent created (name: {agent.name}, version: {agent.version})")

    # Ask each question inside its own span
    with tracer.start_as_current_span("morning-planning-review") as shift_span:
        shift_span.set_attribute("caldova.site", "ashford")
        conversation = openai_client.conversations.create()

        for number, question in enumerate(QUESTIONS, start=1):
            with tracer.start_as_current_span("planner-question") as question_span:
                question_span.set_attribute("caldova.question_number", number)
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=question,
                    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                )
                question_span.set_attribute("caldova.answer_length", len(response.output_text))
                print(f"\nQ{number}: {question}")
                print(f"A{number}: {response.output_text}")

    # Clean up resources by deleting the agent version
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("\nAgent deleted")
