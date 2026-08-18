---
title: 'Task 1 – Create a Foundry IQ knowledge agent and connect from code'
lab:
    title: 'Task 1 – Create a Foundry IQ knowledge agent and connect from code'
    description: 'Create an enterprise-knowledge agent in the Microsoft Foundry portal, ground it on the Caldova knowledge base with Foundry IQ, require approval before knowledge lookups, then connect from code and handle the approval flow.'
    type: 'task'
    parent: 'B'
    order: 1
    section: 'core'
    difficulty: 3
    duration: 35
    access: 'open'
    level: 300
    concepts: 'Foundry IQ, enterprise knowledge grounding, tool approvals, conversations API'
    status: 'draft'
---

# Task 1 — Create a Foundry IQ knowledge agent and connect from code

*Part of the **Integrate agents with enterprise knowledge and Microsoft 365** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project (with a deployed model) and the
> starter code. If you haven't already, complete [Getting started](B0-getting-started.md) to
> create your project, clone the code, and set `PROJECT_ENDPOINT` and `MODEL_DEPLOYMENT_NAME`
> in `Python/.env`. Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 1
```

> **Continuing from a previous task?** If your project, virtual environment, and `.env` are
> already set, you can skip the setup and go straight to **Create an agent** below.

---

You'll build the **Caldova staff knowledge assistant**: an agent grounded on the
company's internal documents (site operations, plant capacity, CMO directory, tech transfer, suppliers)
using **Foundry IQ**, then connect to it from a Python app that controls each knowledge lookup with
an approval step.

<style>
/* "Ask Anton" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
  border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Anton: "; font-weight:700;
  padding-left:1.5em;
  background:url("../Media/anton-avatar.png") left center / 1.25em 1.25em no-repeat; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>What is Foundry IQ?</summary>
<div class="concept-body" markdown="1">

**Foundry IQ** connects an agent to a **knowledge base** — a searchable index built from your
own documents backed by Azure AI Search. When the agent needs facts, it performs *agentic
retrieval* against that knowledge base and cites what it finds. You can require **approval**
before each lookup so your application reviews and controls every knowledge-base access.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/)

</div>
</details>

## Create an agent

If you created the `caldova-knowledge-agent` during Getting started, open it now
(**Build** → **Agents** → **caldova-knowledge-agent**) and skip to **Configure your data and
Foundry IQ**. Otherwise:

1. On the home page, select the **Build** tab, then on the **Agents** tab select **Create agent**.
1. Create your agent with the name `caldova-knowledge-agent`.

When creating an agent, it deploys the default model (like `gpt-5`). Once your agent is created, you'll see the agent playground with that default model automatically selected for you.

## Configure your data and Foundry IQ

Now you'll configure your agent to use Foundry IQ to search the Caldova knowledge base.

1. First, give your agent the following instructions:

    ```
    You are the Caldova staff knowledge assistant, specializing in plant capacity,
    contract manufacturers, tech transfer, site operations, and suppliers. You must
    ALWAYS search the knowledge base to answer questions about our capacity, policies,
    or procedures. Provide detailed, accurate information and always cite your sources.
    If you don't find relevant information in the knowledge base, say so clearly.
    ```

1. Select **Save** to save your current agent configuration.
1. Then, in the **Knowledge** section, expand the **Add** dropdown, and select **Connect to Foundry IQ**.
1. In the Foundry IQ setup window, select **Connect to an AI Search resource** and then **Create new resource** which should open up a dialog to create the resource.
1. Create a search resource with the default settings:
    - **Resource name**: *A globally unique name*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Use the same resource group as your project*
    - **Region**: *The same location as your project*
    - **Pricing tier**: Free *if available, otherwise choose Basic*

Now you'll upload the Caldova knowledge documents to connect to with Foundry IQ.

1. Download the sample knowledge documents. These are the Markdown files in the starter code under `Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Python/data/`:
    - `caldova-site-operations.md`
    - `caldova-plant-capacity.md`
    - `caldova-cmo-directory.md`
    - `caldova-tech-transfer-playbook.md`
    - `caldova-capacity-booking-policy.md`
    - `caldova-supplier-guide.md`

    > **Tip**: You already have these locally from Getting started. If you'd rather download them directly, browse to the `data` folder in the [repository](https://github.com/MicrosoftLearning/mslearn-ai-agents/tree/main/Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Python/data) and save each file.

1. Open a new tab and navigate to the Azure portal at `https://portal.azure.com`. In the top search bar, search for **Storage accounts** and select **Storage accounts** from the services section.
1. Create a storage account with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Use the same resource group as your project*
    - **Storage account name**: *A unique storage account name*
    - **Region**: *The same location as your project*
    - **Primary service**: *Azure Blob Storage or Azure Data Lake Storage*
    - **Performance**: *Standard*
    - **Redundancy**: *Locally-redundant storage (LRS)*
