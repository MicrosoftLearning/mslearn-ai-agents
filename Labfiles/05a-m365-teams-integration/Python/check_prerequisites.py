"""
Lab 5 - Prerequisites Checker
Validates all required tools are installed for the deployment lab
"""

import subprocess
import sys
import platform
from typing import Tuple, List

class PrerequisiteChecker:
    def __init__(self):
        self.results = []
        self.all_passed = True
    
    def check_command(self, name: str, command: List[str], min_version: str = None) -> Tuple[bool, str]:
        """Check if a command exists and optionally verify version"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                # Clean up version output
                version = version.split('\n')[0][:80]
                
                if min_version:
                    return True, f"✅ {name}: {version}"
                else:
                    return True, f"✅ {name}: Installed"
            else:
                return False, f"❌ {name}: Command failed"
                
        except FileNotFoundError:
            return False, f"❌ {name}: Not found"
        except subprocess.TimeoutExpired:
            return False, f"❌ {name}: Command timeout"
        except Exception as e:
            return False, f"❌ {name}: Error - {str(e)}"
    
    def check_azure_login(self) -> Tuple[bool, str]:
        """Check if user is logged into Azure"""
        try:
            result = subprocess.run(
                ["az", "account", "show"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Extract subscription name from output
                output = result.stdout
                if "name" in output:
                    return True, "✅ Azure CLI: Logged in"
                return True, "✅ Azure CLI: Authenticated"
            else:
                return False, "⚠️  Azure CLI: Not logged in (run 'az login')"
                
        except Exception as e:
            return False, f"⚠️  Azure CLI: Cannot verify login - {str(e)}"
    
    def check_docker_running(self) -> Tuple[bool, str]:
        """Check if Docker Desktop is running"""
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, "✅ Docker: Running"
            else:
                return False, "❌ Docker: Not running (start Docker Desktop)"
                
        except FileNotFoundError:
            return False, "❌ Docker: Not installed"
        except Exception as e:
            return False, f"❌ Docker: Error - {str(e)}"
    
    def run_all_checks(self):
        """Run all prerequisite checks"""
        print("=" * 70)
        print("Lab 5: Prerequisites Check")
        print("=" * 70)
        print()
        
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info >= (3, 10):
            self.results.append((True, f"✅ Python: {python_version}"))
        else:
            self.results.append((False, f"❌ Python: {python_version} (need 3.10+)"))
            self.all_passed = False
        
        # Check Azure Developer CLI
        passed, msg = self.check_command(
            "Azure Developer CLI",
            ["azd", "version"],
            min_version="1.23.0"
        )
        self.results.append((passed, msg))
        if not passed:
            self.all_passed = False
        
        # Check Azure CLI
        passed, msg = self.check_command(
            "Azure CLI",
            ["az", "--version"]
        )
        self.results.append((passed, msg))
        if not passed:
            self.all_passed = False
        
        # Check Docker
        passed, msg = self.check_command(
            "Docker",
            ["docker", "--version"]
        )
        self.results.append((passed, msg))
        if not passed:
            self.all_passed = False
        
        # Check if Docker is running
        passed, msg = self.check_docker_running()
        self.results.append((passed, msg))
        if not passed and "Not installed" not in msg:
            self.all_passed = False
        
        # Check Azure login status (warning only)
        passed, msg = self.check_azure_login()
        self.results.append((passed, msg))
        # Don't fail on login - user can do this later
        
        # Check git (optional but recommended)
        passed, msg = self.check_command(
            "Git",
            ["git", "--version"]
        )
        self.results.append((passed, msg))
        # Git is optional, don't fail
        
        # Display results
        print("\nPrerequisites Check Results:")
        print("-" * 70)
        for _, message in self.results:
            print(message)
        print("-" * 70)
        print()
        
        if self.all_passed:
            print("✅ All required prerequisites are installed!")
            print()
            print("Next Steps:")
            print("1. Run: python deploy_helper.py")
            print("2. Follow the interactive deployment wizard")
            print()
        else:
            print("❌ Some prerequisites are missing. Please install them:")
            print()
            print("Azure Developer CLI:")
            if platform.system() == "Windows":
                print("  powershell -ex AllSigned -c \"Invoke-RestMethod 'https://aka.ms/install-azd.ps1' | Invoke-Expression\"")
            else:
                print("  curl -fsSL https://aka.ms/install-azd.sh | bash")
            print()
            print("Docker Desktop:")
            print("  Download from: https://www.docker.com/products/docker-desktop")
            print()
            print("Azure CLI:")
            print("  Visit: https://learn.microsoft.com/cli/azure/install-azure-cli")
            print()
        
        return self.all_passed

def main():
    checker = PrerequisiteChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
