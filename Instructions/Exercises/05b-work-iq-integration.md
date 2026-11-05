---
lab:
    title: 'Work IQ - Workplace intelligence for AI agents (optional)'
    description: 'Build AI agents that access Microsoft 365 workplace data using Work IQ for meeting prep, project tracking, and action items.'
    level: 300
    duration: 40
    islab: true
    status: 'released'
---

# Work IQ - Workplace intelligence for AI agents

In this lab, you'll use the **Microsoft Foundry portal** to create an AI agent that accesses your Microsoft 365 workplace data using **Work IQ** - Microsoft's workplace intelligence layer. You'll configure a Work IQ MCP tool, add it to an agent, and ask questions about your meetings, email, and Teams messages.

This lab takes approximately **40** minutes.

> **Note:** This is an **optional/advanced lab** that requires usage-based billing with Copilot Credits for Work IQ API access.

## Prerequisites

Before you begin, ensure you have:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- A **Microsoft 365 account** with workplace data (emails, meetings, or Teams chats) to query.
- Basic familiarity with the Microsoft Foundry portal.
- [Usage-based billing with Copilot Credits](https://learn.microsoft.com/en-us/microsoft-365-copilot/usage-based-billing-overview-copilot-credits) enabled for Work IQ API access.
- **Azure RBAC roles**:
    - The **Foundry User** role on the Foundry project for the developer identity, the agent's runtime identity, and any user identity involved in OAuth flows.
    - The **Foundry Project Manager** role on the Foundry project for creating a Foundry connection to the Work IQ endpoint.
- The **Microsoft Entra Global Administrator** role assigned to your account, or an eligible assignment you can activate through **Microsoft Entra Privileged Identity Management (PIM)**, in your Microsoft 365 tenant. You'll use this role to provision the Work IQ service principal and grant admin consent for `WorkIQAgent.Ask`. Activate the role just in time and deactivate it after setup. Day-to-day Work IQ use doesn't require this role.

## Create a Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that open the first time you sign in and, if necessary, use the **Foundry** logo at the top left to navigate to the home page.

    > **Important**: For this lab, you're using the **New** Foundry experience.

2. In the top banner, select **Start building** to try the new Microsoft Foundry experience.

3. When prompted, create a **new** project and enter a valid name for your project (for example, *work-iq-lab*).

4. Expand **Advanced options** and specify the following settings:
    - **Foundry resource**: *Create a new Foundry resource or select an existing one*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: *Select any available region*\*

    > \* Some Azure AI resources are constrained by regional model quotas. If you exceed a quota limit later in the exercise, you may need to create another resource in a different region.

5. Select **Create** and wait for your project to be created.

6. When your project is created, close any welcome dialogs.

## Provision the Work IQ service principal

The Work IQ service principal must exist in your tenant before you can add Work IQ API permissions to an app registration. This is a **one-time setup per organization**. Check whether it already exists before provisioning it.

1. Open the [Microsoft Entra admin center](https://entra.microsoft.com), select your Microsoft 365 tenant, and go to **Entra ID** > **Enterprise applications** > **All applications**. Remove restrictive filters, including **Application type**, and filter by **Application ID** using `fdcc1f02-fc51-4226-8753-f668596af7f7`.

    - If a matching application exists, skip to **Create or reuse a Microsoft Entra app registration**.

2. If provisioning is needed, open [Azure Cloud Shell](https://shell.azure.com) and sign in with your Microsoft 365 tenant account.

    Alternatively, use a terminal with [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed and sign in using `az login --tenant <tenant-id>`, replacing `<tenant-id>` with your Microsoft 365 tenant ID.

3. Run the following command to provision the Work IQ service principal:

    ```azurecli
   az ad sp create --id fdcc1f02-fc51-4226-8753-f668596af7f7
    ```

4. Confirm that the command returns service principal details with `appId` set to `fdcc1f02-fc51-4226-8753-f668596af7f7`. If the command reports that the service principal already exists, you can continue. Resolve any other errors before proceeding.

    > **Note:** For the full tenant setup guidance, see [Enable your tenant for Work IQ](https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/enable-work-iq).

## Create or reuse a Microsoft Entra app registration

If your organization already has an app registration approved for this Work IQ connection, reuse it. Confirm that it is in the same tenant as your Microsoft 365 account and has the delegated **WorkIQAgent.Ask** permission with admin consent. Otherwise, complete the following steps.

1. Open the [Microsoft Entra admin center](https://entra.microsoft.com) and select **Entra ID** > **App registrations**.

2. Select **New registration** and enter a descriptive name, such as `work-iq-lab-app`.

3. Set **Supported account types** to **Accounts in this organizational directory only**, and select **Register**.

4. On the app's **Overview** page, copy the **Application (client) ID** and **Directory (tenant) ID**. Keep these values for the Foundry connection.

5. Select **API permissions** > **Add a permission** > **APIs my organization uses**.

6. Search for **Work IQ** (application ID `fdcc1f02-fc51-4226-8753-f668596af7f7`) and select it.

7. Select **Delegated permissions**, select **WorkIQAgent.Ask**, and then select **Add permissions**.

    This permission lets the app query the signed-in user's Microsoft 365 workplace intelligence, including mail, files, meetings, and chats.

8. Select **Grant admin consent for [your tenant]**, review the confirmation dialog, and select **Yes**.

9. Confirm that admin consent has been granted for this permission in your tenant.

## Create a client secret for the Foundry connection

If you are reusing an existing app registration and have an approved, unexpired client secret available from your organization's secret store, reuse it. Otherwise, create a secret as follows.

1. In your app registration, select **Certificates & secrets** > **Client secrets** > **New client secret**.

2. Enter a description, choose an expiration that complies with your organization's policy, and select **Add**.

3. Immediately copy the secret **Value**, not the **Secret ID**. The value is only displayed once. Store it in **Azure Key Vault** or another approved secret store.

    > **Important:** Never commit the secret to source control or print or log it. Rotate it before it expires. If the value is no longer available, create a new secret rather than trying to recover it.

4. Ensure you have the **Application (client) ID**, **Directory (tenant) ID**, and **client secret value** available for creating the Foundry connection.

    You'll use these values in the next section to configure the Work IQ MCP tool.

5. If you activated the **Global Administrator** role through PIM, deactivate it when tenant setup and admin consent are complete. Day-to-day Work IQ use doesn't require this role.

## Create the Work IQ MCP tool

Now you'll connect the remote Work IQ MCP server to your Foundry project using the app registration details.

1. Return to your project in the [Foundry portal](https://ai.azure.com).

2. In the left navigation, select **Tools**, and then select the **Tools** tab.

3. Select **Connect a tool**. In **Select a tool**, select the **Catalog** tab.

4. Search for **Work IQ MCP**, select it, and then select **Create**.

5. If prompted for a name, enter `work-iq-mcp`. Confirm that the MCP endpoint is:

    ```text
   https://workiq.svc.cloud.microsoft/mcp
    ```

6. Configure authentication using the following values:

    | Field | Value |
    | --- | --- |
    | **Client ID** | Your app registration's **Application (client) ID** |
    | **Client secret** | Your app registration's client secret **Value** |
    | **Authorization URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/authorize` |
    | **Token URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
    | **Refresh URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
    | **Scopes** | `offline_access fdcc1f02-fc51-4226-8753-f668596af7f7/WorkIQAgent.Ask` |

    Replace `{tenant-id}` in all three URLs with your **Directory (tenant) ID**.

7. Save the tool connection and copy the **OAuth redirect URL** provided by Foundry.

    > **Important:** If connection fields can't be edited after creation, delete and recreate the lab connection to correct any values. Don't delete a shared connection used by other agents.

### Register the OAuth redirect URL

Before you can sign in through the tool, your app registration must accept the redirect URL generated by Foundry.

1. In the [Microsoft Entra admin center](https://entra.microsoft.com), go to **Entra ID** > **App registrations** and open the app you configured earlier.

2. Select **Authentication** > **Add Redirect URI configuration** > **Web**. If the app already has a Web platform, add a redirect URI to that platform instead.

3. Paste the exact **OAuth redirect URL** from Foundry into **Redirect URIs**, and select **Configure** or **Save**, as appropriate.

    Be sure to preserve any existing redirect URIs if you are reusing an app registration.

4. Return to your Foundry project. Confirm that the configured **Work IQ MCP** tool is listed on the **Tools** page.

    > **Note:** This integration uses delegated authentication. Work IQ requests run as the user who authorizes the connection and honor that user's Microsoft 365 permissions. Application-only authentication isn't supported. For more information, see [Connect a Microsoft Foundry project to Work IQ](https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/mcp/quickstart/foundry).

## Create an agent and add Work IQ

1. In your Foundry project, navigate to **Agents**.

2. Select **New Agent** > **Build an agent** and create a new agent named `workplace-intelligence-agent`.

    For this agent, you can leave the default **Interaction mode** set to **Text**.

3. Set the agent's **Instructions** to:

    ```text
   You are a workplace intelligence assistant.
   Use Work IQ to answer questions about the signed-in user's Microsoft 365
   meetings, email, and Teams messages.
   Keep responses concise and include source links when available.
   If no matching data is found, say so. Don't invent workplace information.
   If a tool call fails, explain the failure instead of presenting it as no data.
   For this lab, only read and summarize information. Don't create, send,
   update, or delete Microsoft 365 content.
    ```

4. In the agent's **Tools** section, select **Add** > **Add tools**.

5. In the list of Configured tools, select the **Work IQ MCP** tool you created.

6. Save the agent configuration. Confirm that **Work IQ MCP** appears in the agent's tools list.

## Authorize the connection and approve a tool call

The app's admin consent, your sign-in authorization, and tool-call approval serve different purposes. Admin consent approves the app's delegated permission; authorization connects your user account; tool-call approval lets you review an individual request before it runs.

1. In the agent playground, start a new conversation and enter:

    ```text
   Use Work IQ to summarize my upcoming meetings for today.
    ```

    You may be prompted to authorize the connection to Work IQ. Follow the prompts to authorize access.

2. When the agent requests permission to call the tool, inspect the tool name and arguments. Confirm that the request matches your question and doesn't change any workplace data, then select **Allow** or **Approve** for this call.

3. Wait for the agent's response. Inspect the tool-call details in the playground and confirm that the Work IQ call completed without errors.

4. Compare the answer with your calendar and follow any source links provided. If you have no meetings today, try a day when you know you have a meeting.

## Verify connectivity with basic prompts

Try a few more questions in the playground. Review and approve the Work IQ tool calls for each request. Responses depend on your account's data and permissions, so use topics and dates that you recognize.

### Find recent email

1. Enter:

    ```text
   Use Work IQ to find three recent emails I received this week.
   List the subject, sender, and date, and include source links when available.
    ```

2. Compare the results with your mailbox. If no matching messages are found, broaden the time range to the past month.

### Find a Teams discussion

1. Enter the following prompt, replacing `[topic]` with a topic you know appears in your Teams messages:

    ```text
   Use Work IQ to find recent Teams messages about [topic] from the past month.
   Summarize the discussion and include source links when available.
    ```

2. Check that the summary matches a discussion you can access in Teams. If your account has no Teams messages, try another email or meeting query instead.

### Ask a follow-up question

1. Refer to a meeting, email, or discussion returned in an earlier answer:

    ```text
   Using Work IQ, find any action items assigned to me in that discussion.
   Include deadlines only if they are explicitly stated in the source.
    ```

2. Check the answer against the original source. It is valid for the agent to report that no explicit action items were found.

You've verified connectivity when you can observe successful Work IQ tool calls and compare at least one grounded response with data in your calendar, mailbox, or Teams. Great work!

## Clean up

The portal doesn't automatically delete the resources created in this lab.

1. If you no longer need the agent, delete `workplace-intelligence-agent` from your project's **Agents** page.

2. On the project's **Tools** page, remove the Work IQ MCP tool connection if you created it solely for this lab and no other agent uses it.

3. In the Microsoft Entra admin center, delete the client secret you created solely for this lab. If you created a dedicated lab app registration and no other application or connection uses it, delete that app registration as well. Don't delete shared app registrations, secrets, or the tenant's Work IQ service principal.

4. If you created an Azure resource group solely for this lab, open the [Azure portal](https://portal.azure.com), review its contents, and delete it only after confirming that all its resources are no longer needed. If you reused a resource group, don't delete it; remove only lab-specific resources you no longer need, including any model deployment created solely for this lab.

    > **Important:** Model usage and Work IQ requests can incur charges. Follow your organization's retention and billing policies when deciding what to keep.