---
lab:
    title: 'Use a custom function in an AI agent'
    description: 'Learn how to use functions to add custom capabilities to your agents.'
---

# Use a custom function in an AI agent

In this exercise you'll explore creating an agent that can use custom functions as a tool to complete tasks. The agent will act as an astronomy assistant that can provide information about astronomical events and calculate the cost of telescope rentals based on user inputs. You'll define the function tools and implement the logic to process function calls made by the agent.

> **Tip**: The code used in this exercise is based on the for Microsoft Foundry SDK for Python. You can develop similar solutions using the SDKs for Microsoft .NET, JavaScript, and Java. Refer to [Microsoft Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) for details.

This exercise should take approximately **60** minutes to complete.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting this exercise, ensure you have:
- Visual Studio Code installed
- An active Azure subscription
- Python version 3.10 or higher installed

## Install the Microsoft Foundry VS Code extension

Let's start by installing and setting up the VS Code extension.

1. Open Visual Studio Code.

1. Select **Extensions** from the left pane (or press **Ctrl+Shift+X**).

1. In the search bar, type **Microsoft Foundry** and press Enter.

1. Select the **Microsoft Foundry** extension from Microsoft and click **Install**.

1. After installation is complete, verify the extension appears in the primary navigation bar on the left side of Visual Studio Code.

## Sign in to Azure and create a project

Now you'll connect to your Azure resources and create a new AI Foundry project.

1. In the VS Code sidebar, select the **Microsoft Foundry** extension icon.

1. In the Resources view, select **Sign in to Azure...** and follow the authentication prompts.

   > **Note**: You won't see this option if you're already signed in.

1. Create a new Foundry project by selecting the **+** (plus) icon next to **Resources** in the Foundry Extension view.

1. Select your Azure subscription from the dropdown.

1. Choose whether to create a new resource group or use an existing one:
   
   **To create a new resource group:**
   - Select **Create new resource group** and press Enter
   - Enter a name for your resource group (e.g., "rg-ai-agents-lab") and press Enter
   - Select a location from the available options and press Enter
   
   **To use an existing resource group:**
   - Select the resource group you want to use from the list and press Enter

1. Enter a name for your Foundry project (e.g., "ai-agents-project") in the textbox and press Enter.

1. Wait for the project deployment to complete. A popup will appear with the message "Project deployed successfully."

## Deploy a model

In this task, you'll deploy a model from the Model Catalog to use with your agent.

1. When the "Project deployed successfully" popup appears, select the **Deploy a model** button. This opens the Model Catalog.

   > **Tip**: You can also access the Model Catalog by selecting the **+** icon next to **Models** in the Resources section, or by pressing **F1** and running the command **Microsoft Foundry: Open Model Catalog**.

1. In the Model Catalog, locate the **gpt-4.1** model (you can use the search bar to find it quickly).

    ![Screenshot of the Model Catalog in the Foundry VS Code extension.](Media/vs-code-model.png)

1. Select **Deploy** next to the gpt-4.1 model.

1. Configure the deployment settings:
   - **Deployment name**: Enter a name like "gpt-4.1"
   - **Deployment type**: Select **Global Standard** (or **Standard** if Global Standard is not available)
   - **Model version**: Leave as default
   - **Tokens per minute**: Leave as default

1. Select **Deploy in Microsoft Foundry** in the bottom-left corner.

1. In the confirmation dialog, select **Deploy** to deploy the model.

1. Wait for the deployment to complete. Your deployed model will appear under the **Models** section in the Resources view.

1. Right-click the name project deployment and select **Copy Project Endpoint**. You'll need this URL to connect your agent to the Foundry project in the next steps.

   <img src="Media/vs-code-endpoint.png" alt="Screenshot of copying the project endpoint in the Foundry VS Code extension." width="550">

## Clone the starter code repository

For this exercise, you'll use starter code that will help you connect to your Foundry project and create an agent that uses custom function tools.

1. Navigate to the **Welcome** tab in VS Code (you can open it by selecting **Help > Welcome** from the menu bar).

1. Select **Clone git repository** and enter the URL of the starter code repository: `https://github.com/MicrosoftLearning/mslearn-ai-agents.git`

1. Create a new folder and choose **Select as Repository Destination**, then open the cloned repository when prompted.

1. In the Explorer view, navigate to the **Labfiles/02-agent-custom-tools/Python** folder to find the starter code for this exercise.

1. Right-click on the **requirements.txt** file and select **Open in Integrated Terminal**.

1. In the terminal, enter the following command to install the required Python packages in a virtual environment:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

1. Open the **.env** file, replace the **your_project_endpoint** placeholder with the endpoint for your project (copied from the project deployment resource in the Microsoft Foundry extension) and ensure that the MODEL_DEPLOYMENT_NAME variable is set to your model deployment name. Use **Ctrl+S** to save the file after making these changes.

Now you're ready to create an AI agent that uses MCP server tools to access external data sources and APIs.

## Create a function for the agent to use

1. Open the **functions.py** file and review the existing code.

    This file includes several functions that you can use as tools for your agent. The functions use sample files located inthe **data** folder to retrieve information about astronomical events and locations.

