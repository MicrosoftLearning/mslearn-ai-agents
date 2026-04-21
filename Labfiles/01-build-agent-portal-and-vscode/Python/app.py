import os
import uuid
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Lazy-initialized OpenAI client for the published agent endpoint
_client = None

# Maximum number of messages to retain per conversation to avoid
# unbounded growth and context-window limits.
MAX_HISTORY = 50


def get_openai_client():
    """Initialize the OpenAI client on first use for better error handling."""
    global _client
    if _client is None:
        endpoint = os.environ.get("AGENT_APP_ENDPOINT")

        if not endpoint:
            raise ValueError(
                "AGENT_APP_ENDPOINT environment variable is not set. "
                "Please configure your .env file."
            )

        # TODO: Create a token provider using DefaultAzureCredential with
        # the scope "https://ai.azure.com/.default", then initialize the
        # OpenAI client with the token provider, endpoint, and api-version.

    return _client


# Server-side conversation history: session_id -> list of messages
# Published agents use the stateless Responses API, so the client
# must send full conversation history with each request.
conversations = {}


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/api/conversation", methods=["POST"])
def create_conversation():
    try:
        # Validate credentials eagerly so the user sees errors early
        get_openai_client()
        session_id = str(uuid.uuid4())
        conversations[session_id] = []
        return jsonify({"conversation_id": session_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        session_id = data.get("conversation_id")
        message = data.get("message")

        if not session_id or not message:
            return jsonify({"error": "Missing conversation_id or message"}), 400

        if session_id not in conversations:
            return jsonify({
                "error": "Invalid session. Please start a new chat."
            }), 400

        client = get_openai_client()

        # Append user message to conversation history
        conversations[session_id].append({
            "role": "user",
            "content": message,
        })

        # Trim history to stay within limits
        if len(conversations[session_id]) > MAX_HISTORY:
            conversations[session_id] = conversations[session_id][-MAX_HISTORY:]

        # TODO: Use the client to call the Responses API, passing the full
        # conversation history as the input parameter. Then extract the
        # response and store the assistant's reply in the conversation history
        # so future turns have context.

        return jsonify({"text": "", "citations": [], "images": []})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def extract_response(response):
    """Extract text and citations from the agent response."""
    text = ""
    citations = []

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

                            # Extract citations from file search
                            if (
                                hasattr(content, "annotations")
                                and content.annotations
                            ):
                                for ann in content.annotations:
                                    if getattr(ann, "type", "") == "file_citation":
                                        citations.append({
                                            "filename": getattr(
                                                ann, "filename", "Source"
                                            ),
                                        })
            elif hasattr(item, "text") and item.text:
                text += item.text

    # Fall back to output_text if no structured output was found
    if not text and hasattr(response, "output_text") and response.output_text:
        text = response.output_text

    return {"text": text, "citations": citations, "images": []}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
