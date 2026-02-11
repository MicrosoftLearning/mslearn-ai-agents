"""
Lab 5 - Azure AI Search Setup
Automates creation of Azure AI Search resource and document indexing
"""

import subprocess
import sys
import json
import os
import time
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.core.credentials import AzureKeyCredential
import hashlib

class SearchSetup:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.docs_dir = self.project_dir / "sample_documents"
        self.resource_group = None
        self.location = None
        self.search_service_name = None
        self.search_endpoint = None
        self.search_key = None
        self.index_name = "company-knowledge"
        
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
    
    def get_deployment_info(self):
        """Get deployment info from azd"""
        self.print_step(1, "Retrieving Deployment Information")
        
        try:
            result = subprocess.run(
                ["azd", "env", "get-values"],
                capture_output=True,
                text=True,
                check=True
            )
            
            env_vars = {}
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"')
            
            self.resource_group = env_vars.get('AZURE_RESOURCE_GROUP')
            self.location = env_vars.get('AZURE_LOCATION', 'northcentralus')
            
            if not self.resource_group:
                print("❌ Could not find resource group")
                print("   Make sure deployment completed successfully")
                return False
            
            print(f"✅ Resource Group: {self.resource_group}")
            print(f"✅ Location: {self.location}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def create_search_service(self):
        """Create Azure AI Search resource"""
        self.print_step(2, "Creating Azure AI Search Service")
        
        # Generate unique search service name
        rg_hash = hashlib.md5(self.resource_group.encode()).hexdigest()[:6]
        self.search_service_name = f"search-{rg_hash}"
        
        print(f"Creating search service: {self.search_service_name}")
        print("Tier: Basic (suitable for labs)")
        print("\n⏱️  This takes 2-3 minutes...\n")
        
        try:
            # Create search service
            result = subprocess.run([
                "az", "search", "service", "create",
                "--name", self.search_service_name,
                "--resource-group", self.resource_group,
                "--sku", "basic",
                "--location", self.location,
                "--partition-count", "1",
                "--replica-count", "1"
            ], capture_output=True, text=True, check=True)
            
            print("✅ Search service created successfully!")
            
            # Get endpoint
            self.search_endpoint = f"https://{self.search_service_name}.search.windows.net"
            print(f"   Endpoint: {self.search_endpoint}")
            
            # Get admin key
            result = subprocess.run([
                "az", "search", "admin-key", "show",
                "--service-name", self.search_service_name,
                "--resource-group", self.resource_group
            ], capture_output=True, text=True, check=True)
            
            key_info = json.loads(result.stdout)
            self.search_key = key_info.get("primaryKey")
            
            if self.search_key:
                print("✅ Retrieved admin key")
            
            return True
            
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr or "already exists" in e.stdout:
                print(f"⚠️  Search service '{self.search_service_name}' already exists")
                print("   Using existing service...")
                
                self.search_endpoint = f"https://{self.search_service_name}.search.windows.net"
                
                # Get admin key
                try:
                    result = subprocess.run([
                        "az", "search", "admin-key", "show",
                        "--service-name", self.search_service_name,
                        "--resource-group", self.resource_group
                    ], capture_output=True, text=True, check=True)
                    
                    key_info = json.loads(result.stdout)
                    self.search_key = key_info.get("primaryKey")
                    print("✅ Retrieved admin key")
                    return True
                except:
                    print("❌ Could not retrieve admin key")
                    return False
            else:
                print(f"❌ Failed to create search service: {e.stderr}")
                return False
    
    def create_search_index(self):
        """Create search index with schema"""
        self.print_step(3, "Creating Search Index")
        
        print(f"Creating index: {self.index_name}")
        
        try:
            credential = AzureKeyCredential(self.search_key)
            index_client = SearchIndexClient(
                endpoint=self.search_endpoint,
                credential=credential
            )
            
            # Define index schema
            fields = [
                SimpleField(
                    name="id",
                    type=SearchFieldDataType.String,
                    key=True
                ),
                SearchableField(
                    name="title",
                    type=SearchFieldDataType.String,
                    searchable=True
                ),
                SearchableField(
                    name="content",
                    type=SearchFieldDataType.String,
                    searchable=True
                ),
                SimpleField(
                    name="category",
                    type=SearchFieldDataType.String,
                    filterable=True,
                    facetable=True
                ),
                SimpleField(
                    name="source_file",
                    type=SearchFieldDataType.String
                )
            ]
            
            index = SearchIndex(
                name=self.index_name,
                fields=fields
            )
            
            # Create or update index
            result = index_client.create_or_update_index(index)
            
            print(f"✅ Index '{self.index_name}' created successfully!")
            print(f"   Fields: id, title, content, category, source_file")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create index: {str(e)}")
            return False
    
    def upload_documents(self):
        """Upload sample documents to the index"""
        self.print_step(4, "Uploading Sample Documents")
        
        # Check if sample_documents folder exists
        if not self.docs_dir.exists():
            print(f"⚠️  Sample documents folder not found: {self.docs_dir}")
            return False
        
        # Get all document files
        doc_files = list(self.docs_dir.glob("*.*"))
        
        if not doc_files:
            print(f"⚠️  No documents found in: {self.docs_dir}")
            return False
        
        print(f"Found {len(doc_files)} documents to upload:\n")
        
        try:
            credential = AzureKeyCredential(self.search_key)
            search_client = SearchClient(
                endpoint=self.search_endpoint,
                index_name=self.index_name,
                credential=credential
            )
            
            documents = []
            
            for doc_file in doc_files:
                print(f"   📄 {doc_file.name}")
                
                # Read file content
                try:
                    content = doc_file.read_text(encoding='utf-8')
                except:
                    print(f"      ⚠️  Could not read as text, skipping...")
                    continue
                
                # Extract title from first line or filename
                lines = content.strip().split('\n')
                title = lines[0][:100] if lines else doc_file.stem
                
                # Determine category from filename
                category = "Policy"
                if "handbook" in doc_file.name.lower():
                    category = "Handbook"
                elif "security" in doc_file.name.lower():
                    category = "Security"
                elif "expense" in doc_file.name.lower():
                    category = "Finance"
                
                # Create document
                doc = {
                    "id": hashlib.md5(doc_file.name.encode()).hexdigest(),
                    "title": title,
                    "content": content[:50000],  # Limit content size
                    "category": category,
                    "source_file": doc_file.name
                }
                
                documents.append(doc)
            
            # Upload batch
            if documents:
                result = search_client.upload_documents(documents=documents)
                print(f"\n✅ Uploaded {len(documents)} documents successfully!")
            else:
                print("\n⚠️  No documents to upload")
                return False
            
            return True
            
        except Exception as e:
            print(f"\n❌ Failed to upload documents: {str(e)}")
            return False
    
    def test_search(self):
        """Test search functionality"""
        self.print_step(5, "Testing Search")
        
        print("Running test query: 'remote work'...\n")
        
        try:
            credential = AzureKeyCredential(self.search_key)
            search_client = SearchClient(
                endpoint=self.search_endpoint,
                index_name=self.index_name,
                credential=credential
            )
            
            # Simple search
            results = search_client.search(
                search_text="remote work",
                top=3
            )
            
            found_results = False
            for result in results:
                found_results = True
                print(f"   📄 {result.get('title', 'Untitled')[:60]}")
                print(f"      Category: {result.get('category', 'N/A')}")
                print(f"      Source: {result.get('source_file', 'N/A')}")
                print()
            
            if found_results:
                print("✅ Search is working correctly!")
            else:
                print("⚠️  No results found (documents may still be indexing)")
            
            return True
            
        except Exception as e:
            print(f"❌ Search test failed: {str(e)}")
            return False
    
    def save_configuration(self):
        """Save search configuration to .env"""
        self.print_step(6, "Saving Configuration")
        
        env_file = self.project_dir / ".env"
        
        print(f"Adding search configuration to .env file...\n")
        
        # Read existing .env if present
        existing_content = ""
        if env_file.exists():
            existing_content = env_file.read_text()
        
        # Add or update search variables
        search_vars = f"""
# Azure AI Search Configuration
SEARCH_ENDPOINT={self.search_endpoint}
SEARCH_KEY={self.search_key}
SEARCH_INDEX_NAME={self.index_name}
SEARCH_SERVICE_NAME={self.search_service_name}
"""
        
        # Append if not already present
        if "SEARCH_ENDPOINT" not in existing_content:
            with open(env_file, 'a') as f:
                f.write(search_vars)
            print("✅ Configuration saved to .env")
        else:
            print("✅ Configuration already in .env (not modified)")
        
        print(f"\n   Search Endpoint: {self.search_endpoint}")
        print(f"   Index Name: {self.index_name}")
        
        return True
    
    def show_next_steps(self):
        """Display next steps"""
        print("\n" + "=" * 70)
        print("  Next Steps")
        print("=" * 70 + "\n")
        
        print("Your Azure AI Search is ready! 🎉\n")
        
        print("Next: Connect your agent to search (Lab Step 3)")
        print("\n1️⃣  Open Foundry Portal: https://ai.azure.com")
        print("\n2️⃣  Navigate to: Management Center → Connected Resources")
        print("\n3️⃣  Add Connection:")
        print("   • Click: + New Connection")
        print("   • Type: Azure AI Search")
        print(f"   • Service: {self.search_service_name}")
        print("   • Authentication: API Key")
        print("\n4️⃣  Update your agent:")
        print("   • Go to Build → Agents")
        print("   • Edit your agent")
        print("   • Add Tool: Azure AI Search")
        print("   • Select your connection")
        print(f"   • Index: {self.index_name}")
        print("\n5️⃣  Test in Playground:")
        print("   • Ask: 'What is our remote work policy?'")
        print("   • Ask: 'How do I submit expense reports?'")
        print()
    
    def run(self):
        """Run the full setup workflow"""
        self.print_header("Lab 5: Azure AI Search Setup")
        
        print("This script will:")
        print("  1. Create an Azure AI Search service")
        print("  2. Create a search index")
        print("  3. Upload sample company documents")
        print("  4. Test search functionality")
        print("  5. Save configuration")
        
        input("\nPress Enter to begin...")
        
        # Step 1: Get deployment info
        if not self.get_deployment_info():
            return False
        
        # Step 2: Create search service
        if not self.create_search_service():
            return False
        
        # Step 3: Create index
        if not self.create_search_index():
            return False
        
        # Step 4: Upload documents
        if not self.upload_documents():
            return False
        
        # Give indexing a moment
        print("\n⏱️  Waiting for indexing to complete (10 seconds)...")
        time.sleep(10)
        
        # Step 5: Test search
        self.test_search()
        
        # Step 6: Save config
        if not self.save_configuration():
            return False
        
        # Show next steps
        self.show_next_steps()
        
        return True

def main():
    setup = SearchSetup()
    success = setup.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
