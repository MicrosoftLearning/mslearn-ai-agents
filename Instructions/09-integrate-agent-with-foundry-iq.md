---
lab:
    title: 'Integrate an AI agent with Foundry IQ'
    description: 'Use Azure AI Agent Service to develop an agent that uses Foundry IQ to search knowledge bases.'
---

# Integrate an AI agent with Foundry IQ

In this exercise, you'll use Azure AI Foundry portal to create an agent that integrates with Foundry IQ to search and retrieve information from knowledge bases. You'll create a search resource, configure a knowledge base with sample data, build an agent in the portal, and then connect to it from Visual Studio Code to interact programmatically.

> **Tip**: The code used in this exercise is based on the Microsoft Foundry SDK for Python. You can develop similar solutions using the SDKs for Microsoft .NET, JavaScript, and Java. Refer to [Microsoft Foundry SDK client libraries](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/sdk-overview) for details.

This exercise should take approximately **45** minutes to complete.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Create a Foundry project

Let's start by creating a Foundry project with the new Foundry experience.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.

    > **Important**: Make sure the **New Foundry** toggle is *On* for this lab to use the updated user interface.

1. Once you toggle to the **New Foundry**, you'll be asked to select a project. In the dropdown, select **Create a new project**.
1. In the **Create a project** dialog, enter a valid name for your project (for example, *agent-iq-lab*).
1. Confirm or configure the following settings for your project:
    - **Hub**: *Create a new hub or select an existing one*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: *Select any available region*\*

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created. This may take a few minutes.
1. When your project is created, you'll see the project home page.

## Create an agent

1. On the home page, under **Start building**, select **Create an agent**.
1. Give your agent a name, such as `product-expert-agent`.
1. Select **Create**.

When creating an agent, it will deploy the default model (like `gpt-4.1`). Once your agent is created, you'll see the agent playground with that default model automatically selected for you.

## Configure your data and Foundry IQ

Now you'll configure your agent that uses Foundry IQ to search the knowledge base.

1. First, give your agent the following instructions:
    ```
    You are a helpful AI assistant for Contoso, specializing in outdoor camping and hiking products. 
    You must ALWAYS search the knowledge base to answer questions about our products or product 
    catalog. Provide detailed, accurate information and always cite your sources.
    If you don't find relevant information in the knowledge base, say so clearly.
    ```

1. Select **Save** to save your current agent configuration.
1. Then, in the **Knowledge** section, expand the **Add** dropdown, and select **Connect to Foundry IQ**.
1. In the Foundry IQ setup window, select **Connect to an AI Search resource** and then **Create new resource** which should open up the Azure portal in a new tab.
1. Create a search resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Use the same resource group as your project*
    - **Service name**: *A globally unique name*
    - **Location**: *The same location as your project*
    - **Pricing tier**: *Free* if available, otherwise choose *Basic*

Now you'll upload sample product information documents to connect to with Foundry IQ.

1. Download the sample product information files by opening a new browser tab and navigating to `https://github.com/MicrosoftLearning/mslearn-ai-agents/raw/main/Labfiles/09-integrate-agent-with-foundry-iq/data/contoso-products.zip`
1. Extract the files from the zip, which should be 3 PDFs detailing the products from Contoso.
1. In the Azure Portal tab, in the top search bar, search fo **Storage accounts** and select **Storage accounts** from the services section.
1. Create a storage account with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Use the same resource group as your project*
    - **Storage account name**: *A unique storage account name*
    - **Region**: *The same location as your project*
    - **Preferred storage type**: *Azure Blob Storage or Azure Data Lake Storage Gen 2*
    - **Performance**: *Standard*
    - **Redundancy**: *Locally-redundant storage (LRS)*
1. Once created, go to the storage account you created and select **Upload** from the top bar.
1. In the **Upload blob** blade, create a new container named `contosoproducts`.
1. Browse for the files extracted from the zip file, select all 3 PDF files, and select **Upload**.
1. Once your files are uploaded, close the Azure Portal tab and navigate back to the Foundry IQ page in Microsoft Foundry and refresh the page.
1. Select your search service, and click **Connect**.
1. On the Foundry IQ page, select **Create a knowledge base**, choosing **Azure Blob Storage** as your knowledge source, then select **Connect**.
1. Configure your knowledge source with the following settings:
    - **Name**: `ks-contosoproducts`
    - **Description**: `Contoso product catalog items`
    - **Storage account name**: *Select your storage account*
    - **Container name**: `contosoproducts`
    - **Content extraction mode**: *minimal*
    - **Authentication type**: *API Key*
    - **Include embedding model**: *Selected*
    - **Embedding model**: *Select the available deployed model, likely text-embedding-3-small*
    - **Chat completions model**: *Select the available deployed model, likely gpt-4.1*
1. Select **Create**.
1. On the knowledge base creation page, select the `gpt-4.1` model from the **Chat completions model** dropdown, leaving the rest of the optional fields as is.
1. Select **Save knowledge base**, and then refresh your browser to verify the knowledge source status is *active*. If it isn't yet, wait a minute and refresh your page until it is.
1. On the top right, expand the **Use in an agent** dropdown, and select your `product-expert-agent`.

## Test the Agent in the playground

Before connecting from code, test your agent in the portal playground.

1. In the agent page, you should see a playground tab selected and your knowledge base listed in the knowledge section.
1. Try the following test queries to verify the agent can retrieve information from the knowledge base:
    - `What types of tents does Contoso offer?`
    - `Tell me about which backpacks are available in XL.`
    - `What camping accessories are available?`
    
1. Review the responses and notice:
    - The agent provides specific information from the knowledge base
    - Citations or references to the source documents may be included
    - The agent stays focused on product information

