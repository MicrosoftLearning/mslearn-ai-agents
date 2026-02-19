---
lab:
    title: 'Build AI Agents with Portal and VS Code'
    description: 'Create an AI agent using both Microsoft Foundry portal and VS Code extension with built-in tools like file search and code interpreter.'
    level: 300
    duration: 45
---

# Build AI Agents with Portal and VS Code

In this exercise, you'll build a complete AI agent solution using both the Microsoft Foundry portal and the Microsoft Foundry VS Code extension. You'll start by creating a basic agent in the portal with grounding data and built-in tools, then interact with it programmatically using VS Code to leverage advanced capabilities like code interpreter for data analysis.

This exercise takes approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Learning Objectives

By the end of this exercise, you'll be able to:

1. Create and configure an AI agent in the Microsoft Foundry portal
2. Add grounding data and enable built-in tools (file search, code interpreter)
3. Use the Microsoft Foundry VS Code extension to work with agents programmatically
4. Leverage code interpreter to analyze data and generate insights
5. Understand when to use portal-based vs code-based approaches for agent development

## Prerequisites

Before starting this exercise, ensure you have:

- An Azure subscription with sufficient permissions and quota to provision Azure AI resources
- Visual Studio Code installed on your local machine
- Python 3.12 or later installed
- Basic familiarity with Azure AI services and Python programming

## Scenario

You'll build an **IT Support Agent** that helps employees with common technical issues. The agent will:

- Answer questions based on IT policy documentation (grounding data)
- Use built-in tools like file search to find relevant information
- Analyze system performance data using code interpreter to identify trends and issues

---

## Create an AI agent in Microsoft Foundry portal

Let's start by creating a Foundry project and a basic agent using the portal.

### Create a Foundry project

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

1. In the top banner, select **Start building** to try the new Microsoft Foundry Experience.

1. When prompted, create a **new** project, and enter a valid name for your project (e.g., `it-support-agent-project`).

1. Expand **Advanced options** and specify the following settings:
    - **Microsoft Foundry resource**: *A valid name for your Foundry resource*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Select your resource group, or create a new one*
    - **Region**: *Select any **AI Foundry recommended***\**

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created.

1. When your project is created, select **Start building**, and select **Create agent** from the drop-down menu.

1. Set the **Agent name** to `it-support-agent` and create the agent.

The playground will open for your newly created agent. You'll see that an available deployed model is already selected for you.

### Configure your agent with instructions and grounding data

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

### Test your agent

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

Great! You've created an agent with grounding data, file search, and code interpreter capabilities. In the next section, you'll interact with this agent programmatically using VS Code.

---

## Interact with your agent using VS Code

Now you'll use the Microsoft Foundry VS Code extension to work with your agent programmatically and see how to interact with it from code.

### Install and configure the VS Code extension

If you already have installed the extension for Foundry, you can skip this section.

1. Open Visual Studio Code on your local machine.

1. Select **Extensions** from the left pane (or press **Ctrl+Shift+X**).

1. In the search bar, type **Microsoft Foundry** and press Enter.

1. Select the **Microsoft Foundry** extension from Microsoft and click **Install**.

1. After installation is complete, verify the extension appears in the primary navigation bar on the left side.

### Connect to your Foundry project

1. In the VS Code sidebar, select the **Microsoft Foundry** extension icon.

1. In the Resources view, select **Sign in to Azure...** and follow the authentication prompts.

    > **Note**: You won't see this option if you're already signed in.

1. After signing in, expand your subscription in the Resources view.

1. Locate and expand your Foundry resource, then find the project you created earlier (`it-support-agent-project`).

1. Right-click on your project and select **Set as active project**.

1. Expand your project in the Resources view and verify you can see your `it-support-agent` listed under **Agents**.

### Create a Python application

Now let's create a Python application that interacts with your agent programmatically.

1. In VS Code, open the Command Palette (**Ctrl+Shift+P** or **View > Command Palette**).

1. Type **Git: Clone** and select it from the list.

1. Enter the repository URL:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Choose a location on your local machine to clone the repository.

1. When prompted, select **Open** to open the cloned repository in VS Code.

1. Once the repository opens, select **File > Open Folder** and navigate to `mslearn-ai-agents/Labfiles/01-build-agent-portal-and-vscode/Python`, then click **Select Folder**.

1. In the Explorer pane, open the `agent_with_functions.py` file. You'll see it's currently empty.

