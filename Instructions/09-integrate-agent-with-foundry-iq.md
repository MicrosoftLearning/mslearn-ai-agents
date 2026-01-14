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

1. In the home page, select **+ Create project**.
1. In the **Create a project** dialog, enter a valid name for your project (for example, *agent-iq-lab*).
1. Confirm or configure the following settings for your project:
    - **Hub**: *Create a new hub or select an existing one*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: *Select any available region*\*

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created. This may take a few minutes.
1. When your project is created, you'll see the project home page.

## Deploy a language model

Before creating your agent, you need a language model deployed in your project.

1. In the left navigation pane, under **My assets**, select **Models + endpoints**.
1. Select **+ Deploy model**, then choose **Deploy base model**.
1. Search for and select the **gpt-4.1** model, then select **Confirm**.
1. Use the default deployment settings:
    - **Deployment name**: *gpt-4.1*
    - **Deployment type**: *Standard* or *Global Standard* (depending on availability)
    - **Model version**: *Default*
    
1. Select **Deploy** and wait for the deployment to complete.

## Create a Search Resource

To use Foundry IQ, you need an Azure AI Search resource to power the knowledge base.

1. In the left navigation pane, select **AI Search**.
1. Select **+ New AI Search**.
1. Configure the search resource with the following settings:
    - **Search service name**: *A globally unique name*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Use the same resource group as your project*
    - **Location**: *The same location as your project*
    - **Pricing tier**: *Basic* or *Standard*
    
1. Select **Create** and wait for the search resource to be provisioned. This may take a few minutes.
1. Once the deployment completes, **refresh your browser** to see the new search resource available in your project.

## Create a Knowledge Base

Now you'll create a knowledge base with sample product information documents.

1. Download the sample product information files:
    - In a new browser tab, navigate to `https://github.com/MicrosoftLearning/mslearn-ai-agents/tree/main/Labfiles/09-integrate-agent-with-foundry-iq/data`
    - Download the following PDF files to your local computer:
        - `contoso-tents-catalog.pdf`
        - `contoso-backpacks-guide.pdf`
        - `contoso-camping-accessories.pdf`

1. In the Foundry portal, in the left navigation pane, select **Data + indexes**.
1. Select **+ New data source**.
1. Choose **Upload files** as the data source type.
1. Configure the data source:
    - **Data source name**: *contoso-products*
    - **Index name**: *contoso-products-index*
    
1. Select **Browse** and upload the three PDF files you downloaded.
1. Select **Next** to configure the index settings:
    - **Vector settings**: Enable vector search
    - **Chunk size**: *Default (1024)*
    - **Overlap**: *Default (128)*
    
1. Select **Create** and wait for the indexing process to complete. This may take several minutes as the documents are processed and embedded.
1. When complete, you should see your data source and index listed in the **Data + indexes** page.

## Create an Agent in the Portal

Now you'll create an agent that uses Foundry IQ to search the knowledge base.

1. In the left navigation pane, select **Agents**.
1. Select **+ New agent**.
1. Configure the agent with the following settings:
    - **Agent name**: *product-expert-agent*
    - **Description**: *An AI agent that provides information about Contoso outdoor and camping products*
    - **Instructions**: Enter the following:
        ```
        You are a helpful AI assistant for Contoso, specializing in outdoor camping and hiking products. 
        Use the knowledge base to answer questions about our product catalog, including tents, backpacks, 
        and camping accessories. Provide detailed, accurate information and always cite your sources.
        If you don't find relevant information in the knowledge base, say so clearly.
        ```
    - **Model**: *gpt-4.1*
    - **Temperature**: *0.7*

1. In the **Tools** section, enable **Foundry IQ**.
1. Under Foundry IQ settings:
    - Select **+ Add data source**
    - Choose the **contoso-products-index** you created earlier
    - Set **Retrieval mode**: *Hybrid (vector + keyword)*
    - Set **Top K results**: *5*

1. Select **Create agent**.

## Test the Agent in the Portal

Before connecting from code, test your agent in the portal playground.

1. In the agent page, you should see a playground/chat interface on the right side.
1. Try the following test queries to verify the agent can retrieve information from the knowledge base:
    - `What types of tents does Contoso offer?`
    - `Tell me about the features of your waterproof backpacks.`
    - `What camping accessories are available?`
    
1. Review the responses and notice:
    - The agent provides specific information from the knowledge base
    - Citations or references to the source documents may be included
    - The agent stays focused on product information

1. In the agent details page, locate and copy the following information to a notepad (you'll need these later):
    - **Agent ID**: Found in the agent details or URL
    - **Project endpoint**: Found in the project settings or overview

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
    - Replace `your_agent_id` with your agent ID (from earlier)
1. Save the file.

### Complete the agent client code

1. Open the `agent_client.py` file in VS Code. Review the starter code that has been provided, including:
    - Import statements and configuration loading
    - The `send_message_to_agent()` function structure
    - The `display_conversation_history()` function
    - The main program loop

1. Find the first **TODO** comment and add the following code to connect to the project and create a conversation thread:

    ```python
    # Connect to the project and agent
    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        credential=credential,
        conn_str=project_endpoint
    )

    # Create an agent client
    agent_client = project_client.agents

    # Create a thread for the conversation
    thread = agent_client.create_thread()
    print(f"Created conversation thread: {thread.id}\n")
    ```

1. Find the second **TODO** comment inside the `send_message_to_agent()` function and add the following code to send messages and handle responses:

    ```python
    # Add user message to thread
    message = agent_client.create_message(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=user_message
    )
    
    # Run the agent
    run = agent_client.create_run(
        thread_id=thread.id,
        agent_id=agent_id
    )
    
    # Poll for completion
    while run.status in ["queued", "in_progress", "requires_action"]:
        run = agent_client.get_run(thread_id=thread.id, run_id=run.id)
        
    # Check for errors
    if run.status == "failed":
        print(f"\n\nError: Run failed - {run.last_error}\n")
        return None
    
    # Retrieve the agent's response
    messages = agent_client.list_messages(thread_id=thread.id)
    
    # Get the latest assistant message
    latest_message = None
    for msg in messages:
        if msg.role == MessageRole.ASSISTANT:
            latest_message = msg
            break
    
    if latest_message and latest_message.content:
        # Extract text content
        response_text = ""
        for content_item in latest_message.content:
            if isinstance(content_item, MessageTextContent):
                response_text = content_item.text.value
                break
        
        print(f"{response_text}\n")
        
        # Check for citations/annotations
        if latest_message.content[0].text.annotations:
            print("\nSources:")
            for annotation in latest_message.content[0].text.annotations:
                if hasattr(annotation, 'file_citation'):
                    print(f"  - {annotation.file_citation.file_id}")
        
        # Store in conversation history
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    else:
        print("No response received.\n")
        return None
    ```

1. Save the file.

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

