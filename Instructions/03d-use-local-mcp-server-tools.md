# Connect AI agents to tools using Model Context Protocol (MCP)

In this exercise, you'll create an agent that can connect to an MCP server and automatically discover callable functions.

You'll build a simple inventory assessment agent for a cosmetics retailer. Using the MCP server, the agent will be able to retrieve information about the inventory and make restock or clearance suggestions.

> **Tip**: The code used in this exercise is based on the for Microsoft Foundry and MCP SDKs for Python. You can develop similar solutions using the SDKs for Microsoft .NET. Refer to [Microsoft Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) and [MCP C# SDK](https://modelcontextprotocol.github.io/csharp-sdk/api/ModelContextProtocol.html) for details.

This exercise should take approximately **30** minutes to complete.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Create a Foundry project

Let's start by creating a Foundry project.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Foundry** logo at the top left to navigate to the home page, which looks similar to the following image (close the **Help** pane if it's open):

    ![Screenshot of Foundry portal.](./Media/ai-foundry-home.png)

    > **Important**: Make sure the **New Foundry** toggle is *Off* for this lab.

1. In the home page, select **Create an agent**.
1. When prompted to create a project, enter a valid name for your project and expand **Advanced options**.
1. Confirm the following settings for your project:
    - **Foundry resource**: *A valid name for your Foundry resource*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: *Select any **AI Foundry recommended***\*

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created.
1. If prompted, deploy a **gpt-4o** model using either the *Global Standard* or *Standard* deployment option (depending on your quota availability).

    >**Note**: If quota is available, a GPT-4o base model may be deployed automatically when creating your Agent and project.

1. When your project is created, the Agents playground will be opened.

1. In the navigation pane on the left, select **Overview** to see the main page for your project; which looks like this:

    ![Screenshot of a Foundry project overview page.](./Media/ai-foundry-project.png)

1. Copy the **Foundry project endpoint** value to a notepad, as you'll use it to connect to your project in a client application.

## Develop an agent that uses MCP function tools

Now that you've created your project in AI Foundry, let's develop an app that integrates an AI agent with an MCP server.

### Clone the repo containing the application code

