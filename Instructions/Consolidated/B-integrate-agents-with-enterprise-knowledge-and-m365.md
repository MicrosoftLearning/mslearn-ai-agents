---
title: 'Integrate agents with enterprise knowledge and Microsoft 365'
lab:
    title: 'Integrate agents with enterprise knowledge and Microsoft 365'
    description: 'Build the Caldova staff knowledge assistant: ground it on enterprise documents with Foundry IQ, then deliver it through Microsoft Teams, Microsoft 365 Copilot, and Work IQ. A modular lab you can complete end to end or one task at a time.'
    type: 'lab'
    id: 'B'
    order: 2
    difficulty: 3
    duration: 35
    access: 'open'
    level: 300
    concepts: 'enterprise knowledge grounding, Foundry IQ, Microsoft 365, Model Context Protocol (MCP)'
    islab: true
    status: 'draft'
---

# Integrate agents with enterprise knowledge and Microsoft 365

**Level** ▰▰▰▱▱ **L300**  (**L100** beginner → **L500** expert)

An agent becomes genuinely useful to a business when it answers from the company's *own*
knowledge and shows up where employees already work. In this lab you'll build a **grounded
enterprise-knowledge agent** and then **deliver it through Microsoft 365**.

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
<summary>What is enterprise knowledge grounding?</summary>
<div class="concept-body" markdown="1">

Grounding an agent on **enterprise knowledge** means connecting it to your organization's own
documents — policies, catalogs, procedures — so it answers from that trusted material instead of
guessing. **Foundry IQ** does this at scale: it indexes a knowledge base and performs *agentic
retrieval*, and it can require an **approval** step before each lookup so your app stays in control.

[Learn more →](https://learn.microsoft.com/azure/ai-foundry/)

</div>
</details>

**Your scenario:** you work at **Caldova**, a pharmaceutical manufacturer preparing an
accelerated product launch. Planning and materials teams constantly field questions about
site capacity, contract manufacturers, tech transfer, and suppliers — and the answers all
live in internal documents. In this lab you'll build
the **Caldova staff knowledge assistant**: first grounding it on those enterprise docs
with Foundry IQ, then publishing it to Microsoft Teams and Microsoft 365 Copilot so staff can use
it where they already work, and finally exploring **Work IQ** to bring live Microsoft 365 signals
into an agent.

You'll start with the **Core** task that gets you to a working, grounded enterprise-knowledge
agent. From there, a set of **Optional** tasks lets you deliver and extend it.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** task of this exercise, you'll be able to:

- **Create and ground an enterprise-knowledge agent** with **Foundry IQ** in the Microsoft
  Foundry portal, and require **approval** before it searches the knowledge base.
- **Connect to the agent from code** and handle the knowledge-tool approval flow yourself.

The **Optional** tasks let you additionally:

- **Publish the agent to Microsoft Teams** so staff can chat with it in Teams.
- **Publish the agent to Microsoft 365 Copilot** as a Copilot agent.
- **Bring Microsoft 365 workplace signals into an agent with Work IQ** over MCP.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every code task also shares one starter
folder, one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](B0-getting-started.md)** — create your Microsoft Foundry
   project (in the portal or with one `azd up` command), get the starter code, and set up
   your `.env`. Every task begins from here; if you're doing the whole lab in one sitting, you
   only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** task first — it ends with a working, grounded enterprise-knowledge agent
you can call from code. Then expand any **Optional** tasks that interest you.

<!-- BEGIN GENERATED: task-table - do not edit by hand; run: python tools/generate_lab_blocks.py -->
| Section | Task | Level | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Create a Foundry IQ knowledge agent and connect from code](B1-create-a-foundry-iq-knowledge-agent.md) | ▰▰▰▱▱ L300 | ~35 min |
| *Optional* | [Task 2 – Publish your agent to Microsoft Teams](B2-publish-to-microsoft-teams.md) 🔒 | ▰▰▱▱▱ L200 | ~20 min |
| *Optional* | [Task 3 – Publish your agent to Microsoft 365 Copilot](B3-publish-to-microsoft-365-copilot.md) 🔒 | ▰▰▱▱▱ L200 | ~15 min |
| *Optional* | [Task 4 – Work IQ: bring Microsoft 365 signals into an agent](B4-work-iq-workplace-intelligence.md) 🔒 | ▰▰▰▰▱ L400 | ~40 min |

**Core tasks:** about **35 minutes**. **Full lab**, including every optional task: about **1 hour 50 minutes**.

> 🔒 Tasks marked with a lock need access your account may not have. Each one opens
> with a quick check and tells you what to do if you don't have it — nothing else in
> this lab depends on them.
<!-- END GENERATED: task-table -->

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~35 min):** do Task 1.
- **Core + delivery (~1h 10m):** also do **Task 2** and **Task 3** to publish the agent to M365.
- **Everything (~1h 50m):** add **Task 4** (Work IQ) for live workplace intelligence.

> **One assistant, delivered everywhere**: Tasks 1–3 all revolve around the **same** grounded
> agent (`caldova-knowledge-agent`). You build and ground it once (Task 1), then Tasks 2 and 3
> simply *publish* that same agent to Teams and Copilot — no new code. Task 4 explores a
> different Microsoft 365 capability (Work IQ) with its own agent.

## Summary

Across this lab you:

- Created and **grounded** an enterprise-knowledge agent with **Foundry IQ** in the Foundry
  portal, requiring approval before each knowledge lookup.
- **Connected to the agent from code** and handled the approval flow yourself.
- (Optionally) **published** the agent to **Microsoft Teams** and **Microsoft 365 Copilot**, and
  explored **Work IQ** to bring live Microsoft 365 signals into an agent.

Together these show how to take an agent from a grounded knowledge base all the way to the
Microsoft 365 surfaces your organization uses every day.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry and Azure AI Search resources.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> The code you run in Task 4 already deletes the agent version it creates. Portal agents are
> removed when you delete the resource group. If you provisioned with `azd`, run `azd down`
> instead to remove everything it created.
