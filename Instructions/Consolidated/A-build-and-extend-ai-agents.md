---
title: 'Build and extend AI agents'
lab:
    title: 'Build and extend AI agents'
    description: 'Build the Caldova supply chain assistant: ground it in company policy, then extend it with tools using remote MCP servers, custom functions, and a client app. A modular lab you can complete end to end or one task at a time.'
    type: 'lab'
    id: 'A'
    order: 1
    difficulty: 3
    duration: 35
    access: 'open'
    level: 300
    concepts: 'agent creation and grounding, tools, Model Context Protocol (MCP)'
    islab: true
    status: 'draft'
---

# Build and extend AI agents

**Level** ▰▰▰▱▱ **L300**

(**L100** beginner → **L500** expert)

Build a practical AI agent with Microsoft Foundry and Python, then extend it with company
knowledge and tools.

## The case

You work at **Caldova**, a pharmaceutical manufacturer. Caldova plans to launch a product
sooner than expected, but its three factories can produce about 7% less than the launch
requires.

The planning team must decide whether to move work between Caldova's factories or hire an
approved manufacturing partner, also called a contract manufacturer. You build a supply
chain assistant to help them decide. It uses company policy, analyzes factory output, finds
available production time, estimates partner costs, and checks whether enough materials are
in stock.

## What you'll do

Complete the two core tasks for a working agent, then choose optional tasks based on what
you want to practice.

<!-- BEGIN GENERATED: task-table - do not edit by hand; run: python tools/generate_lab_blocks.py -->
| Section | Task | Level | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Create and ground an agent](A1-create-and-ground-an-agent.md) | ▰▰▱▱▱ L200 | ~15 min |
| **Core** | [Task 2 – Connect a remote MCP server](A2-connect-a-remote-mcp-server.md) | ▰▰▰▱▱ L300 | ~20 min |
| *Optional* | [Task 3 – Call your agent from a client app](A3-call-your-agent-from-a-client-app.md) | ▰▰▰▱▱ L300 | ~20 min |
| *Optional* | [Task 4 – Add custom function tools](A4-add-custom-function-tools.md) | ▰▰▰▱▱ L300 | ~25 min |
| *Optional* | [Task 5 – Capstone: build your own MCP server](A5-capstone-build-your-own-mcp-server.md) | ▰▰▰▰▱ L400 | ~35 min |
| *Optional* | [Task 6 – Promote your assistant to a hosted agent](A6-promote-your-assistant-to-a-hosted-agent.md) | ▰▰▰▱▱ L300 | ~30 min |

**Core tasks:** about **35 minutes**. **Full lab**, including every optional task: about **2 hours 25 minutes**.
<!-- END GENERATED: task-table -->

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

Start with [Getting started](A0-getting-started.md) to create your Microsoft Foundry project
and prepare the shared starter code. Each task includes the setup needed to start
independently. If you complete the lab in order, you reuse the same environment and skip
repeated setup.

![Anton](../Media/anton-avatar.png)

**Meet Anton, your AI guide.**

You'll spot **Ask Anton** tips throughout this lab. For more interactive help, use the
*[Ask Anton](https://aka.ms/choose-anton)* app.

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
<summary>What is an agent?</summary>
<div class="concept-body" markdown="1">

An AI agent is a software service that uses generative AI to understand a request, decide
what to do, and take action on a user's behalf. What makes an agent genuinely useful isn't
the model alone. It also needs relevant **knowledge** and **tools**.

[Learn more →](https://review.learn.microsoft.com/en-us//training/modules/build-extend-ai-agents/1-introduction?branch=pr-en-us-55509)

</div>
</details>

## Is this lab for you?

Choose this lab if you want hands-on practice building an agent with Microsoft Foundry and
Python. You write the agent code, connect remote and custom tools, and work directly with the
tool-calling loop. The web chat interface is provided.

Tasks 4 and 5 also include a ready-to-run Microsoft Agent Framework version for comparison.
Task 6 lets you deploy your code as a hosted agent.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> The code you ran in Task 2 already deletes the agent version it creates. Portal
> agents are removed when you delete the resource group. If you provisioned with `azd`, run
> `azd down` instead to remove everything it created.
