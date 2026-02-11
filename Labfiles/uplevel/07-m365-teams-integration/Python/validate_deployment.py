"""
Lab 5 - Deployment Validator
Checks that the agent deployment was successful and provides next steps
"""

import subprocess
import sys
import json
import os
from pathlib import Path
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient

class DeploymentValidator:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.endpoint = None
        self.project_name = None
        self.resource_group = None
        
    def print_header(self, title):
        """Print a formatted section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def get_azd_env_values(self):
        """Get environment values from azd"""
        print("🔍 Retrieving deployment information from azd...\n")
        
        try:
            # Get all environment values
            result = subprocess.run(
                ["azd", "env", "get-values"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse key=value pairs
            env_vars = {}
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"')
            
            # Extract key values
            self.endpoint = env_vars.get('AZUREAI_PROJECT_ENDPOINT') or env_vars.get('PROJECT_ENDPOINT')
            self.project_name = env_vars.get('AZUREAI_PROJECT_NAME') or env_vars.get('PROJECT_NAME')
            self.resource_group = env_vars.get('AZURE_RESOURCE_GROUP') or env_vars.get('RESOURCE_GROUP')
            
            if self.endpoint:
                print(f"   ✅ Found endpoint: {self.endpoint}")
            if self.project_name:
                print(f"   ✅ Found project: {self.project_name}")
            if self.resource_group:
                print(f"   ✅ Found resource group: {self.resource_group}")
                
            return bool(self.endpoint)
            
        except subprocess.CalledProcessError:
            print("   ❌ Could not retrieve azd environment values")
            print("   Make sure deployment completed successfully")
            return False
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
    
    def check_project_connection(self):
        """Try to connect to the AI Project"""
        print("\n🔍 Testing connection to AI Project...\n")
        
        if not self.endpoint:
            print("   ❌ No endpoint found")
            return False
        
        try:
            # Create credential and client
            credential = DefaultAzureCredential()
            project_client = AIProjectClient(
                credential=credential,
                endpoint=self.endpoint
            )
            
            # Try to get project info
            project_info = project_client.get_project()
            
            print(f"   ✅ Successfully connected to project!")
            print(f"   Project Name: {project_info.get('name', 'N/A')}")
            print(f"   Location: {project_info.get('location', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"   ⚠️  Could not connect to project: {str(e)}")
            print("   This is normal if project is still provisioning")
            return False
    
    def check_azure_resources(self):
        """Check Azure resources were created"""
        print("\n🔍 Checking Azure resources...\n")
        
        if not self.resource_group:
            print("   ⚠️  No resource group found")
            return False
        
        try:
            # List resources in resource group
            result = subprocess.run(
                ["az", "resource", "list", "--resource-group", self.resource_group],
                capture_output=True,
                text=True,
                check=True
            )
            
            resources = json.loads(result.stdout)
            
            if not resources:
                print("   ⚠️  No resources found yet")
                return False
            
            print(f"   ✅ Found {len(resources)} resources in '{self.resource_group}':")
            
            # Show key resource types
            resource_types = {}
            for resource in resources:
                rtype = resource.get('type', '').split('/')[-1]
                resource_types[rtype] = resource_types.get(rtype, 0) + 1
            
            for rtype, count in sorted(resource_types.items()):
                print(f"      • {rtype}: {count}")
            
            return True
            
        except subprocess.CalledProcessError:
            print("   ⚠️  Could not list resources")
            return False
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)}")
            return False
    
    def get_portal_urls(self):
        """Generate portal URLs"""
        print("\n🌐 Portal URLs:\n")
        
        # Foundry portal
        foundry_url = "https://ai.azure.com"
        print(f"   Foundry Portal: {foundry_url}")
        
        # Azure portal (if we have resource group)
        if self.resource_group:
            azure_portal_url = f"https://portal.azure.com/#@/resource/subscriptions/{{subscription}}/resourceGroups/{self.resource_group}"
            print(f"   Azure Portal: https://portal.azure.com")
            print(f"   Resource Group: {self.resource_group}")
        
        print()
    
    def show_next_steps(self):
        """Display next steps for the learner"""
        print("\n" + "=" * 70)
        print("  Next Steps")
        print("=" * 70 + "\n")
        
        print("1️⃣  Test your agent in Foundry Portal:")
        print("   • Visit: https://ai.azure.com")
        print("   • Navigate to: Build → Agents")
        print("   • Find your deployed agent")
        print("   • Click 'Open in playground'")
        print("   • Send a test message: 'Hello! What can you help me with?'")
        print()
        
        print("2️⃣  Add document search capabilities:")
        print("   • Run: python setup_search.py")
        print("   • This will create Azure AI Search")
        print("   • Upload sample company documents")
        print("   • Connect search to your agent")
        print()
        
        print("3️⃣  Connect to search in Foundry Portal (Step 3):")
        print("   • Follow the lab instructions")
        print("   • Use the portal UI to add search connection")
        print()
        
        print("4️⃣  Publish to Microsoft Teams (Step 4):")
        print("   • Follow the lab instructions")
        print("   • Use the portal UI to publish")
        print()
    
    def run(self):
        """Run all validation checks"""
        self.print_header("Lab 5: Deployment Validation")
        
        print("This script validates your agent deployment was successful.\n")
        
        # Check 1: Get deployment info
        if not self.get_azd_env_values():
            print("\n❌ Could not retrieve deployment information")
            print("   Make sure you ran: python deploy_helper.py")
            return False
        
        # Check 2: Test project connection
        connection_ok = self.check_project_connection()
        
        # Check 3: Check Azure resources
        resources_ok = self.check_azure_resources()
        
        # Show portal URLs
        self.get_portal_urls()
        
        # Summary
        print("\n" + "=" * 70)
        print("  Validation Summary")
        print("=" * 70 + "\n")
        
        if connection_ok and resources_ok:
            print("✅ All checks passed!")
            print("✅ Your agent is deployed and ready to use!")
            self.show_next_steps()
            return True
        elif resources_ok:
            print("✅ Resources are created")
            print("⚠️  Project connection pending (may still be provisioning)")
            print("\n   Wait 2-3 minutes and run this script again")
            return True
        else:
            print("⚠️  Deployment validation incomplete")
            print("   Some resources may still be provisioning")
            print("   Wait a few minutes and run this script again")
            return False

def main():
    validator = DeploymentValidator()
    success = validator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