1. Once created, go to the storage account you created and select **Upload** from the top bar.
1. In the **Upload blob** blade, create a new container named `caldovaproducts`.
1. Browse for the six Caldova Markdown files from the `data` folder, select all of them, and select **Upload**.
1. Once your files are uploaded, navigate to the search service you created.
1. On the left pane, under **Security + networking** > **Keys**, select **Both** for API Access control and confirm the selection. Once complete, leave the Azure Portal tab open and navigate back to the Foundry portal tab and refresh the page.
1. Verify you are on the **Knowledge** page, select **Create a knowledge base**, choosing **Azure Blob Storage** as your knowledge source, then select **Connect**.
1. Configure your knowledge source with the following settings:
    - **Name**: `ks-caldovaproducts`
    - **Description**: `Caldova staff knowledge base`
    - **Storage account name**: *Select your storage account*
    - **Container name**: `caldovaproducts`
    - **Authentication type**: *API Key*
    - **Content extraction mode**: *minimal*
    - **Embedding model**: *Select the available deployed model, likely text-embedding-3-small*
    - **Chat completions model**: *Select the available deployed model, likely gpt-5*
1. Select **Create**.
1. On the knowledge base creation page, select the `gpt-5` model from the **Chat completions model** dropdown, leaving the rest of the field defaults as is.
1. Select **Save knowledge base**, and then refresh your browser to verify the knowledge source status is *active*. If it isn't yet, wait a minute and refresh your page until it is.
1. Select the back button to return to the **Knowledge** page, then select the **Manage** link next to the *Connection* drop-down.
1. Scroll down to the **Connected resources**, where you should see your search service. Select that row, find the **Authentication** section.
1. Select **Key authentication** and then select **Edit authentication**.
1. Leaving the dialog open, return to the Azure portal tab which should still be on your search service **Keys** page. Copy one of those keys into the dialog in Foundry and select **Save**.

Your Foundry IQ settings should now be complete.

## Test the agent in the playground

Before connecting from code, test your agent in the portal playground.

1. Navigate back to your agent on the **Build** > **Agents** page, and select the agent you created.
2. In the agent page, you should see a playground tab selected. Find the knowledge section and add Foundry IQ, selecting the connection and knowledge base you created.
1. Try the following test queries to verify the agent can retrieve information from the knowledge base:
    - `Which sites can make oral solid dose product?`
    - `Tell me which contract manufacturers are qualified for sterile work.`
    - `How much headroom does Calderwood have?`

1. Review the responses and notice:
    - The agent provides specific information from the knowledge base
    - Citations or references to the source documents may be included
    - The agent stays focused on Caldova information

