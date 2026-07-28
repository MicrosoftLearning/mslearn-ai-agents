---
lab:
    title: 'Task 3 – Generate recommended responses'
    description: 'Add a second AI agent to the Tailwind Traders triage workflow that drafts a category-appropriate support reply for non-billing tickets.'
    level: 300
    concepts: 'agent workflows, multi-agent handoff, response generation'
    islab: true
    status: 'draft'
---

# Task 3 — Generate recommended responses

*Part of the **Design agent workflows in Microsoft Foundry** lab. New here? Start with [Getting started](D0-getting-started.md).*

> **What you need:** the **Tailwind-Traders-Support-Triage** workflow from
> [Task 1](D1-classify-and-route-a-ticket.md) (optionally with the confidence gate from
> [Task 2](D2-handle-low-confidence-tickets.md)), open in the Foundry visual designer. Haven't
> built it yet? Do [Task 1](D1-classify-and-route-a-ticket.md) first. This task is completed
> entirely in the portal.

> **Continuing from a previous task?** If you just finished Task 1 or Task 2 in the same
> workflow, it's already open and saved — go straight to **Add a resolution agent** below.

---

So far, non-billing tickets just get a placeholder "handling automatically" message. In this
task you'll replace that with a **second AI agent** — a **Resolution-Agent** — that reads the
ticket and drafts a real, category-appropriate support reply. This is a simple **agent
hand-off**: the Triage-Agent decides *what kind* of ticket it is; the Resolution-Agent decides
*how to respond*.

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
<summary>Why use a second agent?</summary>
<div class="concept-body" markdown="1">

You *could* ask one agent to both classify and reply, but splitting the work keeps each agent
focused and easy to tune. The Triage-Agent is constrained to emit clean JSON for routing; the
Resolution-Agent is free to write natural, on-brand prose. Passing the triage output into the
resolution step is a **hand-off** — the same pattern that scales up to full multi-agent systems.

</div>
</details>

## Add a resolution agent

You'll replace the **Handle non-billing tickets automatically** message from Task 1 with an
agent node on the same **Else** branch (the non-billing path).

1. In the visualizer, find the **Deliver a message** node on the **Else** branch of the category-routing **If/Else** node (the one that sends `Handling automatically: "{Local.CurrentTicket}"`). Delete it.

    > If you'd rather keep it, you can instead add the agent node **below** that message — but replacing it keeps the branch clean.

1. On that same **Else** branch, select the **+** (plus) icon to add a new node.

1. In the workflow actions menu, under **Invoke**, select **Agent** to add an agent node.

1. In the **Agent** node editor, select **Create new agent**.

1. Enter an agent name such as *Resolution-Agent* and select **Create**.

1. In the agent editor, set the **Instructions** field to the following prompt:

    ```output
    You are a customer support resolution assistant for Tailwind Traders, an outdoor-gear retailer that also runs guided trips.

    Your task is to draft a clear, professional, and friendly support response based on the issue category and customer message.

    Guidelines:
    If the issue category is Gear:
    Suggest 1-2 common troubleshooting steps at a high level.

    Avoid asking for serial numbers, order numbers, or sensitive data.

    Do not imply fault by the customer.
    If the issue category is General:
    Provide a concise, helpful explanation or guidance.
    Keep the response under 5 sentences.

    Tone:
    Professional, calm, and supportive
    Clear and concise
    No emojis

    Output:
    Return only the drafted response text.
    Do not include internal reasoning or analysis.
    ```

1. Select **Node settings** to configure the input and output of the agent.

1. Set the **Input message** field to the `Local.TriageOutputText` variable.

1. Under **Save agent output message as**, create a new variable named `ResolutionOutputText`.

1. Select **Done** to save the node.

## Preview the workflow

1. Select the **Save** button to save all changes to your workflow.

1. Select the **Preview** button, then enter `Start processing support tickets.` to trigger the workflow.

1. Watch the workflow run. Billing tickets are still escalated, but non-billing tickets (the gear and general questions) now receive a drafted response from the Resolution-Agent. For example:

    ```output
    Current Ticket:
    The GPS on my TrailMate hiking watch keeps losing signal even after I did a full factory reset.


    Copilot said:
    Thanks for reaching out about your TrailMate watch losing GPS signal. Try taking the watch outdoors with a clear view of the sky and giving it a minute to reacquire satellites, and make sure it's running the latest firmware from the Tailwind Traders companion app. If it still can't hold a signal after that, reply here and we'll arrange a closer look.
    ```

> ✅ **Checkpoint**: Your workflow now hands non-billing tickets to a second agent that drafts a
> category-appropriate reply — a Triage-Agent to *classify* and a Resolution-Agent to *respond*.

---

**Next (optional):** [Task 4 — Call your workflow from a client app](D4-call-your-workflow-from-a-client-app.md)
