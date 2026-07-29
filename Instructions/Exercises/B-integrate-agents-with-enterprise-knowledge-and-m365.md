---
lab:
    title: 'Integrate agents with enterprise knowledge and Microsoft 365'
    description: 'Build the Tailwind Traders staff knowledge assistant: ground it on enterprise documents with Foundry IQ, then deliver it through Microsoft Teams, Microsoft 365 Copilot, and Work IQ. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'enterprise knowledge grounding, Foundry IQ, Microsoft 365, Model Context Protocol (MCP)'
    duration: 35
    islab: true
    status: 'draft'
---

<!--
PILOT NOTE (remove before publishing):
This is a pilot of the new lab template (Core + Optional tasks) applied to
"Lab B" = a consolidation of the current exercises 04, 05a, and 05b.
Starter code lives in a single folder — Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Python/ —
shared by every code task (one virtual environment, one .env). The completed reference code is
in Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/Solution/Python/.

This landing page is the lab overview. Setup lives in B0-getting-started.md and each task is
its own page (B1–B4) so it can be completed on its own. Optional per-task fast-forward and
provisioning scripts live in Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365/setup/ and infra/.
-->

# Integrate agents with enterprise knowledge and Microsoft 365

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

An agent becomes genuinely useful to a business when it answers from the company's *own*
knowledge and shows up where employees already work. In this lab you'll build a **grounded
enterprise-knowledge agent** and then **deliver it through Microsoft 365**.

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

**Your scenario:** you work at **Tailwind Traders**, an outdoor-gear retailer that also runs
guided trips. Store staff constantly field questions about products, store operations, returns,
rentals, and suppliers — and the answers all live in internal documents. In this lab you'll build
the **Tailwind Traders staff knowledge assistant**: first grounding it on those enterprise docs
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

Complete the **Core** task first (about **35 minutes**) — it ends with a working, grounded
enterprise-knowledge agent you can call from code. Then expand any **Optional** tasks that
interest you. The full lab, including all optional tasks, takes about **1 hour 50 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Create a Foundry IQ knowledge agent and connect from code](B1-create-a-foundry-iq-knowledge-agent.md) | ▰▰▰▱▱ L300 | ~35 min |
| *Optional* | [Task 2 – Publish your agent to Microsoft Teams](B2-publish-to-microsoft-teams.md) | ▰▰▱▱▱ L200 | ~20 min |
| *Optional* | [Task 3 – Publish your agent to Microsoft 365 Copilot](B3-publish-to-microsoft-365-copilot.md) | ▰▰▱▱▱ L200 | ~15 min |
| *Optional* | [Task 4 – Work IQ: bring Microsoft 365 signals into an agent](B4-work-iq-workplace-intelligence.md) | ▰▰▰▰▱ L400 | ~40 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~35 min):** do Task 1.
- **Core + delivery (~1h 10m):** also do **Task 2** and **Task 3** to publish the agent to M365.
- **Everything (~1h 50m):** add **Task 4** (Work IQ) for live workplace intelligence.

> **One assistant, delivered everywhere**: Tasks 1–3 all revolve around the **same** grounded
> agent (`tailwind-knowledge-agent`). You build and ground it once (Task 1), then Tasks 2 and 3
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
