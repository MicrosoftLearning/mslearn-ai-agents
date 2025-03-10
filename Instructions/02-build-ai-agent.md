---
lab:
    title: 'Create an AI agent'
    description: 'Learn how to use the Azure AI Agent Service to build an agent that uses built-in tools.'
---

# Create an AI agent

In this exercise you will explore using built-in tools in Azure AI Foundry to connect to knowledge sources and interpret code. Then, you'll develop a basic agent in Python or C# (C# coming soon).

This exercise should take approximately **30** minutes to complete.

## Before you start

To complete this exercise, you'll need:

- An Azure subscription. If you don't already have one, you can [sign up for one](https://azure.microsoft.com/?azure-portal=true).

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that might open.
1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a suitable project name (for example, `my-agent-project`).
1. If you don't have a hub yet created, you'll see the new hub name and can expand the section below to review the Azure resources that will be automatically created to support your project. If you are reusing a hub, skip the following step.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A unique name - for example `my-ai-hub`*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name (for example, `my-ai-resources`), or select an existing one*
    - **Location**: Select **Help me choose** and then select **gpt-4** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource with an appropriate name (for example, `my-ai-services`) or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

    > \* Model quotas are constrained at the tenant level by regional quotas. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another project in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.

## Create an AI agent

Now you're ready to create your agent.

1. In the pane on the left for your project, in the **Build and customize** section, select the **Agents** page.
1. If prompted to select an Azure OpenAI Service resource, select the one created with your hub name used above.
1. If you haven't deployed a model in your hub, you'll see a **Deploy a model** wizard come up. Select a **gpt-4** model and deploy it with the following settings:
    - **Deployment name**: *A unique name for your model deployment - for example `gpt-4-model`*
    - **Deployment type**: Global Standard
    - **Model version**: turbo-2024-04-09
    - **Connected AI resource**: *Select your Azure OpenAI resource connection*
    - **Tokens per Minute Rate Limit (thousands)**: 50k
    - **Content filter**: DefaultV2
      
1. Wait for the agents list to load, where you'll see a new agent created with a default name. Select it, and change the **Agent name** to **MovieTrendAgent**.

## Integrate built-in tools

Now that you have your agent created, you're ready to customize its behavior. Here you'll be adding built-in tools to find current information and visualize data.

> **Tip**: This section uses **Grounding with Bing Search**, which has additional usage and security considerations covered on the documentation [overview page](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/bing-grounding?pivots=overview).

1. In the **Setup** pane, update the instructions to be:

    ```text
    You are a helpful agent who provides information about movie trends.
    Keep answers concise, but include as much relevant data as possible.
    ```

1. Select the **Try in playground** button to see behavior without tools.
1. In the agent chat window, send the question `What were the 10 most popular movies in 2024?`.
1. Observe the response, which will indicate the model was trained in 2023 and doesn't have that current data.
1. In the **Setup** pane, scroll down to the **Knowledge** section and select **+ Add**.
1. Select **Grounding with Bing Search**, and then select the **+ Create connection** button.
1. On the Azure portal page that pops up, create a **Grounding with Bing Search** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose the resource group you created with your Azure AI Foundry project*
    - **Name**: *Choose a globally unique name (for example `<your-initials>-bing-search`)*
    - **Region**: Global
    - **Pricing tier**: *Select the only available pricing tier*
    - **Terms**: *Select the checkbox confirming you read and understood the notice*
1. Navigate back to the **Agents playground** tab and again select the **+ Create connection** button.
1. Here you'll see your Bing Search resource. Select the **Add connection** button, and once connected click **Connect**.
1. In the **Setup** pane, find the **Actions** tool section and select **+ Add**.
1. Select **Code Interpreter** and then save without uploading any files.
1. In the chat window, send the prompt `What were the 10 most popular movies in 2024? Chart out the total gross revenue for those movies`.
1. While the response might take a bit longer, you'll see your agent is accessing your Bing Search resource for current movie data, and then using that information in Python code to generate a chart.
1. Review the results, which should include a chart with the 10 most popular movies from 2024 with gross revenues charted. If you hover over the message above that starts with *code_interpreter*, you can see the code it wrote to generate the chart.

Here you saw your agent go find the right information on Bing, write code to create a diagram, and return it to you all without you developing any of the code for those connections! The agent can use the power of the language model to understand what you are looking for and how to create it, allowing it to complete tasks that were previously very difficult or impossible.

