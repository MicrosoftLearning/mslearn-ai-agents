---
lab:
    title: 'Deploy Agents to Microsoft Teams and Copilot'
    description: 'Publish AI agents to Microsoft Teams and Microsoft 365 Copilot for enterprise access'
    level: 300
    duration: 40
---

# Deploy Agents to Microsoft Teams and Copilot

In this lab, you'll learn how to publish AI agents to **Microsoft Teams** and **Microsoft 365 Copilot** so employees can access them where they already work. You'll create a simple agent in the Foundry portal, add knowledge grounding, then deploy it to both platforms.

This lab focuses on **deployment and publishing workflows**, not agent development.

This lab takes approximately **40** minutes.

> **Note**: Publishing to Microsoft 365 Copilot requires a Copilot license. The Teams deployment works with standard Microsoft 365 accounts.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Create a basic agent quickly in the Microsoft Foundry portal
2. Add knowledge grounding using file search
3. Publish agents to Microsoft Teams as a custom app
4. Publish agents to Microsoft 365 Copilot as an extension
5. Understand the differences between Teams and Copilot deployment
6. Manage and update published agents

## Prerequisites

Before starting this lab, ensure you have:

- **Azure subscription** with permissions to create AI resources
- **Microsoft 365 account** with Teams access
- **Microsoft 365 Copilot license** (optional, for Copilot deployment)
- Basic familiarity with the Microsoft Foundry portal

## Scenario

You'll deploy an **Enterprise Knowledge Agent** that:

- Answers questions about company policies
- Uses uploaded documents for grounding
- Is accessible via Microsoft Teams chat
- Is available as a Copilot extension (optional)

---

## Create an Agent in the Portal

First, you'll quickly create an agent using the Microsoft Foundry portal. This takes about 5 minutes.

### Open the Foundry portal

1. Open your browser and navigate to the Foundry portal at `https://ai.azure.com`

2. Sign in with your Azure credentials

3. If prompted, select your subscription and create or select a project

### Create a new agent

1. In the Foundry portal, select **Build** from the left navigation

2. Select **Agents**

3. Click **+ New agent**

4. Configure the agent:
   - **Name**: `enterprise-knowledge-agent`
   - **Description**: Enterprise assistant for company policies and information

5. Set the **Instructions** to:

    ```
    You are an Enterprise Knowledge Assistant for Contoso Corporation.
    
    Your role:
    - Answer questions about company policies and procedures
    - Provide accurate information from uploaded documents
    - Be professional, helpful, and concise
    - If you don't know the answer, say so and suggest who to contact
    
    Always cite your sources when referencing specific policies.
    ```

6. Click **Create**

Your agent is now created! You'll see the agent playground where you can test it.

### Quick test

1. In the chat panel, send a test message:
    ```
    Hello! What can you help me with?
    ```

2. The agent should respond explaining it's an Enterprise Knowledge Assistant

The agent works, but it doesn't have any company knowledge yet. Let's add that next.

---

## Add Knowledge with File Search

Now you'll add company documents so the agent can answer questions with real information.

### Enable file search

1. In your agent's configuration, scroll to the **Tools** section

2. Enable **File search**

3. Click **Save**

### Upload company documents

1. Under **File search**, click **Upload files**

2. Download the sample policy documents. Open new browser tabs and save each file:

    **IT Security Policy:**
    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/05a-m365-teams-integration/Python/sample_documents/it_security_policy.txt
    ```

    **Remote Work Policy:**
    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/05a-m365-teams-integration/Python/sample_documents/remote_work_policy.txt
    ```

3. Return to the Foundry portal and upload both files

