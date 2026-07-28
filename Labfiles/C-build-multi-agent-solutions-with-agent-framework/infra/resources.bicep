// Foundry account + project + model deployment for the lab.
// Deployed into the resource group created by main.bicep.

@description('Location for all resources.')
param location string

@description('Tags applied to every resource.')
param tags object = {}

@description('Globally-unique name for the Foundry (Azure AI Services) account.')
param accountName string

@description('Name of the Foundry project.')
param projectName string

@description('Name of the chat model to deploy.')
param modelName string

@description('Version of the chat model to deploy.')
param modelVersion string

@description('Deployment name the lab uses (MODEL_DEPLOYMENT_NAME in .env).')
param modelDeploymentName string

@description('Model deployment capacity, in thousands of tokens per minute.')
param modelCapacity int

// The Microsoft Foundry resource (an Azure AI Services account with project
// support). allowProjectManagement enables the new Foundry project experience.
resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    // Use the account name as the custom subdomain so the project endpoint
    // resolves to https://<accountName>.services.ai.azure.com/...
    customSubDomainName: accountName
    publicNetworkAccess: 'Enabled'
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: projectName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {}
}

// Deploy the chat model. The deployment's name is what the lab references as
// MODEL_DEPLOYMENT_NAME. Model deployments live on the account, not the project.
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: modelDeploymentName
  sku: {
    name: 'GlobalStandard'
    capacity: modelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
  }
}

// Project endpoint in the form the lab's .env expects:
//   https://<account>.services.ai.azure.com/api/projects/<project>
output projectEndpoint string = 'https://${account.name}.services.ai.azure.com/api/projects/${project.name}'
output modelDeploymentName string = modelDeployment.name
output accountName string = account.name
output projectName string = project.name
