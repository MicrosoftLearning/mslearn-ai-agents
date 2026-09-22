---
title: 'Task 1 – Trace your agent'
lab:
    title: 'Task 1 – Trace your agent'
    description: 'Instrument an agent with OpenTelemetry, export traces to Azure Monitor, add your own spans and attributes, and read the result in the Foundry portal.'
    type: 'task'
    parent: 'D'
    order: 1
    section: 'core'
    difficulty: 3
    duration: 25
    access: 'open'
    level: 300
    concepts: 'tracing, OpenTelemetry, Azure Monitor, Application Insights'
    islab: true
    status: 'draft'
---

# Task 1 — Trace your agent

*Part of the **Observe, evaluate, and secure your agents** lab. New here? Start with [Getting started](D0-getting-started.md).*

> **Set up (start here):** This task needs a Foundry project, an **Application Insights
> resource connected to it**, a grounded agent to trace, and the starter code. If you
> haven't already, complete [Getting started](D0-getting-started.md) to create your
> project, clone the code, set `PROJECT_ENDPOINT` and `AGENT_NAME` in `Python/.env` (point
> it at your [Lab B](B-integrate-agents-with-enterprise-knowledge-and-m365.md) agent, or
> create one with `python ../setup/bootstrap_agent.py`), and connect Application Insights.
> Then, from the `Python` folder you opened in VS Code, verify you're ready:

```
python ../setup/check_env.py --task 1
```

> **Continuing from a previous task?** If you just finished another task in the same
> `Python` folder, your project, virtual environment, and `.env` are already set — go
> straight to **Instrument the agent** below.

---

It's Monday morning at Caldova's Ashford site. Planners are firing questions at
the assistant between meetings, and the planning lead says some answers "take ages". You
have no idea which ones, or why: the terminal shows you an answer, and nothing about how it
got there.

**Tracing** fixes that. Your code emits **spans** — timed, named, nested records of work —
and ships them to **Application Insights**, where the Foundry portal renders them as a
waterfall you can step through.

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
<summary>What is OpenTelemetry?</summary>
<div class="concept-body" markdown="1">

**OpenTelemetry** is a vendor-neutral standard for emitting traces, metrics and logs. A
**span** is one unit of work with a start, an end, and attributes; spans nest to form a
**trace** of a whole operation. Because it's a standard, the Azure SDKs, the OpenAI client
and your own code all produce spans that line up in the same waterfall — and you could point
them at a different backend tomorrow without rewriting your instrumentation.

</div>
</details>

> **Server-side traces come free.** Now that Application Insights is connected to your
> project, Foundry already records traces for agents it hosts — no code required. What you
> add here is **client-side** instrumentation: spans around *your* code. Both land in the same
> Application Insights resource, but Foundry's **Agents > Traces** page only renders its own
> server-side view (`Invoke Agent` / `Execute tool` / `Chat`) — to see your own spans and
> attributes alongside it, you'll look directly at Application Insights.

Open the `Python` folder and activate the virtual environment from [Getting started](D0-getting-started.md) (`.\labenv\Scripts\Activate.ps1`), then continue below.

### Instrument the agent

Open **traced_agent.py** and add code at each commented placeholder.

> **Tip**: As you add code, keep the indentation aligned with the comments.

