---
lab:
    title: 'Develop an Azure AI agent with the Microsoft Agent Framework SDK'
    description: 'Learn how to use the Microsoft Agent Framework SDK to create and use an Azure AI chat agent.'
    level: 300
    duration: 30
---

# Develop an Azure AI chat agent with the Microsoft Agent Framework SDK

In this exercise, you'll use Azure AI Agent Service and Microsoft Agent Framework to create an AI agent that processes expense claims.

This exercise should take approximately **30** minutes to complete.

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

    ![Screenshot of the Model Catalog in the Foundry VS Code extension.](../Media/vs-code-model.png)

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

   <img src="../Media/vs-code-endpoint.png" alt="Screenshot of copying the project endpoint in the Foundry VS Code extension." width="550">

## Clone the starter code repository

For this exercise, you'll use starter code that will help you connect to your Foundry project and create an agent that can process expenses data. You'll clone this code from a GitHub repository.

1. Navigate to the **Welcome** tab in VS Code (you can open it by selecting **Help > Welcome** from the menu bar).

1. Select **Clone git repository** and enter the URL of the starter code repository: `https://github.com/MicrosoftLearning/mslearn-ai-agents.git`

1. Create a new folder and choose **Select as Repository Destination**, then open the cloned repository when prompted.

1. In the Explorer view, navigate to the **Labfiles/07-agent-framework/Python** folder to find the starter code for this exercise.

1. Right-click on the **requirements.txt** file and select **Open in Integrated Terminal**.

1. In the terminal, enter the following command to install the required Python packages in a virtual environment:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

1. Open the **.env** file, replace the **your_project_endpoint** placeholder with the endpoint for your project (copied from the project deployment resource in the Microsoft Foundry extension) and ensure that the MODEL_DEPLOYMENT_NAME variable is set to your model deployment name. Use **Ctrl+S** to save the file after making these changes.

Now you're ready to create an AI agent that uses a custom tool to process expenses data.

## Write code for an agent app

> **Tip**: As you add code, be sure to maintain the correct indentation. Use the existing comments as a guide, entering the new code at the same level of indentation.

1. Open the **agent-framework.py** file in the code editor.

1. Review the code in the file. It contains:
    - Some **import** statements to add references to commonly used namespaces
    - A *main* function that loads a file containing expenses data, asks the user for instructions, and and then calls...
    - A **process_expenses_data** function in which the code to create and use your agent must be added

1. At the top of the file, after the existing **import** statement, find the comment **Add references**, and add the following code to reference the namespaces in the libraries you'll need to implement your agent:

    ```python
   # Add references
   from agent_framework import tool
   from agent_framework.azure import AzureOpenAIResponsesClient
   from azure.identity import AzureCliCredential
   from pydantic import Field
   from typing import Annotated
    ```

1. Near the bottom of the file, find the comment **Create a tool function for the email functionality**, and add the following code to define a function that your agent will use to send email (tools are a way to add custom functionality to agents)

    ```python
   # Create a tool function for the email functionality
   @tool(approval_mode="never_require")
   def submit_claim(
       to: Annotated[str, Field(description="Who to send the email to")],
       subject: Annotated[str, Field(description="The subject of the email.")],
       body: Annotated[str, Field(description="The text body of the email.")]):
           print("\nTo:", to)
           print("Subject:", subject)
           print(body, "\n")
    ```

    > **Note**: The function *simulates* sending an email by printing it to the console. In a real application, you'd use an SMTP service or similar to actually send the email!

1. Back up above the **send_email** code, in the **process_expenses_data** function, find the comment **Create a client and initialize an agent with the tool and instructions**, and add the following code:

    (Be sure to maintain the indentation level)

    ```python
   # Create a client and initialize an agent with the tool and instructions
   async with (
        AzureCliCredential() as credential,
        Agent(
            client=AzureOpenAIResponsesClient(
                credential=credential,
                deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
                project_endpoint=os.getenv("PROJECT_ENDPOINT"),
            ),
            instructions="""You are an AI assistant for expense claim submission.
                        At the user's request, create an expense claim and use the plug-in function to send an email to expenses@contoso.com with the subject 'Expense Claim`and a body that contains itemized expenses with a total.
                        Then confirm to the user that you've done so. Don't ask for any more information from the user, just use the data provided to create the email.""",
            tools=[submit_claim],
        ) as agent,
    ):
    ```

    Note that the **AzureCliCredential** object will allow your code to authenticate to your Azure account. The **AzureOpenAIResponsesClient** object includes the Foundry project settings from the .env configuration. The **Agent** object is initialized with the client, instructions for the agent, and the tool function you defined to send emails.

1.

1. Find the comment **Use the agent to process the expenses data**, and add the following code to create a thread for your agent to run on, and then invoke it with a chat message.

    (Be sure to maintain the indentation level):

    ```python
   # Use the agent to process the expenses data
   try:
       # Add the input prompt to a list of messages to be submitted
       prompt_messages = [f"{prompt}: {expenses_data}"]
       # Invoke the agent for the specified thread with the messages
       response = await agent.run(prompt_messages)
       # Display the response
       print(f"\n# Agent:\n{response}")
   except Exception as e:
       # Something went wrong
       print (e)
    ```

1. Review that the completed code for your agent, using the comments to help you understand what each block of code does, and then save your code changes (**CTRL+S**).

## Run the app

1. In the integrated terminal, enter the following command to run the application:

    ```
   python agent-framework.py
    ```

1. When asked what to do with the expenses data, enter the following prompt:

    ```
   Submit an expense claim
    ```

1. When the application has finished, review the output. The agent should have composed an email for an expenses claim based on the data that was provided.

    > **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

1. When you're finished, enter `deactivate` in the terminal to exit the Python virtual environment.

## Summary

In this exercise, you used the Microsoft Agent Framework SDK to create an agent with a custom tool.

## Clean up

If you've finished exploring Azure AI Agent Service, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

### Delete your model

1. In VS Code, refresh the **Azure Resources** view.

1. Expand the **Models** subsection.

1. Right-click on your deployed model and select **Delete**.

### Delete the resource group

1. Open the [Azure portal](https://portal.azure.com).

1. Navigate to the resource group containing your AI Foundry resources.

1. Select **Delete resource group** and confirm the deletion.