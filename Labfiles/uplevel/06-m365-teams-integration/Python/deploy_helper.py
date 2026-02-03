"""
Lab 5 - Deployment Helper
Interactive wizard to guide learners through Azure deployment using azd
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path

class DeploymentHelper:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.env_file = self.project_dir / ".env"
        
    def print_header(self, title):
        """Print a formatted section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def print_step(self, step_num, title):
        """Print a step header"""
        print(f"\n{'─' * 70}")
        print(f"Step {step_num}: {title}")
        print('─' * 70)
    
    def run_command(self, command, description=None, check=True):
        """Run a shell command with nice output"""
        if description:
            print(f"\n🔧 {description}...")
        
        print(f"   Running: {' '.join(command)}\n")
        
        try:
            result = subprocess.run(
                command,
                check=check,
                text=True,
                capture_output=False  # Show output in real-time
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Command failed with exit code {e.returncode}")
            return False
        except FileNotFoundError:
            print(f"\n❌ Command not found: {command[0]}")
            print("   Make sure all prerequisites are installed.")
            return False
    
    def check_prerequisites(self):
        """Quick check of prerequisites"""
        self.print_step(1, "Checking Prerequisites")
        
        print("Verifying required tools are installed...")
        
        checks = [
            (["azd", "version"], "Azure Developer CLI"),
            (["az", "--version"], "Azure CLI"),
            (["docker", "--version"], "Docker"),
        ]
        
        all_passed = True
        for command, name in checks:
            try:
                result = subprocess.run(command, capture_output=True, timeout=5)
                if result.returncode == 0:
                    print(f"   ✅ {name}")
                else:
                    print(f"   ❌ {name} - Not working")
                    all_passed = False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print(f"   ❌ {name} - Not found")
                all_passed = False
        
        if not all_passed:
            print("\n❌ Some prerequisites are missing.")
            print("   Run: python check_prerequisites.py")
            return False
        
        print("\n✅ All prerequisites installed!")
        return True
    
    def azure_login(self):
        """Ensure user is logged into Azure"""
        self.print_step(2, "Azure Authentication")
        
        print("Checking Azure login status...")
        
        # Check if already logged in
        result = subprocess.run(
            ["az", "account", "show"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Already logged into Azure CLI")
            
            # Get subscription info
            try:
                account_info = json.loads(result.stdout)
                subscription_name = account_info.get("name", "Unknown")
                subscription_id = account_info.get("id", "Unknown")
                print(f"   Subscription: {subscription_name}")
                print(f"   ID: {subscription_id}")
            except:
                pass
        else:
            print("Need to log into Azure CLI...")
            if not self.run_command(["az", "login"], "Logging into Azure"):
                return False
        
        # Check azd login
        print("\nChecking Azure Developer CLI login...")
        result = subprocess.run(
            ["azd", "auth", "login", "--check-status"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Already logged into Azure Developer CLI")
        else:
            print("Need to log into Azure Developer CLI...")
            if not self.run_command(["azd", "auth", "login"], "Logging into azd"):
                return False
        
        return True
    
    def initialize_project(self):
        """Initialize azd project"""
        self.print_step(3, "Initialize Project")
        
        # Check if already initialized
        azure_yaml = self.project_dir / "azure.yaml"
        if azure_yaml.exists():
            print("✅ Project already initialized (azure.yaml found)")
            response = input("\n   Reinitialize? This will reset configuration (y/N): ")
            if response.lower() != 'y':
                return True
        
        print("Initializing Azure Developer CLI project...")
        print("\nThis will:")
        print("   • Create azure.yaml configuration")
        print("   • Set up project structure for deployment")
        print("   • Configure agent deployment settings")
        
        # Initialize with template
        success = self.run_command(
            ["azd", "init", "--template", "Azure-Samples/azd-ai-starter-basic"],
            "Initializing project",
            check=False
        )
        
        if not success:
            print("\n⚠️  Template initialization failed, trying basic init...")
            success = self.run_command(
                ["azd", "init"],
                "Initializing project",
                check=False
            )
        
        if success:
            print("\n✅ Project initialized successfully!")
        else:
            print("\n❌ Project initialization failed")
            print("   You may need to initialize manually with: azd init")
            
        return success
    
    def configure_deployment(self):
        """Configure deployment settings"""
        self.print_step(4, "Configure Deployment")
        
        print("Let's configure your deployment settings.\n")
        
        # Get environment name
        env_name = input("Enter environment name (e.g., 'dev', 'lab5'): ").strip()
        if not env_name:
            env_name = "lab5"
            print(f"   Using default: {env_name}")
        
        # Get Azure region
        print("\nRecommended regions for Azure OpenAI:")
        print("   • northcentralus")
        print("   • eastus")
        print("   • eastus2")
        print("   • westus")
        region = input("\nEnter Azure region: ").strip()
        if not region:
            region = "northcentralus"
            print(f"   Using default: {region}")
        
        # Set environment
        print(f"\n🔧 Creating environment '{env_name}'...")
        self.run_command(
            ["azd", "env", "new", env_name],
            check=False
        )
        
        # Set location
        print(f"\n🔧 Setting region to '{region}'...")
        self.run_command(
            ["azd", "env", "set", "AZURE_LOCATION", region],
            check=False
        )
        
        print("\n✅ Deployment configured!")
        return True
    
    def deploy_to_azure(self):
        """Deploy everything to Azure"""
        self.print_step(5, "Deploy to Azure")
        
        print("This will deploy your agent to Azure.")
        print("\n⏱️  Expected time: 5-10 minutes")
        print("\nWhat will be created:")
        print("   • Azure AI Foundry project")
        print("   • Azure OpenAI deployment")
        print("   • Container Registry")
        print("   • Application Insights")
        print("   • Agent deployment")
        
        response = input("\nReady to deploy? (Y/n): ")
        if response.lower() == 'n':
            print("Deployment cancelled.")
            return False
        
        print("\n🚀 Starting deployment...\n")
        
        success = self.run_command(
            ["azd", "up"],
            "Deploying to Azure"
        )
        
        if success:
            print("\n" + "=" * 70)
            print("  🎉 Deployment Successful!")
            print("=" * 70)
            print("\nYour agent has been deployed to Azure!")
            print("\nNext steps:")
            print("   1. Run: python validate_deployment.py")
            print("   2. Open Foundry portal: https://ai.azure.com")
            print("   3. Navigate to your agent in the portal")
            print("   4. Test in the playground")
            print()
        else:
            print("\n❌ Deployment failed")
            print("   Check the error messages above for details")
            print("   Common issues:")
            print("   • Azure subscription not configured")
            print("   • Region quota limits")
            print("   • Docker not running")
            
        return success
    
    def run(self):
        """Run the full deployment workflow"""
        self.print_header("Lab 5: Agent Deployment Helper")
        
        print("Welcome to the Azure AI Agent Deployment Lab!")
        print("\nThis wizard will guide you through deploying your first AI agent to Azure.")
        print("The process uses Azure Developer CLI (azd) for automated deployment.")
        
        input("\nPress Enter to begin...")
        
        # Step 1: Prerequisites
        if not self.check_prerequisites():
            print("\n⚠️  Please install missing prerequisites first.")
            return False
        
        # Step 2: Azure login
        if not self.azure_login():
            print("\n⚠️  Azure login required to continue.")
            return False
        
        # Step 3: Initialize project
        if not self.initialize_project():
            print("\n⚠️  Project initialization failed.")
            return False
        
        # Step 4: Configure
        if not self.configure_deployment():
            print("\n⚠️  Configuration failed.")
            return False
        
        # Step 5: Deploy
        if not self.deploy_to_azure():
            print("\n⚠️  Deployment failed.")
            return False
        
        print("\n" + "=" * 70)
        print("  Deployment Complete! 🎉")
        print("=" * 70)
        print("\nYou've successfully deployed your AI agent to Azure!")
        print("\nNext: Run validate_deployment.py to verify everything works.")
        print()
        
        return True

def main():
    helper = DeploymentHelper()
    success = helper.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
