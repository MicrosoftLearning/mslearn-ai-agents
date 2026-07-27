---
lab:
    title: 'Task 2 – Handle low-confidence tickets'
    description: 'Add conditional logic to the Tailwind Traders triage workflow so tickets the agent is unsure about ask for more detail instead of being routed blindly.'
    level: 300
    concepts: 'confidence scores, conditional logic, if/else branching'
    islab: true
    status: 'draft'
---

# Task 2 — Handle low-confidence tickets

*Part of the **Design agent workflows in Microsoft Foundry** lab. New here? Start with [Getting started](D0-getting-started.md).*

> **What you need:** the **Tailwind-Traders-Support-Triage** workflow from
> [Task 1](D1-classify-and-route-a-ticket.md), open in the Foundry visual designer. Haven't
> built it yet? Do [Task 1](D1-classify-and-route-a-ticket.md) first — it takes about 20
> minutes and this task adds one branch to it. This task is completed entirely in the portal.
>
> > **Continuing from a previous task?** If you just finished Task 1 in the same workflow, it's
> > already open and saved — go straight to **Add a confidence gate** below.

---

The Triage-Agent returns a **confidence score** alongside each category. A low score means the
agent is guessing — routing that ticket automatically risks sending it the wrong way. In this
task you'll add a **confidence gate**: only well-classified tickets continue to routing;
uncertain ones are sent back for more detail.

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
<summary>Why gate on confidence?</summary>
<div class="concept-body" markdown="1">

A classifier is only as useful as it is *certain*. Acting on a low-confidence guess can escalate
the wrong ticket or auto-reply with irrelevant help. A confidence threshold turns "I think this
is Billing" into a safe default: **when unsure, ask a human or the customer for more** instead of
committing. `0.6` is a reasonable starting threshold — raise it to be more cautious.

</div>
</details>

## Add a confidence gate

You'll insert a new **If/Else** node between the Triage-Agent node and the category routing you
built in Task 1. Its condition checks the confidence score; the routing you already built moves
under the high-confidence (**If**) branch.

1. In the visualizer, select the **+** (plus) icon **directly below the Invoke agent node** (and above the category-routing **If/Else** you added in Task 1) to add a new node.

1. In the workflow actions menu, under **Flow**, select **If/Else** to add a conditional logic node.

1. In the **If/Else** node editor, select the **Add a path** button to create the if-branch condition, then select the pencil icon to edit the condition.

1. Set the **Condition** field to the following expression to check whether the confidence score is above 0.6:

    ```output
   Local.TriageOutputJson.confidence > 0.6
    ```

1. Select **Done** to save the node.

## Move the category routing under the If branch

The high-confidence path should do the routing you already built. Place the category-routing
**If/Else** (and its **Escalate** / **Handle automatically** branches from Task 1) **under the
If branch** of your new confidence node.

- If the designer lets you drag the existing category **If/Else** node into the **If** branch, do that.
- If not, it's quick to rebuild: under the **If** branch, add an **If/Else** node with the condition `Local.TriageOutputJson.category = "Billing"`, then re-add the two **Deliver a message** nodes from [Task 1](D1-classify-and-route-a-ticket.md#route-the-ticket-based-on-category) (escalate on the **If** branch; handle automatically on the **Else** branch).

> The goal is this shape: **Agent → If confidence > 0.6 → (If) route by category / (Else) ask for more detail.**

## Recommend additional info for low-confidence tickets

1. In the visualizer, under the **Else** branch of your new confidence **If/Else** node, select the **+** (plus) icon to add a new node.

1. In the workflow actions menu, under **Basics**, select **Deliver a message** to add a send message activity.

1. In the **Deliver a message** node editor, set the **Message to send** field to the following response:

    ```output
   The support ticket classification has low confidence. Requesting more details about the issue: "{Local.CurrentTicket}"
    ```

1. Select **Done** to save the node.

## Preview the workflow

1. Select the **Save** button to save all changes to your workflow.

1. Select the **Preview** button, then enter `Start processing support tickets.` to trigger the workflow.

1. Watch how each ticket now passes through the confidence gate first. Tickets the agent is confident about are routed by category as before; any low-confidence ticket instead receives the "requesting more details" message.

> ✅ **Checkpoint**: Your workflow now protects against uncertain classifications — only
> confidently classified tickets are routed, and the rest are sent back for more detail.

---

**Next (optional):** [Task 3 — Generate recommended responses](D3-generate-recommended-responses.md)
