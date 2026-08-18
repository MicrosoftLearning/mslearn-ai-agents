---
title: 'Task 3 – Publish your agent to Microsoft 365 Copilot'
lab:
    title: 'Task 3 – Publish your agent to Microsoft 365 Copilot'
    description: 'Publish the Caldova knowledge agent to Microsoft 365 Copilot so staff can reach it inside Copilot.'
    type: 'task'
    parent: 'B'
    order: 3
    section: 'optional'
    difficulty: 2
    duration: 15
    access: 'gated'
    requires: 'A Microsoft 365 Copilot licence, and permission to publish agents to Copilot in your tenant'
    verify: 'In the Foundry portal, open your agent and select **Publish**. If Microsoft 365 Copilot is greyed out or returns a consent error, you don''t have the rights this task needs.'
    level: 200
    concepts: 'agent publishing, Microsoft 365 Copilot, Copilot agents'
    status: 'draft'
---

# Task 3 — Publish your agent to Microsoft 365 Copilot

*Part of the **Integrate agents with enterprise knowledge and Microsoft 365** lab. New here? Start with [Getting started](B0-getting-started.md).*

<!-- BEGIN GENERATED: gated-notice - do not edit by hand; run: python tools/generate_lab_blocks.py -->
> ### Check your access before you start
>
> **This task needs:** A Microsoft 365 Copilot licence, and permission to publish agents to Copilot in your tenant.
>
> In the Foundry portal, open your agent and select **Publish**. If Microsoft 365 Copilot is greyed out or returns a consent error, you don't have the rights this task needs.
>
> **Don't have it?** Skip this task. Nothing else in this lab depends on it, and you can still read through the steps to see how it works.
<!-- END GENERATED: gated-notice -->

> **Set up (start here):** This task publishes the grounded `caldova-knowledge-agent` from
> [Task 1](B1-create-a-foundry-iq-knowledge-agent.md). If you don't have that agent yet, complete
> Task 1 first (or create and ground it in code with `python ../setup/bootstrap_agent.py` from
> the `Python` folder you opened in VS Code). This task is completed
> entirely in the portal and Copilot — no local code or `.env` file is required.

> **Continuing from a previous task?** If you already published to Teams in
> [Task 2](B2-publish-to-microsoft-teams.md), the same publishing flow makes the agent available
> in Copilot too — go straight to **Publish to Microsoft 365 Copilot** below.

---

Publishing to **Microsoft 365 Copilot** makes your agent a **Copilot agent** that staff can reach
directly inside Copilot. This task focuses on the **publishing workflow** — you won't write any code.

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
<summary>What is a Microsoft 365 Copilot agent?</summary>
<div class="concept-body" markdown="1">

When you publish to Copilot, your agent becomes a **Copilot agent** (also called an extension or
declarative agent). Staff can invoke it with **@mentions** in Copilot, access its knowledge
alongside Copilot's own capabilities, and switch between Copilot and your agent seamlessly.

</div>
</details>

## Publish to Microsoft 365 Copilot

When you publish to Copilot, users can:

- Invoke your agent using @mentions in Copilot
- Access your agent's knowledge alongside Copilot's capabilities
- Switch between Copilot and your agent seamlessly

### Publish from the portal

1. Return to the Foundry portal (**<https://ai.azure.com>**)

2. Navigate to your agent (**Build** → **Agents** → **caldova-knowledge-agent**)

3. Select the **Publish** button

4. Select **Publish to Teams and Microsoft 365 Copilot**

5. Select **Continue**

> **Note**: This is the same publishing flow used for Teams. The agent becomes available in both Teams and Copilot through a single publishing process.

### Configure publishing details

If you haven't already published this agent, fill in the configuration (same as the Teams section):

- **Name**: Caldova Knowledge Assistant
- **Description**: AI assistant for Caldova staff
- **Icons**: Upload your 192x192 and 32x32 icons
- **Publisher information**: Your name and placeholder URLs

### Choose publish scope

Select your distribution scope:

| Scope | Visibility | Admin Approval | Best For |
|-------|-----------|----------------|----------|
| **Shared** | Under "Your agents" in agent store | Not required | Personal testing, small teams |
| **Organization** | Under "Built by your org" for all users | Required | Organization-wide distribution |

For this lab, select **Shared scope** for immediate access without admin approval.

### Complete publishing

1. Select **Prepare Agent** and wait for packaging (1-2 minutes)

2. Select **Continue the in-product publishing flow**

3. Confirm your scope selection and select **Publish**

4. Wait for publishing to complete

### Access in Microsoft 365 Copilot

Once published with shared scope, your agent is immediately available:

1. Open **Microsoft 365 Copilot** (copilot.microsoft.com or in Microsoft 365 apps)

2. Look for the agent store or **Extensions** panel

3. Find your agent under **Your agents** (for shared scope)

4. Start a conversation:

    ```
    @Caldova Knowledge Assistant How much headroom does Calderwood have?
    ```

5. Or select your agent and ask directly:

    ```
    When should we reorder sterile vials, and who is our component supplier?
    ```

6. Copilot routes the query to your agent and returns information from the Caldova knowledge base

> **Note**: For **organization scope**, an admin must first approve the app in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) under **Requests**. Once approved, the agent appears under **Built by your org** for all users.

> ✅ **Checkpoint**: Your grounded knowledge agent is now reachable inside Microsoft 365 Copilot,
> answering staff questions from the enterprise knowledge base.

## Cleanup

To avoid unnecessary charges, clean up resources when done.

### Delete the agent

1. In the Foundry portal, go to **Build** → **Agents**

2. Find **caldova-knowledge-agent**

3. Select the **...** menu → **Delete**

4. Confirm deletion

This also removes:

- The Azure Bot Service
- Associated configurations
- Published deployments

### Uninstall from Teams

1. Open Microsoft Teams

2. Go to **Apps** → **Manage your apps**

3. Find **Caldova Knowledge Assistant**

4. Select **...** → **Uninstall**

5. Confirm uninstallation

### Remove Copilot agent

If you published to Copilot:

1. The agent becomes inactive when the underlying agent is deleted
2. Users will see an error if they try to use it
3. An admin may need to remove it from the organization catalog

---

**Next (optional):** [Task 4 — Work IQ: bring Microsoft 365 signals into an agent](B4-work-iq-workplace-intelligence.md)