1. Find the comment **Determine the next visible astronomical event for a given location** and add the following code:

    ```python   
   # Determine the next visible astronomical event for a given location
   def next_visible_event(location: str) -> str:
       """Returns the next visible astronomical event for a location."""
       today = int(datetime.now().strftime("%m%d"))
       loc = location.lower().replace(" ", "_")

       # Retrieve the next event visible from the location, starting with events later this year
       for name, event_type, date, date_str, locs in EVENTS:
           if loc in locs and date >= today:
               return json.dumps({"event": name, "type": event_type, "date": date_str, "visible_from": sorted(locs)})

       return json.dumps({"message": f"No upcoming events found for {location}."})
    ```

    This function checks the sample events data to find the next astronomical event that is visible from a specified location, and returns the event details as a JSON string. Next, let's create an agent that can use this function.

## Connect to the Foundry project

1. Open the **agent.py** file. 

   > **Tip**: As you add code, be sure to maintain the correct indentation. Use the comment indentation levels as a guide.

1. Find the comment **Add references** and add the following code to import the classes you'll need to build an Azure AI agent that uses a function tool:

    ```python
   # Add references
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import FunctionTool
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
   from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
   from functions import next_visible_event, calculate_observation_cost, generate_observation_report
    ```

    Notice that the functions you defined in the **functions.py** file are imported so they can be used as tools for the agent.

1. Find the comment **Connect to the project client** and add the following code:

    ```python
    # Connect to the project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    ```

## Define the function tools

In this task, you'll define each of the function tools that the agent can use. The parameters for each function tool are defined using a JSON schema, which specifies the name, type, description, and other attributes for each parameter of the function.

1. Find the comment **Define the event function tool** and add the following code:

    ```python
   # Define the event function tool
   event_tool = FunctionTool(
       name="next_visible_event",
       description="Get the next visible event in a given location.",
       parameters={
           "type": "object",
           "properties": {
               "location": {
                   "type": "string",
                   "description": "continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')",
               },
           },
           "required": ["location"],
           "additionalProperties": False,
       },
       strict=True,
   )
    ```

1. Find the comment **Define the observation cost function tool** and add the following code:

    ```python
   # Define the observation cost function tool
   cost_tool = FunctionTool(
       name="calculate_observation_cost",
       description="Calculate the cost of an observation based on the telescope tier, number of hours, and priority level.",
       parameters={
           "type": "object",
           "properties": {
               "telescope_tier": {
                   "type": "string",
                   "description": "the tier of the telescope (e.g. 'standard', 'advanced', 'premium')",
               },
               "hours": {
                   "type": "number",
                   "description": "the number of hours for the observation",
               },
               "priority": {
                   "type": "string",
                   "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
               },
           },
           "required": ["telescope_tier", "hours", "priority"],
           "additionalProperties": False,
       },
       strict=True,
   )
    ```

1. Find the comment **Define the observation report generation function tool** and add the following code:

    ```python
   # Define the observation report generation function tool
   report_tool = FunctionTool(
       name="generate_observation_report",
       description="Generate a report summarizing an astronomical observation",
       parameters={
           "type": "object",
           "properties": {
               "event_name": {
                   "type": "string",
                   "description": "the name of the astronomical event being observed",
               },
               "location": {
                   "type": "string",
                   "description": "the location of the observer",
               },
               "telescope_tier": {
                   "type": "string",
                   "description": "the tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')",
               },
               "hours": {
                   "type": "number",
                   "description": "the number of hours the telescope was used for the observation",
               },
               "priority": {
                   "type": "string",
                   "description": "the priority level of the observation (e.g. 'low', 'normal', 'high')",
               },
               "observer_name": {
                   "type": "string",
                   "description": "the name of the person who conducted the observation",
               },                   
           },
           "required": ["event_name", "location", "telescope_tier", "hours", "priority", "observer_name"],
           "additionalProperties": False,
       },
       strict=True,
   )
    ```

## Create the agent that uses the function tools

Now that you've defined the function tools, you can create an agent that can use those tools to complete tasks.

1. Find the comment **Create a new agent with the function tools** and add the following code:

    ```python
   # Create a new agent with the function tools
   agent = project_client.agents.create_version(
       agent_name="astronomy-agent",
       definition=PromptAgentDefinition(
           model=model_deployment,
           instructions=
               """You are an astronomy observations assistant that helps users find 
               information about astronomical events and calculate telescope rental costs. 
               Use the available tools to assist users with their inquiries.""",
           tools=[event_tool, cost_tool, report_tool],
       ),
   )
    ```

## Send a message to the agent and process the response

Now that you've created the agent with the function tools, you can send messages to the agent and process its responses.

1. Find the comment **Create a thread for the chat session** and add the following code:

    ```python
   # Create a thread for the chat session
   conversation = openai_client.conversations.create()
    ```

    This code creates the chat session with the agent.

1. Find the comment **Create an input list to hold function call outputs to send back to the model** and add the following code:

    ```python
   # Create a list to hold function call outputs that will be sent back as input to the agent
   input_list: ResponseInputParam = []
   ```