1. In the agent details page, locate and copy the following information to a notepad (you'll need these later):
    - **Agent name**: This is the name you created (`caldova-knowledge-agent`)
    - **Project endpoint**: Found in the project settings or home page

### Configure the agent to require approval for tool calls

When you create an agent in the portal, its Foundry IQ (knowledge) tool runs **without** asking for approval by default. To ensure your app can review and control each knowledge base lookup, you'll change the agent to require approval before it uses tools with the Foundry Toolkit for VS Code extension.

> **Note**: The Foundry portal doesn't currently expose a setting to change this approval behavior, so you'll configure it from the Foundry Toolkit extension instead.

1. In Visual Studio Code, select **Extensions** from the left pane (or press **Ctrl+Shift+X**), then search the marketplace for the `Foundry Toolkit for VS Code` extension from Microsoft and select **Install** (if it isn't already installed).

    > **Note**: The extension is currently listed as **Foundry Toolkit**, but some VS Code labels, commands, or older screenshots may still refer to **AI Toolkit**. In this lab, treat those names as referring to the same extension experience.

1. Select the **Foundry Toolkit** icon in the sidebar, and sign in to your Azure account if you're prompted.

    > **Note**: If you're unable to sign in with the Foundry Toolkit extension, you may need to select the Azure extension. Sign in there, then navigate back to the Foundry Toolkit to access your resources.

1. Under **Microsoft Foundry Resources**, choose **Set Default Project** and select the project you created earlier.
1. Expand the project section. Under **Prompt Agents**, select your `caldova-knowledge-agent` agent to open the **Agent Builder** window.
1. In the **Tools** section, find the tool named with a `kb-knowledgebase` prefix followed by a unique ID (for example, `kb-knowledgebase677-7w5fj`). This is the Foundry IQ knowledge base tool, and it was added automatically when you connected Foundry IQ in the portal.

    > **Note**: The agent lists more than one tool. The Foundry portal adds a **Web search** tool to new agents by default, and you may also see a standalone **Azure AI Search** tool. The agent actually calls the `kb-knowledgebase...` tool when it searches your knowledge base, so setting approval on any other tool has no effect.
1. Select the three dots on the `kb-knowledgebase...` tool. Then, in the **Require approval before using tools** dropdown, select **Ask for approval for all tools**, and save your changes if you're prompted.

Your agent will now request approval each time it uses Foundry IQ to search the knowledge base, which the client app you complete next will handle.

## Connect to your agent from code

Now you'll complete a Python console client that talks to your agent and handles the approval flow. The starter file is provided in the `Python` folder.

Open the `Python` folder and activate the virtual environment from [Getting started](B0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

1. In **Python/.env**, make sure `AGENT_NAME` is set to `caldova-knowledge-agent` (the default in `.env.example`). Save the file.

1. Open **knowledge_agent.py** and review the starter code, including:
    - Import statements and configuration loading
    - The `send_message_to_agent()` function structure
    - The `display_conversation_history()` function
    - The main program loop

1. Find the first **TODO** comment and add the following code to connect to the project, get the OpenAI client, retrieve the agent, and create a new conversation:

    > **Tip**: Be careful to maintain the correct indentation level.

    ```python
    # Connect to the project and agent
    credential = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
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

1. Find the second **TODO** comment inside the `send_message_to_agent()` function and add the following code to send messages and handle responses, including the Foundry IQ approval request:

    ```python
    # Add user message to the conversation
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": user_message}],
    )

    # Store in conversation history (client-side)
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Create a response using the agent
    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        input=""
    )

    # Check if the response output contains an MCP approval request
    approval_request = None
    if hasattr(response, 'output') and response.output:
        for item in response.output:
            if hasattr(item, 'type') and item.type == 'mcp_approval_request':
                approval_request = item
                break

    # Handle approval request if present
    if approval_request:
        print(f"[Approval required for: {approval_request.name}]\n")
        print(f"Server: {approval_request.server_label}")

        # Parse and display the arguments (optional, for transparency)
        import json
        try:
            args = json.loads(approval_request.arguments)
            print(f"Arguments: {json.dumps(args, indent=2)}\n")
        except Exception:
            print(f"Arguments: {approval_request.arguments}\n")

        # Prompt user for approval
        approval_input = input("Approve this action? (yes/no): ").strip().lower()

        if approval_input in ['yes', 'y']:
            print("Approving action...\n")

            # Create approval response item
            approval_response = {
                "type": "mcp_approval_response",
                "approval_request_id": approval_request.id,
                "approve": True
            }
        else:
            print("Action denied.\n")

            # Create denial response item
            approval_response = {
                "type": "mcp_approval_response",
                "approval_request_id": approval_request.id,
                "approve": False
            }

        # Add the approval response to the conversation
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[approval_response]
        )

        # Get the actual response after approval/denial
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            input=""
        )
    ```

1. After you've added the code, save the file.

1. Review how the code uses the conversations API to manage interactions with your agent, where:
    - A conversation is created and tracked by its ID
    - User messages are added to the conversation using `conversations.items.create()`
    - Responses are generated using `responses.create()` with an agent reference
    - **Approval handling**: When the agent needs to access Foundry IQ, it returns an `mcp_approval_request` in the response output
    - The code prompts you to approve or deny the action before proceeding
    - After approval/denial, an `mcp_approval_response` is added to the conversation and a new response is generated

## Test the integration

Now you'll run your application and test the agent's ability to retrieve information from the knowledge base.

1. In the terminal (in the `Python` folder), sign into Azure:

    ```
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter.

