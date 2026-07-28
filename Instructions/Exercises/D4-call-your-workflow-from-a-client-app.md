---
lab:
    title: 'Task 4 – Call your workflow from a client app'
    description: 'Invoke your saved Tailwind Traders triage workflow from your own code with the Azure AI Projects SDK — as a console script or a browser chat window.'
    level: 300
    concepts: 'Azure AI Projects SDK, Responses API, workflow invocation'
    islab: true
    status: 'draft'
---

# Task 4 — Call your workflow from a client app

*Part of the **Design agent workflows in Microsoft Foundry** lab. New here? Start with [Getting started](D0-getting-started.md).*

> **Set up (start here):** This task needs the **Tailwind-Traders-Support-Triage** workflow
> from [Task 1](D1-classify-and-route-a-ticket.md) (Tasks 2 and 3 optional but recommended),
> **plus** VS Code, Python, and the starter code. If you haven't built the workflow yet, do
> [Task 1](D1-classify-and-route-a-ticket.md) first.

> **Continuing from a previous task?** Your workflow is already built and saved in the
> portal. You still need to get the starter code and set `PROJECT_ENDPOINT` (below), since the
> earlier tasks were portal-only.

---

**Goal**: Now that your workflow runs in the portal, invoke it from **your own code** using the
Azure AI Projects SDK — so you can integrate triage into an application or automate it.

**Concept reinforced**: driving a saved workflow programmatically — you create a conversation,
reference the workflow **by name**, stream its events, and print the result.

## Get the starter code

1. In VS Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-agents.git
    ```

1. Open the cloned repo, then **File > Open Folder** and select `mslearn-ai-agents/Labfiles/D-design-agent-workflows-in-foundry/Python`.

1. Right-click **requirements.txt** and choose **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

## Configure the application

1. In the browser, return to the workflow visualizer in the Foundry portal.

1. Select **Code** in the upper right corner of the visualizer. Then select **.env variables** to view the environment variables required to connect to your Foundry project from code.

1. Copy the value of the **AZURE_EXISTING_AIPROJECT_ENDPOINT** variable — this is the endpoint URL for your Foundry project.

1. In VS Code, copy **.env.example** to **.env**, then open **.env** and set `PROJECT_ENDPOINT` to the endpoint you just copied. Save the file (**Ctrl+S**).

1. Confirm your environment is ready. From the same **Python** folder terminal, run:

    ```
    python ..\setup\check_env.py --task 4
    ```

    You should see `[OK ] PROJECT_ENDPOINT`. If it reports the value missing, revisit the step above.

## Invoke the workflow from code

Open **workflow.py**. It already contains a `print_workflow_output` helper that formats the
results; you'll fill in the connection and invocation using the comments in the file.

> **Try it first**: Before revealing the solution, predict — how does the client tell the
> Responses API to run a *workflow* rather than a single agent? (Hint: look at how Task 1's
> agent node referenced an agent by name.)

<details markdown="1">
<summary>Show a solution</summary>

Work through the comments in **workflow.py**:

1. Find the comment **Add references** and add the imports:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    ```

1. Find the comment **Connect to the AI Project client** and add:

    ```python
    # Connect to the AI Project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    ```

    > **Tip**: When adding the subsequent code, keep the right level of indentation.

1. Find the comment **Specify the workflow** and add (use the exact name you saved in Task 1):

    ```python
        # Specify the workflow
        workflow = {
            "name": "Tailwind-Traders-Support-Triage"
        }
    ```

1. Find the comment **Create a conversation and run the workflow** and add:

    ```python
        # Create a conversation and run the workflow
        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")

        stream = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": workflow["name"], "type": "agent_reference"}},
            input="Start",
            stream=True,
        )
    ```

1. Find the comment **Process events from the workflow run** and add:

    ```python
        # Process events from the workflow run
        for event in stream:
            if (event.type == "response.completed"):
                print("\nResponse completed:")
                response = openai_client.responses.retrieve(event.response.id)
                print_workflow_output(response.output_text)
    ```

1. Find the comment **Clean up resources** and add:

    ```python
        # Clean up resources
        openai_client.conversations.delete(conversation_id=conversation.id)
        print("\nConversation deleted")
    ```

1. Save the file (**Ctrl+S**).

</details>

## Test the client application

1. In the integrated terminal, sign in and run the app:

    ```
    az login
    ```

    ```
   python workflow.py
    ```

1. Wait a moment for the workflow to process the tickets. You should see console output for each ticket — its category, confidence, and the drafted response or escalation. For example:

    ```output
    ================================================================================
    Ticket 1: Gear (93% confidence)
    --------------------------------------------------------------------------------
    Issue: The GPS on my TrailMate hiking watch keeps losing signal even after I did a full factory reset.

    Response:
    Thanks for reaching out about your TrailMate watch losing GPS signal. Try taking the watch outdoors with a clear view of the sky...
    ================================================================================
    ```

1. When you're finished, enter `deactivate` in the terminal to exit the virtual environment.

## Optional: run it as a web chat app

The lab also ships a **web chat** version, `workflow_ui.py` (in the `Solution/Python` folder),
that runs the same invocation behind the shared Gradio chat shell (`tailwind_ui.py`) — so your
workflow feels like a real app. You provide a `respond()` function; the shell turns it into a
browser chat window. You don't edit `tailwind_ui.py`.

To try it, copy `workflow_ui.py` next to your `workflow.py`, then run:

```
python workflow_ui.py
```

Your browser opens a chat window at `http://localhost:7860`. Type any message (for example,
`Start processing support tickets`) and the classified, routed tickets render inline. Close the
tab and press **Ctrl+C** in the terminal to stop the app.

> The complete, ready-to-run versions of both files are in
> `Labfiles/D-design-agent-workflows-in-foundry/Solution/Python`.

**Stretch**: after each response, print the number of tickets escalated versus auto-resolved.

> ✅ **Checkpoint**: You've driven your saved Foundry workflow from your own code — creating a
> conversation, referencing the workflow by name, and printing (or chatting) its results.

---

**Back to the overview:** [Design agent workflows in Microsoft Foundry](D-design-agent-workflows-in-foundry.md)
