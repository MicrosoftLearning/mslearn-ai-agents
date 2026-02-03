---
lab:
    title: 'Build AI Agents with Portal and VS Code'
    description: 'Create an AI agent using both Microsoft Foundry portal and VS Code extension with built-in tools and custom functions.'
---

# Build AI Agents with Portal and VS Code

In this exercise, you'll build a complete AI agent solution using both the Microsoft Foundry portal and the Microsoft Foundry VS Code extension. You'll start by creating a basic agent in the portal with grounding data and built-in tools, then extend it programmatically using VS Code with custom functions.

This exercise takes approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Learning Objectives

By the end of this exercise, you'll be able to:

1. Create and configure an AI agent in the Microsoft Foundry portal
2. Add grounding data and enable built-in tools (file search, code interpreter)
3. Use the Microsoft Foundry VS Code extension to work with agents programmatically
4. Implement custom functions to extend agent capabilities
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
- Execute custom functions to check system status and create support tickets

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
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/uplevel/10-build-agent-portal-and-vscode/IT_Policy.txt
    ```

    Save the file to your local machine.

    > **Note**: This document contains sample IT policies for password resets, software installation requests, and hardware troubleshooting.

1. Return to the agent playground. In the **Tools** section, enable **File search**.

1. Under **File search**, select **Upload files** and upload the `IT_Policy.txt` file you just downloaded.

1. Wait for the file to be indexed. You'll see a confirmation when it's ready.

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

1. Now ask a question that isn't covered in the policy:

    ```
    What's the weather like today?
    ```

1. The agent should respond appropriately, indicating this is outside its scope.

Great! You've created a basic agent with grounding data and file search capability. In the next section, you'll extend this agent using the VS Code extension.

---

## Extend your agent with VS Code

Now you'll use the Microsoft Foundry VS Code extension to work with your agent programmatically and add custom functions.

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

### Retrieve project connection details

To work with your agent programmatically, you'll need your project's connection information.

1. In the Foundry extension, right-click on your project and select **View in Portal**.

1. In the portal that opens, navigate to **Overview** in the left sidebar.

1. Copy the following values and save them somewhere (you'll need them shortly):
    - **Project name**
    - **Foundry project endpoint** (the connection string)

1. Also copy the **Subscription ID** and **Resource group** name from the Overview page.

1. Note the **Project endpoint** URL - you'll use this to connect your Python applications to the project.

### Create a Python application

Now let's create a Python application that interacts with your agent and adds custom functions.

1. In VS Code, create a new folder on your local machine for this project (e.g., `C:\labs\it-support-agent`).

1. Open this folder in VS Code (**File > Open Folder**).

1. Create a new file named `agent_with_functions.py` in the folder.

1. Add the following code to the file:

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    import json
    from datetime import datetime
    
    # System status simulator
    def check_system_status(system_name: str) -> str:
        """
        Check the status of a system or service.
        
        Args:
            system_name: Name of the system to check (e.g., 'email', 'vpn', 'printer')
        
        Returns:
            JSON string with status information
        """
        # Simulate system status
        systems = {
            "email": {"status": "operational", "uptime": "99.9%"},
            "vpn": {"status": "degraded", "uptime": "95.2%", "issue": "Slow connection speeds"},
            "printer": {"status": "operational", "uptime": "98.5%"},
            "network": {"status": "operational", "uptime": "99.7%"}
        }
        
        system_lower = system_name.lower()
        if system_lower in systems:
            result = {
                "system": system_name,
                "timestamp": datetime.now().isoformat(),
                **systems[system_lower]
            }
        else:
            result = {
                "system": system_name,
                "timestamp": datetime.now().isoformat(),
                "status": "unknown",
                "message": "System not found in monitoring"
            }
        
        return json.dumps(result)
    
    
    def create_support_ticket(issue_type: str, description: str, priority: str = "medium") -> str:
        """
        Create a support ticket for an IT issue.
        
        Args:
            issue_type: Type of issue (e.g., 'hardware', 'software', 'network', 'access')
            description: Detailed description of the issue
            priority: Priority level - 'low', 'medium', or 'high' (default: 'medium')
        
        Returns:
            JSON string with ticket information
        """
        # Simulate ticket creation
        import random
        ticket_id = f"TICKET-{random.randint(10000, 99999)}"
        
        result = {
            "ticket_id": ticket_id,
            "issue_type": issue_type,
            "description": description,
            "priority": priority,
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "message": f"Support ticket {ticket_id} has been created successfully"
        }
        
        return json.dumps(result)
    
    
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
        
        # Function map for execution
        function_map = {
            "check_system_status": check_system_status,
            "create_support_ticket": create_support_ticket
        }
        
        # Chat loop
        print("\n" + "="*60)
        print("IT Support Agent Ready!")
        print("Ask questions or request help. Type 'exit' to quit.")
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
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                input=""
            )
            
            # Handle function calls if needed
            while True:
                # Check if response needs function execution
                needs_function_call = False
                if hasattr(response, 'output') and response.output:
                    for item in response.output:
                        if hasattr(item, 'type') and item.type == 'function_call':
                            needs_function_call = True
                            function_name = item.name
                            function_args = json.loads(item.arguments) if hasattr(item, 'arguments') else {}
                            
                            print(f"\n[Calling function: {function_name}]")
                            
                            # Execute the function
                            if function_name in function_map:
                                function_result = function_map[function_name](**function_args)
                                
                                # Add function result to conversation
                                openai_client.conversations.items.create(
                                    conversation_id=conversation.id,
                                    items=[{
                                        "type": "function_call_output",
                                        "call_id": item.call_id if hasattr(item, 'call_id') else item.id,
                                        "output": function_result
                                    }]
                                )
                
                # If function was called, get new response
                if needs_function_call:
                    response = openai_client.responses.create(
                        conversation=conversation.id,
                        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
                        input=""
                    )
                else:
                    break
            
            # Display response
            if hasattr(response, 'output_text') and response.output_text:
                print(f"\nAgent: {response.output_text}\n")
            elif hasattr(response, 'output') and response.output:
                # Fallback: extract text from output items
                for item in response.output:
                    if hasattr(item, 'text'):
                        print(f"\nAgent: {item.text}\n")
    
    
    if __name__ == "__main__":
        main()
    ```