1. Add the following code to the file:

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    import base64
    from pathlib import Path
    
    
    def save_image(image_data, filename):
        """Save base64 image data to a file."""
        output_dir = Path("agent_outputs")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / filename
        
        # Decode and save the image
        image_bytes = base64.b64decode(image_data)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        return str(filepath)
    
    
    def main():
        # Initialize the project client
        project_endpoint = os.environ.get("PROJECT_ENDPOINT")
        agent_name = os.environ.get("AGENT_NAME", "it-support-agent")
        
        if not project_endpoint:
            print("Error: PROJECT_ENDPOINT environment variable not set")
            print("Please set it in your .env file or environment")
            return
        
        print("Connecting to Microsoft Foundry project...")
        credential = DefaultAzureCredential()
        project_client = AIProjectClient(
            credential=credential,
            endpoint=project_endpoint
        )
        
        # Get the OpenAI client for Responses API
        openai_client = project_client.get_openai_client()
        
        # Get the agent created in the portal
        print(f"Loading agent: {agent_name}")
        agent = project_client.agents.get(agent_name=agent_name)
        print(f"Connected to agent: {agent.name} (id: {agent.id})")
        
        # Create a conversation
        conversation = openai_client.conversations.create(items=[])
        print(f"Conversation created (id: {conversation.id})")
        
        # Chat loop
        print("\n" + "="*60)
        print("IT Support Agent Ready!")
        print("Ask questions, request data analysis, or get help.")
        print("Type 'exit' to quit.")
        print("="*60 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Add user message to conversation
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}]
            )
            
            # Get response from agent
            print("\n[Agent is thinking...]")
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                input=""
            )
            
            # Display response
            if hasattr(response, 'output_text') and response.output_text:
                print(f"\nAgent: {response.output_text}\n")
            elif hasattr(response, 'output') and response.output:
                # Extract text from output items
                image_count = 0
                for item in response.output:
                    if hasattr(item, 'text') and item.text:
                        print(f"\nAgent: {item.text}\n")
                    elif hasattr(item, 'type'):
                        # Handle other output types like images from code interpreter
                        if item.type == 'image':
                            image_count += 1
                            filename = f"chart_{image_count}.png"
                            
                            # Download and save the image
                            if hasattr(item, 'image') and hasattr(item.image, 'data'):
                                filepath = save_image(item.image.data, filename)
                                print(f"\n[Agent generated a chart - saved to: {filepath}]")
                            else:
                                print(f"\n[Agent generated an image]")
                        elif item.type == 'file':
                            print(f"\n[Agent created a file]")
    
    
    if __name__ == "__main__":
        main()
    ```

### Configure environment and run the application

1. In the Explorer pane, you'll see `.env.example` and `requirements.txt` files already present in the folder.

1. Duplicate the `.env.example` file, and rename to `.env`.

1. In the `.env` file, replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    AGENT_NAME=it-support-agent
    ```
    
    **To get your project endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

1. Save the `.env` file (**Ctrl+S** or **File > Save**).

1. Open a terminal in VS Code (**Terminal > New Terminal**).

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

1. Run the application:

    ```bash
    python agent_with_functions.py
    ```

### Test the agent with code interpreter

When the agent starts, try these prompts to test different capabilities:

1. Test policy search with file search:
    ```
    What's the policy for password resets?
    ```

2. Request data analysis with code interpreter:
    ```
    Analyze the system performance data and identify any periods where CPU usage exceeded 80%
    ```

3. Request a visualization:
    ```
    Create a line chart showing memory usage trends over time
    ```

4. Ask for statistical analysis:
    ```
    What are the average, minimum, and maximum values for disk usage in the performance data?
    ```

5. Combined analysis:
    ```
    Find any correlation between high CPU usage and memory usage in the performance data
    ```

Observe how the agent uses both file search (for policy questions) and code interpreter (for data analysis) to fulfill your requests. The code interpreter will analyze the CSV data, perform calculations, and can even generate visualizations. Type `exit` when done testing.

---

## Portal vs Code: When to use each approach

Now that you've worked with both approaches, here's guidance on when to use each:

### Use the Portal when:
- Rapid prototyping and testing agent configurations
- Quick adjustments to instructions and system prompts
- Testing with grounding data and built-in tools
- Demonstrating concepts to stakeholders
- You need a quick agent without writing code

### Use VS Code / SDK when:
- Building production applications
- Integrating agents with existing code and systems
- Managing conversations and responses programmatically
- Version control and CI/CD pipelines
- Advanced orchestration and multi-agent scenarios
- Programmatic agent management at scale

### Hybrid Approach (Best Practice):
1. **Prototype** in the portal to validate concepts
2. **Develop** in VS Code for production implementation
3. **Monitor and iterate** using both tools

---

## Cleanup

To avoid unnecessary Azure charges, delete the resources you created:

1. In the Foundry portal, navigate to your project
1. Select **Settings** > **Delete project**
1. Alternatively, delete the entire resource group from the Azure portal

---

## Troubleshooting

### Common Issues

**Issue**: "Project endpoint invalid"
- **Solution**: Ensure you copied the full project endpoint from the portal. It should start with `https://` and include your project details.

**Issue**: "Agent not found"
- **Solution**: Make sure you set the correct project as active in the VS Code extension.

**Issue**: "Code interpreter not generating visualizations"
- **Solution**: Ensure the CSV file was properly uploaded to the agent and that code interpreter is enabled in the agent settings.

---

## Summary

In this exercise, you:

Created an AI agent in the Microsoft Foundry portal with grounding data  
Enabled built-in tools like file search and code interpreter  
Connected to your project using the VS Code extension  
Interacted with the agent programmatically using Python  
Leveraged code interpreter for data analysis and visualization  
Learned when to use portal vs code-based approaches  

You now have the foundational skills to build AI agents using both visual and code-based workflows!

## Next Steps

Ready to take your agent development skills to the next level? Continue with:

- **Lab 2: Advanced Tool Calling** - Learn to use advanced tool calling for dynamic data processing, implement advanced async function patterns, and master file operations with batch processing.

### Additional Resources

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Microsoft Foundry VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-ai)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
