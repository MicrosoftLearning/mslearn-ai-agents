---
lab:
    title: 'Build AI agents with portal and VS Code'
    description: 'Create an AI agent using both Microsoft Foundry portal and the AI Toolkit VS Code extension with built-in tools like file search and code interpreter, then use it in a web chat application.'
    level: 300
    duration: 45
    islab: true
---

# Build AI agents with portal and VS Code

In this exercise, you'll build a complete AI agent solution end to end. You'll start by creating and configuring an agent in the Microsoft Foundry portal, refine it using the AI Toolkit extension in VS Code, and then run a web chat application that lets you interact with your deployed agent through a browser-based UI.

This exercise takes approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting this exercise, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine
- [Python 3.13](https://www.python.org/downloads/) or later installed
- [Git](https://git-scm.com/downloads) installed on your local machine
- Basic familiarity with Azure AI services and Python programming

> \* Python 3.13 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

1. In the top banner, select **Start building** to try the new Microsoft Foundry Experience.

1. When prompted, create a **new** project, and enter a valid name for your project (e.g., `it-support-agent-project`).

1. Expand **Advanced options** and specify the following settings:
    - **Microsoft Foundry resource**: *A valid name for your Foundry resource*
    - **Region**: *Select one available near you*\**
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select your resource group, or create a new one*

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created.

2. When your project is created, a welcome dialog may appear. Select **Next** to read through the welcome message, and then select **Create agent**.

    You can also select **Start building** on the home page, and select **Create agents** from the drop-down menu.

3. Set the **Agent name** to `it-support-agent` and create the agent.

The playground will open for your newly created agent. You'll see that an available deployed model is already selected for you.

## Configure your agent with instructions and grounding data

Now that you have an agent created, let's configure it with instructions and add grounding data.

1. In the agent playground, set the **Instructions** to:

    ```prompt
    You are an IT Support Agent for Contoso Corporation.
    You help employees with technical issues and IT policy questions.
    
    Guidelines:
    - Always be professional and helpful
    - Use the IT policy documentation to answer questions accurately
    - If you don't know the answer, admit it and suggest contacting IT support directly
    - When creating tickets, collect all necessary information before proceeding
    ```

1. Download the IT policy document from the lab repository. Open a new browser tab and navigate to:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-build-agent-portal-and-vscode/IT_Policy.txt
    ```

    Save the file to your local machine.

    > **Note**: This document contains sample IT policies for password resets, software installation requests, and hardware troubleshooting.

1. Return to the agent playground. In the **Tools** section, enable both **File search** and **Code interpreter**.

1. Under **File search**, select **Upload files** and upload the `IT_Policy.txt` file you just downloaded.

1. Wait for the file to be indexed. You'll see a confirmation when it's ready.

1. Now let's add some performance data for the code interpreter to analyze. Download the system performance data file from:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/01-build-agent-portal-and-vscode/system_performance.csv
    ```

    Save this file to your local machine.

1. Under **Code interpreter**, select **Upload files** and upload the `system_performance.csv` file you just downloaded.

    > **Note**: This CSV file contains simulated system metrics (CPU, memory, disk usage) over time that the agent can analyze.

## Test your agent in the portal

Let's test the agent to see how it responds using the grounding data.

1. In the chat interface on the right side of the playground, enter the following prompt:

    ```
    What's the policy for password resets?
    ```

1. Review the response. The agent should reference the IT policy document and provide accurate information about password reset procedures.

1. Try another prompt:

    ```
    How do I request new software?
    ```

1. Again, review the response and observe how the agent uses the grounding data.

1. Now test the code interpreter with a data analysis request:

    ```
    Can you analyze the system performance data and tell me if there are any concerning trends?
    ```

1. The agent should use the code interpreter to analyze the CSV file and provide insights about system performance.

1. Try asking for a visualization:

    ```
    Create a chart showing CPU usage over time from the performance data
    ```

1. The agent will use code interpreter to generate visualizations and analysis.

Great! You've created an agent with grounding data, file search, and code interpreter capabilities. In the next section, you'll work with this agent in VS Code.

## Refine your agent in VS Code

As a developer, you may spend some time working in the Foundry portal; but you're also likely to spend a lot of time in Visual Studio Code. The AI Toolkit extension provides a convenient way to work with Foundry project resources without leaving the development environment.

### Install and configure the AI Toolkit extension

If you already have the AI Toolkit extension installed, you can skip this section.

1. Open Visual Studio Code.

2. Select **Extensions** from the left pane (or press **Ctrl+Shift+X**).

3. Search the extensions marketplace for the `AI Toolkit` extension from Microsoft and select **Install**.

4. After installing the extension, select its icon in the sidebar to open the AI Toolkit view.

    You should be prompted to sign in to your Azure account if you haven't already.

### Test and update your agent in VS Code

1. In **My Resources**, under **Microsoft Foundry** select the three horizontal bar icon to select your default project.

    If a default project is already active, the project name will appear next to the **Microsoft Foundry** section. You can select a different project by selecting the same **Select project** icon.

2. Expand the **Microsoft Foundry** section. Under **Agents**, you should see the `it-support-agent` you created in the portal. Select the agent name to open the Agent Builder interface.

    The agent playground will appear in the Agent Builder interface, allowing you to interact with the agent and configure its settings without leaving VS Code.

3. In the playground chat pane, test the agent with a question:

    ```
    What is the policy for reporting a lost or stolen device?
    ```

4. Review the agent's response. It should use the grounding data you uploaded earlier to provide relevant IT policy information.

5. Now let's refine the agent's instructions. In the Agent Builder, update the **Instructions** to add response formatting guidelines:

    ```prompt
    You are an IT Support Agent for Contoso Corporation.
    You help employees with technical issues and IT policy questions.
    
    Guidelines:
    - Always be professional and helpful
    - Use the IT policy documentation to answer questions accurately
    - If you don't know the answer, admit it and suggest contacting IT support directly
    - When creating tickets, collect all necessary information before proceeding
    - Format responses using markdown for readability (use headers, lists, and bold text)
    - When analyzing data, always provide a brief summary before detailed findings
    ```

6. Test the updated instructions with another question to see the improved formatting:

    ```
    Give me a complete overview of the VPN access policy
    ```

7. Notice how the response now uses markdown formatting to make the information clearer and more structured.

    > **Tip**: The Agent Builder in VS Code lets you rapidly iterate on your agent's configuration. You can update instructions, manage tools, and test changes — all without switching back to the portal.

## Build a web chat application

Now that your agent is configured and working, let's connect it to a real web application. You'll run a Flask-based chat app that provides a browser UI for interacting with your deployed agent.

### Clone the lab repository

1. In VS Code, open the Command Palette (**Ctrl+Shift+P** or **View > Command Palette**).

1. Type **Git: Clone** and select it from the list.

1. Enter the repository URL:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Choose a location on your local machine to clone the repository.

1. When prompted, select **Open** to open the cloned repository in VS Code.

1. Once the repository opens, select **File > Open Folder** and navigate to `mslearn-ai-agents/Labfiles/01-build-agent-portal-and-vscode/Python`, then choose **Select Folder**.

### Explore the web application code

Before running the app, take a moment to understand how it works.

1. In the Explorer pane, you'll see the following project structure:

    - `app.py` — The Flask backend that connects to your Foundry agent
    - `templates/chat.html` — The HTML template for the chat interface
    - `static/css/style.css` — Styling for the chat UI
    - `static/js/chat.js` — Frontend JavaScript that handles messaging
    - `.env.example` — Template for environment configuration
    - `requirements.txt` — Python dependencies

1. Open `app.py` and review the key components:

    - **`get_azure_clients()`** — Lazily initializes the Azure AI Projects SDK and loads your agent. This means the app only connects to Azure when the first request comes in, making startup errors easier to diagnose.
    - **`/api/conversation`** (POST) — Creates a new conversation session with the agent.
    - **`/api/chat`** (POST) — Sends a user message to the agent and returns the response, including any text, citations from file search, and images generated by code interpreter.
    - **`extract_response()`** — Parses the agent's response to extract structured content (text, source citations, and generated images).

1. Open `static/js/chat.js` and notice how the frontend:

    - Creates a conversation when the page loads
    - Sends messages via the `/api/chat` endpoint
    - Renders agent responses with markdown formatting
    - Displays source citations when the agent references grounding data
    - Shows generated charts and images inline

### Configure and run the application

1. Duplicate the `.env.example` file, and rename the copy to `.env`.

1. In the `.env` file, replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    AGENT_NAME=it-support-agent
    ```

    **To get your project endpoint:** In VS Code, open the **AI Toolkit** extension, right-click on your active project, and select **Copy Endpoint**.

1. Save the `.env` file (**Ctrl+S** or **File > Save**).

1. Open a terminal in VS Code (**Terminal > New Terminal**).

1. Install the required packages and sign in to Azure:

    ```bash
    pip install -r requirements.txt
    ```

    ```bash
    az login
    ```

1. Start the web application:

    ```bash
    python app.py
    ```

1. You should see output indicating the Flask server is running:

    ```
     * Running on http://127.0.0.1:5000
    ```

1. Open a browser and navigate to `http://127.0.0.1:5000`. The Contoso IT Support chat interface will appear.

## Test the web application

With the chat app running in your browser, test the full range of agent capabilities.

1. Start with a policy question to test **file search**. Type in the chat or select one of the suggestion chips:

    ```
    What's the policy for password resets?
    ```

    Notice that the response includes a **Sources** section at the bottom, showing which documents the agent referenced.

2. Test **code interpreter** with a data analysis request:

    ```
    Analyze the system performance data and identify any periods where CPU usage exceeded 80%
    ```

3. Request a **visualization** to see inline chart rendering:

    ```
    Create a line chart showing memory usage trends over time
    ```

    The agent will generate a chart using code interpreter, and it will appear inline in the chat.

4. Try a **combined query** that exercises both tools:

    ```
    Based on the IT policy, what's the escalation process for critical issues? Also, were there any critical performance spikes in the system data?
    ```

5. Start a **new conversation** by selecting the **+ New Chat** button in the header, then try:

    ```
    What are the average, minimum, and maximum values for disk usage in the performance data?
    ```

Observe how the web application provides a rich, interactive experience — rendering markdown-formatted responses, displaying source citations from grounding data, and showing generated charts inline. This is the same agent you built and tested in the portal and VS Code, now accessible through a real application.

Press **Ctrl+C** in the terminal to stop the web server when you're done testing.

## Summary

In this exercise, you built an AI agent in the Microsoft Foundry portal with file search and code interpreter tools, refined it using the AI Toolkit extension in VS Code, and connected it to a Flask-based web chat application.

## Clean up

To avoid unnecessary Azure charges, delete the resources you created:

1. In the Foundry portal, navigate to your project
1. Select **Settings** > **Delete project**
1. Alternatively, delete the entire resource group from the Azure portal
