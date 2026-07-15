---
lab:
    title: 'Task 4 – Add custom function tools'
    description: 'Give an agent tools backed by your own Python functions and process the function-calling loop.'
    level: 300
    concepts: 'function tools, function calling, Microsoft Agent Framework'
    islab: true
    status: 'draft'
---

# Task 4 — Add custom function tools

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Starting here on its own?** First complete [Getting started](A0-getting-started.md) to
> create your Foundry project, clone the starter code, and set up your `.env`.
>
> **This task needs** `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in `Python/.env`. The helper
> file `functions.py` is already in the starter folder. Verify you're ready:
>
> ```
> python setup/check_env.py --task 4
> ```

---

**Goal**: Give an agent tools backed by your **own Python functions**, and process the
function calls it makes.

**Concept reinforced**: the function-calling loop — the agent decides *which* tool to
call and with *what* arguments; your code executes it and returns the result.

**Set up:**

1. Use the same `Labfiles/A-build-and-extend-ai-agents/Python` folder and virtual environment
    you set up in [Getting started](A0-getting-started.md) (reactivate with `.\labenv\Scripts\Activate.ps1` if needed); your
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` in **.env** are already set. Review
    **functions.py**, which contains the trip planner's helper functions.

> **Try it first**: Look at `next_available_trip(region)` in **functions.py**. How would
> you describe its single `region` parameter to the model so it knows when and how to
> call it? Write the JSON schema before revealing the solution.

<details markdown="1">
<summary>Show a solution</summary>

Work through the comments in **functions_agent.py**. Add references and connect to the project (the
same pattern as Task 2). The file is structured so your agent setup runs once, then a
`respond()` function handles each chat message and hands the reply to `run_chat_app()`:

1. **Define the three function tools.** Each schema tells the model how to call one of the
    Python functions — for example the trip lookup tool:

    ```python
    # Define the trip lookup function tool
    trip_tool = FunctionTool(
        name="next_available_trip",
        description="Get the next available guided trip in a given region.",
        parameters={
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')",
                },
            },
            "required": ["region"],
            "additionalProperties": False,
        },
        strict=True,
    )
    ```

    Define `cost_tool` (`calculate_rental_cost`) and `report_tool`
    (`generate_booking_report`) the same way, matching each function's parameters.

2. **Create the agent with all three tools:**

    ```python
    agent = project_client.agents.create_version(
        agent_name="trip-planner-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""You are a trip planning assistant for Trailhead Adventure Works that helps
                customers find guided trips and calculate gear rental costs.
                Use the available tools to assist users with their inquiries.""",
            tools=[trip_tool, cost_tool, report_tool],
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
            if item.name == "next_available_trip":
                result = next_available_trip(**json.loads(item.arguments))
            elif item.name == "calculate_rental_cost":
                result = calculate_rental_cost(**json.loads(item.arguments))
            elif item.name == "generate_booking_report":
                result = generate_booking_report(**json.loads(item.arguments))
            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result,
                )
            )
    ```

    The rest of `respond()` (already provided) sends the outputs back and returns the final
    answer to the chat window:

    ```python
    # Send function call outputs back to the model and retrieve a response
    if input_list:
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )

    return AgentReply(text=response.output_text)
    ```

Run `python functions_agent.py`. Your browser opens the chat window — try a prompt that needs **two**
tools at once:

```
Find me the next trip I can join in Patagonia and give me the cost for 5 days of premium gear rental at priority service.
```

The agent calls both functions in one turn and combines the results, for example:

```
The next trip available in Patagonia is the Patagonia Glacier Trek on February 17th.
The cost for 5 days of premium gear rental at priority service is $1,875.
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
trip-planner assistant.

The difference is the tool definition and the loop. Instead of a hand-written `FunctionTool`
schema, you decorate the function with `@tool` and describe each parameter inline:

```python
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from pydantic import Field
from typing import Annotated

@tool(approval_mode="never_require")
def next_available_trip(
    region: Annotated[str, Field(description="Region to find the next guided trip in (e.g. 'pacific_northwest', 'rockies', 'patagonia')")],
) -> str:
    """Get the next available guided trip in a given region."""
    return functions.next_available_trip(region)
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
    name="trip-planner-agent",
    instructions="You are a trip planning assistant for Trailhead Adventure Works...",
    tools=[next_available_trip, calculate_rental_cost, generate_booking_report],
)

# agent.run() decides which tools to call, runs them, and returns the final answer
result = await agent.run(user_message, session=session)
```

Same result, far less code — because the framework does the plumbing you wrote by hand above.
Writing it yourself first is what makes it clear *what* `agent.run()` is doing for you.

</details>

---

**Next:** [Task 5 — Capstone: build your own MCP server](A5-capstone-build-your-own-mcp-server.md)