4. Wait for the files to be indexed (you'll see a confirmation for each)

### Test with knowledge queries

1. In the playground, ask a question about IT security:
    ```
    What are the password requirements for my laptop?
    ```

2. The agent should provide specific information from the IT security policy (minimum 12 characters, uppercase, lowercase, numbers, special characters, etc.)

3. Try a question about remote work:
    ```
    What are the core hours for remote employees?
    ```

4. The agent should respond with information from the remote work policy (9 AM - 3 PM)

5. Try another query:
    ```
    What encryption is required on company laptops?
    ```

6. Notice how the agent finds the right document and provides accurate answers about BitLocker requirements

**Your agent now has knowledge grounding!** It can answer questions based on your company documents.

---

## Publish to Microsoft Teams

Now you'll publish your agent to Microsoft Teams so employees can chat with it directly in Teams.

### What gets created

When you publish to Teams, the Foundry portal automatically:
- Creates an Azure Bot Service
- Generates a Teams app manifest
- Packages app icons and configuration
- Provides a downloadable app package

### Prepare app information

Before publishing, gather this information:

| Field | Value |
|-------|-------|
| **App Name** | Enterprise Knowledge Agent |
| **Short Description** | AI assistant for company policies |
| **Full Description** | Enterprise AI assistant that answers questions about company policies, IT procedures, and employee resources |
| **Developer Name** | Your name or company name |
| **Website URL** | https://contoso.com (placeholder is fine for lab) |
| **Privacy Policy URL** | https://contoso.com/privacy |
| **Terms of Use URL** | https://contoso.com/terms |

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

1. In the Foundry portal, open your agent (**Build** → **Agents** → **enterprise-knowledge-agent**)

2. Click the **Publish** button at the top of the page

3. Select **Microsoft Teams** as the deployment target

4. Click **Continue**

### Configure Teams app details

Fill in the configuration form:

**Basic Information:**
- **App Name**: Enterprise Knowledge Agent
- **Short Description**: AI assistant for company policies
- **Full Description**: Enterprise AI assistant that answers questions about company policies, IT procedures, and employee resources

**Developer Information:**
- **Developer Name**: Your name
- **Website**: https://contoso.com
- **Privacy Policy**: https://contoso.com/privacy
- **Terms of Use**: https://contoso.com/terms

**App Icons:**
- Upload your **color icon** (192x192 px)
- Upload your **outline icon** (32x32 px)

**App Scope:**
- Select **Personal** for individual chat access
- Optionally select **Team** for channel access

Click **Prepare Agent**

### Deploy to Teams

After the agent package is prepared (this takes 1-2 minutes), you have two options:

#### Option A: Direct publish (recommended)

This option publishes directly to Teams without manually uploading a package:

1. When the package is ready, select **Continue the in-product publishing flow**

2. Choose your publish scope:
   - **Shared scope**: Agent appears under "Your agents" in the Teams agent store. No admin approval required. Best for personal testing.
   - **Organization scope**: Agent appears under "Built by your org" for all users. Requires admin approval.

3. For this lab, select **Shared scope**

4. Click **Publish**

5. Wait for publishing to complete (you'll see a success message)

6. Your agent is now available in Teams! Find it under **Apps** → **Your agents**

#### Option B: Download and manually upload

This option gives you a package to upload manually, useful for testing or when direct publishing isn't available:

1. When the package is ready, click **Download the package**

2. Save the `manifest.zip` file to your computer

3. Open **Microsoft Teams** (desktop app or https://teams.microsoft.com)

4. Click **Apps** in the left sidebar

5. Click **Manage your apps** at the bottom left

6. Click **Upload an app** → **Upload a custom app**

7. Browse and select your downloaded `manifest.zip`

8. Review the app details and click **Add**

The app will install and open automatically.

### Test your agent in Teams

1. The agent chat should open after installation (or find it under **Apps** → **Your agents**)

2. Send a greeting:
    ```
    Hello! What can you help me with?
    ```

3. Test a knowledge query:
    ```
    What are the laptop password requirements?
    ```

4. Try another question:
    ```
    What MFA methods are supported?
    ```

5. The agent should respond with information from the IT security policy document!

**🎉 Congratulations!** Your agent is now available in Microsoft Teams!

### Sharing with others

**For personal use:**
- The app is already installed for you

**For team-wide access:**
1. Go to a Team channel
2. Click **+** to add a tab or app
3. Search for your app name
4. Add it to the channel

**For organization-wide access:**
1. Contact your Teams administrator
2. They can publish the app to the organization's app catalog
3. All employees can then find and install it

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
- Verify file search is enabled on the agent
- Confirm documents were uploaded and indexed
- Test knowledge queries in the Foundry playground

---

## Publish to Microsoft 365 Copilot

Now you'll publish your agent as a Microsoft 365 Copilot extension, allowing users to access it directly within Copilot.

> **Note**: This section requires a Microsoft 365 Copilot license. If you don't have one, you can read through the steps to understand the process.

### Understanding Copilot extensions

When you publish to Copilot, your agent becomes a **Copilot extension** (also called a plugin or declarative agent). Users can:

- Invoke your agent using @mentions in Copilot
- Access your agent's knowledge alongside Copilot's capabilities
- Switch between Copilot and your agent seamlessly

### Differences: Teams vs Copilot

| Aspect | Teams App | Copilot Extension |
|--------|-----------|-------------------|
| **Access** | Standalone chat in Teams | Within Microsoft 365 Copilot |
| **Invocation** | Open the app directly | @mention or select from extensions |
| **Context** | Isolated conversation | Can combine with Copilot's context |
| **License** | Standard M365 | Requires Copilot license |
| **Discovery** | Teams app store | Copilot extensions panel |

### Publish from the portal

1. Return to the Foundry portal (**https://ai.azure.com**)

2. Navigate to your agent (**Build** → **Agents** → **enterprise-knowledge-agent**)

3. Click the **Publish** button

4. Select **Publish to Teams and Microsoft 365 Copilot**

5. Click **Continue**

> **Note**: This is the same publishing flow used for Teams. The agent becomes available in both Teams and Copilot through a single publishing process.

### Configure publishing details

If you haven't already published this agent, fill in the configuration (same as the Teams section):

- **Name**: Enterprise Knowledge Agent
- **Description**: AI assistant for company IT policies
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

1. Click **Prepare Agent** and wait for packaging (1-2 minutes)

2. Select **Continue the in-product publishing flow**

3. Confirm your scope selection and click **Publish**

4. Wait for publishing to complete

### Access in Microsoft 365 Copilot

Once published with shared scope, your agent is immediately available:

1. Open **Microsoft 365 Copilot** (copilot.microsoft.com or in Microsoft 365 apps)

2. Look for the agent store or **Extensions** panel

3. Find your agent under **Your agents** (for shared scope)

4. Start a conversation:
    ```
    @Enterprise Knowledge Agent What are the laptop security requirements?
    ```

5. Or select your agent and ask directly:
    ```
    What MFA methods are supported for company systems?
    ```

6. Copilot routes the query to your agent and returns information from the IT security policy

> **Note**: For **organization scope**, an admin must first approve the app in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) under **Requests**. Once approved, the agent appears under **Built by your org** for all users.

### Managing your published agent

**Update the agent:**
1. Make changes to your agent in the Foundry portal (instructions, documents, tools)
2. Minor changes take effect automatically
3. Major changes may require re-publishing

**Monitor usage:**
1. Check analytics in the Foundry portal
2. Review conversation logs
3. Monitor for errors or issues

**Unpublish:**
1. In the Foundry portal, go to your agent's details
2. Find the publish status section
3. Click **Unpublish** to remove access from Teams and Copilot

---

## Update Published Agents

After publishing, you may need to update your agent. Here's how updates work.

### Making changes

1. In the Foundry portal, open your agent

2. Make your changes:
   - Update instructions
   - Add or remove documents
   - Modify tool settings

3. Click **Save**

### Propagating updates

**For Teams apps:**
- Instruction and document changes take effect immediately
- No need to re-upload the manifest
- Users see updated responses in their next conversation

**For Copilot extensions:**
- Minor changes (instructions, documents) may take effect automatically
- Major changes may require re-submission for approval
- Check the publish status for any pending reviews

### Version management

Best practices for managing agent versions:

1. **Document changes**: Keep a changelog of updates
2. **Test before publishing**: Always test in the playground first
3. **Communicate updates**: Let users know about significant changes
4. **Monitor after updates**: Watch for issues after deploying changes

---

## Cleanup

To avoid unnecessary charges, clean up resources when done.

### Delete the agent

1. In the Foundry portal, go to **Build** → **Agents**

2. Find **enterprise-knowledge-agent**

3. Click the **...** menu → **Delete**

4. Confirm deletion

This also removes:
- The Azure Bot Service
- Associated configurations
- Published deployments

### Uninstall from Teams

1. Open Microsoft Teams

2. Go to **Apps** → **Manage your apps**

3. Find **Enterprise Knowledge Agent**

4. Click **...** → **Uninstall**

5. Confirm uninstallation

### Remove Copilot extension

If you published to Copilot:

1. The extension becomes inactive when the agent is deleted
2. Users will see an error if they try to use it
3. Admin may need to remove it from the organization catalog

---

## Summary

**Congratulations!** 🎉 You've completed this lab!

### What You Accomplished

| Task | Status |
|------|--------|
| Created an agent in the Foundry portal | ✅ |
| Added knowledge with file search | ✅ |
| Published to Microsoft Teams | ✅ |
| Published to Microsoft 365 Copilot | ✅ |
| Learned to update published agents | ✅ |

### Key Takeaways

**Teams deployment:**
- Quick to set up using the Foundry portal
- Creates Azure Bot Service automatically
- Users access via Teams app
- Good for standalone chat experiences

**Copilot deployment:**
- Integrates with Microsoft 365 Copilot
- Users invoke via @mention or selection
- Requires Copilot license
- Good for contextual assistance within Copilot

**Best practices:**
- Test thoroughly in playground before publishing
- Keep documents up to date for accurate responses
- Monitor usage and feedback
- Update instructions based on user needs

### When to Use Each Platform

| Use Case | Recommended Platform |
|----------|---------------------|
| Dedicated support chat | Teams |
| Quick policy lookups | Copilot |
| Team-specific assistant | Teams (channel) |
| Organization-wide knowledge | Both |
| Integration with M365 workflow | Copilot |
| Standalone conversational experience | Teams |

### Next Steps

To build on this lab:

1. **Add more documents** for comprehensive knowledge coverage
2. **Customize instructions** for specific use cases
3. **Add tools** like code interpreter for advanced capabilities
4. **Implement authentication** for sensitive information
5. **Set up monitoring** to track usage and quality

---

## Troubleshooting Reference

### Teams Issues

| Issue | Solution |
|-------|----------|
| Can't upload custom app | Check Teams admin settings for custom app policy |
| App won't install | Verify manifest.zip isn't corrupted; check icon sizes |
| Agent not responding | Test in Foundry playground first; wait 30 seconds after install |
| Generic responses | Verify file search enabled and documents indexed |
| "Bot not found" error | Check Bot Service is running in Azure portal |

### Copilot Issues

| Issue | Solution |
|-------|----------|
| Extension not appearing | Check approval status; may be pending admin review |
| @mention not working | Ensure extension is enabled in your Copilot settings |
| Wrong responses | Test agent in Foundry playground; check document content |
| "Extension unavailable" | Verify agent is running and not deleted |
| Approval rejected | Review rejection reason; update and resubmit |

### General Issues

| Issue | Solution |
|-------|----------|
| Agent not saving | Check browser connection; try refreshing |
| Documents not indexing | Wait a few minutes; try re-uploading |
| Slow responses | Large documents take longer; consider chunking |
| Incorrect citations | Review document content and formatting |

---

## Additional Resources

**Microsoft Documentation:**
- [Publish agents to Teams](https://learn.microsoft.com/azure/ai-services/agents/how-to/publish-to-teams)
- [Copilot extensibility](https://learn.microsoft.com/microsoft-365-copilot/extensibility/)
- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/)

**Tools:**
- [Foundry Portal](https://ai.azure.com)
- [Microsoft Teams](https://teams.microsoft.com)
- [Microsoft 365 Copilot](https://copilot.microsoft.com)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)

---

**Lab Complete!** 🎉

You've successfully deployed an AI agent to both Microsoft Teams and Microsoft 365 Copilot!
