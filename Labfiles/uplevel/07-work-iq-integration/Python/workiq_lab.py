"""
Lab 7: Work IQ Integration - Workplace Intelligence Agent

This application demonstrates how to build agents that access Microsoft 365 
workplace data using Work IQ (Model Context Protocol server for M365 Copilot).

Scenarios covered:
1. Meeting Prep - Get context for upcoming meetings
2. Project Status - Track project updates from M365 data
3. Action Items - Extract tasks from emails and meetings
4. Combined Intelligence - Use both Work IQ + Foundry IQ
5. Custom Query - Ask your own workplace questions

Run this single file to explore all Work IQ capabilities.
"""

import os
import time
import json
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.mcp import StdioMCPClient

# Load environment variables
load_dotenv()

class WorkIQLab:
    def __init__(self):
        """Initialize the lab with Microsoft Foundry connection."""
        self.project_endpoint = os.getenv("PROJECT_ENDPOINT")
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
        
        if not self.project_endpoint:
            print("❌ Error: PROJECT_ENDPOINT not set in .env file")
            print("Please configure .env with your Microsoft Foundry project endpoint")
            exit(1)
        
        print("Connecting to Microsoft Foundry project...")
        self.credential = DefaultAzureCredential()
        self.project_client = None
        self.openai_client = None
        self.workiq_client = None
        self.agent = None
        
    def validate_workiq_setup(self):
        """Check if Work IQ is installed and accessible."""
        import subprocess
        
        print("\n" + "=" * 70)
        print("VALIDATING WORK IQ SETUP")
        print("=" * 70)
        
        try:
            # Check if workiq command is available
            result = subprocess.run(
                ["workiq", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ Work IQ is installed")
                print(f"   Version: {result.stdout.strip()}\n")
                return True
            else:
                print("❌ Work IQ not found or not working properly")
                print("\nTo install Work IQ:")
                print("   npm install -g @microsoft/workiq")
                print("   workiq accept-eula\n")
                return False
                
        except FileNotFoundError:
            print("❌ Work IQ command not found")
            print("\nTo install Work IQ:")
            print("   npm install -g @microsoft/workiq")
            print("   workiq accept-eula\n")
            return False
        except Exception as e:
            print(f"⚠️  Could not validate Work IQ setup: {e}")
            print("   Continuing anyway - you may encounter errors\n")
            return True
    
    def connect(self):
        """Establish connection to Microsoft Foundry and Work IQ."""
        try:
            # Validate Work IQ first
            if not self.validate_workiq_setup():
                print("⚠️  Warning: Work IQ validation failed, but continuing...")
                print("   Make sure Work IQ is installed and configured.\n")
            
            # Create project client
            self.project_client = AIProjectClient(
                credential=self.credential,
                endpoint=self.project_endpoint
            )
            
            # Get OpenAI-compatible client for Responses API
            self.openai_client = self.project_client.get_openai_client()
            
            # Initialize Work IQ MCP client
            print("Connecting to Work IQ MCP server...")
            self.workiq_client = StdioMCPClient(
                command="npx",
                args=["-y", "@microsoft/workiq", "mcp"]
            )
            
            # Get available tools from Work IQ
            print("✅ Connected to Microsoft Foundry and Work IQ MCP\n")
            
            # Create a single agent with Work IQ tools
            self._create_workplace_agent()
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\nTroubleshooting:")
            print("  1. Ensure Work IQ is installed: npm install -g @microsoft/workiq")
            print("  2. Accept EULA: workiq accept-eula")
            print("  3. Ensure you have M365 Copilot license and admin consent")
            print("  4. Test with: workiq ask -q 'What meetings do I have today?'")
            return False
    
    def _create_workplace_agent(self):
        """Create the workplace intelligence agent with Work IQ tools."""
        try:
            print("Creating workplace intelligence agent...")
            
            # Get Work IQ tools
            workiq_tools = [tool.model_dump() for tool in self.workiq_client.tools]
            
            # Create agent using Responses API pattern
            self.agent = self.openai_client.agents.create_version(
                agent_name="workplace-intelligence-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a workplace intelligence assistant with access to Microsoft 365 data through Work IQ.

Your capabilities:
- Search emails, meetings, calendar, Teams messages, and documents
- Provide context for meetings and projects
- Extract action items and tasks
- Summarize communications and decisions

Guidelines:
- Always cite sources with timestamps when available
- Respect user privacy and data sensitivity
- Provide concise, actionable information
- If you can't find information, explain what you searched and suggest alternatives""",
                    "tools": workiq_tools
                }
            )
            
            print(f"✅ Created agent: {self.agent.name} (version {self.agent.version})\n")
            
        except Exception as e:
            print(f"❌ Failed to create agent: {e}")
            raise
    
    def _execute_query(self, query, scenario_name="Query"):
        """Execute a query against the workplace agent."""
        try:
            print(f"\n{'=' * 70}")
            print(f"🔍 {scenario_name}")
            print(f"{'=' * 70}")
            print(f"\nQuery: {query}\n")
            print("Processing with Work IQ tools...")
            
            # Create conversation
            conversation = self.openai_client.conversations.create(
                items=[{"type": "message", "role": "user", "content": query}]
            )
            
            # Create response with agent
            response = self.openai_client.responses.create(
                conversation=conversation.id,
                extra_body={
                    "agent": {
                        "type": "agent_reference",
                        "name": self.agent.name,
                        "version": self.agent.version
                    }
                }
            )
            
            # Extract and display response
            print("\n📋 Response:")
            print("-" * 70)
            
            if response.output:
                for item in response.output:
                    if item.type == "message" and item.content:
                        for content_item in item.content:
                            if content_item.type == "text":
                                print(content_item.text.value)
                                print()
            else:
                print("No response received from agent.")
            
            print("-" * 70)
            
        except Exception as e:
            print(f"\n❌ Error executing query: {e}")
            print("\nPossible issues:")
            print("  - Work IQ MCP server not responding")
            print("  - No M365 Copilot license or admin consent")
            print("  - Agent doesn't have access to requested data")
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 70)
        print("        LAB 7: WORK IQ - WORKPLACE INTELLIGENCE")
        print("=" * 70)
        print("\n📚 Choose a scenario:\n")
        print("  1. Meeting Prep")
        print("     Get context for your next meeting")
        print()
        print("  2. Project Status")
        print("     Check latest updates on a project")
        print()
        print("  3. Action Items")
        print("     Find your open tasks and action items")
        print()
        print("  4. Combined Intelligence")
        print("     Search both workplace data AND knowledge base")
        print()
        print("  5. Custom Query")
        print("     Ask your own workplace question")
        print()
        print("  6. View Work IQ Capabilities")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def scenario_1_meeting_prep(self):
        """Scenario 1: Meeting preparation with context."""
        print("\n" + "=" * 70)
        print("SCENARIO 1: MEETING PREP")
        print("=" * 70)
        print("\nThis scenario helps you prepare for meetings by gathering")
        print("context from emails, previous meetings, and shared documents.\n")
        
        # Get meeting topic from user
        meeting_topic = input("📅 Enter meeting topic or time (e.g., '2pm meeting', 'Q4 Planning'): ").strip()
        
        if not meeting_topic:
            meeting_topic = "my next meeting"
        
        query = f"""Help me prepare for {meeting_topic}. Please:
1. Find the meeting details (time, attendees, agenda)
2. Search for recent emails about this topic
3. Look for previous meetings on this topic
4. Summarize key points and decisions I should know
5. Suggest discussion points or questions

Provide a concise prep summary with sources."""
        
        self._execute_query(query, "Meeting Prep")
    
    def scenario_2_project_status(self):
        """Scenario 2: Project status tracking."""
        print("\n" + "=" * 70)
        print("SCENARIO 2: PROJECT STATUS")
        print("=" * 70)
        print("\nThis scenario tracks project updates by searching across")
        print("emails, Teams chats, meetings, and shared documents.\n")
        
        # Get project name from user
        project_name = input("📊 Enter project name (e.g., 'Project Alpha', 'Website Redesign'): ").strip()
        
        if not project_name:
            project_name = "current projects"
        
        query = f"""Give me a status update on {project_name}. Please:
1. Search recent emails and Teams messages about this project
2. Find related meetings and their outcomes
3. Identify recent decisions and changes
4. List any blockers or issues mentioned
5. Summarize next steps and deadlines

Provide a concise status report with sources and dates."""
        
        self._execute_query(query, "Project Status")
    
    def scenario_3_action_items(self):
        """Scenario 3: Action item extraction."""
        print("\n" + "=" * 70)
        print("SCENARIO 3: ACTION ITEMS")
        print("=" * 70)
        print("\nThis scenario extracts your open tasks and action items")
        print("from meetings, emails, and Teams messages.\n")
        
        # Optional: time filter
        time_filter = input("⏰ Time range (e.g., 'this week', 'last 3 days', or press Enter for 'recent'): ").strip()
        
        if not time_filter:
            time_filter = "the past week"
        
        query = f"""Find my open action items and tasks from {time_filter}. Please:
1. Search meeting notes for assigned action items
2. Look for task-related emails sent to me
3. Check Teams messages where I was mentioned or assigned tasks
4. Identify items with deadlines or due dates
5. Categorize by urgency if possible

Provide a prioritized list with sources, deadlines, and who assigned each item."""
        
        self._execute_query(query, "Action Items")
    
    def scenario_4_combined_intelligence(self):
        """Scenario 4: Work IQ + Foundry IQ combined."""
        print("\n" + "=" * 70)
        print("SCENARIO 4: COMBINED INTELLIGENCE")
        print("=" * 70)
        print("\nThis scenario demonstrates using BOTH Work IQ (workplace signals)")
        print("and Foundry IQ (knowledge base) together for comprehensive context.\n")
        print("⚠️  Note: This requires Foundry IQ search to be configured in your project.\n")
        
        topic = input("🔍 Enter topic to research (workplace + knowledge base): ").strip()
        
        if not topic:
            topic = "our company policies on remote work"
        
        query = f"""Research {topic} using both workplace data and knowledge base. Please:

FROM WORKPLACE DATA (Work IQ):
1. Search recent emails and messages about this topic
2. Find relevant meetings and discussions
3. Identify who has been involved and what was decided

FROM KNOWLEDGE BASE (Foundry IQ):
4. Search official documentation
5. Find policies, guidelines, or procedures

SYNTHESIS:
6. Compare workplace discussions with official documentation
7. Identify any gaps or inconsistencies
8. Provide a comprehensive summary with sources from both

Label each piece of information with its source (workplace or knowledge base)."""
        
        self._execute_query(query, "Combined Intelligence")
    
    def scenario_5_custom_query(self):
        """Scenario 5: User-defined custom query."""
        print("\n" + "=" * 70)
        print("SCENARIO 5: CUSTOM QUERY")
        print("=" * 70)
        print("\nAsk any workplace question! Examples:")
        print("  - What did my manager say about the project?")
        print("  - Find emails about Q4 budget")
        print("  - What did the engineering team discuss yesterday?")
        print("  - Show me shared documents about security policies")
        print("  - Summarize this week's standups\n")
        
        custom_query = input("❓ Your workplace question: ").strip()
        
        if not custom_query:
            print("\n⚠️  No query entered. Returning to menu.")
            return
        
        self._execute_query(custom_query, "Custom Query")
    
    def show_capabilities(self):
        """Display Work IQ capabilities and architecture."""
        print("\n" + "=" * 70)
        print("WORK IQ CAPABILITIES")
        print("=" * 70)
        print("\n🏢 What is Work IQ?")
        print("-" * 70)
        print("Work IQ is Microsoft's contextual intelligence layer for Microsoft 365.")
        print("It provides AI agents with access to workplace data through the")
        print("Model Context Protocol (MCP).\n")
        
        print("📊 Data Sources:")
        print("  ✉️  Emails (Outlook)")
        print("  📅 Calendar and meetings")
        print("  💬 Teams messages and chats")
        print("  📄 OneDrive and SharePoint documents")
        print("  👥 People and organizational data")
        print("  🔔 Notifications and signals\n")
        
        print("🔐 Security & Privacy:")
        print("  ✅ Respects existing M365 permissions")
        print("  ✅ Uses Microsoft Entra ID authentication")
        print("  ✅ Requires M365 Copilot license")
        print("  ✅ Requires admin consent for organizational use")
        print("  ✅ All data access is logged and auditable\n")
        
        print("🔄 Work IQ vs Foundry IQ:")
        print("  Work IQ:    Workplace signals (who said what, when)")
        print("  Foundry IQ: Knowledge base (curated documents, data)")
        print("  Together:   Complete context for decision-making\n")
        
        print("🛠️  MCP Architecture:")
        print("  1. Work IQ runs as MCP server (npx @microsoft/workiq mcp)")
        print("  2. Agent connects via StdioMCPClient")
        print("  3. Agent calls Work IQ tools to query M365")
        print("  4. Work IQ returns data with proper permissions")
        print("  5. Agent synthesizes and presents results\n")
        
        print("💡 Use Cases:")
        print("  - Meeting preparation and context")
        print("  - Project status tracking")
        print("  - Action item extraction")
        print("  - Document discovery and search")
        print("  - Communication summarization")
        print("  - Team activity monitoring")
        print("  - Decision history and rationale\n")
        
        print("=" * 70)
        input("\nPress Enter to return to menu...")
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.agent:
                print("\nCleaning up resources...")
                self.openai_client.agents.delete_version(
                    agent_name=self.agent.name,
                    version=self.agent.version
                )
                print("✅ Agent deleted")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 70)
        print("   LAB 7: WORK IQ - WORKPLACE INTELLIGENCE FOR AI AGENTS")
        print("=" * 70)
        print("\nThis lab demonstrates how to build AI agents that access")
        print("Microsoft 365 workplace data using Work IQ.\n")
        
        # Connect to services
        if not self.connect():
            print("\n❌ Failed to connect. Please check your configuration.")
            return
        
        # Main menu loop
        while True:
            self.show_menu()
            choice = input("\nSelect option (0-6): ").strip()
            
            if choice == "1":
                self.scenario_1_meeting_prep()
            elif choice == "2":
                self.scenario_2_project_status()
            elif choice == "3":
                self.scenario_3_action_items()
            elif choice == "4":
                self.scenario_4_combined_intelligence()
            elif choice == "5":
                self.scenario_5_custom_query()
            elif choice == "6":
                self.show_capabilities()
            elif choice == "0":
                print("\nExiting lab...")
                break
            else:
                print("\n⚠️  Invalid option. Please choose 0-6.")
            
            input("\nPress Enter to continue...")
        
        # Cleanup
        self.cleanup()
        print("\n✅ Lab complete! Thank you for exploring Work IQ.\n")


if __name__ == "__main__":
    lab = WorkIQLab()
    lab.run()
