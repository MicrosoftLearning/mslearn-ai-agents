---
title: 'Task 5 – Capstone: build your own MCP server'
lab:
    title: 'Task 5 – Capstone: build your own MCP server'
    description: 'Capstone: build your own MCP server and combine it with your function tools into one Caldova assistant.'
    type: 'task'
    parent: 'A'
    order: 5
    section: 'optional'
    difficulty: 4
    duration: 35
    access: 'open'
    level: 400
    concepts: 'MCP server, tool orchestration, Microsoft Agent Framework'
    status: 'draft'
---

# Task 5 — Capstone: build your own MCP server

*Part of the **Build and extend AI agents** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **Set up (start here):** This is the **capstone**. It needs a Foundry project and the
> starter code. If you haven't already, complete [Getting started](A0-getting-started.md) to
> create your project, clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`
> in `Python/.env`. It reuses `functions.py` from [Task 4](A4-add-custom-function-tools.md) —
> already in the starter folder, so you don't need to have finished Task 4. Then, from the
> `Python` folder you opened in VS Code, verify:

```
python ../setup/check_env.py --task 5
```

> **Continuing from a previous task?** If you just finished an earlier task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Set up** below to start editing `server.py` and `client.py`.

---

**Goal**: Host your **own** tools on an MCP server, then bring the lab together into a single
**Caldova Supply Chain Assistant** — one agent that both **plans capacity and estimates transfers**
(the function tools from Task 4) *and* **checks live material stock and consumption** (the tools
you host here).

**Concept reinforced**: the MCP server/client split — a server *registers* tools; a client
*discovers and calls* them — plus how one agent can hold **more than one kind of tool** at
once. In `respond()` you *route* each call to the right place: local Python functions run
in-process, MCP tools run over the server session.

> **How this builds on Task 4**: This capstone *combines* the capacity-planner tools from Task 4
> with a new MCP server. You don't need to have finished Task 4 — those tools
> (`next_available_slot`, `calculate_transfer_cost`, `generate_capacity_report`) are provided
> ready-made in `client.py` — so you can focus on the new work: hosting your MCP server and
> *combining* both tool sets on one agent. (Already did Task 4? Even better — you'll recognize them.)

**Set up:**

1. In the `Labfiles/A-build-and-extend-ai-agents/Python` folder, activate the virtual
    environment (`.\labenv\Scripts\Activate.ps1`) and confirm your **.env** has
    `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME` (see [Getting started](A0-getting-started.md)).
    You'll edit **server.py** and **client.py**.

> **Try it first**: Wire up **server.py** and **client.py** using the comments in each file.
> As you go, consider: why must diagnostic output go to `stderr` (or be suppressed) rather
> than `stdout`? *(Hint: MCP speaks JSON-RPC over stdio, so anything printed to stdout is
> parsed as protocol messages — a stray banner corrupts the stream. That's why the server
> starts with `show_banner=False`.)* And: once the agent has **both** tool sets, how does
> your code know whether a given `function_call` should run a local function or an MCP tool?

<details markdown="1">
<summary>Show a solution</summary>

**In `server.py`** — create the server and expose the two provided functions as tools:

```python
# Add references
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Inventory")

@mcp.tool()
def get_inventory_levels() -> dict:
    ...  # returns the sample inventory dict already in the file

@mcp.tool()
def get_weekly_consumption() -> dict:
    ...  # returns the sample consumption dict already in the file

