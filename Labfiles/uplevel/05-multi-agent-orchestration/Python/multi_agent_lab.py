"""
Lab 5: Multi-Agent Orchestration - Unified Interactive Application

This application demonstrates the progression of multi-agent coordination:
1. Local multi-agent coordination (agents in same process)
2. Distributed agents with A2A protocol (agents as separate services)
3. Visual orchestration concepts

Run this single file to explore all multi-agent patterns.
"""

import os
import time
import asyncio
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool

# Load environment variables
load_dotenv()

class MultiAgentLab:
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
        
    def connect(self):
        """Establish connection to Microsoft Foundry."""
        try:
            # Create project client
            self.project_client = AIProjectClient(
                credential=self.credential,
                endpoint=self.project_endpoint
            )
            
            # Get OpenAI-compatible client for Responses API
            self.openai_client = self.project_client.get_openai_client()
            
            print("✅ Connected to Microsoft Foundry\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 70)
        print("        LAB 5: MULTI-AGENT ORCHESTRATION")
        print("=" * 70)
        print("\n📚 Choose a step:\n")
        print("  1. Step 1: Local Multi-Agent Coordination")
        print("     (3 specialized agents working together)")
        print()
        print("  2. Step 2: Distributed A2A Communication")
        print("     (Real HTTP-based agent services)")
        print()
        print("  3. Step 3: Interactive Content Creation")
        print("     (User-driven multi-agent pipeline)")
        print()
        print("  4. View Architecture Overview")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def step_1_local_multi_agent(self):
        """Step 1: Local multi-agent coordination."""
        print("\n" + "=" * 70)
        print("STEP 1: LOCAL MULTI-AGENT COORDINATION")
        print("=" * 70)
        print("\nIn this exercise, you'll create a content creation pipeline")
        print("with 3 specialized agents coordinated by a main agent.\n")
        print("Agents:")
        print("  🔍 Research Agent - Gathers information on topics")
        print("  📋 Outline Agent - Creates structured outlines")
        print("  ✍️  Writer Agent - Generates final content\n")
        
        try:
            # Create specialized agents
            print("Creating specialized agents...\n")
            
            # Research Agent
            research_agent = self.openai_client.agents.create_version(
                agent_name="research-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a Research Agent specializing in gathering information.
                Your role:
                - Research topics thoroughly
                - Identify key points and facts
                - Cite sources when possible
                - Provide structured research data
                
                Return your research as a bulleted list of key findings."""
                }
            )
            print(f"✅ Created Research Agent (v{research_agent.version})")
            
            # Outline Agent
            outline_agent = self.openai_client.agents.create_version(
                agent_name="outline-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are an Outline Agent specializing in content structure.
                Your role:
                - Take research data and create structured outlines
                - Organize information logically
                - Create clear section headers
                - Ensure logical flow
                
                Return outlines in hierarchical format with numbered sections."""
                }
            )
            print(f"✅ Created Outline Agent (v{outline_agent.version})")
            
            # Writer Agent
            writer_agent = self.openai_client.agents.create_version(
                agent_name="writer-agent",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": """You are a Writer Agent specializing in content creation.
                Your role:
                - Take outlines and expand into full content
                - Write clear, engaging prose
                - Maintain consistent tone
                - Follow the outline structure
                
                Return polished, publication-ready content."""
                }
            )
            print(f"✅ Created Writer Agent (v{writer_agent.version})\n")
            
            # Demonstrate multi-agent workflow
            topic = "The benefits of AI agents in business automation"
            
            print("=" * 70)
            print(f"CONTENT CREATION PIPELINE: '{topic}'")
            print("=" * 70 + "\n")
            
            # Step 1: Research
            print("📍 Step 1: Research Phase")
            print("-" * 70)
            
            # Create conversation for research agent
            research_conversation = self.openai_client.conversations.create(
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": f"Research the following topic and provide 5-7 key findings: {topic}"
                    }
                ]
            )
            
            print("🔍 Research Agent working...")
            
            # Get response from research agent
            research_response = self.openai_client.responses.create(
                conversation=research_conversation.id,
                extra_body={
                    "agent": {
                        "type": "agent_reference",
                        "name": research_agent.name,
                        "version": research_agent.version
                    }
                }
            )
            
            # Extract research results
            research_results = ""
            for item in research_response.output:
                if item.type == "message":
                    for content in item.content:
                        if hasattr(content, 'text'):
                            research_results = content.text
                            break
            
            print(f"\n📊 Research Results:\n{research_results}\n")
            print("-" * 70 + "\n")
            
            # Step 2: Create Outline
            print("📍 Step 2: Outline Phase")
            print("-" * 70)
            
            # Create conversation for outline agent
            outline_conversation = self.openai_client.conversations.create(
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": f"Based on this research, create a structured outline:\n\n{research_results}"
                    }
                ]
            )
            
            print("📋 Outline Agent working...")
            
            # Get response from outline agent
            outline_response = self.openai_client.responses.create(
                conversation=outline_conversation.id,
                extra_body={
                    "agent": {
                        "type": "agent_reference",
                        "name": outline_agent.name,
                        "version": outline_agent.version
                    }
                }
            )
            
            # Extract outline
            outline_results = ""
            for item in outline_response.output:
                if item.type == "message":
                    for content in item.content:
                        if hasattr(content, 'text'):
                            outline_results = content.text
                            break
            
            print(f"\n📝 Outline:\n{outline_results}\n")
            print("-" * 70 + "\n")
            
            # Step 3: Write Content
            print("📍 Step 3: Writing Phase")
            print("-" * 70)
            
            # Create conversation for writer agent
            writer_conversation = self.openai_client.conversations.create(
                items=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": f"Based on this outline, write a complete article (3-4 paragraphs):\n\n{outline_results}"
                    }
                ]
            )
            
            print("✍️  Writer Agent working...")
            
            # Get response from writer agent
            writer_response = self.openai_client.responses.create(
                conversation=writer_conversation.id,
                extra_body={
                    "agent": {
                        "type": "agent_reference",
                        "name": writer_agent.name,
                        "version": writer_agent.version
                    }
                }
            )
            
            # Extract final content
            final_content = ""
            for item in writer_response.output:
                if item.type == "message":
                    for content in item.content:
                        if hasattr(content, 'text'):
                            final_content = content.text
                            break
            
            print(f"\n📄 Final Article:\n{final_content}\n")
            print("=" * 70 + "\n")
            
            print("✅ Multi-Agent Pipeline Complete!\n")
            print("💡 Key Observations:")
            print("  • Each agent specializes in one task")
            print("  • Output from one agent feeds the next")
            print("  • Sequential coordination (research → outline → write)")
            print("  • All agents run in the same process (local)\n")
            
            # Cleanup - delete agent versions
            print("🗑️  Cleaning up agents...")
            self.openai_client.agents.delete_version(
                agent_name=research_agent.name,
                version=research_agent.version
            )
            self.openai_client.agents.delete_version(
                agent_name=outline_agent.name,
                version=outline_agent.version
            )
            self.openai_client.agents.delete_version(
                agent_name=writer_agent.name,
                version=writer_agent.version
            )
            print("✅ Agents deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Step 1: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def step_2_a2a_protocol(self):
        """Step 2: Real Agent-to-Agent communication with HTTP services."""
        print("\n" + "=" * 70)
        print("STEP 2: DISTRIBUTED AGENT-TO-AGENT (A2A) COMMUNICATION")
        print("=" * 70)
        print("\nIn this step, you'll run agents as separate HTTP services")
        print("and orchestrate them via HTTP requests - true distributed A2A!\n")
        
        print("🏗️  A2A Architecture:")
        print("""
    ┌─────────────────┐     HTTP      ┌─────────────────┐
    │ Coordinator     │ ───────────►  │ Research Agent  │
    │ (This script)   │               │ (Port 5001)     │
    └────────┬────────┘               └─────────────────┘
             │                 
             │ HTTP            ┌─────────────────┐
             └─────────────►   │ Writer Agent    │
                               │ (Port 5002)     │
                               └─────────────────┘
        """)
        
        print("\n📋 Setup Instructions:\n")
        print("Before running this demo, you need to start the agent services:")
        print()
        print("1. Open a NEW terminal and run:")
        print("   python research_service.py")
        print()
        print("2. Open ANOTHER terminal and run:")
        print("   python writer_service.py")
        print()
        print("3. Come back here and press Enter to continue")
        print()
        
        input("Press Enter when both services are running...")
        
        # Check if services are running
        import requests
        
        print("\n🔍 Checking agent services...")
        
        services_ready = True
        
        # Check research agent
        try:
            response = requests.get("http://localhost:5001/health", timeout=2)
            if response.status_code == 200:
                print("   ✅ Research Agent (port 5001) - Ready")
            else:
                print("   ❌ Research Agent (port 5001) - Not responding")
                services_ready = False
        except:
            print("   ❌ Research Agent (port 5001) - Not running")
            print("      Run: python research_service.py")
            services_ready = False
        
        # Check writer agent
        try:
            response = requests.get("http://localhost:5002/health", timeout=2)
            if response.status_code == 200:
                print("   ✅ Writer Agent (port 5002) - Ready")
            else:
                print("   ❌ Writer Agent (port 5002) - Not responding")
                services_ready = False
        except:
            print("   ❌ Writer Agent (port 5002) - Not running")
            print("      Run: python writer_service.py")
            services_ready = False
        
        if not services_ready:
            print("\n⚠️  Agent services not ready. Start them first!")
            input("\nPress Enter to return to menu...")
            return
        
        print("\n✅ All services ready!\n")
        
        # Run A2A workflow
        topic = "The benefits of AI agents in business automation"
        
        print("=" * 70)
        print(f"A2A WORKFLOW: '{topic}'")
        print("=" * 70 + "\n")
        
        # Step 1: Call Research Agent via HTTP
        print("📍 Step 1: Calling Research Agent (HTTP POST)")
        print(f"   → POST http://localhost:5001/invoke")
        
        try:
            response = requests.post(
                "http://localhost:5001/invoke",
                json={"task": f"Research this topic and provide 5-7 key findings: {topic}"},
                timeout=60
            )
            
            if response.status_code == 200:
                research_data = response.json()
                research_results = research_data.get("result", "")
                print(f"   ← Response received ({len(research_results)} chars)")
                print(f"\n📊 Research Results:\n{research_results}\n")
            else:
                print(f"   ❌ Research failed: {response.status_code}")
                input("\nPress Enter to return to menu...")
                return
                
        except Exception as e:
            print(f"   ❌ Error calling research agent: {e}")
            input("\nPress Enter to return to menu...")
            return
        
        print("-" * 70 + "\n")
        
        # Step 2: Call Writer Agent via HTTP
        print("📍 Step 2: Calling Writer Agent (HTTP POST)")
        print(f"   → POST http://localhost:5002/invoke")
        
        try:
            response = requests.post(
                "http://localhost:5002/invoke",
                json={"task": f"Write a 2-3 paragraph article based on this research:\n\n{research_results}"},
                timeout=60
            )
            
            if response.status_code == 200:
                writer_data = response.json()
                final_content = writer_data.get("result", "")
                print(f"   ← Response received ({len(final_content)} chars)")
                print(f"\n📄 Final Article:\n{final_content}\n")
            else:
                print(f"   ❌ Writing failed: {response.status_code}")
                input("\nPress Enter to return to menu...")
                return
                
        except Exception as e:
            print(f"   ❌ Error calling writer agent: {e}")
            input("\nPress Enter to return to menu...")
            return
        
        print("=" * 70 + "\n")
        
        print("✅ A2A Workflow Complete!\n")
        
        print("💡 Key Observations:")
        print("  • Each agent runs as an independent HTTP service")
        print("  • Coordinator orchestrates via HTTP POST requests")
        print("  • Agents can scale independently")
        print("  • Services can run on different machines")
        print("  • True distributed agent architecture!\n")
        
        print("🔐 Production Considerations:")
        print("  • Add authentication (API keys, OAuth)")
        print("  • Use service mesh for resilience")
        print("  • Implement retry logic and timeouts")
        print("  • Monitor all HTTP calls")
        print("  • Deploy to containers (Docker, Kubernetes)\n")
        
        print("📦 Deployment Options:")
        print("  • Azure Container Apps (recommended)")
        print("  • Azure Kubernetes Service (AKS)")
        print("  • Azure App Service")
        print("  • Azure Functions (serverless)\n")
        
        input("\nPress Enter to return to menu...")
    
    def step_3_interactive_demo(self):
        """Step 3: Interactive content creation pipeline."""
        print("\n" + "=" * 70)
        print("STEP 3: INTERACTIVE CONTENT CREATION PIPELINE")
        print("=" * 70)
        print("\nCreate content interactively using coordinated agents.")
        print("You specify the topic, agents collaborate to produce content.\n")
        print("Type 'quit' to exit this exercise.\n")
        print("=" * 70 + "\n")
        
        try:
            # Create the agent team
            print("🔧 Setting up agent team...\n")
            
            research_agent = self.openai_client.agents.create_version(
                agent_name="research-agent-interactive",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": "Research topics and provide key findings in bullet points."
                }
            )
            
            writer_agent = self.openai_client.agents.create_version(
                agent_name="writer-agent-interactive",
                definition={
                    "kind": "prompt",
                    "model": self.model_deployment,
                    "instructions": "Take research data and write clear, engaging content."
                }
            )
            
            print("✅ Agent team ready (Research + Writer)\n")
            print("💡 Suggested topics:")
            print("  • 'Benefits of microservices architecture'")
            print("  • 'Getting started with Kubernetes'")
            print("  • 'AI ethics in healthcare'\n")
            
            while True:
                topic = input("Enter a topic to research and write about (or 'quit'): ").strip()
                
                if topic.lower() in ['quit', 'exit', 'q']:
                    print("\nExiting interactive demo...")
                    break
                
                if not topic:
                    continue
                
                print(f"\n📍 Creating content about: '{topic}'")
                print("=" * 70 + "\n")
                
                # Step 1: Research
                print("🔍 Step 1: Research Agent working...")
                research_conversation = self.openai_client.conversations.create(
                    items=[{
                        "type": "message",
                        "role": "user",
                        "content": f"Research this topic and provide 5 key findings: {topic}"
                    }]
                )
                
                research_response = self.openai_client.responses.create(
                    conversation=research_conversation.id,
                    extra_body={
                        "agent": {
                            "type": "agent_reference",
                            "name": research_agent.name,
                            "version": research_agent.version
                        }
                    }
                )
                
                research_results = ""
                for item in research_response.output:
                    if item.type == "message":
                        for content in item.content:
                            if hasattr(content, 'text'):
                                research_results = content.text
                                break
                
                print(f"   ✓ Research complete\n")
                
                # Step 2: Write
                print("✍️  Step 2: Writer Agent working...")
                writer_conversation = self.openai_client.conversations.create(
                    items=[{
                        "type": "message",
                        "role": "user",
                        "content": f"Write a concise article (2-3 paragraphs) based on this research:\n\n{research_results}"
                    }]
                )
                
                writer_response = self.openai_client.responses.create(
                    conversation=writer_conversation.id,
                    extra_body={
                        "agent": {
                            "type": "agent_reference",
                            "name": writer_agent.name,
                            "version": writer_agent.version
                        }
                    }
                )
                
                final_content = ""
                for item in writer_response.output:
                    if item.type == "message":
                        for content in item.content:
                            if hasattr(content, 'text'):
                                final_content = content.text
                                break
                
                print(f"   ✓ Writing complete\n")
                
                # Display results
                print("=" * 70)
                print("📄 GENERATED CONTENT")
                print("=" * 70)
                print(f"\n{final_content}\n")
                print("=" * 70 + "\n")
            
            # Cleanup
            self.openai_client.agents.delete_version(
                agent_name=research_agent.name,
                version=research_agent.version
            )
            self.openai_client.agents.delete_version(
                agent_name=writer_agent.name,
                version=writer_agent.version
            )
            print("\n✅ Step 3 complete! Agents deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Step 3: {e}")
        
        input("\nPress Enter to return to menu...")
    
    def show_architecture(self):
        """Display multi-agent architecture overview."""
        print("\n" + "=" * 70)
        print("MULTI-AGENT ORCHESTRATION ARCHITECTURE")
        print("=" * 70)
        print("""
    🏗️  ARCHITECTURE EVOLUTION

    1️⃣  LOCAL COORDINATION (Step 1)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ┌─────────────────────────────────────────┐
    │        Single Python Process            │
    │                                         │
    │  ┌────────┐  ┌────────┐  ┌──────────┐ │
    │  │Research│─►│Outline │─►│  Writer  │ │
    │  │ Agent  │  │ Agent  │  │  Agent   │ │
    │  └────────┘  └────────┘  └──────────┘ │
    │                                         │
    │  • Sequential execution                │
    │  • Shared memory                       │
    │  • Simple coordination                 │
    └─────────────────────────────────────────┘
    
    
    2️⃣  DISTRIBUTED A2A (Step 2)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ┌──────────────┐
    │ Coordinator  │
    │   Agent      │
    └──────┬───────┘
           │ HTTP
           ├─────────────────┬─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐  ┌──────▼──────┐
    │  Research   │   │   Outline   │  │   Writer    │
    │   Service   │   │   Service   │  │   Service   │
    │  :5001      │   │  :5002      │  │  :5003      │
    └─────────────┘   └─────────────┘  └─────────────┘
    
    • Independent services
    • HTTP communication
    • Scalable & resilient
    • Polyglot (any language)
    
    
    3️⃣  VISUAL WORKFLOWS (Step 3)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ┌─────────────────────────────────────────┐
    │      Foundry Workflow Designer          │
    │  ┌───────────────────────────────────┐  │
    │  │ [Start]──►[Research]──►[Outline]  │  │
    │  │              │           │         │  │
    │  │              ▼           ▼         │  │
    │  │         [Write]──►[Review]──►[End] │  │
    │  └───────────────────────────────────┘  │
    │                                         │
    │  • Visual design                        │
    │  • Low-code orchestration              │
    │  • Export to code                       │
    └─────────────────────────────────────────┘

""")
        
        print("=" * 70)
        print("COMPARISON MATRIX")
        print("=" * 70)
        print()
        print("│ Pattern    │ Complexity │ Scalability │ Best For              │")
        print("├────────────┼────────────┼─────────────┼───────────────────────┤")
        print("│ Local      │ Low        │ Limited     │ Simple workflows      │")
        print("│ A2A        │ Medium     │ High        │ Production systems    │")
        print("│ Visual     │ Low-Med    │ High        │ Business users        │")
        print()
        
        print("=" * 70)
        print("BEST PRACTICES")
        print("=" * 70)
        print()
        print("🎯 **Agent Design**")
        print("  • Single responsibility per agent")
        print("  • Clear input/output contracts")
        print("  • Stateless when possible")
        print("  • Idempotent operations")
        print()
        print("🔄 **Coordination Patterns**")
        print("  • Sequential: A → B → C")
        print("  • Parallel: A + B → C")
        print("  • Conditional: A → (B or C) → D")
        print("  • Loop: A → B → C → (repeat if needed)")
        print()
        print("🛡️  **Error Handling**")
        print("  • Retry with exponential backoff")
        print("  • Circuit breakers for failing agents")
        print("  • Fallback agents for critical paths")
        print("  • Dead letter queues for failed messages")
        print()
        print("📊 **Monitoring**")
        print("  • Log all agent interactions")
        print("  • Track execution time per agent")
        print("  • Monitor error rates")
        print("  • Alert on workflow failures")
        print()
        print("🔐 **Security**")
        print("  • Authenticate agent-to-agent calls")
        print("  • Encrypt data in transit")
        print("  • Validate all inputs")
        print("  • Audit all operations")
        print()
        
        input("\nPress Enter to return to menu...")
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 70)
        print("  LAB 5: MULTI-AGENT ORCHESTRATION")
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
                self.step_1_local_multi_agent()
            elif choice == "2":
                self.step_2_a2a_protocol()
            elif choice == "3":
                self.step_3_interactive_demo()
            elif choice == "4":
                self.show_architecture()
            elif choice == "0":
                print("\n👋 Exiting Lab 4. Excellent work!")
                print("Continue to Lab 5: M365 & Teams Integration\n")
                break
            else:
                print("\n⚠️  Invalid choice. Please select 0-5.")
                time.sleep(1)

def main():
    """Entry point."""
    try:
        lab = MultiAgentLab()
        lab.run()
    except KeyboardInterrupt:
        print("\n\n👋 Lab interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