> **Important**: According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. If using this tool in your own application, be sure to follow those guidelines.

## Develop an agent in your app

Now that you've seen how agents work and how they can accomplish tasks on your behalf, let's develop an app that implements an agent using the same built-in tools.

### Prepare the application configuration

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-agents -f
    git clone https://github.com/microsoftlearning/mslearn-ai-agents mslearn-ai-agents
    ```

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
   cd mslearn-ai-agents/Labfiles/02-build-ai-agent/Python
    ```

1. In the cloud shell command line pane, enter the following command to install the libraries you'll use, which are:
    - **python-dotenv** : Used to load settings from an application configuration file.
    - **azure-identity**: Used to authenticate with Entra ID credentials.
    - **azure-ai-projects**: Used to work with an Azure AI Foundry project.

    ```
   pip install python-dotenv azure-identity azure-ai-projects
    ```

1. Enter the following command to edit the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_endpoint** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal), and the **your_model_deployment** placeholder with the name you assigned to your GPT-4 model deployment.
1. In the Agents playground, copy the name displayed in the **Setup** pane for your Bing resource and enter it in place of the **your_bing_connection** placeholder.
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Write code to connect to your project and chat with your model

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. Enter the following command to edit the code file that has been provided:

    ```
   code basic-agent.py
    ```

> **Tip**: In this exercise, you're actually building the whole agent mostly from scratch in your app to understand how to do so. During your own development, you can instead reference the agent ID of the agent you created in the Foundry portal to use that agent definition by using the `project_client.agents.get_agent("<agent_id>")`.

1. Review the included libraries, taking note of the *Azure AI Projects* libraries for the client and tools.
1. In the definition for *Initialize tools*, add the following code to create the tool definitions and toolset:

    ```python
    def initialize_tools():
        # Create bing grounding tool
        bing_connection = project_client.connections.get(
            connection_name=os.getenv("BING_CONNECTION_NAME")
        )
        conn_id = bing_connection.id
        bing = BingGroundingTool(connection_id=conn_id)
    
        # Create code interpreter tool
        code_interpreter = CodeInterpreterTool()
    
        # Create toolset of tools
        toolset = ToolSet()
        toolset.add(bing)
        toolset.add(code_interpreter)
        return toolset
    ```

1. Under the comment **Create an agent**, add the following code to create your agent:

    ```python
    # Create an agent
    agent = project_client.agents.create_agent(
        model=deployed_model,
        name="my-agent",
        instructions="You are a helpful agent who provides information about movie trends. Keep answers concise, but include as much relevant data as possible.",
        toolset=toolset,
    )
    print(f"Created agent, agent ID: {agent.id}")

    # Create a thread
    thread = project_client.agents.create_thread()
    print(f"Created thread, thread ID: {thread.id}")

    # Create a message
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="What were the 10 most popular movies in 2024? Chart out the total gross revenue for those movies",
    )
    print(f"Created message, message ID: {message.id}")
    ```

1. Review the code you just added, taking note of the creation of the agent, thread, and message.
1. Under the comment **Run the agent**, add the following code to run your agent and get the messages from the thread, taking note of the client calls required to do so:

    ```python
    # Run the agent
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Check if you got "Rate limit is exceeded.", then you want to get more quota
        print(f"Run failed: {run.last_error}")

    # Get messages from the thread
    messages = project_client.agents.list_messages(thread_id=thread.id)
    ```

1. Use the **CTRL+S** command to save your changes to the code file and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

1. In the cloud shell command line pane, enter the following command to run the app:

    ```
   python basic-agent.py
    ```

> **Note**: If the script returns the error `AzureCliCredential.get_token_info failed: Failed to invoke the Azure CLI`, run the command `az login` and authenticate your connection before running the app again.

1. Observe the output, which will display the agent's text response and download the image file. Open that file with the following command, and you'll see your agent has created a graphical chart with movie revenues:

    ```
   download ./<your_image_filename>
    ```
    
1. Feel free to edit the message content to try other questions, such as popular movies from other years or certain genres.

## Clean up

Now that you've finished the exercise, you should delete the cloud resources you've created to avoid unnecessary resource usage.

1. Open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and view the contents of the resource group where you deployed the hub resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