1. When prompted, complete the sign-in process, selecting the subscription containing your Foundry resource if prompted.

1. Run your application:

    ```
    python knowledge_agent.py
    ```

1. When the application starts, test the agent with the following queries:

    **Query 1 - Product categories:**

    ```
    Which sites can make oral solid dose product?
    ```

    When prompted for approval, type **yes** to allow the agent to search the knowledge base. Observe how the agent retrieves information from multiple documents.

    **Query 2 - Capacity policy:**

    ```
    How much headroom does Calderwood have and how are transfer costs calculated?
    ```

    Approve the request and notice how the agent provides specific details from the capacity request policy.

    **Query 3 - Contract manufacturer comparison:**

    ```
    What's the difference between Norvent and Halden for a sterile transfer?
    ```

    Approve the request and see how the agent synthesizes information from the CMO directory.

    **Query 4 - Supplier and reorder:**

    ```
    When should we reorder sterile vials, and who is our component supplier?
    ```

    Approve the request and observe the agent answering from the supplier guide.

    **Query 5 - Follow-up question:**

    ```
    What are our site core hours?
    ```

    Notice how the agent maintains conversation context and answers from the site operations doc.

1. Type `history` to view the complete conversation history.

1. Type `quit` when you're done testing.

> ✅ **Checkpoint**: You've created and **grounded** an enterprise-knowledge agent with Foundry
> IQ, required **approval** before each knowledge lookup, and connected to it from code —
> handling the approval flow yourself. That's the Core of this lab. Everything below is optional.

### Optional: run the same agent as a web chat app

The same grounded agent can be served through the shared Caldova web chat window. From the `Python` folder, run:

```
python knowledge_chat_app.py
```

A browser opens at `http://localhost:7860` with the **Caldova Staff Knowledge Assistant**. This variant **auto-approves** the Foundry IQ knowledge tool so the chat stays smooth. Ask it the same questions as above. Close the tab and press **Ctrl+C** to stop it.

> **Fast-forward**: If you'd rather ground an agent in code instead of the portal, run
> `python ../setup/bootstrap_agent.py` from the `Python` folder. It creates
> `caldova-knowledge-agent`, grounds it on the six knowledge docs with File Search, and writes
> `AGENT_NAME` to `.env`. The client code you run against it is identical.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next (optional):** [Task 2 — Publish to Microsoft Teams](B2-publish-to-microsoft-teams.md) · [Task 3 — Publish to Microsoft 365 Copilot](B3-publish-to-microsoft-365-copilot.md) · [Task 4 — Work IQ](B4-work-iq-workplace-intelligence.md)
