import base64
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# The shared chat UI shell (provided – you don't edit this file)
from trailhead_ui import run_chat_app, AgentReply


OUTPUT_DIR = Path("agent_outputs")
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def get_output_path(filename):
    """Create a unique path for generated files."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    file_name = Path(filename).name
    stem = Path(file_name).stem or "output"
    suffix = Path(file_name).suffix
    output_path = OUTPUT_DIR / file_name

    counter = 1
    while output_path.exists():
        output_path = OUTPUT_DIR / f"{stem}_{counter}{suffix}"
        counter += 1

    return output_path


def save_bytes(file_bytes, filename):
    """Save binary content to a local file."""
    output_path = get_output_path(filename)
    with open(output_path, "wb") as file_handle:
        file_handle.write(file_bytes)
    return output_path


def save_image(image_data, filename):
    """Save base64 image data to a file."""
    return save_bytes(base64.b64decode(image_data), filename)


def download_container_file(openai_client, annotation, downloaded_files):
    """Download a cited container file once and return its local path."""
    cache_key = (annotation.container_id, annotation.file_id)
    if cache_key in downloaded_files:
        return downloaded_files[cache_key]

    file_content = openai_client.containers.files.content.retrieve(
        file_id=annotation.file_id,
        container_id=annotation.container_id,
    )
    output_path = save_bytes(
        file_content.read(),
        annotation.filename or f"{annotation.file_id}.bin",
    )
    downloaded_files[cache_key] = output_path
    return output_path


def format_output_text(content_item, openai_client, downloaded_files):
    """Replace sandbox file citations with local file paths."""
    text = content_item.text or ""
    replacements = []
    referenced_files = set()

    for annotation in content_item.annotations or []:
        if getattr(annotation, "type", "") != "container_file_citation":
            continue

        output_path = download_container_file(openai_client, annotation, downloaded_files)
        replacement_text = f"{annotation.filename} (saved to {output_path})"
        referenced_files.add(output_path)

        start_index = getattr(annotation, "start_index", None)
        end_index = getattr(annotation, "end_index", None)
        if start_index is not None and end_index is not None:
            replacements.append((start_index, end_index, replacement_text))
            continue

        annotated_text = getattr(annotation, "text", "")
        if annotated_text:
            text = text.replace(annotated_text, replacement_text)

    for start_index, end_index, replacement_text in sorted(replacements, reverse=True):
        text = f"{text[:start_index]}{replacement_text}{text[end_index:]}"

    return text, referenced_files


# Initialize the project client
load_dotenv()
project_endpoint = os.environ.get("PROJECT_ENDPOINT")
agent_name = os.environ.get("AGENT_NAME", "trailhead-agent")

if not project_endpoint:
    raise SystemExit(
        "Error: PROJECT_ENDPOINT is not set. Add it to your .env file (see .env.example)."
    )

credential = DefaultAzureCredential()
project_client = AIProjectClient(credential=credential, endpoint=project_endpoint)

# Get the OpenAI client for the Responses API
openai_client = project_client.get_openai_client()

# Load the agent you created in the portal, by name
agent = project_client.agents.get(agent_name=agent_name)

# Create a conversation so the chat keeps context between messages
conversation = openai_client.conversations.create(items=[])


def respond(user_message):
    """Handle one message from the chat window and return the agent's reply."""

    # Add the user's message to the conversation
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )

    # Ask the portal agent to respond (may include analysis and generated charts)
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input="",
    )

    reply_texts = []
    images = []
    downloaded_files = {}
    referenced_files = set()
    image_count = 0

    if getattr(response, "output", None):
        for item in response.output:
            item_type = getattr(item, "type", "")

            if item_type == "message" and getattr(item, "content", None):
                for content_item in item.content:
                    if getattr(content_item, "type", "") != "output_text":
                        continue
                    formatted_text, message_files = format_output_text(
                        content_item, openai_client, downloaded_files
                    )
                    referenced_files.update(message_files)
                    if formatted_text:
                        reply_texts.append(formatted_text)

            elif getattr(item, "text", None):
                reply_texts.append(item.text)

            elif item_type == "image":
                image_count += 1
                if hasattr(item, "image") and hasattr(item.image, "data"):
                    file_path = save_image(item.image.data, f"chart_{image_count}.png")
                    images.append(str(file_path))

        # Any downloaded charts/files that are images should render inline
        for file_path in downloaded_files.values():
            if str(file_path).lower().endswith(IMAGE_SUFFIXES):
                images.append(str(file_path))

    text = "\n\n".join(reply_texts)
    if not text and getattr(response, "output_text", None):
        text = response.output_text

    return AgentReply(text=text, images=images)


# Launch the browser chat window (replaces the old console loop)
run_chat_app(
    respond,
    title="Trailhead Adventure Works Assistant",
    subtitle="Ask about store policy or request an analysis of the weekly sales data.",
)
