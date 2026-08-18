---
title: 'Task 3 – Connect remote agents with A2A'
lab:
    title: 'Task 3 – Connect remote agents with A2A'
    description: 'Use the Agent-to-Agent (A2A) protocol to connect agents that run in separate processes: a routing agent discovers and delegates to a transfer-title agent and a transfer-outline agent, which collaborate to plan Caldova tech transfers.'
    type: 'task'
    parent: 'C'
    order: 3
    section: 'optional'
    difficulty: 4
    duration: 30
    access: 'open'
    level: 400
    concepts: 'A2A protocol, remote agents, multi-agent orchestration'
    status: 'draft'
---

# Task 3 — Connect remote agents with A2A

*Part of the **Build multi-agent solutions with the Agent Framework** lab. New here? Start with [Getting started](C0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](C0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 3
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Create a discoverable agent** below.

---

So far your agents have lived in a single process. Real systems are often split across services —
each agent runs on its own, and they collaborate over the network. The **Agent-to-Agent (A2A)
protocol** is a standard way for agents to advertise what they can do and send each other work.
In this task you'll build a Caldova transfer-planning system from three remote agents: a
**transfer-title agent** suggests a headline, a **transfer-outline agent** drafts a plan, and a
**routing agent** discovers both and delegates each request to the right one.

<style>
/* "Ask Anton" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
  border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Anton: "; font-weight:700;
  padding-left:1.5em;
  background:url("../Media/anton-avatar.png") left center / 1.25em 1.25em no-repeat; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>What is the A2A protocol?</summary>
<div class="concept-body" markdown="1">

The **Agent-to-Agent (A2A) protocol** lets agents in separate processes discover and call one
another. Each agent publishes an **agent card** — a small document describing its name, skills,
and endpoint — so other agents can find it at runtime. One agent (here, the routing agent) reads
those cards, decides who should handle a request, and sends a message over HTTP; the remote agent
does the work and returns a response.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/agents/overview)

</div>
</details>

Open the `Python` folder and activate the virtual environment from [Getting started](C0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

The starter code for this task is organized into one folder per agent, plus a client and a
launcher:

```output
Python
├── outline_agent/       # remote agent: drafts a transfer plan outline (provided complete)
│   ├── agent.py
│   ├── agent_executor.py
│   └── server.py
├── routing_agent/       # orchestrator that discovers and delegates to the other agents
│   ├── agent.py
│   └── server.py
├── title_agent/         # remote agent: suggests a transfer brief title
│   ├── agent.py
│   ├── agent_executor.py
│   └── server.py
├── client.py            # sends your prompt to the routing agent
└── run_all.py           # launches all three agent servers
```

Each agent folder contains the Foundry agent code and a server to host it. The **routing agent**
discovers and communicates with the **transfer-title** and **transfer-outline** agents. The **client**
lets you submit prompts to the routing agent. `run_all.py` launches all the servers.

> The `outline_agent` (transfer-outline agent) is provided **complete** as a reference — you'll
> build the equivalent code in the `title_agent`, then wire up the `routing_agent`.

### Create a discoverable agent

In this task you complete the transfer-title agent that suggests headlines for Caldova
tech transfers. You also define the agent's skills and card, which the A2A protocol uses to make
the agent discoverable.

> **Tip**: As you add code, keep the indentation aligned with the comments.

1. Open **title_agent/agent.py**.

1. Find the comment **Create the agents client** and add the code to connect to your Foundry project:

    ```python
    # Create the agents client
    self.client = AgentsClient(
        endpoint=os.environ['PROJECT_ENDPOINT'],
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )
    ```

1. Find the comment **Create the title agent** and add the code to create the agent:

    ```python
    # Create the title agent
    self.agent = self.client.create_agent(
        model=os.environ['MODEL_DEPLOYMENT_NAME'],
        name='transfer-title-agent',
        instructions="""
        You are a helpful planning assistant for Caldova.
        Given a site or capability the planner names, suggest a single clear transfer brief title.
        """,
    )
    ```

1. Find the comment **Create a thread for the chat session** and add:

    ```python
    # Create a thread for the chat session
    thread = self.client.threads.create()
    ```

1. Find the comment **Send user message** and add:

    ```python
    # Send user message
    self.client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=user_message)
    ```

1. Find the comment **Create and run the agent** and add:

    ```python
    # Create and run the agent
    run = self.client.runs.create_and_process(thread_id=thread.id, agent_id=self.agent.id)
    ```

    The rest of the file processes and returns the agent's response.

1. Save the file (**Ctrl+S**). Now share the agent's skills and card with the A2A protocol.

1. Open **title_agent/server.py**.

1. Find the comment **Define agent skills** and add:

    ```python
    # Define agent skills
    skills = [
        AgentSkill(
            id='generate_trip_title',
            name='Generate Transfer Title',
            description='Generates a transfer brief title based on a site or capability',
            tags=['title'],
            examples=[
                'Can you give me a title for a packaging transfer at Ashford?',
            ],
        ),
    ]
    ```

1. Find the comment **Create agent card** and add the metadata that makes the agent discoverable:

    ```python
    # Create agent card
    agent_card = AgentCard(
        name='Caldova Transfer Title Agent',
        description='An intelligent title generator agent powered by Foundry. '
        'I can help you generate clear titles for Caldova tech transfers.',
        url=f'http://{host}:{port}/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(),
        skills=skills,
    )
    ```

1. Find the comment **Create agent executor** and add:

    ```python
    # Create agent executor
    agent_executor = create_foundry_agent_executor(agent_card)
    ```

1. Find the comment **Create request handler** and add:

    ```python
    # Create request handler
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )
    ```

1. Find the comment **Create A2A application** and add:

    ```python
    # Create A2A application
    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    ```

    This creates an A2A server that shares the transfer-title agent's information and handles incoming requests using the agent executor.

1. Save the file (**Ctrl+S**).

### Enable messages between the agents

In this task you use the A2A protocol to let the routing agent send messages to the other agents,
and let the transfer-title agent receive them by completing its agent executor.

1. Open **routing_agent/agent.py**.

    The routing agent orchestrates the system: when a user message arrives, it starts a thread,
    uses `create_and_process` to decide which remote agent should handle the request, and routes
    the message to that agent over HTTP with the `send_message` function. The `send_message`
    method is async and must be awaited for the run to complete.

1. Find the comment **Retrieve the remote agent's A2A client using the agent name** and add:

    ```python
    # Retrieve the remote agent's A2A client using the agent name 
    client = self.remote_agent_connections[agent_name]
    ```

1. Find the comment **Construct the payload to send to the remote agent** and add:

    ```python
    # Construct the payload to send to the remote agent
    payload: dict[str, Any] = {
        'message': {
            'role': 'user',
            'parts': [{'kind': 'text', 'text': task}],
            'messageId': message_id,
        },
    }
    ```

1. Find the comment **Wrap the payload in a SendMessageRequest object** and add:

    ```python
    # Wrap the payload in a SendMessageRequest object
    message_request = SendMessageRequest(id=message_id, params=MessageSendParams.model_validate(payload))
    ```

1. Find the comment **Send the message to the remote agent client and await the response** and add:

    ```python
    # Send the message to the remote agent client and await the response
    send_response: SendMessageResponse = await client.send_message(message_request=message_request)
    ```

1. Save the file (**Ctrl+S**). The routing agent can now discover and message the remote agents.
    Next, complete the transfer-title agent's executor so it can handle those incoming messages.

1. Open **title_agent/agent_executor.py**.

    The `AgentExecutor` class must implement `execute` and `cancel`. The `cancel` method is
    provided. The `execute` method uses a `TaskUpdater` object to manage events and signal when
    the task is complete — add the execution logic below.

1. In the `execute` method, find the comment **Process the request** and add:

    ```python
    # Process the request
    await self._process_request(context.message.parts, context.context_id, updater)
    ```

1. In the `_process_request` method, find the comment **Get the title agent** and add:

    ```python
    # Get the title agent
    agent = await self._get_or_create_agent()
    ```

1. Find the comment **Update the task status** and add:

    ```python
    # Update the task status
    await task_updater.update_status(
        TaskState.working,
        message=new_agent_text_message('Title Agent is processing your request...', context_id=context_id),
    )
    ```

1. Find the comment **Run the agent conversation** and add:

    ```python
    # Run the agent conversation
    responses = await agent.run_conversation(user_message)
    ```

1. Find the comment **Update the task with the responses** and add:

    ```python
    # Update the task with the responses
    for response in responses:
        await task_updater.update_status(
            TaskState.working,
            message=new_agent_text_message(response, context_id=context_id),
        )
    ```

1. Find the comment **Mark the task as complete** and add:

    ```python
    # Mark the task as complete
    final_message = responses[-1] if responses else 'Task completed.'
    await task_updater.complete(
        message=new_agent_text_message(final_message, context_id=context_id)
    )
    ```

    The transfer-title agent is now wrapped with an executor that the A2A protocol uses to handle messages.

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and start all three agent servers:

    ```
    az login
    ```

    ```
    python run_all.py
    ```

    The servers start using your authenticated Azure session. Wait until each server reports it's ready.

1. In a **second** terminal (with the virtual environment activated), run the client:

    ```
    python client.py
    ```

1. When prompted, enter a prompt such as:

    ```
    Create a title and outline for a packaging transfer at Ashford.
    ```

    After a few moments, the routing agent delegates to the transfer-title and transfer-outline agents, and you should see a suggested title and a plan outline in the response.

    > **Tip**: If a server fails to start because a port is already in use, stop any earlier run (Ctrl+C in the `run_all.py` terminal) and try again, or change the `*_PORT` values in `.env`.

1. When you're finished, press **Ctrl+C** in the `run_all.py` terminal to stop every server, then enter `deactivate` in each terminal to exit the virtual environment.

> ✅ **Checkpoint**: You've connected agents running in separate processes with the A2A protocol —
> publishing agent cards, routing requests to the right remote agent, and returning their results.

---

**Next (optional):** [Task 4 — Classify and route a support ticket](C4-classify-and-route-a-ticket.md)
