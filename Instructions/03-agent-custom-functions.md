---
lab:
    title: 'Use a custom function in an AI agent'
    description: 'Learn how to use functions to add custom capabilities to your agents.'
---

# Use a custom function in an AI agent

In this exercise you'll explore creating an agent that can use custom functions as a tool to complete tasks. You'll build a simple technical support agent that can collect details of a technical problem and generate a support ticket.

> **Tip**: The code used in this exercise is based on the for Microsoft Foundry SDK for Python. You can develop similar solutions using the SDKs for Microsoft .NET, JavaScript, and Java. Refer to [Microsoft Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) for details.

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

1. Copy the **Foundry project endpoint** values to a notepad, as you'll use them to connect to your project in a client application.

## Develop an agent that uses function tools

Now that you've created your project in AI Foundry, let's develop an app that implements an agent using custom function tools.

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
   cd ai-agents/Labfiles/03-ai-agent-functions/Python
   ls -a -l
    ```

    The provided files include application code and a file for configuration settings.

### Configure the application settings

1. In the cloud shell command-line pane, enter the following command to install the libraries you'll use:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt azure-ai-projects azure-ai-agents
    ```

    >**Note:** You can ignore any warning or error messages displayed during the library installation.

1. Enter the following command to edit the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_endpoint** placeholder with the endpoint for your project (copied from the project **Overview** page in the Foundry portal) and ensure that the MODEL_DEPLOYMENT_NAME variable is set to your model deployment name (which should be *gpt-4o*).
1. After you've replaced the placeholder, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Define a custom function

1. Enter the following command to edit the code file that has been provided for your function code:

    ```
   code user_functions.py
    ```

1. Find the comment **Create a function to submit a support ticket** and add the following code, which generates a ticket number and saves a support ticket as a text file.

    ```python
   # Create a function to submit a support ticket
   def submit_support_ticket(email_address: str, description: str) -> str:
        script_dir = Path(__file__).parent  # Get the directory of the script
        ticket_number = str(uuid.uuid4()).replace('-', '')[:6]
        file_name = f"ticket-{ticket_number}.txt"
        file_path = script_dir / file_name
        text = f"Support ticket: {ticket_number}\nSubmitted by: {email_address}\nDescription:\n{description}"
        file_path.write_text(text)
    
        message_json = json.dumps({"message": f"Support ticket {ticket_number} submitted. The ticket file is saved as {file_name}"})
        return message_json
    ```

1. Find the comment **Define a set of callable functions** and add the following code, which statically defines a set of callable functions in this code file (in this case, there's only one - but in a real solution you may have multiple functions that your agent can call):

    ```python
   # Define a set of callable functions
   user_functions: Set[Callable[..., Any]] = {
        submit_support_ticket
    }
    ```
1. Save the file (*CTRL+S*).

### Write code to implement an agent that can use your function

1. Enter the following command to begin editing the agent code.

    ```
    code agent.py
    ```

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. Review the existing code, which retrieves the application configuration settings and sets up a loop in which the user can enter prompts for the agent. The rest of the file includes comments where you'll add the necessary code to implement your technical support agent.
1. Find the comment **Add references** and add the following code to import the classes you'll need to build an Azure AI agent that uses your function code as a tool:

    ```python
   # Add references
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import PromptAgentDefinition, FunctionTool, ToolSet
   from user_functions import user_functions
    ```

1. Find the comment **Connect to the AI Project client** and add the following code to connect to the Azure AI project using the current Azure credentials.

    > **Tip**: Be careful to maintain the correct indentation level.

    ```python
   # Connect to the AI Project client
   with (
       DefaultAzureCredential() as credential,
       AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
   ):
    ```
    
1. Find the comment **Define an agent that can use the custom functions** section, and add the following code to add your function code to a toolset, enable auto function calling, and then create an agent that can use the toolset and a conversation on which to run the chat session.

    ```python
   # Define an agent that can use the custom functions
   functions = FunctionTool(user_functions)
   toolset = ToolSet()
   toolset.add(functions)

   with project_client.get_openai_client() as openai_client:
        project_client.enable_auto_function_calls(toolset)
        
        agent = project_client.agents.create_version(
            agent_name="support-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions="""You are a technical support agent.
                                When a user has a technical issue, you get their email address and a description of the issue.
                                Then you use those values to submit a support ticket using the function available to you.
                                If a file is saved, tell the user the file name.
                             """,
                toolset=toolset
            ),
        )
        print(f"You're chatting with: {agent.name} ({agent.id})")

        # Create a conversation for the chat session
        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")

    ```

1. Find the comment **Send a prompt to the agent** and add the following code to add the user's prompt as a message and get a response from the agent.

    ```python
   # Send a prompt to the agent
   openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_prompt}],
   )

   response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        input="",
   )
    ```

    > **Note**: The agent automatically finds your functions and chooses to use them based on their names and parameters.

1. Find the comment **Check the response status for failures** and add the following code to show any errors that occur.

    ```python
   # Check the response status for failures
   if response.status == "failed":
        print(f"Response failed: {response.error}")
    ```

1. Find the comment **Show the latest response from the agent** and add the following code to display the response from the agent.

    ```python
   # Show the latest response from the agent
   print(f"Agent: {response.output_text}")
    ```

1. Find the comment **Get the conversation history** and add the following code to print out the messages from the conversation

    ```python
   # Get the conversation history
   print("\nConversation Log:\n")
   items = openai_client.conversations.items.list(conversation_id=conversation.id)
   for item in items.data:
        if item.type == "message":
            role = item.role.upper()
            content = item.content[0].text.value if item.content and item.content[0].type == "text" else ""
            print(f"{role}: {content}\n")
    ```

1. Find the comment **Clean up** and add the following code to delete the conversation and agent when no longer needed.

    ```python
   # Clean up
   openai_client.conversations.delete(conversation_id=conversation.id)
   print("Conversation deleted")

   project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
   print("Agent deleted")
    ```

1. Review the code, using the comments to understand how it:
    - Adds your set of custom functions to a toolset
    - Connects to the AI project and gets an OpenAI client
    - Enables auto function calling for the toolset
    - Creates an agent that uses the toolset.
    - Creates a conversation for the chat session.
    - Adds user messages to the conversation and gets responses from the agent.
    - Checks the status of the response in case there's a failure
    - Displays the agent's response.
    - Displays the conversation history
    - Deletes the conversation and agent when they're no longer required.

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
   python agent.py
    ```
    
    The application runs using the credentials for your authenticated Azure session to connect to your project and create and run the agent.

1. When prompted, enter a prompt such as:

    ```
   I have a technical problem
    ```

    > **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

1. View the response. The agent may ask for your email address and a description of the issue. You can use any email address (for example, `alex@contoso.com`) and any issue description (for example `my computer won't start`)

    When it has enough information, the agent should choose to use your function as required.

1. You can continue the conversation if you like. The thread is *stateful*, so it retains the conversation history - meaning that the agent has the full context for each response. Enter `quit` when you're done.
1. Review the conversation messages that were retrieved from the thread, and the tickets that were generated.
1. The tool should have saved support tickets in the app folder. You can use the `ls` command to check, and then use the `cat` command to view the file contents, like this:

    ```
   cat ticket-<ticket_num>.txt
    ```

## Clean up

Now that you've finished the exercise, you should delete the cloud resources you've created to avoid unnecessary resource usage.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and view the contents of the resource group where you deployed the hub resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
