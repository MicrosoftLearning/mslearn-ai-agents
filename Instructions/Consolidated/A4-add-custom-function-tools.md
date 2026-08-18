---
title: 'Task 4 – Add custom function tools'
lab:
    title: 'Task 4 – Add custom function tools'
    description: 'Give an agent tools backed by your own Python functions and process the function-calling loop.'
    type: 'task'
    parent: 'A'
    order: 4
    section: 'optional'
    difficulty: 3
    duration: 25
    access: 'open'
    level: 300
    concepts: 'function tools, function calling, Microsoft Agent Framework'
    status: 'draft'
---

# Task 4 — Add custom function tools

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project and the starter code. If you
> haven't already, complete [Getting started](A0-getting-started.md) to create your project,
> clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`. The
> helper file `functions.py` is already in the starter folder. Then, from the `Python` folder
> you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 4
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to reviewing **functions.py** in **Set up** below.

---

**Goal**: Give an agent tools backed by your **own Python functions**, and process the
function calls it makes.

**Concept reinforced**: the function-calling loop — the agent decides *which* tool to
call and with *what* arguments; your code executes it and returns the result.

**Set up:**

1. In the `Labfiles/A-build-and-extend-ai-agents/Python` folder, activate the virtual
    environment (`.\labenv\Scripts\Activate.ps1`) and confirm `PROJECT_ENDPOINT` and
    `MODEL_DEPLOYMENT_NAME` are set in **.env** (see [Getting started](A0-getting-started.md)).
    Then review **functions.py**, which contains the capacity planner's helper functions.

> **Try it first**: Look at `next_available_slot(site)` in **functions.py**. How would
> you describe its single `site` parameter to the model so it knows when and how to
> call it? Write the JSON schema before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Work through the comments in **functions_agent.py**. Add references and connect to the project (the
same pattern as Task 2). The file is structured so your agent setup runs once, then a
`respond()` function handles each chat message and hands the reply to `run_chat_app()`:

1. **Define the three function tools.** Each schema tells the model how to call one of the
    Python functions — for example the slot lookup tool:

    ```python
    # Define the slot lookup function tool
    slot_tool = FunctionTool(
        name="next_available_slot",
        description="Get the next open production slot at a given site.",
        parameters={
            "type": "object",
            "properties": {
                "site": {
                    "type": "string",
                    "description": "site to find the next open production slot at (e.g. 'ashford', 'brightwater', 'calderwood')",
                },
            },
            "required": ["site"],
            "additionalProperties": False,
        },
        strict=True,
    )
    ```

    Define `cost_tool` (`calculate_transfer_cost`) and `report_tool`
    (`generate_capacity_report`) the same way, matching each function's parameters.

2. **Create the agent with all three tools:**

    ```python
    agent = project_client.agents.create_version(
        agent_name="capacity-planner-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""You are a capacity planning assistant for Caldova that helps
                planners find open production slots and estimate contract manufacturing costs.
                Use the available tools to assist users with their inquiries.""",
            tools=[slot_tool, cost_tool, report_tool],
        ),
    )
    ```

3. **Fill in the tool-calling loop** inside `respond()` — read each `function_call` from the
    response, run the matching Python function, and collect a `FunctionCallOutput`:

    ```python
    # Process function calls
    for item in response.output:
        if item.type == "function_call":
            result = None
            if item.name == "next_available_slot":
                result = next_available_slot(**json.loads(item.arguments))
            elif item.name == "calculate_transfer_cost":
                result = calculate_transfer_cost(**json.loads(item.arguments))
            elif item.name == "generate_capacity_report":
                result = generate_capacity_report(**json.loads(item.arguments))
            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result,
                )
            )
    ```

    The rest of `respond()` (already provided) sends the outputs back and returns the final
    answer to the chat window. Note that it attaches the outputs to the same **conversation**
    so the tool calls are resolved in conversation state — sending them back with
    `previous_response_id` instead would make the *next* message fail with *"No tool output
    found for function call"*:

    ```python
    # Send function call outputs back to the model and retrieve a response
    if input_list:
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=input_list,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)
    ```

Run `python functions_agent.py`. Your browser opens the chat window — try a prompt that needs **two**
tools at once:

```
Find me the next open slot at Brightwater and give me the cost for 5 weeks of premium contract capacity at expedited priority.
```

The agent calls both functions in one turn and combines the results, for example:

```
The next open slot at Brightwater is the Line 3 Changeover on March 3rd.
The cost for 5 weeks of premium contract capacity at expedited priority is $1,875K.
```

Close the browser tab and press **Ctrl+C** in the terminal to stop the app (the agent is
deleted automatically on exit).

</details>

**Stretch**: add a fourth function tool of your own and update the instructions to mention it.

<details markdown="1">
<summary>Compare: the same agent with the Microsoft Agent Framework</summary>

You just wrote two schemas per tool and a dispatch loop that matches each `function_call` to a
Python function. The **Microsoft Agent Framework** removes both. Open **functions_agent_maf.py**
(provided complete) and run it with `python functions_agent_maf.py` — it produces the *same*
capacity-planner assistant.

The difference is the tool definition and the loop. Instead of a hand-written `FunctionTool`
schema, you decorate the function with `@tool` and describe each parameter inline:

```python
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field
from typing import Annotated

@tool(approval_mode="never_require")
def next_available_slot(
    site: Annotated[str, Field(description="Site to find the next open production slot at (e.g. 'ashford', 'brightwater', 'calderwood')")],
) -> str:
    """Get the next open production slot at a given site."""
    return functions.next_available_slot(site)
```

Then you create the agent with the decorated functions and let `agent.run()` handle the whole
tool-calling loop — no reading `response.output`, no matching names, no sending outputs back:

```python
agent = Agent(
    client=FoundryChatClient(
        project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        credential=AzureCliCredential(),
    ),
    name="capacity-planner-agent",
    instructions="You are a capacity planning assistant for Caldova...",
    tools=[next_available_slot, calculate_transfer_cost, generate_capacity_report],
)

# agent.run() decides which tools to call, runs them, and returns the final answer
result = await agent.run(user_message, session=session)
```

Same result, far less code — because the framework does the plumbing you wrote by hand above.
Writing it yourself first is what makes it clear *what* `agent.run()` is doing for you.

</details>

---

**Next:** [Task 5 — Capstone: build your own MCP server](A5-capstone-build-your-own-mcp-server.md)
