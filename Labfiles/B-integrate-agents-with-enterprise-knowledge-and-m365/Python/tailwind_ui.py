"""
Tailwind Traders – shared chat UI shell (provided).

You don't need to edit this file. It gives every task in the lab the same simple
web chat window so your agent feels like a real app instead of a console script.

Each task provides a `respond` function that takes the user's message and returns
either a plain string, or an `AgentReply` carrying text plus any image files to
show inline (for example, a chart produced by the code interpreter). The function
may be synchronous or asynchronous (Task 5 uses an async one for the MCP session).
"""

import inspect
from dataclasses import dataclass, field
from typing import Callable

import gradio as gr


@dataclass
class AgentReply:
    """A single reply from the agent."""
    text: str = ""
    images: list = field(default_factory=list)  # local image file paths to display inline


def run_chat_app(
    respond: Callable,
    title: str = "Tailwind Traders Assistant",
    subtitle: str = "",
    placeholder: str = "Ask the assistant...",
    server_port: int = 7860,
):
    """Launch a browser chat window that routes each message to `respond`."""

    async def handle(user_message, history):
        history = (history or []) + [{"role": "user", "content": user_message}]

        # Call the task's respond function (await it if it's async)
        result = respond(user_message)
        if inspect.isawaitable(result):
            result = await result

        if isinstance(result, str):
            result = AgentReply(text=result)

        if result and result.text:
            history.append({"role": "assistant", "content": result.text})
        for image_path in (result.images if result else []):
            history.append({"role": "assistant", "content": {"path": image_path}})

        return history, ""

    with gr.Blocks(title=title) as demo:
        gr.Markdown(f"## \U0001F3D4\uFE0F {title}")
        if subtitle:
            gr.Markdown(subtitle)
        chatbot = gr.Chatbot(height=460, show_label=False)
        with gr.Row():
            textbox = gr.Textbox(
                placeholder=placeholder, show_label=False, scale=8, autofocus=True
            )
            send = gr.Button("Send", variant="primary", scale=1)

        for trigger in (textbox.submit, send.click):
            trigger(handle, [textbox, chatbot], [chatbot, textbox])

    demo.launch(server_port=server_port, inbrowser=True, css="footer {visibility: hidden}", theme=gr.themes.Soft())