### Configure environment and run the application

1. In the lab repository, navigate to `Labfiles/uplevel/01-build-agent-portal-and-vscode/Python/` and locate the provided `.env` and `requirements.txt` files.

1. Copy these files to your project folder (`C:\labs\it-support-agent`).

1. Open the `.env` file and replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    AGENT_NAME=it-support-agent
    ```
    
    **To get your project endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

1. Open a terminal in VS Code (**Terminal > New Terminal**).

1. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

1. Run the application:

    ```bash
    python agent_with_functions.py
    ```

### Test the custom functions

When the agent starts, try these prompts:

1. Check system status:
    ```
    Is the email system working?
    ```

2. Create a support ticket:
    ```
    I need to create a ticket for a printer issue. The printer on floor 3 is not printing color documents.
    ```

3. Combined request:
    ```
    Check the VPN status and if there's an issue, create a high priority ticket
    ```

Observe how the agent uses the custom functions to fulfill your requests. Type `exit` when done testing.

---

## Portal vs Code: When to use each approach

Now that you've worked with both approaches, here's guidance on when to use each:

### Use the Portal when:
- ✅ Rapid prototyping and testing agent configurations
- ✅ Quick adjustments to instructions and system prompts
- ✅ Testing with grounding data and built-in tools
- ✅ Demonstrating concepts to stakeholders
- ✅ You need a quick agent without writing code

### Use VS Code / SDK when:
- ✅ Building production applications
- ✅ Implementing custom functions and complex logic
- ✅ Integrating with existing code and systems
- ✅ Version control and CI/CD pipelines
- ✅ Advanced orchestration and multi-agent scenarios
- ✅ Programmatic agent management at scale

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

**Issue**: "Function not executing"
- **Solution**: Verify the function schema matches the implementation and check that required parameters are provided.

---

## Summary

In this exercise, you:

✅ Created an AI agent in the Microsoft Foundry portal with grounding data  
✅ Enabled built-in tools like file search  
✅ Connected to your project using the VS Code extension  
✅ Implemented custom functions programmatically  
✅ Learned when to use portal vs code-based approaches  

You now have the foundational skills to build AI agents using both visual and code-based workflows!

## Next Steps

Ready to take your agent development skills to the next level? Continue with:

- **Lab 2: Advanced Tool Calling and Code Interpreter** - Learn to use code interpreter for dynamic data analysis, implement advanced async function patterns, and master file operations with batch processing.

### Additional Resources

- [Azure AI Agent Service Documentation](https://learn.microsoft.com/azure/ai-services/agents/)
- [Microsoft Foundry VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.vscode-ai)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
