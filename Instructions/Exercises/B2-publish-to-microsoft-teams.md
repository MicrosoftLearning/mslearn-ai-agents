---
title: 'Task 2 – Publish your agent to Microsoft Teams'
lab:
    title: 'Task 2 – Publish your agent to Microsoft Teams'
    description: 'Publish the Tailwind Traders knowledge agent to Microsoft Teams so staff can chat with it where they already work.'
    level: 300
    concepts: 'agent publishing, Microsoft Teams, Azure Bot Service'
    islab: true
    status: 'draft'
---

# Task 2 — Publish your agent to Microsoft Teams

*Part of the **Integrate agents with enterprise knowledge and Microsoft 365** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **Set up (start here):** This task publishes the grounded `tailwind-knowledge-agent` from
> [Task 1](B1-create-a-foundry-iq-knowledge-agent.md). If you don't have that agent yet, complete
> Task 1 first (or, for the quickest path, create and ground it in code with
> `python setup/bootstrap_agent.py` from the `Labfiles/B-integrate-agents-with-enterprise-knowledge-and-m365`
> folder). You also need a **Microsoft 365 account with Teams access**. This task is completed
> entirely in the portal and Teams — no local code or `.env` file is required.

> **Continuing from a previous task?** If you just finished Task 1 and your
> `tailwind-knowledge-agent` is grounded and saved in the Foundry portal, you're ready — go
> straight to **Publish to Microsoft Teams** below.

---

Publishing to **Microsoft Teams** lets Tailwind Traders staff chat with the knowledge assistant
directly in Teams, without leaving the tools they already use. This task focuses on the
**deployment and publishing workflow** — you won't write any code.

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
<summary>What happens when I publish to Teams?</summary>
<div class="concept-body" markdown="1">

When you publish an agent to Teams, the Foundry portal automatically **creates an Azure Bot
Service**, generates a **Teams app manifest**, packages **app icons and configuration**, and
provides a **downloadable app package**. You don't build any of that by hand — you fill in a
short form and the portal wires it up.

</div>
</details>

## Publish to Microsoft Teams

When you publish to Teams, the Foundry portal automatically:

- Creates an Azure Bot Service
- Generates a Teams app manifest
- Packages app icons and configuration
- Provides a downloadable app package

### Prepare app information

Before publishing, gather this information:

| Field | Value |
|-------|-------|
| **App Name** | Tailwind Traders Knowledge Assistant |
| **Short Description** | AI assistant for Tailwind Traders staff |
| **Full Description** | Enterprise AI assistant that answers staff questions about products, store operations, returns, rentals, and suppliers |
| **Developer Name** | Your name or company name |
| **Website URL** | <https://tailwindtraders.com> (placeholder is fine for lab) |
| **Privacy Policy URL** | <https://tailwindtraders.com/privacy> |
| **Terms of Use URL** | <https://tailwindtraders.com/terms> |

### Create app icons

You'll need two icons for the Teams app:

1. **Color icon** (192x192 pixels)
   - Full color version of your app logo
   - PNG format

2. **Outline icon** (32x32 pixels)
   - White outline on transparent background
   - PNG format
   - Used in the Teams sidebar

> **Quick option for this lab**: Create a simple colored square with text or initials using PowerPoint, Paint, or an online tool like Canva.

### Publish from the portal

1. In the Foundry portal, open your agent (**Build** → **Agents** → **tailwind-knowledge-agent**)

2. Select the **Publish** button at the top of the page

3. Select **Publish to Teams and Microsoft 365 Copilot**.

4. Select **Continue**

### Configure Teams app details

Fill in the configuration form:

**Basic Information:**

- **App Name**: Tailwind Traders Knowledge Assistant
- **Short Description**: AI assistant for Tailwind Traders staff
- **Full Description**: Enterprise AI assistant that answers staff questions about products, store operations, returns, rentals, and suppliers

**Developer Information:**

- **Developer Name**: Your name
- **Website**: <https://tailwindtraders.com>
- **Privacy Policy**: <https://tailwindtraders.com/privacy>
- **Terms of Use**: <https://tailwindtraders.com/terms>

**App Icons:**

- Upload your **color icon** (192x192 px)
- Upload your **outline icon** (32x32 px)

**App Scope:**

- Select **Personal** for individual chat access
- Optionally select **Team** for channel access

Select **Prepare Agent**

### Deploy to Teams

After the agent package is prepared (this takes 1-2 minutes), you can deploy it to Teams:

1. When the package is ready, select **Continue the in-product publishing flow**

2. Choose your publish scope:
   - **Individual scope**: Agent appears under "Your agents" in the Teams agent store. No admin approval required. Best for personal testing.
   - **Organization (tenant) scope**: Agent appears under "Built by your org" for all users. Requires admin approval.

3. For this lab, select **Individual scope**

4. Select **Submit**

5. Wait for publishing to complete (you'll see a success message)

> **Alternative if direct publishing fails**: If the publish dialog returns a **400** error, and your Microsoft 365 account has permission to publish custom apps, open the **Download & customize** tab instead and follow the instructions.

6. Your agent is now available in Teams! Find it under **Apps** → **Your agents**

### Test your agent in Teams

1. The agent chat should open after installation (or find it under **Apps** → **Your agents**)

2. Send a greeting:

    ```
    Hello! What can you help me with?
    ```

3. Test a knowledge query:

    ```
    What is the return window for a tent?
    ```

4. Try another question:

    ```
    What are our store's core hours?
    ```

5. The agent should respond with information from the Tailwind Traders knowledge base!

> ✅ **Checkpoint**: Your grounded knowledge agent is now available in Microsoft Teams, answering
> staff questions from the enterprise knowledge base.

### Troubleshooting Teams deployment

**Can't find the agent in Teams (after direct publish):**

- Check the **Apps** → **Your agents** section in Teams
- Wait 1-2 minutes for the agent to appear after publishing
- Verify publishing completed successfully in the Foundry portal

**Can't upload the app (manual upload):**

- Ensure the manifest.zip file isn't corrupted (re-download if needed)
- Check that your Teams admin hasn't disabled custom app uploads
- Verify the icons are the correct sizes (192x192 and 32x32)

**Agent doesn't respond:**

- Wait 30 seconds after installation for the bot to initialize
- Check that the Azure Bot Service was created (shown during publishing)
- Test the agent in the Foundry playground first

**Responses are generic (no knowledge):**

- Verify Foundry IQ (or file search) is enabled on the agent
- Confirm documents were uploaded and indexed
- Test knowledge queries in the Foundry playground

---

**Next (optional):** [Task 3 — Publish to Microsoft 365 Copilot](B3-publish-to-microsoft-365-copilot.md) · [Task 4 — Work IQ](B4-work-iq-workplace-intelligence.md)