1. Find the comment **Send a prompt to the agent** and add the following code:

    ```python
   # Send a prompt to the agent
   openai_client.conversations.items.create(
       conversation_id=conversation.id,
       items=[{"type": "message", "role": "user", "content": user_input}],
   )
    ```

1. Find the comment **Retrieve the agent's response, which may include function calls** and add the following code:

    ```python
   # Retrieve the agent's response, which may include function calls
   response = openai_client.responses.create(
       conversation=conversation.id,
       extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
       input=input_list,
   )

   # Check the run status for failures
   if response.status == "failed":
       print(f"Response failed: {response.error}")
    ```

    In this code, you send a user prompt to the agent and retrieve the response. You also check if the response indicates a failure and print the error if so.

## Process function calls and display the agent's response

1. Find the comment **Process function calls** and add the following code to handle any function calls made by the agent:

    ```python
   # Process function calls
   for item in response.output:
       if item.type == "function_call":
           # Retrieve the matching function tool
           function_name = item.name
           result = None
           if item.name == "next_visible_event":
               result = next_visible_event(**json.loads(item.arguments))
           elif item.name == "calculate_observation_cost":
               result = calculate_observation_cost(**json.loads(item.arguments))
           elif item.name == "generate_observation_report":
               result = generate_observation_report(**json.loads(item.arguments))
                
           # Append the output text
           input_list.append(
               FunctionCallOutput(
                   type="function_call_output",
                   call_id=item.call_id,
                   output=result,
               )
           )
    ```

    This code iterates through the items in the agent's response to check for any function calls. If a function call is found, it retrieves the corresponding function tool, executes the function with the provided arguments, and appends the result to the input list that will be sent back to the agent.

1. Find the comment **Send function call outputs back to the model and retrieve a response** and add the following code:

    ```python
   # Send function call outputs back to the model and retrieve a response
   if input_list:
       response = openai_client.responses.create(
           input=input_list,
           previous_response_id=response.id,
           extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
       )
   # Display the agent's response
   print(f"AGENT: {response.output_text}")
    ```

    This code checks if there are any function call outputs in the input list, and if so, it sends them back to the agent as input to retrieve an updated response. Finally, it prints the agent's response.

1. Find the comment  **Delete the conversation when done** and add the following code:

    ```python
   # Delete the agent when done
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Deleted agent.")
    ```

1. Review the complete code you've added to the file. It should now include sections that:
   - Import necessary libraries
    - Connect to the Foundry project and OpenAI client
    - Define function tools for the agent to use
    - Create an agent with those function tools
    - Send a message to the agent and retrieve the response
    - Process any function calls made by the agent and send the outputs back to the agent
    - Display the agent's response
    - Delete the agent when done

1. Save the code file (*CTRL+S*) when you have finished. 

## Run the agent application

1. In the integrated terminal, enter the following command to run the application:

    ```
   python agent.py
    ```

1. When prompted, enter a prompt such as:

    ```
   Find me the next event I can see from South America and give me the cost for 5 hours of premium telescope time at normal priority.
    ```

    Notice that this prompt asks the agent to use both of the function tools you defined: `next_visible_event` and `calculate_observation_cost`. The agent is able to invoke both functions in the same conversation turn, and use the outputs from those function calls to provide a helpful response to the user.

    > **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

    You should see some output similar to the folloiwng:

    ```output
    AGENT: The next astronomical event you can observe from South America is the Jupiter-Venus Conjunction, taking place on May 1st.
    The cost for 5 hours of premium telescope time at normal priority for this observation will be $1,875. 
    ```

1. Enter a follow-up prompt to generate an observation report, such as:

    ```
    Generate that information in a report for Bellows College.
    ```

    You should see a response similar to the following:

    ```output
    AGENT: Here is your report for Bellows College:

    - Next visible astronomical event: Jupiter-Venus Conjunction
    - Date: May 1st
    - Visible from: South America
    - Observation details:
        - Telescope tier: Premium
        - Duration: 5 hours
        - Priority: Normal
    - Observation cost: $1,875

    A formal report has been generated for Bellows College.
    ```

    In the file explorer, you can see that a new file named `report-<event-type>.txt` has been created, which contains the generated report. You can open this file to view the contents of the report.

1. Enter `quit` to exit the application.

    You can also use `deactivate` to exit the Python virtual environment in the terminal.

## Summary

In this exercise, you created an AI agent that uses custom function tools to retrieve information and perform calculations based on user prompts. You defined the function tools with JSON schemas to specify their parameters, and implemented the logic to process function calls made by the agent. You then ran the application and interacted with the agent to see how it used the function tools to provide helpful responses. Great work!

## Clean up

When you've finished exploring the Foundry VS Code extension, you should clean up the resources to avoid incurring unnecessary Azure costs.

### Delete your model

1. In VS Code, refresh the **Azure Resources** view.

1. Expand the **Models** subsection.

1. Right-click on your deployed model and select **Delete**.

### Delete the resource group

1. Open the [Azure portal](https://portal.azure.com).

1. Navigate to the resource group containing your AI Foundry resources.

1. Select **Delete resource group** and confirm the deletion.