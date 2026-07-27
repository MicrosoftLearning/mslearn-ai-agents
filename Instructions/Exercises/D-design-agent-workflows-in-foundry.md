---
lab:
    title: 'Design agent workflows in Microsoft Foundry'
    description: 'Design a Tailwind Traders customer-support workflow in the Microsoft Foundry visual workflow designer: classify each ticket with an AI agent and route it to the right place. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'agent workflows, ticket classification, conditional routing'
    duration: 20
    islab: true
    status: 'draft'
---

<!--
PILOT NOTE (remove before publishing):
This is a pilot of the new lab template (Core + Optional tasks) applied to
"Lab D" = a standalone consolidation of the current exercise 06 (Build a workflow in
Microsoft Foundry), reskinned to the Tailwind Traders scenario.

This lab is built mostly in the Foundry portal's visual workflow designer, so there is
very little code. The copy/paste assets for the portal steps live in
Labfiles/D-design-agent-workflows-in-foundry/assets/, and the optional client app
(starter + complete solution) lives in Labfiles/D-design-agent-workflows-in-foundry/.

This landing page is the lab overview. Setup lives in D0-getting-started.md and each task is
its own page (D1-D4) so it can be completed on its own.
-->

# Design agent workflows in Microsoft Foundry

Some jobs are bigger than a single agent turn. When work needs to happen **in a sequence** —
loop over a batch, ask an agent to make a decision, then branch on that decision — you need a
**workflow**. In this lab you'll design one in the Microsoft Foundry **visual workflow
designer**, no orchestration code required.

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
<summary>What is a workflow?</summary>
<div class="concept-body" markdown="1">

A **workflow** is a UI-defined sequence of actions that can include AI agents. Instead of
writing an orchestration loop in code, you drag and connect **nodes** — set a variable, loop
over a list, invoke an agent, branch with if/else — in the Foundry visual designer. Agents make
the *decisions*; the workflow controls the *flow* around them.

</div>
</details>

**Your scenario:** you work at **Tailwind Traders**, an outdoor-gear retailer that also runs
guided trips. The support inbox is overflowing, so you'll design a workflow that **triages
customer support tickets**: it reads each ticket, uses an AI agent to classify it as
**Billing**, **Gear**, or **General** with a confidence score, and then routes it — escalating
billing issues to a human while handling the rest automatically.

You'll start with the **Core** task that gets a working classify-and-route workflow running as
quickly as possible. From there, a set of **Optional** tasks lets you make the workflow smarter
and connect it to your own code.

> **Note**: The workflow designer in Microsoft Foundry is currently in preview. You may
> experience some unexpected behavior, warnings, or errors. If you encounter an issue that
> blocks your progress, you may need to start over with a new project and workflow.

## What you'll learn

By completing the **Core** task of this exercise, you'll be able to:

- **Design a sequential workflow** in the Foundry visual designer using variables, a for-each
  loop, and conditional (if/else) routing.
- **Invoke an AI agent from a workflow** to classify each support ticket into a category with a
  confidence score, using a structured JSON response.

The **Optional** tasks let you additionally:

- Add **conditional logic for low-confidence classifications** so uncertain tickets ask for
  more detail instead of being routed blindly.
- **Generate a recommended response** for non-billing tickets with a second AI agent.
- **Call your workflow from a client application** using the Azure AI Projects SDK — as a
  console script or a browser chat window.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own** — so you can pick a
single task and do just that one. The optional tasks each extend the same workflow, so if you'd
rather work straight through, you can.

1. **Start with [Getting started](D0-getting-started.md)** — create your Microsoft Foundry
   project. Every task begins from here; you only need to do this once.
2. **Do the Core task**, then any Optional tasks. Each task lists the setup it needs so you can
   start it independently. If you're moving straight from the previous task, a short
   *"Continuing from a previous task?"* note lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** task first (about **20 minutes**) — it ends with a working
classify-and-route workflow. Then expand any **Optional** tasks that interest you. The full
lab, including all optional tasks, takes about **55 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Classify and route a support ticket](D1-classify-and-route-a-ticket.md) | ★★☆ | ~20 min |
| *Optional* | [Task 2 – Handle low-confidence tickets](D2-handle-low-confidence-tickets.md) | ★☆☆ | ~10 min |
| *Optional* | [Task 3 – Generate recommended responses](D3-generate-recommended-responses.md) | ★★☆ | ~10 min |
| *Optional* | [Task 4 – Call your workflow from a client app](D4-call-your-workflow-from-a-client-app.md) | ★★☆ | ~15 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~20 min):** do Task 1.
- **Core + smarter workflow (~40 min):** also do **Task 2** and **Task 3** (they build on the
  workflow from Task 1, so do Task 1 first).
- **Everything (~55 min):** add **Task 4** to drive the finished workflow from your own code.

> **One workflow, growing capabilities**: Tasks 2–3 keep editing the **same**
> `Tailwind-Traders-Support-Triage` workflow you build in Task 1 — each adds one node or branch.
> Task 4 then invokes that finished workflow from code, so build it first.

## Summary

Across this lab you:

- Designed a **sequential workflow** that loops over a batch of Tailwind Traders support tickets.
- Used an **AI agent to classify** each ticket and **conditional logic to route** it — escalating
  billing issues while handling gear and general questions automatically.
- (Optionally) added **low-confidence handling**, **agent-drafted responses**, and a **client
  app** that runs the whole workflow from your own code.

Together these show how workflows let agents make decisions while you stay in control of the
flow — loops, branches, and hand-offs — without writing orchestration code.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> Agents created inside the workflow are removed when you delete the resource group.