# Run the MCP server
mcp.run(show_banner=False)
```

**In `client.py`** — connect to the server, discover its tools, register them **alongside**
the capacity-planner tools on one agent, then route each call in `respond()`. Because the chat UI
runs on an async event loop, the connection code lives in an async `setup()` that runs once on
the first message.

1. Add the MCP references at the top of the file:

    ```python
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    ```

    The `capacity_planner_tools` list and the `local_functions` dispatch dict (the Task 4 tools)
    are already provided near the top of the file — you don't need to rewrite them.

2. Inside `setup()`, start the server over stdio and open a session, then list the available
    tools and wrap each as a callable:

    ```python
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    tools = (await session.list_tools()).tools

    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            return await session.call_tool(tool_name, kwargs)
        tool_func.__name__ = tool_name
        return tool_func

    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}

    mcp_function_tools = [
        FunctionTool(
            name=tool.name,
            description=tool.description,
            parameters={"type": "object", "properties": {}, "additionalProperties": False},
            strict=True,
        )
        for tool in tools
    ]
    ```

3. Create the agent with **both** tool sets — the capacity planner *and* the materials tools:

    ```python
    agent = project_client.agents.create_version(
        agent_name="caldova-assistant",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""
            You are the Caldova supply chain assistant. You help planners find open
            production capacity and estimate contract manufacturing costs, and you help
            the materials team check live stock and consumption.

            Capacity planning and transfers:
            - Use the slot and transfer tools to find open capacity, estimate cost, and draft capacity requests.

            Material inventory:
            - Recommend reorder if material inventory < 10 and weekly consumption > 15
            - Flag for review if material inventory > 20 and weekly consumption < 5
            """,
            tools=[*capacity_planner_tools, *mcp_function_tools],
        ),
    )
    ```

4. In `respond()`, route each `function_call` to the right executor — local functions run
    directly (they return a string); MCP tools are awaited over the session:

    ```python
    for item in response.output:
        if item.type == "function_call":
            kwargs = json.loads(item.arguments)

            if item.name in local_functions:
                output_text = local_functions[item.name](**kwargs)          # Task 4 function
            else:
                result = await functions_dict[item.name](**kwargs)          # your MCP tool
                output_text = result.content[0].text

            input_list.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=output_text,
                )
            )

    # ...send outputs back, then:
    return AgentReply(text=response.output_text)
    ```

Run `python client.py`. Your browser opens the chat window — the server is launched for you
over stdio on the first message. Now try a prompt that exercises **both** halves of the
assistant in one conversation:

```
Plan capacity: find the next open slot at Brightwater and price 5 weeks of premium contract capacity at expedited priority.
```
```
Now check materials — are there any we should reorder?
```

The first prompt calls your Task 4 capacity-planner functions; the second calls your MCP
inventory tools — all on the **same** agent, in the **same** chat. Close the browser tab and
press **Ctrl+C** in the terminal to stop the app.

</details>

**Stretch**: add a third MCP tool (for example, `get_reorder_threshold`) and watch the agent
discover it without any other client changes — the routing already handles any tool it
doesn't recognize as a local function.

<details markdown="1">
<summary>Compare: the same capstone with the Microsoft Agent Framework</summary>

In `client.py` you hand-wired the MCP client (`ClientSession`, `stdio_client`), wrapped each
discovered tool, built `FunctionTool` schemas, and then *routed* every `function_call` yourself
— local function or MCP tool. The **Microsoft Agent Framework** collapses all of that. Open
**client_maf.py** (provided complete) and run it with `python client_maf.py` — same capstone,
same two-tool-sets-on-one-agent behavior.

Your `server.py` is unchanged — you still author the MCP server. What disappears is the client
wiring and the routing loop. An `MCPStdioTool` launches the server and exposes its tools, and
you hand it to `agent.run()` alongside the agent's own `@tool` functions:

```python
from agent_framework import tool, Agent, MCPStdioTool

agent = Agent(
    client=FoundryChatClient(...),
    name="caldova-assistant",
    instructions="You are the Caldova supply chain assistant...",
    tools=[next_available_slot, calculate_transfer_cost, generate_capacity_report],
)

async with MCPStdioTool(name="Inventory", command="python", args=["server.py"]) as mcp_tool:
    # One call handles either tool set — no manual "local vs MCP" routing
    result = await agent.run(user_message, tools=mcp_tool, session=session)
```

Notice there's no `if item.name in local_functions ... else ...` branch: `agent.run()` invokes
whichever tool the model picks, whether it's one of your Python functions or a tool hosted on
your MCP server. Having built the routing by hand first, you can see exactly which step the
framework is taking over.

</details>

---

**Next (optional):** [Task 6 — Promote your assistant to a hosted agent](A6-promote-your-assistant-to-a-hosted-agent.md), or head **back to the** [lab overview](A-build-and-extend-ai-agents.md).
