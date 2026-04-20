import os
import base64
from flask import Flask, render_template, request, jsonify
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Lazy-initialized Azure clients
_project_client = None
_openai_client = None
_agent = None


def get_azure_clients():
    """Initialize Azure clients on first use for better error handling."""
    global _project_client, _openai_client, _agent
    if _project_client is None:
        project_endpoint = os.environ.get("PROJECT_ENDPOINT")
        agent_name = os.environ.get("AGENT_NAME", "it-support-agent")

        if not project_endpoint:
            raise ValueError(
                "PROJECT_ENDPOINT environment variable is not set. "
                "Please configure your .env file."
            )

        credential = DefaultAzureCredential()
        _project_client = AIProjectClient(
            credential=credential, endpoint=project_endpoint
        )
        _openai_client = _project_client.get_openai_client()
        _agent = _project_client.agents.get(agent_name=agent_name)

    return _project_client, _openai_client, _agent


# Track valid conversation IDs server-side
active_conversations = set()


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/api/conversation", methods=["POST"])
def create_conversation():
    try:
        _, openai_client, _ = get_azure_clients()
        conversation = openai_client.conversations.create(items=[])
        active_conversations.add(conversation.id)
        return jsonify({"conversation_id": conversation.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        conversation_id = data.get("conversation_id")
        message = data.get("message")

        if not conversation_id or not message:
            return jsonify({"error": "Missing conversation_id or message"}), 400

        if conversation_id not in active_conversations:
            return jsonify({
                "error": "Invalid conversation. Please start a new chat."
            }), 400

        _, openai_client, agent = get_azure_clients()

        # Add user message to the conversation
        openai_client.conversations.items.create(
            conversation_id=conversation_id,
            items=[{
                "type": "message",
                "role": "user",
                "content": message
            }],
        )

        # Get agent response
        response = openai_client.responses.create(
            conversation=conversation_id,
            extra_body={
                "agent_reference": {
                    "name": agent.name,
                    "type": "agent_reference",
                }
            },
            input="",
        )

        result = extract_response(response, openai_client)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_response(response, openai_client):
    """Extract text, citations, and images from the agent response."""
    text = ""
    citations = []
    images = []

    if hasattr(response, "output") and response.output:
        for item in response.output:
            if hasattr(item, "type") and item.type == "message":
                if hasattr(item, "content"):
                    for content in item.content:
                        if (
                            hasattr(content, "type")
                            and content.type == "output_text"
                        ):
                            if hasattr(content, "text"):
                                text = content.text

                            # Extract citations and file references
                            if (
                                hasattr(content, "annotations")
                                and content.annotations
                            ):
                                for ann in content.annotations:
                                    ann_type = getattr(ann, "type", "")
                                    if ann_type == "file_citation":
                                        citations.append({
                                            "filename": getattr(
                                                ann, "filename", "Source"
                                            ),
                                        })
                                    elif ann_type == "container_file_citation":
                                        file_id = getattr(
                                            ann, "file_id", ""
                                        )
                                        filename = getattr(
                                            ann, "filename", ""
                                        )
                                        container_id = getattr(
                                            ann, "container_id", ""
                                        )
                                        _try_download_image(
                                            openai_client,
                                            file_id,
                                            filename,
                                            container_id,
                                            images,
                                        )
            elif hasattr(item, "text") and item.text:
                text += item.text

    # Fall back to output_text if no structured output was found
    if not text and hasattr(response, "output_text") and response.output_text:
        text = response.output_text

    return {"text": text, "citations": citations, "images": images}


def _try_download_image(
    openai_client, file_id, filename, container_id, images
):
    """Download a generated file and add it to the images list if it's an image."""
    if not file_id or not container_id:
        return

    image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".svg")
    if not filename.lower().endswith(image_extensions):
        return

    try:
        file_content = openai_client.containers.files.content.retrieve(
            file_id=file_id, container_id=container_id
        )
        file_bytes = file_content.read()
        b64 = base64.b64encode(file_bytes).decode("utf-8")
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = f"image/{'jpeg' if ext == 'jpg' else ext}"
        images.append({
            "data": f"data:{mime};base64,{b64}",
            "filename": filename,
        })
    except Exception:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
