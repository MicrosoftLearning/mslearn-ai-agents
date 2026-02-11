"""
Lab 5: M365 & Teams Integration - Unified Interactive Application

This application demonstrates production deployment patterns for AI agents:
1. Foundry IQ for enterprise knowledge
2. Microsoft Teams deployment concepts
3. Microsoft 365 (Graph API) integration

UPDATED: Now uses the Responses API pattern with OpenAI client

Run this single file to explore all production integration patterns.
"""

import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Load environment variables
load_dotenv()

class M365TeamsLab:
    def __init__(self):
        """Initialize the lab with Microsoft Foundry connection."""
        self.project_endpoint = os.getenv("PROJECT_ENDPOINT")
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1")
        
        if not self.project_endpoint:
            print("❌ Error: PROJECT_ENDPOINT not set in .env file")
            print("Please configure .env with your Microsoft Foundry project endpoint")
            exit(1)
        
        print("Connecting to Microsoft Foundry project...")
        self.credential = DefaultAzureCredential()
        self.project_client = None
        self.openai_client = None
        
    def connect(self):
        """Establish connection to Microsoft Foundry using Responses API pattern."""
        try:
            # New pattern: Create AIProjectClient with endpoint
            self.project_client = AIProjectClient(
                credential=self.credential,
                endpoint=self.project_endpoint
            )
            
            # Get the OpenAI client for Responses API
            self.openai_client = self.project_client.get_openai_client()
            
            print("✅ Connected to Microsoft Foundry (Responses API)\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 70)
        print("      LAB 5: M365 & TEAMS INTEGRATION")
        print("=" * 70)
        print("\n📚 Choose a step:\n")
        print("  1. Step 1: Foundry IQ Knowledge Agent")
        print("     (Enterprise knowledge search with AI Search)")
        print()
        print("  2. Step 2: Microsoft Teams Deployment Concepts")
        print("     (Deploy agents to Teams with Teams Toolkit)")
        print()
        print("  3. Step 3: Microsoft 365 (Graph API) Integration")
        print("     (Connect agents to SharePoint, Calendar, Email)")
        print()
        print("  4. Step 4: Production Deployment Demo")
        print("     (Complete enterprise knowledge agent)")
        print()
        print("  5. View Architecture & Deployment Guide")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def step_1_foundry_iq(self):
        """Step 1: Foundry IQ Knowledge Agent."""
        print("\n" + "=" * 70)
        print("STEP 1: FOUNDRY IQ KNOWLEDGE AGENT")
        print("=" * 70)
        print("\nFoundry IQ enables agents to search enterprise knowledge bases")
        print("using Azure AI Search and grounding data.\n")
        
        print("🏗️  Foundry IQ Architecture:")
        print("""
    ┌─────────────────────────────────────────┐
    │        Your AI Agent                    │
    │   (Microsoft Foundry Project)            │
    └────────┬────────────────────────────────┘
             │
             │ Foundry IQ Connection
             ▼
    ┌─────────────────────────────────────────┐
    │      Azure AI Search                    │
    │   (Enterprise Knowledge Base)           │
    │                                         │
    │  • Company documents                    │
    │  • Product documentation                │
    │  • Internal wikis                       │
    │  • SharePoint content                   │
    └─────────────────────────────────────────┘
        """)
        
        print("\n📊 Key Components:\n")
        
        print("1. **Azure AI Search Index**")
        print("   - Stores and indexes your documents")
        print("   - Supports semantic search")
        print("   - Vector embeddings for similarity search")
        print("   - Scales to millions of documents\n")
        
        print("2. **Foundry IQ Connection**")
        print("   - Links AI Search to your agent")
        print("   - Automatic grounding and citations")
        print("   - Security and access control")
        print("   - Query optimization\n")
        
        print("3. **Agent Configuration**")
        print("   ```python")
        print("   # Create agent with Foundry IQ using Responses API")
        print("   agent = openai_client.agents.create_version(")
        print("       agent_name='knowledge-agent',")
        print("       definition={")
        print("           'kind': 'prompt',")
        print("           'model': 'gpt-4.1',")
        print("           'instructions': 'Search and answer from knowledge base',")
        print("           'tools': [")
        print("               {'type': 'azure_ai_search', ...}")
        print("           ]")
        print("       }")
        print("   )")
        print("   ```\n")
        
        print("=" * 70)
        print("DEMONSTRATION: Enterprise Knowledge Agent")
        print("=" * 70 + "\n")
        
        try:
            # Create a knowledge agent using Responses API
            agent = self.openai_client.agents.create_version(
                agent_name="enterprise-knowledge-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are an Enterprise Knowledge Assistant.
                    You help employees find information from company documentation,
                    policies, and procedures.
                    
                    Provide accurate answers based on company knowledge.
                    Always cite sources when available.
                    If information isn't in the knowledge base, say so clearly."""
                }
            )
            
            print(f"✅ Created Knowledge Agent (version {agent.version})\n")
            
            # Simulate knowledge queries
            knowledge_queries = [
                "What is our remote work policy?",
                "How do I submit expense reports?",
                "What are the company's security guidelines for laptops?"
            ]
            
            print("🔍 Testing knowledge queries:\n")
            
            for i, query in enumerate(knowledge_queries, 1):
                print(f"[Query {i}] {query}")
                
                # Create conversation
                conversation = self.openai_client.conversations.create(
                    items=[{"type": "message", "role": "user", "content": query}]
                )
                
                print("   ⏳ Searching knowledge base...")
                
                # Get response
                response = self.openai_client.responses.create(
                    conversation=conversation.id,
                    extra_body={
                        "agent": {
                            "type": "agent_reference",
                            "name": agent.name,
                            "version": agent.version
                        }
                    }
                )
                
                # Display response
                if response.output:
                    for item in response.output:
                        if item.type == "message" and item.content:
                            for content_item in item.content:
                                if content_item.type == "text":
                                    print(f"   ✅ Response: {content_item.text[:100]}...")
                
                print()
            
            # Cleanup
            self.openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
            print("✅ Demonstration complete!\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("💡 Key Takeaways:")
        print("  ✅ Foundry IQ connects agents to Azure AI Search")
        print("  ✅ Automatic grounding and citations")
        print("  ✅ Scales to enterprise knowledge bases")
        print("  ✅ Security through Azure RBAC\n")
        
        print("🔧 Setup Steps (in production):")
        print("  1. Create Azure AI Search resource")
        print("  2. Index your documents (PDFs, Word, web pages)")
        print("  3. Create Foundry IQ connection in AI Foundry portal")
        print("  4. Configure agent with search tool")
        print("  5. Test queries and refine search relevance\n")
        
        input("\nPress Enter to return to menu...")
    
    def step_2_teams_deployment(self):
        """Step 2: Microsoft Teams deployment concepts."""
        print("\n" + "=" * 70)
        print("STEP 2: MICROSOFT TEAMS DEPLOYMENT")
        print("=" * 70)
        print("\nDeploy your AI agents to Microsoft Teams for seamless")
        print("collaboration and enterprise-wide access.\n")
        
        print("🏗️  Teams Agent Architecture:")
        print("""
    ┌─────────────────────────────────────────┐
    │      Microsoft Teams Client             │
    │  (Desktop, Web, Mobile)                 │
    └────────┬────────────────────────────────┘
             │ Secure Channel
             ▼
    ┌─────────────────────────────────────────┐
    │      Teams App (Your Agent)             │
    │                                         │
    │  • Adaptive Cards UI                    │
    │  • Bot conversation                     │
    │  • Message extensions                   │
    └────────┬────────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────────┐
    │   Microsoft Foundry Agent                │
    │   (Backend Logic)                       │
    └─────────────────────────────────────────┘
        """)
        
        print("\n📦 Deployment Components:\n")
        
        print("1. **Teams Toolkit (VS Code Extension)**")
        print("   - Project scaffolding")
        print("   - Local development and debugging")
        print("   - One-click deployment to Azure")
        print("   - App manifest configuration\n")
        
        print("2. **App Manifest (manifest.json)**")
        print("   ```json")
        print("   {")
        print('     "name": { "short": "Knowledge Agent" },')
        print('     "description": { "short": "Enterprise knowledge assistant" },')
        print('     "bots": [{')
        print('       "botId": "${{BOT_ID}}",')
        print('       "scopes": ["personal", "team", "groupchat"]')
        print("     }]")
        print("   }")
        print("   ```\n")
        
        print("3. **Adaptive Cards**")
        print("   Rich, interactive UI components")
        print("   ```json")
        print("   {")
        print('     "type": "AdaptiveCard",')
        print('     "body": [{')
        print('       "type": "TextBlock",')
        print('       "text": "Search Results",')
        print('       "weight": "bolder"')
        print("     }],")
        print('     "actions": [{')
        print('       "type": "Action.Submit",')
        print('       "title": "More Details"')
        print("     }]")
        print("   }")
        print("   ```\n")
        
        print("=" * 70)
        print("DEPLOYMENT WALKTHROUGH")
        print("=" * 70 + "\n")
        
        deployment_steps = [
            ("Install Teams Toolkit", "VS Code extension from marketplace"),
            ("Create Teams App Project", "Use 'New Project' template"),
            ("Configure Bot Registration", "Azure Bot Service setup"),
            ("Connect to AI Agent", "Link Teams bot to Foundry agent"),
            ("Design Adaptive Cards", "Create rich UI responses"),
            ("Test Locally", "Debug in Teams using ngrok tunnel"),
            ("Deploy to Azure", "One-click publish to App Service"),
            ("Publish to Teams", "Submit to Teams Admin Center"),
            ("Users Install App", "Teams App Store distribution")
        ]
        
        print("📋 Deployment Steps:\n")
        for i, (step, description) in enumerate(deployment_steps, 1):
            print(f"   {i}. {step}")
            print(f"      {description}")
            time.sleep(0.3)
        
        print("\n" + "=" * 70 + "\n")
        
        print("💡 Teams Capabilities:\n")
        print("  ✅ **Personal Chat**: 1-on-1 conversations with agent")
        print("  ✅ **Team Channels**: Agent available in team channels")
        print("  ✅ **Message Extensions**: Search and share results")
        print("  ✅ **Tabs**: Embed agent UI in Teams tabs")
        print("  ✅ **Adaptive Cards**: Rich, interactive responses")
        print("  ✅ **SSO**: Single Sign-On with Microsoft 365")
        print("  ✅ **Notifications**: Proactive messages to users\n")
        
        print("🔒 Security & Compliance:\n")
        print("  • Azure AD authentication")
        print("  • Respects Teams data policies")
        print("  • Audit logging built-in")
        print("  • Data residency compliance")
        print("  • Admin controls and policies\n")
        
        print("📊 Example Use Cases:\n")
        print("  • IT Support Bot (submit tickets)")
        print("  • HR Assistant (benefits, policies)")
        print("  • Sales Assistant (CRM queries)")
        print("  • Knowledge Base Search")
        print("  • Approval Workflows\n")
        
        input("\nPress Enter to return to menu...")
    
    def step_3_graph_api_integration(self):
        """Step 3: Microsoft Graph API integration."""
        print("\n" + "=" * 70)
        print("STEP 3: MICROSOFT 365 (GRAPH API) INTEGRATION")
        print("=" * 70)
        print("\nIntegrate agents with Microsoft 365 services using")
        print("Microsoft Graph API.\n")
        
        print("🌐 Microsoft Graph API:")
        print("""
    ┌─────────────────────────────────────────┐
    │        Your AI Agent                    │
    └────────┬────────────────────────────────┘
             │
             │ Microsoft Graph API
             │ (REST API)
             │
    ┌────────▼────────────────────────────────┐
    │      Microsoft 365 Services             │
    │                                         │
    │  ┌──────────┐  ┌──────────┐  ┌──────┐ │
    │  │SharePoint│  │ Outlook  │  │Teams │ │
    │  └──────────┘  └──────────┘  └──────┘ │
    │  ┌──────────┐  ┌──────────┐  ┌──────┐ │
    │  │OneDrive  │  │Calendar  │  │Users │ │
    │  └──────────┘  └──────────┘  └──────┘ │
    └─────────────────────────────────────────┘
        """)
        
        print("\n📊 Common Integrations:\n")
        
        print("1. **SharePoint Search**")
        print("   ```python")
        print("   # Search SharePoint sites and documents")
        print("   @agent_function")
        print("   def search_sharepoint(query: str) -> dict:")
        print("       endpoint = 'https://graph.microsoft.com/v1.0/search/query'")
        print("       headers = {'Authorization': f'Bearer {token}'}")
        print("       body = {")
        print("           'requests': [{")
        print("               'entityTypes': ['driveItem'],")
        print("               'query': {'queryString': query}")
        print("           }]")
        print("       }")
        print("       response = requests.post(endpoint, headers=headers, json=body)")
        print("       return response.json()")
        print("   ```\n")
        
        print("2. **Calendar Operations**")
        print("   ```python")
        print("   # Get user's calendar events")
        print("   @agent_function")
        print("   def get_calendar_events(days: int = 7) -> list:")
        print("       endpoint = 'https://graph.microsoft.com/v1.0/me/events'")
        print("       params = {")
        print("           '$select': 'subject,start,end,organizer',")
        print("           '$top': 10")
        print("       }")
        print("       response = requests.get(endpoint, headers=auth_headers, params=params)")
        print("       return response.json()['value']")
        print("   ```\n")
        
        print("3. **Email Operations**")
        print("   ```python")
        print("   # Send email via Outlook")
        print("   @agent_function")
        print("   def send_email(to: str, subject: str, body: str) -> bool:")
        print("       endpoint = 'https://graph.microsoft.com/v1.0/me/sendMail'")
        print("       message = {")
        print("           'message': {")
        print("               'subject': subject,")
        print("               'body': {'contentType': 'Text', 'content': body},")
        print("               'toRecipients': [{'emailAddress': {'address': to}}]")
        print("           }")
        print("       }")
        print("       response = requests.post(endpoint, headers=auth_headers, json=message)")
        print("       return response.status_code == 202")
        print("   ```\n")
        
        print("4. **User Profile**")
        print("   ```python")
        print("   # Get current user's profile")
        print("   @agent_function")
        print("   def get_user_profile() -> dict:")
        print("       endpoint = 'https://graph.microsoft.com/v1.0/me'")
        print("       response = requests.get(endpoint, headers=auth_headers)")
        print("       return response.json()")
        print("   ```\n")
        
        print("=" * 70)
        print("AUTHENTICATION FLOW")
        print("=" * 70 + "\n")
        
        print("🔐 OAuth 2.0 Authentication:\n")
        print("1. User signs in with Microsoft account")
        print("2. App requests permissions (scopes)")
        print("3. User consents to permissions")
        print("4. App receives access token")
        print("5. Token used for Graph API calls\n")
        
        print("Required Permissions (Scopes):")
        print("  • Calendars.Read - Read user calendars")
        print("  • Mail.Send - Send email on behalf of user")
        print("  • Files.Read.All - Read files in SharePoint/OneDrive")
        print("  • User.Read - Read user profile")
        print("  • Sites.Read.All - Search SharePoint sites\n")
        
        print("💡 Implementation Pattern:\n")
        print("```python")
        print("from azure.identity import DefaultAzureCredential")
        print("from msgraph import GraphServiceClient")
        print()
        print("# Initialize Graph client")
        print("credential = DefaultAzureCredential()")
        print("scopes = ['https://graph.microsoft.com/.default']")
        print("graph_client = GraphServiceClient(credential, scopes)")
        print()
        print("# Use in agent function")
        print("@agent_function")
        print("def search_company_docs(query: str):")
        print("    # Search SharePoint using Graph API")
        print("    results = graph_client.search.query(query)")
        print("    return format_results(results)")
        print("```\n")
        
        print("✅ Benefits of Graph API Integration:")
        print("  • Unified API for all M365 services")
        print("  • Strong authentication and security")
        print("  • Respects user permissions")
        print("  • Rich data access (files, calendar, mail, teams)")
        print("  • Webhooks for real-time events\n")
        
        input("\nPress Enter to return to menu...")
    
    def step_4_production_demo(self):
        """Step 4: Complete production deployment demo."""
        print("\n" + "=" * 70)
        print("STEP 4: PRODUCTION ENTERPRISE AGENT DEMO")
        print("=" * 70)
        print("\nThis demo shows a complete enterprise agent with:")
        print("  • Knowledge base search")
        print("  • M365 integration concepts")
        print("  • Production-ready patterns\n")
        
        print("Type 'quit' to exit this demo.\n")
        print("=" * 70 + "\n")
        
        try:
            # Create enterprise agent using Responses API
            agent = self.openai_client.agents.create_version(
                agent_name="enterprise-assistant",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are an Enterprise Assistant for Contoso Corporation.
                    
                    You help employees with:
                    • Finding company information and policies
                    • Searching documents and SharePoint
                    • Managing calendar and meetings
                    • Email and communication tasks
                    
                    Always be professional, accurate, and helpful.
                    When you don't have information, suggest where users can find it."""
                }
            )
            
            print(f"✅ Created Enterprise Assistant\n")
            
            # Create conversation for this session
            conversation = self.openai_client.conversations.create()
            
            print("💡 Try these queries:")
            print("   • 'Find documents about remote work policy'")
            print("   • 'Check my calendar for tomorrow'")
            print("   • 'How do I submit an IT ticket?'")
            print("   • 'Search for Q4 sales reports'\n")
            
            while True:
                user_input = input("YOU: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nExiting demo...")
                    break
                
                if not user_input:
                    continue
                
                print("\n⏳ Processing...\n")
                
                # Add message to conversation
                conversation = self.openai_client.conversations.update(
                    conversation_id=conversation.id,
                    items=[{"type": "message", "role": "user", "content": user_input}]
                )
                
                # Get response
                response = self.openai_client.responses.create(
                    conversation=conversation.id,
                    extra_body={
                        "agent": {
                            "type": "agent_reference",
                            "name": agent.name,
                            "version": agent.version
                        }
                    }
                )
                
                # Display response
                if response.output:
                    for item in response.output:
                        if item.type == "message" and item.content:
                            for content_item in item.content:
                                if content_item.type == "text":
                                    print(f"AGENT: {content_item.text}\n")
                else:
                    print("⚠️  No response generated\n")
                
                print("-" * 70 + "\n")
            
            # Cleanup
            self.openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
            print("\n✅ Demo complete! Agent deleted.\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def show_architecture(self):
        """Display production architecture and deployment guide."""
        print("\n" + "=" * 70)
        print("PRODUCTION ARCHITECTURE & DEPLOYMENT GUIDE")
        print("=" * 70)
        print("""
    🏗️  COMPLETE PRODUCTION ARCHITECTURE

    ┌──────────────────────────────────────────────────────────┐
    │                    End Users                             │
    │  (Employees via Teams, Web, Mobile)                      │
    └────────┬─────────────────────────────────────────────────┘
             │
             │ Secure Channel (HTTPS)
             ▼
    ┌──────────────────────────────────────────────────────────┐
    │              Microsoft Teams                             │
    │  • Chat Interface                                        │
    │  • Adaptive Cards                                        │
    │  • Message Extensions                                    │
    └────────┬─────────────────────────────────────────────────┘
             │
             │ Bot Framework
             ▼
    ┌──────────────────────────────────────────────────────────┐
    │         Azure Bot Service (App Service)                  │
    │  • Conversation routing                                  │
    │  • Authentication (SSO)                                  │
    │  • Message handling                                      │
    └────────┬─────────────────────────────────────────────────┘
             │
             ├──────────────────┬────────────────────┐
             │                  │                    │
             ▼                  ▼                    ▼
    ┌────────────────┐  ┌──────────────┐  ┌────────────────┐
    │ AI Foundry     │  │ Azure AI     │  │ Microsoft      │
    │ Agent          │  │ Search       │  │ Graph API      │
    │                │  │              │  │                │
    │ • Core logic   │  │ • Knowledge  │  │ • M365 data    │
    │ • Functions    │  │   base       │  │ • SharePoint   │
    │ • Tools        │  │ • Semantic   │  │ • Calendar     │
    └────────────────┘  │   search     │  │ • Mail         │
                        └──────────────┘  └────────────────┘
        """)
        
        print("\n" + "=" * 70)
        print("DEPLOYMENT CHECKLIST")
        print("=" * 70 + "\n")
        
        print("✅ **Phase 1: Development (Weeks 1-2)**")
        print("  □ Create AI Foundry project and agent")
        print("  □ Develop and test agent functions")
        print("  □ Set up Azure AI Search index")
        print("  □ Test locally with Foundry portal")
        print()
        
        print("✅ **Phase 2: Teams Integration (Week 3)**")
        print("  □ Install Teams Toolkit in VS Code")
        print("  □ Create Teams app project")
        print("  □ Configure bot registration")
        print("  □ Design Adaptive Cards")
        print("  □ Test locally in Teams")
        print()
        
        print("✅ **Phase 3: M365 Integration (Week 4)**")
        print("  □ Register app in Azure AD")
        print("  □ Configure Graph API permissions")
        print("  □ Implement authentication flow")
        print("  □ Add SharePoint/Calendar functions")
        print("  □ Test with real M365 data")
        print()
        
        print("✅ **Phase 4: Production Deployment (Week 5)**")
        print("  □ Deploy to Azure App Service")
        print("  □ Configure production settings")
        print("  □ Set up monitoring and logging")
        print("  □ Publish to Teams Admin Center")
        print("  □ Pilot with small user group")
        print()
        
        print("✅ **Phase 5: Rollout (Week 6)**")
        print("  □ Train users on agent capabilities")
        print("  □ Publish to Teams App Store")
        print("  □ Monitor usage and errors")
        print("  □ Gather feedback")
        print("  □ Iterate and improve")
        print()
        
        print("=" * 70)
        print("PRODUCTION BEST PRACTICES")
        print("=" * 70 + "\n")
        
        print("🔒 **Security**")
        print("  • Use managed identities (no connection strings)")
        print("  • Implement least-privilege access")
        print("  • Enable audit logging")
        print("  • Encrypt data at rest and in transit")
        print("  • Regular security reviews\n")
        
        print("📊 **Monitoring**")
        print("  • Application Insights for telemetry")
        print("  • Custom metrics (response time, success rate)")
        print("  • Error tracking and alerting")
        print("  • User feedback collection")
        print("  • Cost monitoring (token usage)\n")
        
        print("⚡ **Performance**")
        print("  • Cache frequent queries")
        print("  • Optimize token usage")
        print("  • Use async operations")
        print("  • Implement rate limiting")
        print("  • Scale based on demand\n")
        
        print("👥 **User Experience**")
        print("  • Clear onboarding messages")
        print("  • Helpful error messages")
        print("  • Typing indicators")
        print("  • Rich Adaptive Cards")
        print("  • Feedback mechanisms\n")
        
        print("🔧 **Operations**")
        print("  • CI/CD pipelines")
        print("  • Automated testing")
        print("  • Blue-green deployments")
        print("  • Rollback procedures")
        print("  • Incident response plan\n")
        
        input("\nPress Enter to return to menu...")
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 70)
        print("  LAB 5: M365 & TEAMS INTEGRATION")
        print("=" * 70)
        print("\nInitializing...")
        
        if not self.connect():
            print("\n❌ Failed to connect to Microsoft Foundry")
            print("Please check your .env configuration and try again.")
            return
        
        while True:
            self.show_menu()
            
            choice = input("\nSelect an option (0-5): ").strip()
            
            if choice == "1":
                self.step_1_foundry_iq()
            elif choice == "2":
                self.step_2_teams_deployment()
            elif choice == "3":
                self.step_3_graph_api_integration()
            elif choice == "4":
                self.step_4_production_demo()
            elif choice == "5":
                self.show_architecture()
            elif choice == "0":
                print("\n👋 Congratulations on completing all labs!")
                print("You're ready to build production AI agents!\n")
                break
            else:
                print("\n⚠️  Invalid choice. Please select 0-5.")

def main():
    """Entry point."""
    try:
        lab = M365TeamsLab()
        lab.run()
    except KeyboardInterrupt:
        print("\n\n👋 Lab interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
