---
lab:
    title: 'Deploy agents to Microsoft Teams and Copilot'
    description: 'Publish AI agents to Microsoft Teams and Microsoft 365 Copilot for enterprise access'
    level: 300
    duration: 40
    islab: true
---

# Deploy agents to Microsoft Teams and Copilot

In this lab, you'll learn how to publish AI agents to **Microsoft Teams** and **Microsoft 365 Copilot** so employees can access them where they already work. You'll create a simple agent in the Foundry portal, add knowledge grounding, then deploy it to both platforms.

This lab focuses on **deployment and publishing workflows**, not agent development.

This lab takes approximately **40** minutes.

> **Note**: Publishing to Microsoft 365 Copilot requires a Copilot license. The Teams deployment works with standard Microsoft 365 accounts.

## Prerequisites

Before starting this lab, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources
- **Microsoft 365 account** with Teams access
- **Microsoft 365 Copilot license** (optional, for Copilot deployment)
- Basic familiarity with the Microsoft Foundry portal

## Create a Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that open the first time you sign in, and if necessary use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

1. In the top banner, select **Start building** to try the new Microsoft Foundry Experience.

1. When prompted, create a **new** project, and enter a valid name for your project (for example, *m365-lab*).

1. Expand **Advanced options** and specify the following settings:
    - **Foundry resource**: *Create a new Foundry resource or select an existing one*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: *Select any available region*\

    > \* Some Azure AI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create** and wait for your project to be created.

2. When your project is created, a welcome dialog may appear. Select **Next** to read through the welcome message, and then select **Create agent**.

    You can also select **Start building** on the home page, and select **Create agents** from the drop-down menu.

3. Set the **Agent name** to `enterprise-knowledge-agent` and create the agent.

The playground will open for your newly created agent. You'll see that an available deployed model is already selected for you.

## Configure your agent with instructions and grounding data

Now that you have an agent created, let's configure it with instructions and knowledge to prepare it for publishing.

1. Set the **Instructions** to:

    ```
    You are an Enterprise Knowledge Assistant for Contoso Corporation.
    
    Your role:
    - Answer questions about company policies and procedures
    - Provide accurate information from uploaded documents
    - Be professional, helpful, and concise
    - If you don't know the answer, say so and suggest who to contact
    
    Always cite your sources when referencing specific policies.
    ```

2. Select **Save** to save your current agent configuration.

3. Download the sample policy documents. Open new browser tabs and save each file:

    **IT Security Policy:**

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/05a-m365-teams-integration/Python/sample_documents/it_security_policy.txt
    ```

    **Remote Work Policy:**

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-agents/main/Labfiles/05a-m365-teams-integration/Python/sample_documents/remote_work_policy.txt
    ```

4. Return to your agent's configuration, scroll to the **Tools** section

5. Select **Add** and then **Browse all tools** and **Add tool**.

6. A pop-up to attach files will appear. Attach the files you previously downloaded.

7. Once they complete, select **Attach**.

## Test the agent in the playground

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

    Your agent now has knowledge grounding and can answer questions based on your company documents.

7. Select **Save**.

## Publish to Microsoft Teams

Now you'll publish your agent to Microsoft Teams so employees can chat with it directly in Teams. When you publish to Teams, the Foundry portal automatically:

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
| **Website URL** | <https://contoso.com> (placeholder is fine for lab) |
| **Privacy Policy URL** | <https://contoso.com/privacy> |
| **Terms of Use URL** | <https://contoso.com/terms> |

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

2. Select the **Publish** button at the top of the page

3. Select **Publish to Teams and Microsoft 365 Copilot**.

4. Select **Continue**

### Configure Teams app details

Fill in the configuration form:

**Basic Information:**

- **App Name**: Enterprise Knowledge Agent
- **Short Description**: AI assistant for company policies
- **Full Description**: Enterprise AI assistant that answers questions about company policies, IT procedures, and employee resources

**Developer Information:**

- **Developer Name**: Your name
- **Website**: <https://contoso.com>
- **Privacy Policy**: <https://contoso.com/privacy>
- **Terms of Use**: <https://contoso.com/terms>

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

6. Your agent is now available in Teams! Find it under **Apps** → **Your agents**

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

## Publish to Microsoft 365 Copilot

Now you'll publish your agent as a Microsoft 365 Copilot extension, allowing users to access it directly within Copilot. When you publish to Copilot, your agent becomes a **Copilot extension** (also called a plugin or declarative agent). Users can:

- Invoke your agent using @mentions in Copilot
- Access your agent's knowledge alongside Copilot's capabilities
- Switch between Copilot and your agent seamlessly

> **Note**: This section requires a Microsoft 365 Copilot license. If you don't have one, you can read through the steps to understand the process.

### Publish from the portal

1. Return to the Foundry portal (**<https://ai.azure.com>**)

2. Navigate to your agent (**Build** → **Agents** → **enterprise-knowledge-agent**)

3. Select the **Publish** button

4. Select **Publish to Teams and Microsoft 365 Copilot**

5. Select **Continue**

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
    @Enterprise Knowledge Agent What are the laptop security requirements?
    ```

5. Or select your agent and ask directly:

    ```
    What MFA methods are supported for company systems?
    ```

6. Copilot routes the query to your agent and returns information from the IT security policy

> **Note**: For **organization scope**, an admin must first approve the app in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested) under **Requests**. Once approved, the agent appears under **Built by your org** for all users.

## Cleanup

To avoid unnecessary charges, clean up resources when done.

### Delete the agent

1. In the Foundry portal, go to **Build** → **Agents**

2. Find **enterprise-knowledge-agent**

3. Select the **...** menu → **Delete**

4. Confirm deletion

This also removes:

- The Azure Bot Service
- Associated configurations
- Published deployments

### Uninstall from Teams

1. Open Microsoft Teams

2. Go to **Apps** → **Manage your apps**

3. Find **Enterprise Knowledge Agent**

4. Select **...** → **Uninstall**

5. Confirm uninstallation

### Remove Copilot extension

If you published to Copilot:

1. The extension becomes inactive when the agent is deleted
2. Users will see an error if they try to use it
3. Admin may need to remove it from the organization catalog
