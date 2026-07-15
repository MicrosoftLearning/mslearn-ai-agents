---
lab:
    title: 'Build and extend AI agents'
    description: 'Build the Trailhead Adventure Works assistant: ground it in store policy, then extend it with tools using remote MCP servers, custom functions, and a client app. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'agent creation and grounding, tools, Model Context Protocol (MCP)'
    duration: 35
    islab: true
    status: 'draft'
---

<!--
PILOT NOTE (remove before publishing):
This is a pilot of the new lab template (Core + Optional tasks) applied to
"Lab A" = a consolidation of the current exercises 01, 02, and 03.
Starter code lives in a single folder — Labfiles/A-build-and-extend-ai-agents/Python/ —
shared by every task (one virtual environment, one .env). The completed reference code is
in Labfiles/A-build-and-extend-ai-agents/Solution/Python/.

This landing page is the lab overview. Setup lives in A0-getting-started.md and each task is
its own page (A1–A5) so it can be completed on its own. Optional per-task fast-forward and
provisioning scripts live in Labfiles/A-build-and-extend-ai-agents/setup/ and infra/.
-->

# Build and extend AI agents

An agent becomes genuinely useful when it can *do* things — look up live information,
call your business logic, and act on a user's behalf. In this lab you'll build a
grounded agent and then give it capabilities using **tools**.

**Your scenario:** you work at **Trailhead Adventure Works**, an outdoor-gear retailer that
also runs guided trips. Across this lab you'll build the staff assistant that powers the
business, adding one capability per task: first grounding it in the store's own policies,
then connecting it to live documentation, letting it analyze sales data, take trip
bookings, and check warehouse stock.

You'll start with the **Core** tasks that get you to a working, tool-using agent as
quickly as possible. From there, a set of **Optional** tasks lets you go deeper into the
areas that interest you most.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Create and ground an agent** in the Microsoft Foundry portal so it answers from your
  own data rather than guessing.
- **Extend an agent with a tool** by connecting it to a remote **Model Context Protocol
  (MCP)** server, and handle tool-approval requests in code.

The **Optional** tasks let you additionally:

- Call your agent from a **client application**.
- Give an agent **custom function tools** that run your own Python logic.
- Build and connect your **own MCP server**.
- Compare two ways to build the same agent: the **Foundry SDK + Responses API** (which you
  write) and the **Microsoft Agent Framework** (a provided, ready-to-run variant).

## How this lab is organized

This lab is **modular**. Every task shares one starter folder, one virtual environment, and
one `.env`, so you can work through it end to end **or complete any single task on its own**.

1. **Start with [Getting started](A0-getting-started.md)** — create your Microsoft Foundry
   project (in the portal or with one `azd up` command), get the starter code, and set up
   your `.env`. You only do this once.
2. **Do any task below.** Each task page opens with a *"Starting here on its own?"* callout
   that tells you exactly what it needs and how to fast-forward past earlier tasks (for
   example, a script that creates the grounded agent for you), so you can jump straight in.

## Lab at a glance

Complete the **Core** tasks first (about **35 minutes**) — they end with a working,
tool-using agent. Then expand any **Optional** tasks that interest you. The full lab,
including all optional tasks, takes about **1 hour 55 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Create and ground an agent in the portal](A1-create-and-ground-an-agent.md) | ★☆☆ | ~15 min |
| **Core** | [Task 2 – Connect the agent to a remote MCP server in code](A2-connect-a-remote-mcp-server.md) | ★★☆ | ~20 min |
| *Optional* | [Task 3 – Call your agent from a client app](A3-call-your-agent-from-a-client-app.md) | ★★☆ | ~20 min |
| *Optional* | [Task 4 – Add custom function tools](A4-add-custom-function-tools.md) | ★★☆ | ~25 min |
| *Optional* | [Task 5 – Capstone: your own MCP server + combine every tool](A5-capstone-build-your-own-mcp-server.md) | ★★★ | ~35 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~35 min):** do Tasks 1–2.
- **Core + recommended (~1h 20m):** also do **Task 3** and **Task 4**.
- **Everything (~1h 55m):** add **Task 5** (the capstone builds on Task 4, so do Task 4 first).

> **One assistant, growing capabilities**: Tasks 3–5 all run behind the same provided web
> chat window (`trailhead_ui.py`) — the **Trailhead Adventure Works Assistant**. You focus only
> on the agent code; each task gives the same assistant a new capability (analyzing sales
> data, planning trips, and checking warehouse stock). You don't edit `trailhead_ui.py`; you
> just write a `respond()` function and hand it to `run_chat_app()`.

## Two ways to build the same agent

There's more than one way to write an agent against Microsoft Foundry, and this lab shows you
**two**:

- **The Foundry SDK with the Responses API** — the approach you'll *write* throughout this lab.
  You create the agent with `azure-ai-projects`, describe each tool with an explicit JSON
  schema, and drive the **tool-calling loop yourself**: read the model's response, run the
  tool it asked for, and send the result back. This is deliberately hands-on so you can *see*
  the mechanics every agent runtime performs under the hood.
- **The Microsoft Agent Framework (MAF)** — a higher-level framework that hides that plumbing.
  You decorate a plain Python function with `@tool` (the schema is generated for you) and call
  `await agent.run(...)`, which runs the entire tool-calling loop automatically.

Neither is "more correct" — they're different levels of abstraction. Seeing the raw mechanics
first is what makes the framework's shortcuts meaningful later. To make the contrast concrete,
**Tasks 4 and 5 each ship a ready-to-run MAF edition** of the same assistant
(`functions_agent_maf.py` and `client_maf.py`) that you can read and run alongside your own
version. The Microsoft Agent Framework is covered in depth in **Lab 07 (Agent Framework)** and
**Lab 08 (multi-agent orchestration)**.

## Summary

Across this lab you:

- Created and **grounded** an agent in the Foundry portal so it answers from your data.
- **Extended an agent with a tool** by connecting it to a remote MCP server and handling
  tool-approval requests in code.
- (Optionally) consumed an agent from a **client app**, added **custom function tools**,
  and built your **own MCP server** — then combined the function tools and your MCP tools
  into a single **capstone assistant** that routes each call to the right place.

Together these show the two big levers for making agents useful: giving them the right
**knowledge** (grounding) and the right **capabilities** (tools).

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> The code you ran in Task 2 already deletes the agent version it creates. Portal
> agents are removed when you delete the resource group. If you provisioned with `azd`, run
> `azd down` instead to remove everything it created.
