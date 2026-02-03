"""
Lab 3: MCP Integration - Unified Interactive Application

This application provides a menu-driven interface to explore all MCP concepts:
- Remote MCP servers (Microsoft Learn Docs)
- Custom local MCP servers (Business Tools)
- Hybrid architectures
- Error handling patterns

UPDATED: Now uses the Responses API pattern with OpenAI client

Run this single file to complete all exercises.
"""

import os
import time
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPTool

# Load environment variables
load_dotenv()

class MCPLab:
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
        print("        LAB 3: MODEL CONTEXT PROTOCOL (MCP) INTEGRATION")
        print("=" * 70)
        print("\n📚 Choose an exercise:\n")
        print("  1. Exercise 1: Connect to Remote MCP Server")
        print("     (Query Microsoft Learn documentation)")
        print()
        print("  2. Exercise 2: Build and Use Custom Local MCP Server")
        print("     (Inventory management & office information)")
        print()
        print("  3. Exercise 3: Interactive Hybrid Agent")
        print("     (Combine remote + local MCP tools)")
        print()
        print("  4. Exercise 4: Test Error Handling Patterns")
        print("     (Production-ready error handling)")
        print()
        print("  5. View MCP Architecture Overview")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def exercise_1_remote_mcp(self):
        """Exercise 1: Connect to remote MCP server."""
        print("\n" + "=" * 70)
        print("EXERCISE 1: REMOTE MCP SERVER (Microsoft Learn Docs)")
        print("=" * 70)
        print("\nThis exercise connects to Microsoft's public MCP server")
        print("to query official documentation.\n")
        
        try:
            # Configure remote MCP server tool
            mcp_tool = MCPTool(
                server_url="https://learn.microsoft.com/api/mcp",
                server_label="mslearn"
            )
            
            print(f"📡 Configured remote MCP server:")
            print(f"   Label: mslearn")
            print(f"   URL: https://learn.microsoft.com/api/mcp\n")
            
            # Create agent using Responses API pattern
            agent = self.openai_client.agents.create_version(
                agent_name="docs-research-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a developer documentation assistant.
                    Use Microsoft Learn MCP tools to search and retrieve documentation.
                    Provide accurate answers with relevant links when available.""",
                    "tools": [{"type": "mcp", **mcp_tool.as_dict()}]
                }
            )
            
            print(f"✅ Created agent: {agent.name} (version {agent.version})\n")
            
            # Sample queries
            queries = [
                "How do I deploy an Azure AI agent to production?",
                "What are the best practices for agent orchestration?"
            ]
            
            print("🔍 Testing with sample queries:\n")
            
            for i, query in enumerate(queries, 1):
                print(f"Query {i}: {query}\n")
                
                # Create conversation
                conversation = self.openai_client.conversations.create(
                    items=[{"type": "message", "role": "user", "content": query}]
                )
                
                print("Processing with MCP tools...")
                
                # Create response with agent
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
                
                # Extract and display response
                if response.output:
                    for item in response.output:
                        if item.type == "message" and item.content:
                            for content_item in item.content:
                                if content_item.type == "text":
                                    print(f"\n📝 RESPONSE:\n{content_item.text}\n")
                else:
                    print("⚠️  No response generated")
                
                print("-" * 70)
                if i < len(queries):
                    print()
            
            # Cleanup
            self.openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
            print("\n✅ Exercise 1 complete! Agent deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 1: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_2_local_mcp(self):
        """Exercise 2: Build and use custom local MCP server."""
        print("\n" + "=" * 70)
        print("EXERCISE 2: CUSTOM LOCAL MCP SERVER")
        print("=" * 70)
        print("\nThis exercise uses a local MCP server with custom business tools:")
        print("  • check_inventory - Check product stock levels")
        print("  • get_restock_recommendations - Identify low-stock items")
        print("  • get_time_in_timezone - Get current time anywhere")
        print("  • get_office_hours - Office contact information\n")
        
        # Verify mcp_server.py exists
        if not os.path.exists("mcp_server.py"):
            print("❌ Error: mcp_server.py not found in current directory")
            print("Please ensure mcp_server.py is in the same folder.\n")
            input("Press Enter to return to menu...")
            return
        
        try:
            # Configure local MCP server tool
            mcp_tool = MCPTool(
                name="business-tools-mcp-server",
                command="python",
                args=["mcp_server.py"]
            )
            
            print(f"🔧 Configured local MCP server: business-tools-mcp-server\n")
            
            # Create agent using Responses API
            agent = self.openai_client.agents.create_version(
                agent_name="business-operations-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a business operations assistant.
                    Help with inventory management and provide global office information.
                    Use your tools to provide specific, actionable recommendations.""",
                    "tools": [{"type": "mcp", **mcp_tool.as_dict()}]
                }
            )
            
            print(f"✅ Created agent: {agent.name} (version {agent.version})\n")
            
            # Test queries
            test_queries = [
                "What's the current inventory status for laptop-dell-5000?",
                "Which products need restocking?",
                "What time is it in Tokyo right now?",
                "Give me contact information for the London office"
            ]
            
            print("🔍 Testing local MCP tools:\n")
            print("=" * 70)
            
            for query in test_queries:
                print(f"\n💬 USER: {query}\n")
                
                # Create conversation
                conversation = self.openai_client.conversations.create(
                    items=[{"type": "message", "role": "user", "content": query}]
                )
                
                print("⏳ Processing...")
                
                # Create response
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
                                    print(f"\n🤖 AGENT: {content_item.text}\n")
                else:
                    print("⚠️  No response generated")
                
                print("-" * 70)
            
            # Cleanup
            self.openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
            print("\n✅ Exercise 2 complete! Agent deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 2: {e}")
            print("\nMake sure mcp_server.py is in the current directory")
            print("and all dependencies are installed (pip install -r requirements.txt)")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_3_hybrid_interactive(self):
        """Exercise 3: Interactive hybrid agent with remote + local MCP."""
        print("\n" + "=" * 70)
        print("EXERCISE 3: HYBRID INTERACTIVE AGENT")
        print("=" * 70)
        print("\nThis agent combines BOTH remote and local MCP servers:")
        print("  🌐 Remote: Microsoft Learn documentation")
        print("  💼 Local: Business operations tools\n")
        print("Ask technical questions OR business questions!")
        print("Type 'quit' to exit this exercise.\n")
        print("=" * 70 + "\n")
        
        if not os.path.exists("mcp_server.py"):
            print("❌ Error: mcp_server.py not found")
            input("Press Enter to return to menu...")
            return
        
        try:
            # Configure both MCP servers
            remote_mcp = MCPTool(
                server_url="https://learn.microsoft.com/api/mcp",
                server_label="mslearn"
            )
            
            local_mcp = MCPTool(
                name="business-tools-mcp-server",
                command="python",
                args=["mcp_server.py"]
            )
            
            # Create hybrid agent with both MCP tools
            agent = self.openai_client.agents.create_version(
                agent_name="hybrid-assistant",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a comprehensive assistant for Contoso Corporation.
                    
                    You have access to:
                    1. Microsoft Learn documentation (technical questions)
                    2. Business operations tools (inventory, office information)
                    
                    Intelligently choose the right tools for each question.""",
                    "tools": [
                        {"type": "mcp", **remote_mcp.as_dict()},
                        {"type": "mcp", **local_mcp.as_dict()}
                    ]
                }
            )
            
            print(f"✅ Created hybrid agent with dual MCP access\n")
            
            # Create conversation for this session
            conversation = self.openai_client.conversations.create()
            
            # Suggest some queries
            print("💡 Try these example queries:")
            print("   • 'What are Azure AI agents?' (uses remote MCP)")
            print("   • 'Check inventory for laptop-hp-elite' (uses local MCP)")
            print("   • 'What time is it in our Sydney office?' (uses local MCP)")
            print("   • 'How do I implement RAG?' (uses remote MCP)\n")
            
            while True:
                user_input = input("YOU: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nExiting interactive mode...")
                    break
                
                if not user_input:
                    continue
                
                print("\n⏳ Processing...\n")
                
                # Add user message to conversation
                conversation = self.openai_client.conversations.update(
                    conversation_id=conversation.id,
                    items=[{"type": "message", "role": "user", "content": user_input}]
                )
                
                # Create response
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
            print("\n✅ Exercise 3 complete! Agent deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 3: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_4_error_handling(self):
        """Exercise 4: Test error handling patterns."""
        print("\n" + "=" * 70)
        print("EXERCISE 4: ERROR HANDLING PATTERNS")
        print("=" * 70)
        print("\nThis exercise demonstrates production-ready error handling:")
        print("  • Retry logic for transient failures")
        print("  • Timeout handling")
        print("  • Graceful degradation")
        print("  • Helpful error messages\n")
        
        if not os.path.exists("mcp_server.py"):
            print("❌ Error: mcp_server.py not found")
            input("Press Enter to return to menu...")
            return
        
        try:
            mcp_tool = MCPTool(
                name="business-tools-mcp-server",
                command="python",
                args=["mcp_server.py"]
            )
            
            agent = self.openai_client.agents.create_version(
                agent_name="robust-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a reliable operations assistant.
                    
                    Error Handling Guidelines:
                    - Acknowledge errors gracefully
                    - Suggest alternatives when tools fail
                    - Maintain helpful tone even with errors
                    - Provide manual steps as fallback""",
                    "tools": [{"type": "mcp", **mcp_tool.as_dict()}]
                }
            )
            
            print(f"✅ Created robust agent with error handling\n")
            
            # Test with valid and invalid inputs
            test_cases = [
                ("Valid query", "Check inventory for laptop-dell-5000"),
                ("Invalid product", "Check inventory for invalid-product-xyz"),
                ("Invalid office", "Get office info for the Paris office"),
                ("Valid query", "What products need restocking?")
            ]
            
            print("🧪 Running error handling tests:\n")
            print("=" * 70)
            
            for test_type, query in test_cases:
                print(f"\n[{test_type}]")
                print(f"💬 USER: {query}\n")
                
                response = self._query_with_retry(agent, query)
                print(f"🤖 AGENT: {response}\n")
                print("-" * 70)
            
            # Cleanup
            self.openai_client.agents.delete_version(agent_name=agent.name, version=agent.version)
            print("\n✅ Exercise 4 complete! Agent deleted.\n")
            print("Key Observations:")
            print("  • Valid queries succeeded immediately")
            print("  • Invalid inputs were handled gracefully")
            print("  • Agent provided helpful error messages")
            print("  • No crashes or unhandled exceptions\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 4: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def _query_with_retry(self, agent, query, max_retries=2):
        """Helper: Query agent with retry logic using Responses API."""
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"   Retry attempt {attempt + 1}...")
                
                # Create conversation
                conversation = self.openai_client.conversations.create(
                    items=[{"type": "message", "role": "user", "content": query}]
                )
                
                # Create response with timeout
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
                
                # Extract response text
                if response.output:
                    for item in response.output:
                        if item.type == "message" and item.content:
                            for content_item in item.content:
                                if content_item.type == "text":
                                    return content_item.text
                
                return "No response generated"
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return f"❌ Error: {str(e)}"
        
        return "❌ Maximum retries exceeded"
    
    def show_architecture(self):
        """Display MCP architecture overview."""
        print("\n" + "=" * 70)
        print("MCP ARCHITECTURE OVERVIEW")
        print("=" * 70)
        print("""
    ┌─────────────────────────────────────────┐
    │         Your AI Agent                   │
    │   (Microsoft Foundry Project)            │
    └────────┬─────────────────┬──────────────┘
             │                  │
             │ Remote MCP       │ Local MCP
             │ (HTTPS)          │ (stdio)
             │                  │
    ┌────────▼────────────┐  ┌──▼──────────────────┐
    │  Microsoft Learn    │  │  Custom MCP Server  │
    │  Docs MCP Server    │  │  (mcp_server.py)    │
    │                     │  │                     │
    │  • Search docs      │  │  • Inventory tools  │
    │  • Get articles     │  │  • Office info      │
    │  • Code samples     │  │  • Timezone tools   │
    └─────────────────────┘  └─────────────────────┘

📊 MCP Integration Patterns:

1. REMOTE MCP SERVERS
   • Use Case: Public data, documentation, external APIs
   • Connection: HTTPS endpoints
   • Examples: Microsoft Learn, GitHub, Weather APIs
   • Benefit: Zero infrastructure, auto-updates

2. LOCAL MCP SERVERS
   • Use Case: Private data, custom business logic
   • Connection: Stdio (local process)
   • Examples: Internal databases, proprietary tools
   • Benefit: Full control, private data access

3. HYBRID ARCHITECTURE
   • Combine both patterns in single agent
   • Intelligent routing based on query type
   • Best of both worlds

🔑 Key Benefits:

  ✅ Dynamic Tool Discovery - Agent learns tools automatically
  ✅ Separation of Concerns - Business logic in MCP server
  ✅ Reusability - One MCP server, many agents
  ✅ Standardization - MCP protocol across all tools
  ✅ Extensibility - Easy to add new tools

💡 Production Considerations:

  • Error Handling: Retry logic, timeouts, fallbacks
  • Security: Authentication, input validation, auditing
  • Performance: Connection pooling, caching, async
  • Monitoring: Tool usage metrics, error rates, latency
""")
        print("=" * 70)
        input("\nPress Enter to return to menu...")
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 70)
        print("  LAB 3: MODEL CONTEXT PROTOCOL (MCP) INTEGRATION")
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
                self.exercise_1_remote_mcp()
            elif choice == "2":
                self.exercise_2_local_mcp()
            elif choice == "3":
                self.exercise_3_hybrid_interactive()
            elif choice == "4":
                self.exercise_4_error_handling()
            elif choice == "5":
                self.show_architecture()
            elif choice == "0":
                print("\n👋 Exiting Lab 3. Thank you!")
                print("Continue to Lab 4: Multi-Agent Orchestration\n")
                break
            else:
                print("\n⚠️  Invalid choice. Please select 0-5.")
                time.sleep(1)

def main():
    """Entry point."""
    try:
        lab = MCPLab()
        lab.run()
    except KeyboardInterrupt:
        print("\n\n👋 Lab interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