1. **Add references**:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace
    ```

1. **Turn on GenAI tracing** — the spans that capture model calls are off by default, and
    message content is off separately because prompts can contain personal data. Turn both on
    for this lab:

    ```python
    # Turn on GenAI tracing
    os.environ.setdefault("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING", "true")
    os.environ.setdefault("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "true")
    ```

    > These must be set **before** the client is created, which is why they go at the top of
    > the file. In production, think hard before turning message content on.

1. **Connect to the project**:

    ```python
    # Connect to the project
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):
    ```

1. **Read the Application Insights connection string and start exporting traces** — the
    project hands you the connection string of the resource you connected in setup, and
    `configure_azure_monitor` wires up the exporter:

    ```python
    # Read the Application Insights connection string and start exporting traces
    try:
        connection_string = project_client.telemetry.get_application_insights_connection_string()
    except Exception as error:
        raise SystemExit(
            "Could not read an Application Insights connection string from this project.\n"
            "In the Foundry portal, open your project, select Agents > Traces, and select\n"
            f"Connect to create or connect an Application Insights resource.\n\nDetails: {error}"
        )
    configure_azure_monitor(connection_string=connection_string)
    ```

1. **Get a tracer for this script** — a tracer is what you create your own spans from:

    ```python
    # Get a tracer for this script
    tracer = trace.get_tracer(__name__)
    ```

1. **Look up the agent** — its `id` (not just its name) is needed to correlate traces with
    this specific agent in the Foundry portal:

    ```python
    # Look up the agent so its id can be included in agent_reference
    agent = project_client.agents.get(agent_name=agent_name)
    ```

1. **Ask each question inside its own span** — this is the part that pays off. An outer span
    represents the review; each question gets a child span, tagged with attributes you choose
    so you can tell them apart in the portal. This reuses `caldova-knowledge-agent` rather
    than standing up a separate agent just for this task:

    ```python
    # Ask each question inside its own span
    with tracer.start_as_current_span("morning-planning-review") as shift_span:
        shift_span.set_attribute("caldova.site", "ashford")
        conversation = openai_client.conversations.create()

        for number, question in enumerate(QUESTIONS, start=1):
            with tracer.start_as_current_span("planner-question") as question_span:
                question_span.set_attribute("caldova.question_number", number)
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=question,
                    extra_body={"agent_reference": {"name": agent.name, "id": agent.id, "type": "agent_reference"}},
                )
                question_span.set_attribute("caldova.answer_length", len(response.output_text))
                print(f"\nQ{number}: {question}")
                print(f"A{number}: {response.output_text}")
    ```

1. Save the file (**Ctrl+S**).

### Run and test

1. In the terminal, sign in and run the app:

    ```
    az login
    ```

    ```
    python traced_agent.py
    ```

1. You should see the three answers print:

    ```
    Q1: How long does review take for a capacity request with a complete brief?
    A1: ...
    ```

    > If you get an error about the connection string, Application Insights isn't connected to
    > your project yet — go back to [Getting started](D0-getting-started.md) and connect it.

### Read the traces

**Two views, two purposes.** Foundry's **Agents > Traces** page shows the automatic
**server-side** trace of the agent's own turn (`Invoke Agent` > `Execute tool` / `Chat`) — it
confirms tracing is working, but it doesn't surface the **client-side** spans your script just
added. To see `morning-planning-review`, `planner-question`, and their custom attributes, look
at the Application Insights resource itself:

1. In the [Foundry portal](https://ai.azure.com), open your project, select **Agents**, then
    **caldova-knowledge-agent**, then **Traces**, to confirm the run arrived (telemetry takes a
    minute or two — wait and refresh if it isn't there yet). Selecting a trace here shows
    Foundry's own `Invoke Agent` / `Execute tool` / `Chat` view, not your custom spans.

1. Open the Application Insights resource in the [Azure portal](https://portal.azure.com):
    open the resource group you created for this project, and select the Application Insights
    resource in it.

1. In Application Insights, expand **Investigate** in the left navigation, select **Search**,
    and search for `morning-planning-review`.

1. Select a matching result to open its **end-to-end transaction details**. This is the raw
    span tree: your `morning-planning-review` span at the top, three `planner-question`
    children, and inside each one the model call the SDK emitted.

1. Select a `planner-question` span and look at its properties. Your `caldova.question_number`
    and `caldova.answer_length` are there alongside the standard GenAI attributes.

1. Compare the durations of the three questions. That's the planning lead's complaint,
    answered with data — and the span breakdown tells you *which part* of the slow one was
    slow.

> **Try it**: add a fourth, much harder question to `QUESTIONS` and run again. Does the extra
> time show up in the model call, or somewhere else?

> ✅ **Checkpoint**: You can see inside a running agent — both the SDK's own spans and custom
> spans of your own, with attributes you chose, all in one timeline.

When you're finished, enter `deactivate` to exit the virtual environment.

---

**Next:** [Task 2 — Evaluate answer quality](D2-evaluate-answer-quality.md)
