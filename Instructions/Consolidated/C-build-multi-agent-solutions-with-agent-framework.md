---
title: 'Build multi-agent solutions with the Agent Framework'
lab:
    title: 'Build multi-agent solutions with the Agent Framework'
    description: 'Build Caldova operations agents with the Microsoft Agent Framework: start with a single tool-using agent, then orchestrate several agents in sequence, then connect remote agents across processes with the A2A protocol. A modular lab you can complete end to end or one task at a time.'
    type: 'lab'
    id: 'C'
    order: 3
    difficulty: 3
    duration: 30
    access: 'open'
    level: 300
    concepts: 'Microsoft Agent Framework, tools, multi-agent orchestration, A2A protocol'
    islab: true
    status: 'draft'
---

# Build multi-agent solutions with the Agent Framework

**Level** ▰▰▰▱▱ **L300**  (**L100** beginner → **L500** expert)

A single agent is useful. A *team* of agents — each one focused, and able to hand work to the
others — is how you build real operations. In this lab you'll build up a Caldova
multi-agent system with the **Microsoft Agent Framework (MAF)**, starting from one tool-using
agent and growing to a set of remote agents that call each other over a protocol.

![Anton](../Media/anton-avatar.png)<br /><strong>Meet Anton, your AI guide.</strong><br />You'll spot **Ask Anton** tips throughout this lab. Want more interactive, hands-on help? Chat with Anton in the *[Ask Anton](https://aka.ms/choose-anton)* app.

<details>
<summary><strong><i>About the Ask Anton app</i></strong></summary>

<strong><i><a href="https://aka.ms/choose-anton" target="_blank">Ask Anton</a></i></strong> is a generative AI agent that can answer questions about AI concepts and Microsoft Foundry technologies. It's available in two versions at <code>https://aka.ms/choose-anton</code>:
<ul>
<li><strong>Azure-based</strong>: Best experience <i>(requires an Azure subscription and deployment of a model in a Foundry project)</i>.</li>
<li><strong>Browser-based</strong>: Use a small language model in your browser <i>(reduced functionality - may be slow or work only in "basic" mode in older/lower-spec devices)</i>.</li>
</ul>
<blockquote><i>Ask Anton is <u>not</u> a supported Microsoft product or a component of Microsoft Learn or AI Skills Navigator.</i></blockquote>
</details>

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
<summary>What is the Microsoft Agent Framework?</summary>
<div class="concept-body" markdown="1">

The **Microsoft Agent Framework (MAF)** is a higher-level SDK for building agents on Microsoft
Foundry. You decorate a plain Python function with `@tool` (the schema is generated for you) and
call `await agent.run(...)`, which runs the entire tool-calling loop automatically. It also gives
you building blocks for **multi-agent** solutions — orchestrations that run several agents
together — so you don't have to wire the plumbing by hand.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/agents/overview)

</div>
</details>

**Your scenario:** you work at **Caldova**, a pharmaceutical manufacturer preparing an
accelerated product launch. Across this lab you'll build the automation behind Caldova operations —
starting with a single agent that files site-visit expense claims, then a pipeline of agents that
triage site feedback, and finally a set of specialist transfer-planning agents that live in
separate processes and collaborate over a protocol.

You'll start with the **Core** task that gets you to a working, tool-using agent as quickly as
possible. From there, a set of **Optional** tasks lets you go deeper into multi-agent patterns.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** task of this exercise, you'll be able to:

- **Build an agent with a custom tool** using the Microsoft Agent Framework — decorate a Python
  function with `@tool`, hand it to an `Agent`, and let `agent.run()` drive the tool-calling loop.

The **Optional** tasks let you additionally:

- **Orchestrate multiple agents** in a sequence, passing work from one specialist agent to the
  next and collecting every agent's output.
- **Connect remote agents** that run in separate processes and call each other using the
  **Agent-to-Agent (A2A)** protocol, coordinated by a routing agent.
- **Classify and route** support tickets by turning one agent's **structured output** into
  conditional routing in your own code.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](C0-getting-started.md)** — create your Microsoft Foundry
   project (in the portal or with one `azd up` command), get the starter code, and set up
   your `.env`. Every task begins from here; if you're doing the whole lab in one sitting, you
   only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** task first — it ends with a working, tool-using agent. Then expand any
**Optional** tasks that interest you.

<!-- BEGIN GENERATED: task-table - do not edit by hand; run: python tools/generate_lab_blocks.py -->
| Section | Task | Level | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Build an agent with a tool](C1-create-an-agent-with-a-tool.md) | ▰▰▰▱▱ L300 | ~30 min |
| *Optional* | [Task 2 – Orchestrate multiple agents in sequence](C2-orchestrate-multiple-agents.md) | ▰▰▰▱▱ L300 | ~30 min |
| *Optional* | [Task 3 – Connect remote agents with A2A](C3-connect-remote-agents-with-a2a.md) | ▰▰▰▰▱ L400 | ~30 min |
| *Optional* | [Task 4 – Classify and route a support ticket](C4-classify-and-route-a-ticket.md) | ▰▰▰▱▱ L300 | ~30 min |

**Core tasks:** about **30 minutes**. **Full lab**, including every optional task: about **2 hours**.
<!-- END GENERATED: task-table -->

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~99 min):** do Task 1.
- **Core + one pattern (~1h):** add **Task 2** (sequential orchestration) or **Task 4** (classify + route).
- **Everything (~2h):** add **Task 2**, **Task 3** (remote agents with A2A), and **Task 4**.

## One framework, growing from one agent to many

Every task in this lab is built on the **Microsoft Agent Framework**, so the shape of the code
stays familiar as the solutions get more ambitious:

- In **Task 1**, you build a **single** agent. You describe a tool with `@tool`, attach it to an
  `Agent` backed by a `FoundryChatClient`, and call `agent.run(...)` — the framework runs the
  tool-calling loop for you.
- In **Task 2**, you keep the same client but create **several** agents and hand them to a
  `SequentialBuilder` orchestration, which runs them in order and collects each one's output.
- In **Task 3**, you split the agents across **separate processes** and let a routing agent
  discover and call them using the **A2A protocol** — the same collaboration idea, now over the
  network.
- In **Task 4**, you come back to a **single** agent — but its **structured output** (a JSON
  classification) drives **conditional routing** in your code, escalating or auto-handling each
  support ticket.

Seeing the single-agent mechanics first is what makes the multi-agent patterns meaningful later.

## Summary

Across this lab you:

- Built an **agent with a custom tool** using the Microsoft Agent Framework.
- (Optionally) **orchestrated several agents** in a sequence to triage work step by step.
- (Optionally) connected **remote agents** across processes with the **A2A protocol**, routed by
  a coordinating agent.
- (Optionally) turned an agent's **structured classification** into **conditional routing** in code.

Together these show how the Agent Framework scales from a single focused agent to a coordinated
team of them.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> If you provisioned with `azd`, run `azd down` instead to remove everything it created.
