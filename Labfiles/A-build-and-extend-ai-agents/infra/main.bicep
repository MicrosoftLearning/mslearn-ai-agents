// Optional azd infrastructure for the Trailhead Adventure Works lab.
//
// Provisions a Microsoft Foundry (Azure AI Services) resource, a Foundry
// project, and one chat model deployment — the same resources you would
// otherwise create by hand in the Foundry portal.
//
// azd calls this at subscription scope: it creates the resource group and
// then everything inside it (see infra/resources.bicep).

targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the azd environment — used to name and tag resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources.')
param location string

@description('Name of the chat model to deploy (for example, gpt-4o).')
param modelName string = 'gpt-4o'

@description('Version of the chat model to deploy.')
param modelVersion string = '2024-11-20'

@description('The deployment name the lab uses (MODEL_DEPLOYMENT_NAME in .env).')
param modelDeploymentName string = 'gpt-4o'

@description('Model deployment capacity, in thousands of tokens per minute.')
param modelCapacity int = 30

// azd tags every resource in an environment with this so it can manage them.
var tags = { 'azd-env-name': environmentName }

// A short, deterministic token keeps globally-unique names stable per env.
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module ai 'resources.bicep' = {
  name: 'foundry'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    accountName: 'foundry-${resourceToken}'
    projectName: 'proj-${resourceToken}'
    modelName: modelName
    modelVersion: modelVersion
    modelDeploymentName: modelDeploymentName
    modelCapacity: modelCapacity
  }
}

// azd writes these outputs into the azd environment; the postprovision hook
// then copies them into Python/.env for the lab scripts to read.
output PROJECT_ENDPOINT string = ai.outputs.projectEndpoint
output MODEL_DEPLOYMENT_NAME string = ai.outputs.modelDeploymentName
output AZURE_LOCATION string = location
output AZURE_RESOURCE_GROUP string = resourceGroup.name
