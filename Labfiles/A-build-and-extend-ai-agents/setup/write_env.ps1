# Copies the endpoint + model deployment name that 'azd up' just provisioned
# into the lab's Python/.env, so the task scripts can read them.
#
# azd runs this automatically after provisioning (see azure.yaml). It sets the
# bicep outputs as environment variables, which we read here.

$ErrorActionPreference = 'Stop'

$envPath = Join-Path $PSScriptRoot '..\Python\.env'
$examplePath = Join-Path $PSScriptRoot '..\Python\.env.example'

# Start from the existing .env, or the example if there isn't one yet.
if (-not (Test-Path $envPath)) {
    if (Test-Path $examplePath) { Copy-Item $examplePath $envPath }
    else { New-Item -ItemType File -Path $envPath | Out-Null }
}

function Set-EnvValue([string]$key, [string]$value) {
    if ([string]::IsNullOrWhiteSpace($value)) { return }
    $lines = @(Get-Content $envPath)
    $set = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match "^\s*$key\s*=") {
            $lines[$i] = "$key=$value"
            $set = $true
        }
    }
    if (-not $set) { $lines += "$key=$value" }
    Set-Content -Path $envPath -Value $lines
}

Set-EnvValue 'PROJECT_ENDPOINT' $env:PROJECT_ENDPOINT
Set-EnvValue 'MODEL_DEPLOYMENT_NAME' $env:MODEL_DEPLOYMENT_NAME

Write-Host "Updated $envPath with your provisioned PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME."
Write-Host "Task 3 also needs a grounded agent: run 'python setup/bootstrap_agent.py' to create it."