1. Open a new browser tab (keeping the Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.

    Close any welcome notifications to see the Azure portal home page.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.

    The cloud shell provides a command-line interface in a pane at the bottom of the Azure portal. You can resize or maximize this pane to make it easier to work in.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. In the cloud shell pane, enter the following commands to clone the GitHub repo containing the code files for this exercise (type the command, or copy it to the clipboard and then right-click in the command line and paste as plain text):

    ```
   rm -r ai-agents -f
   git clone https://github.com/MicrosoftLearning/mslearn-ai-agents ai-agents
    ```

    > **Tip**: As you enter commands into the cloudshell, the output may take up a large amount of the screen buffer and the cursor on the current line may be obscured. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. Enter the following command to change the working directory to the folder containing the code files and list them all.

    ```
   cd ai-agents/Labfiles/03d-use-agent-tools-with-mcp/Python
   ls -a -l
    ```

    The provided files include the client and server application code. The Model Context Protocal provides a standardized way to connect AI models to different data sources and tools. We separate `client.py` and `server.py` to keep the agent logic and tool definitions modular and simulate real-world architecture. 
    
    `server.py` defines the tools the agent can use, simulating backend services or business logic. 
    `client.py` handles the AI agent setup, user prompts, and calling the tools when needed.

### Configure the application settings

1. In the cloud shell command-line pane, enter the following command to install the libraries you'll use:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects mcp
    ```

    >**Note:** You can ignore any warning or error messages displayed during the library installation.

1. Enter the following command to edit the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_endpoint** placeholder with the endpoint for your project (copied from the project **Overview** page in the Foundry portal) and ensure that the MODEL_DEPLOYMENT_NAME variable is set to your model deployment name (which should be *gpt-4o*).

1. After you've replaced the placeholder, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Implement an MCP Server

A Model Context Protocol (MCP) Server is a component that hosts callable tools. These tools are Python functions that can be exposed to AI agents. When tools are annotated with `@mcp.tool()`, they become discoverable to the client, allowing an AI agent to call them dynamically during a conversation or task. In this task, you'll add some tools that will allow the agent to perform inventory checks.

1. Enter the following command to edit the code file that has been provided for your function code:

    ```
   code server.py
    ```

    In this code file, you'll define the tools the agent can use to simulate a backend service for the retail store. Notice the server setup code at the top of the file. It uses `FastMCP` to quickly spin up an MCP server instance named "Inventory". This server will host the tools you define and make them accessible to the agent during the lab.

1. Find the comment **Add an inventory check tool** and add the following code:

    ```python
   # Add an inventory check tool
   @mcp.tool()
   def get_inventory_levels() -> dict:
        """Returns current inventory for all products."""
        return {
            "Moisturizer": 6,
            "Shampoo": 8,
            "Body Spray": 28,
            "Hair Gel": 5, 
            "Lip Balm": 12,
            "Skin Serum": 9,
            "Cleanser": 30,
            "Conditioner": 3,
            "Setting Powder": 17,
            "Dry Shampoo": 45
        }
    ```

    This dictionary represents a sample inventory. The `@mcp.tool()` annotation will allow the LLM to discover your function. 

1. Find the comment **Add a weekly sales tool** and add the following code:

    ```python
   # Add a weekly sales tool
   @mcp.tool()
   def get_weekly_sales() -> dict:
        """Returns number of units sold last week."""
        return {
            "Moisturizer": 22,
            "Shampoo": 18,
            "Body Spray": 3,
            "Hair Gel": 2,
            "Lip Balm": 14,
            "Skin Serum": 19,
            "Cleanser": 4,
            "Conditioner": 1,
            "Setting Powder": 13,
            "Dry Shampoo": 17
        }
    ```

1. Save the file (*CTRL+S*).

### Implement an MCP Client

An MCP client is the component that connects to the MCP server to discover and call tools. You can think of it as the bridge between the agent and the server-hosted functions, enabling dynamic tool use in response to user prompts.

1. Enter the following command to begin editing the client code.

    ```
   code client.py
    ```

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. Find the comment **Add references** and add the following code to import the classes:

    ```python
   # Add references
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   from azure.ai.agents import AgentsClient
   from azure.ai.agents.models import FunctionTool, MessageRole, ListSortOrder
   from azure.identity import DefaultAzureCredential
    ```

1. Find the comment **Start the MCP server** and add the following code:

    ```python
   # Start the MCP server
   stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
   stdio, write = stdio_transport
    ```

    In a standard production setup, the server would run separately from the client. But for the sake of this lab, the client is responsible for starting the server using standard input/output transport. This creates a lightweight communication channel between the two components and simplifies the local development setup.

1. Find the comment **Create an MCP client session** and add the following code:

    ```python
   # Create an MCP client session
   session = await exit_stack.enter_async_context(ClientSession(stdio, write))
   await session.initialize()
    ```

    This creates a new client session using the input and output streams from the previous step. Calling `session.initialize` prepares the session to discover and call tools that are registered on the MCP server.

1. Under the comment **List available tools**, add the following code to verify that the client has connected to the server:

    ```python
   # List available tools
   response = await session.list_tools()
   tools = response.tools
   print("\nConnected to server with tools:", [tool.name for tool in tools]) 
    ```

    Now your client session is ready for use with your Azure AI Agent.

### Connect the MCP tools to your agent

In this task, you'll prepare the AI agent, accept user prompts, and invoke the function tools.

1. Find the comment **Connect to the agents client** and add the following code to connect to the Azure AI project using the current Azure credentials.

    ```python
   # Connect to the agents client
   agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
   )
    ```

1. Under the comment **List tools available on the server**, add the following code:

    ```python
   # List tools available on the server
   response = await session.list_tools()
   tools = response.tools
    ```

1. Under the comment **Build a function for each tool** and add the following code:

    ```python
   # Build a function for each tool
   def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result
        
        tool_func.__name__ = tool_name
        return tool_func

   functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}
   mcp_function_tool = FunctionTool(functions=list(functions_dict.values()))
    ```

    This code dynamically wraps tools available in the MCP server so that they can be called by the AI agent. Each tool is turned into an async function and then bundled into a `FunctionTool` for the agent to use.

1. Find the comment **Create the agent** and add the following code:

    ```python
   # Create the agent
   agent = agents_client.create_agent(
        model=model_deployment,
        name="inventory-agent",
        instructions="""
        You are an inventory assistant. Here are some general guidelines:
        - Recommend restock if item inventory < 10  and weekly sales > 15
        - Recommend clearance if item inventory > 20 and weekly sales < 5
        """,
        tools=mcp_function_tool.definitions
   )
    ```

1. Find the comment **Enable auto function calling** and add the following code:

    ```python
   # Enable auto function calling
   agents_client.enable_auto_function_calls(tools=mcp_function_tool)
    ```

1. Under the comment **Create a thread for the chat session**, add the following code:

    ```python
   # Create a thread for the chat session
   thread = agents_client.threads.create()
    ```

1. Locate the comment **Invoke the prompt** and add the following code:

    ```python
   # Invoke the prompt
   message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_input,
   )
   run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
    ```

1. Locate the comment **Retrieve the matching function tool** and add the following code:

    ```python
   # Retrieve the matching function tool
   function_name = tool_call.function.name
   args_json = tool_call.function.arguments
   kwargs = json.loads(args_json)
   required_function = functions_dict.get(function_name)

   # Invoke the function
   output = await required_function(**kwargs)
    ```

    This code uses the information from the agent thread's tool call. The function name and arguments are retrieved and used to invoke the matching function.

1. Under the comment **Append the output text**, add the following code:

    ```python
   # Append the output text
   tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": output.content[0].text,
   })
    ```

1. Under the comment **Submit the tool call output**, add the following code:

    ```python
   # Submit the tool call output
   agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)
    ```

    This code will signal to the agent thread that the required action is complete and update the tool call outputs.

1. Find the comment **Display the response** and add the following code:

    ```python
   # Display the response
   messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
   for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")
    ```

1. Save the code file (*CTRL+S*) when you have finished. You can also close the code editor (*CTRL+Q*); though you may want to keep it open in case you need to make any edits to the code you added. In either case, keep the cloud shell command-line pane open.

### Sign into Azure and run the app

1. In the cloud shell command-line pane, enter the following command to sign into Azure.

    ```
   az login
    ```

    **<font color="red">You must sign into Azure - even though the cloud shell session is already authenticated.</font>**

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.
    
1. When prompted, follow the instructions to open the sign-in page in a new tab and enter the authentication code provided and your Azure credentials. Then complete the sign in process in the command line, selecting the subscription containing your Foundry hub if prompted.

1. After you have signed in, enter the following command to run the application:

    ```
   python client.py
    ```

1. When prompted, enter a query such as:

    ```
   What are the current inventory levels?
    ```

    > **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

    You should see some output similar to the folloiwng:

    ```
    MessageRole.AGENT:
    Here are the current inventory levels:

    - Moisturizer: 6
    - Shampoo: 8
    - Body Spray: 28
    - Hair Gel: 5
    - Lip Balm: 12
    - Skin Serum: 9
    - Cleanser: 30
    - Conditioner: 3
    - Setting Powder: 17
    - Dry Shampoo: 45
    ```

1. You can continue the conversation if you like. The thread is *stateful*, so it retains the conversation history - meaning that the agent has the full context for each response. 

    Try entering prompts such as:

    ```
   Are there any products that should be restocked?
    ```

    ```
   Which products would you recommend for clearance?
    ```

    ```
   What are the best sellers this week?
    ```

    Enter `quit` when you're done.

## Clean up

Now that you've finished the exercise, you should delete the cloud resources you've created to avoid unnecessary resource usage.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and view the contents of the resource group where you deployed the hub resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