1. You can also try interacting with your agent in the **Preview agent** for a more refined webapp experience.

1. In the agent details page, locate and copy the following information to a notepad (you'll need these later):
    - **Agent name**: This is the name you created (`product-expert-agent`)
    - **Project endpoint**: Found in the project settings or overview page

## Connect to Your Agent from Visual Studio Code

Now you'll create a Python application to interact with your agent programmatically. Starter files have been provided in the GitHub repository to help you get started quickly.

### Clone the repository and set up the environment

1. Open **Visual Studio Code** on your local machine.
1. In VS Code, open a terminal (View > Terminal).
1. Clone the repository and navigate to the lab folder:

    ```bash
    git clone https://github.com/MicrosoftLearning/mslearn-ai-agents
    cd mslearn-ai-agents/Labfiles/09-integrate-agent-with-foundry-iq/Python
    ```

1. Create a virtual environment and activate it:

    **Windows (PowerShell):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

    **macOS/Linux:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Configure the application

1. Open the `.env` file in VS Code.
1. Replace the placeholder values with your actual values:
    - Replace `your_project_endpoint` with your project endpoint (from earlier)
    - Replace `your_agent_name` with your agent name (should be `product-expert-agent`)
1. Save the file.

### Complete the agent client code

1. Open the `agent_client.py` file in VS Code. Review the starter code that has been provided, including:
    - Import statements and configuration loading
    - The `send_message_to_agent()` function structure
    - The `display_conversation_history()` function
    - The main program loop

1. Find the first **TODO** comment and add the following code to connect to the project, get the OpenAI client, retrieve the agent, and create a new conversation:

    ```python
    # Connect to the project and agent
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        credential=credential,
        endpoint=project_endpoint
    )

    # Get the OpenAI client
    openai_client = project_client.get_openai_client()

    # Get the agent
    agent = project_client.agents.get(agent_name=agent_name)
    print(f"Connected to agent: {agent.name} (id: {agent.id})\n")

    # Create a new conversation
    conversation = openai_client.conversations.create(items=[])
    print(f"Created conversation (id: {conversation.id})\n")
    ```

1. Find the second **TODO** comment inside the `send_message_to_agent()` function and add the following code to send messages and handle responses using the conversations API:

    ```python
    # Add user message to the conversation
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )
    
    # Create a response using the agent
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        input=""
    )
    
    # Extract the response text
    if response and response.output_text:
        response_text = response.output_text
        
        print(f"{response_text}\n")
        
        # Check for citations if available
        if hasattr(response, 'citations') and response.citations:
            print("\nSources:")
            for citation in response.citations:
                print(f"  - {citation.content if hasattr(citation, 'content') else 'Knowledge Base'}")
        
        # Store in conversation history (client-side)
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    else:
        print("No response received.\n")
        return None
    ```

1. Save the file. The code now uses the conversations API to manage interactions with your agent, where:
    - A conversation is created and tracked by its ID
    - User messages are added to the conversation using `conversations.items.create()`
    - Responses are generated using `responses.create()` with an agent reference
    - The agent automatically retrieves information from Foundry IQ as needed

## Test the Integration

Now you'll run your application and test the agent's ability to retrieve information from the knowledge base.

### Sign in to Azure

1. In the VS Code terminal, sign in to Azure:

    ```bash
    az login
    ```

1. Follow the prompts to complete the authentication process.

### Run the application

1. In the VS Code terminal, run your application:

    ```bash
    python agent_client.py
    ```

1. When the application starts, test the agent with the following queries:

    **Query 1 - Product Categories:**
    ```
    What types of outdoor products does Contoso offer?
    ```
    
    Observe how the agent retrieves information from multiple documents in the knowledge base.

    **Query 2 - Specific Product Details:**
    ```
    Tell me about the weatherproof features of your tents.
    ```
    
    Notice how the agent provides specific details from the tents catalog.

    **Query 3 - Product Comparisons:**
    ```
    What's the difference between your daypacks and expedition backpacks?
    ```
    
    See how the agent can synthesize information from the backpacks guide.

    **Query 4 - Accessories and Add-ons:**
    ```
    What camping accessories would you recommend for a weekend hiking trip?
    ```
    
    Observe the agent's ability to provide recommendations based on the knowledge base.

    **Query 5 - Follow-up Question:**
    ```
    How much do those items typically cost?
    ```
    
    Notice how the agent maintains conversation context from your previous query.

1. Type `history` to view the complete conversation history.

1. Type `quit` when you're done testing.

### Review the results

Consider the following aspects of the agent's responses:

- **Accuracy**: The agent provides information directly from the knowledge base documents
- **Citations**: The agent may include source references or document IDs
- **Context awareness**: The agent remembers previous messages in the conversation
- **Grounding**: The agent indicates when it cannot find relevant information in the knowledge base
- **Error handling**: The application gracefully handles errors and connection issues

## Summary

In this exercise, you:

- Created a Foundry project with the new Foundry UI
- Deployed a GPT-4.1 language model
- Created an Azure AI Search resource from the Foundry portal
- Built a knowledge base with product information documents
- Created an agent in the portal with Foundry IQ enabled
- Connected to your agent from Visual Studio Code using the Python SDK
- Implemented a client application with conversation history, error handling, and streaming support
- Tested the agent's ability to retrieve and synthesize information from the knowledge base

This demonstrates how to integrate AI agents with Foundry IQ to create intelligent applications that can search and retrieve information from enterprise knowledge bases while maintaining conversational context.

## Clean up

If you've finished exploring Azure AI Agent Service and Foundry IQ, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Close Visual Studio Code.
1. Return to your browser and open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
1. Navigate to the resource group containing your Foundry hub and AI Search resources.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.

