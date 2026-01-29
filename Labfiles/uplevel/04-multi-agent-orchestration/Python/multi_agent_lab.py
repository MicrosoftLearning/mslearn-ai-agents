"""
Lab 4: Multi-Agent Orchestration - Unified Interactive Application

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
        self.model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1")
        
        if not self.project_endpoint:
            print("❌ Error: PROJECT_ENDPOINT not set in .env file")
            print("Please configure .env with your Microsoft Foundry project endpoint")
            exit(1)
        
        print("Connecting to Microsoft Foundry project...")
        self.credential = DefaultAzureCredential()
        self.agents_client = None
        
    def connect(self):
        """Establish connection to Microsoft Foundry."""
        try:
            self.agents_client = AIProjectClient.from_connection_string(
                conn_str=self.project_endpoint,
                credential=self.credential
            )
            print("✅ Connected to Microsoft Foundry\n")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 70)
        print("        LAB 4: MULTI-AGENT ORCHESTRATION")
        print("=" * 70)
        print("\n📚 Choose an exercise:\n")
        print("  1. Exercise 1: Local Multi-Agent Coordination")
        print("     (3 specialized agents + coordinator pattern)")
        print()
        print("  2. Exercise 2: Agent-to-Agent (A2A) Communication")
        print("     (Distributed agents with A2A protocol)")
        print()
        print("  3. Exercise 3: Workflow Orchestration Concepts")
        print("     (Visual workflow patterns and best practices)")
        print()
        print("  4. Exercise 4: Complete Content Pipeline Demo")
        print("     (Interactive multi-agent content creation)")
        print()
        print("  5. View Architecture Overview")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def exercise_1_local_multi_agent(self):
        """Exercise 1: Local multi-agent coordination."""
        print("\n" + "=" * 70)
        print("EXERCISE 1: LOCAL MULTI-AGENT COORDINATION")
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
            research_agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="research-agent",
                instructions="""You are a Research Agent specializing in gathering information.
                Your role:
                - Research topics thoroughly
                - Identify key points and facts
                - Cite sources when possible
                - Provide structured research data
                
                Return your research as a bulleted list of key findings."""
            )
            print(f"✅ Created Research Agent (ID: {research_agent.id})")
            
            # Outline Agent
            outline_agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="outline-agent",
                instructions="""You are an Outline Agent specializing in content structure.
                Your role:
                - Take research data and create structured outlines
                - Organize information logically
                - Create clear section headers
                - Ensure logical flow
                
                Return outlines in hierarchical format with numbered sections."""
            )
            print(f"✅ Created Outline Agent (ID: {outline_agent.id})")
            
            # Writer Agent
            writer_agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="writer-agent",
                instructions="""You are a Writer Agent specializing in content creation.
                Your role:
                - Take outlines and expand into full content
                - Write clear, engaging prose
                - Maintain consistent tone
                - Follow the outline structure
                
                Return polished, publication-ready content."""
            )
            print(f"✅ Created Writer Agent (ID: {writer_agent.id})\n")
            
            # Demonstrate multi-agent workflow
            topic = "The benefits of AI agents in business automation"
            
            print("=" * 70)
            print(f"CONTENT CREATION PIPELINE: '{topic}'")
            print("=" * 70 + "\n")
            
            # Step 1: Research
            print("📍 Step 1: Research Phase")
            print("-" * 70)
            
            research_thread = self.agents_client.create_thread()
            self.agents_client.create_message(
                thread_id=research_thread.id,
                role="user",
                content=f"Research the following topic and provide 5-7 key findings: {topic}"
            )
            
            print("🔍 Research Agent working...")
            research_run = self.agents_client.create_and_process_run(
                thread_id=research_thread.id,
                agent_id=research_agent.id
            )
            
            # Wait for completion
            while research_run.status in ["queued", "in_progress"]:
                time.sleep(1)
                research_run = self.agents_client.runs.get(
                    thread_id=research_thread.id,
                    run_id=research_run.id
                )
            
            # Get research results
            research_results = ""
            messages = self.agents_client.messages.list(thread_id=research_thread.id)
            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    research_results = msg.text_messages[-1].text.value
                    break
            
            print(f"\n📊 Research Results:\n{research_results}\n")
            print("-" * 70 + "\n")
            
            # Step 2: Create Outline
            print("📍 Step 2: Outline Phase")
            print("-" * 70)
            
            outline_thread = self.agents_client.create_thread()
            self.agents_client.create_message(
                thread_id=outline_thread.id,
                role="user",
                content=f"Based on this research, create a structured outline:\n\n{research_results}"
            )
            
            print("📋 Outline Agent working...")
            outline_run = self.agents_client.create_and_process_run(
                thread_id=outline_thread.id,
                agent_id=outline_agent.id
            )
            
            while outline_run.status in ["queued", "in_progress"]:
                time.sleep(1)
                outline_run = self.agents_client.runs.get(
                    thread_id=outline_thread.id,
                    run_id=outline_run.id
                )
            
            # Get outline
            outline_results = ""
            messages = self.agents_client.messages.list(thread_id=outline_thread.id)
            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    outline_results = msg.text_messages[-1].text.value
                    break
            
            print(f"\n📝 Outline:\n{outline_results}\n")
            print("-" * 70 + "\n")
            
            # Step 3: Write Content
            print("📍 Step 3: Writing Phase")
            print("-" * 70)
            
            writer_thread = self.agents_client.create_thread()
            self.agents_client.create_message(
                thread_id=writer_thread.id,
                role="user",
                content=f"Based on this outline, write a complete article (3-4 paragraphs):\n\n{outline_results}"
            )
            
            print("✍️  Writer Agent working...")
            writer_run = self.agents_client.create_and_process_run(
                thread_id=writer_thread.id,
                agent_id=writer_agent.id
            )
            
            while writer_run.status in ["queued", "in_progress"]:
                time.sleep(1)
                writer_run = self.agents_client.runs.get(
                    thread_id=writer_thread.id,
                    run_id=writer_run.id
                )
            
            # Get final content
            final_content = ""
            messages = self.agents_client.messages.list(thread_id=writer_thread.id)
            for msg in messages:
                if msg.role == "assistant" and msg.text_messages:
                    final_content = msg.text_messages[-1].text.value
                    break
            
            print(f"\n📄 Final Article:\n{final_content}\n")
            print("=" * 70 + "\n")
            
            print("✅ Multi-Agent Pipeline Complete!\n")
            print("💡 Key Observations:")
            print("  • Each agent specializes in one task")
            print("  • Output from one agent feeds the next")
            print("  • Sequential coordination (research → outline → write)")
            print("  • All agents run in the same process (local)\n")
            
            # Cleanup
            self.agents_client.delete_agent(research_agent.id)
            self.agents_client.delete_agent(outline_agent.id)
            self.agents_client.delete_agent(writer_agent.id)
            print("🗑️  Agents deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 1: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_2_a2a_protocol(self):
        """Exercise 2: Agent-to-Agent communication concepts."""
        print("\n" + "=" * 70)
        print("EXERCISE 2: AGENT-TO-AGENT (A2A) COMMUNICATION")
        print("=" * 70)
        print("\nThe A2A protocol enables distributed agent communication.")
        print("Agents run as separate services and communicate via HTTP.\n")
        
        print("🏗️  A2A Architecture:")
        print("""
    ┌─────────────────┐     HTTP      ┌─────────────────┐
    │ Coordinator     │ ───────────►  │ Research Agent  │
    │ Agent           │               │ (Service 1)     │
    └────────┬────────┘               └─────────────────┘
             │                 
             │ HTTP            ┌─────────────────┐
             └─────────────►   │ Writer Agent    │
                               │ (Service 2)     │
                               └─────────────────┘
        """)
        
        print("\n📋 A2A Protocol Components:\n")
        
        print("1. **Agent Registration**")
        print("   Each agent registers its capabilities and endpoint")
        print("   ```python")
        print("   agent_info = {")
        print('       "name": "research-agent",')
        print('       "description": "Gathers research on topics",')
        print('       "endpoint": "http://localhost:5001/invoke"')
        print("   }")
        print("   ```\n")
        
        print("2. **Agent Discovery**")
        print("   Coordinator discovers available agents")
        print("   ```python")
        print("   available_agents = registry.list_agents()")
        print("   research_agent = registry.find_agent('research-agent')")
        print("   ```\n")
        
        print("3. **Agent Invocation**")
        print("   HTTP POST to agent endpoint with task")
        print("   ```python")
        print("   response = requests.post(")
        print("       research_agent.endpoint,")
        print("       json={'task': 'Research AI benefits'}")
        print("   )")
        print("   ```\n")
        
        print("4. **Response Handling**")
        print("   Agent returns structured JSON response")
        print("   ```python")
        print("   result = response.json()")
        print("   if result['status'] == 'success':")
        print("       process_data(result['data'])")
        print("   ```\n")
        
        print("=" * 70)
        print("SIMULATION: A2A Communication")
        print("=" * 70 + "\n")
        
        # Simulate A2A workflow
        print("🔄 Simulating distributed agent workflow...\n")
        
        steps = [
            ("Coordinator", "Sending task to Research Agent (HTTP POST)"),
            ("Research Agent", "Processing research request..."),
            ("Research Agent", "Returning results to Coordinator"),
            ("Coordinator", "Sending outline task to Outline Agent"),
            ("Outline Agent", "Creating structured outline..."),
            ("Outline Agent", "Returning outline to Coordinator"),
            ("Coordinator", "Workflow complete!")
        ]
        
        for agent, action in steps:
            print(f"  [{agent}] {action}")
            time.sleep(0.5)
        
        print("\n✅ A2A Workflow Simulation Complete!\n")
        
        print("💡 Key Benefits of A2A:")
        print("  ✅ **Scalability**: Each agent scales independently")
        print("  ✅ **Resilience**: Agent failures don't crash entire system")
        print("  ✅ **Flexibility**: Mix languages and technologies")
        print("  ✅ **Deployment**: Deploy to containers, serverless, etc.")
        print("  ✅ **Security**: Network policies, authentication per service\n")
        
        print("📦 Deployment Options:")
        print("  • Azure Container Apps (recommended)")
        print("  • Azure Kubernetes Service (AKS)")
        print("  • Azure App Service")
        print("  • Azure Functions (serverless)\n")
        
        print("🔐 Security Considerations:")
        print("  • Use managed identities for authentication")
        print("  • Implement API keys or OAuth tokens")
        print("  • Enable network policies (VNet integration)")
        print("  • Monitor and log all agent-to-agent calls\n")
        
        input("\nPress Enter to return to menu...")
    
    def exercise_3_workflow_orchestration(self):
        """Exercise 3: Visual workflow orchestration concepts."""
        print("\n" + "=" * 70)
        print("EXERCISE 3: WORKFLOW ORCHESTRATION CONCEPTS")
        print("=" * 70)
        print("\nWorkflow orchestration provides visual, no-code/low-code")
        print("coordination of multi-agent systems.\n")
        
        print("🎨 Visual Workflow Designer (Microsoft Foundry):")
        print("""
    ┌─────────────────────────────────────────────────────────┐
    │                  Workflow Canvas                        │
    │                                                         │
    │  [Start] ──► [Research] ──► [Outline] ──► [Write]     │
    │                   │             │            │          │
    │                   │             │            ▼          │
    │                   │             │        [Review]       │
    │                   │             │            │          │
    │                   │             │        ┌───┴───┐      │
    │                   │             │        │ Good? │      │
    │                   │             │        └───┬───┘      │
    │                   │             │            │          │
    │                   │             │        Yes │  No      │
    │                   │             │            │   │      │
    │                   │             │            ▼   │      │
    │                   │             │        [Publish]      │
    │                   │             │                │      │
    │                   │             └────────────────┘      │
    │                   │                                     │
    └─────────────────────────────────────────────────────────┘
        """)
        
        print("\n📊 Workflow Components:\n")
        
        print("1. **Triggers**")
        print("   - Manual start")
        print("   - HTTP endpoint")
        print("   - Schedule (cron)")
        print("   - Event-driven (message queue)\n")
        
        print("2. **Agent Steps**")
        print("   - Call local agents")
        print("   - Invoke A2A agents")
        print("   - Execute custom code")
        print("   - External API calls\n")
        
        print("3. **Control Flow**")
        print("   - Sequential execution")
        print("   - Parallel branches")
        print("   - Conditional logic (if/else)")
        print("   - Loops and iterations\n")
        
        print("4. **Error Handling**")
        print("   - Try-catch blocks")
        print("   - Retry policies")
        print("   - Fallback agents")
        print("   - Alert notifications\n")
        
        print("5. **Data Flow**")
        print("   - Pass outputs as inputs")
        print("   - Transform data between steps")
        print("   - Store intermediate results")
        print("   - Aggregate final outputs\n")
        
        print("=" * 70)
        print("CODE VS VISUAL COMPARISON")
        print("=" * 70 + "\n")
        
        print("📝 Code-Based Orchestration:")
        print("```python")
        print("# Sequential coordination")
        print("research = await research_agent.run(topic)")
        print("outline = await outline_agent.run(research)")
        print("content = await writer_agent.run(outline)")
        print("")
        print("# Error handling")
        print("try:")
        print("    result = await process_step()")
        print("except Exception:")
        print("    result = await fallback_step()")
        print("```\n")
        
        print("🎨 Visual Workflow (JSON Export):")
        print("```json")
        print("{")
        print('  "workflow": {')
        print('    "name": "content-pipeline",')
        print('    "steps": [')
        print('      {"id": 1, "type": "agent", "agent": "research"},')
        print('      {"id": 2, "type": "agent", "agent": "outline"},')
        print('      {"id": 3, "type": "agent", "agent": "writer"},')
        print('      {"id": 4, "type": "condition", "check": "quality"},')
        print('      {"id": 5, "type": "agent", "agent": "publish"}')
        print("    ],")
        print('    "error_handling": {')
        print('      "retry": 3,')
        print('      "fallback": "alert-admin"')
        print("    }")
        print("  }")
        print("}")
        print("```\n")
        
        print("💡 When to Use Each Approach:\n")
        
        print("✅ **Use Code** when:")
        print("  • Need fine-grained control")
        print("  • Complex custom logic")
        print("  • Version control is critical")
        print("  • Debugging is frequent\n")
        
        print("✅ **Use Visual Workflows** when:")
        print("  • Non-technical stakeholders involved")
        print("  • Rapid prototyping needed")
        print("  • Standard patterns apply")
        print("  • Visual documentation helps\n")
        
        print("🎯 **Best Practice**: Use both!")
        print("  • Prototype visually")
        print("  • Export to code for customization")
        print("  • Deploy code to production")
        print("  • Keep visual docs updated\n")
        
        input("\nPress Enter to return to menu...")
    
    def exercise_4_interactive_demo(self):
        """Exercise 4: Interactive content creation pipeline."""
        print("\n" + "=" * 70)
        print("EXERCISE 4: INTERACTIVE CONTENT CREATION PIPELINE")
        print("=" * 70)
        print("\nCreate content interactively using coordinated agents.")
        print("You specify the topic, agents collaborate to produce content.\n")
        print("Type 'quit' to exit this exercise.\n")
        print("=" * 70 + "\n")
        
        try:
            # Create the agent team
            print("🔧 Setting up agent team...\n")
            
            research_agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="research-agent",
                instructions="Research topics and provide key findings in bullet points."
            )
            
            writer_agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="writer-agent",
                instructions="Take research data and write clear, engaging content."
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
                research_thread = self.agents_client.create_thread()
                self.agents_client.create_message(
                    thread_id=research_thread.id,
                    role="user",
                    content=f"Research this topic and provide 5 key findings: {topic}"
                )
                
                research_run = self.agents_client.create_and_process_run(
                    thread_id=research_thread.id,
                    agent_id=research_agent.id
                )
                
                while research_run.status in ["queued", "in_progress"]:
                    time.sleep(1)
                    research_run = self.agents_client.runs.get(
                        thread_id=research_thread.id,
                        run_id=research_run.id
                    )
                
                research_results = ""
                messages = self.agents_client.messages.list(thread_id=research_thread.id)
                for msg in messages:
                    if msg.role == "assistant" and msg.text_messages:
                        research_results = msg.text_messages[-1].text.value
                        break
                
                print(f"   ✓ Research complete\n")
                
                # Step 2: Write
                print("✍️  Step 2: Writer Agent working...")
                writer_thread = self.agents_client.create_thread()
                self.agents_client.create_message(
                    thread_id=writer_thread.id,
                    role="user",
                    content=f"Write a concise article (2-3 paragraphs) based on this research:\n\n{research_results}"
                )
                
                writer_run = self.agents_client.create_and_process_run(
                    thread_id=writer_thread.id,
                    agent_id=writer_agent.id
                )
                
                while writer_run.status in ["queued", "in_progress"]:
                    time.sleep(1)
                    writer_run = self.agents_client.runs.get(
                        thread_id=writer_thread.id,
                        run_id=writer_run.id
                    )
                
                final_content = ""
                messages = self.agents_client.messages.list(thread_id=writer_thread.id)
                for msg in messages:
                    if msg.role == "assistant" and msg.text_messages:
                        final_content = msg.text_messages[-1].text.value
                        break
                
                print(f"   ✓ Writing complete\n")
                
                # Display results
                print("=" * 70)
                print("📄 GENERATED CONTENT")
                print("=" * 70)
                print(f"\n{final_content}\n")
                print("=" * 70 + "\n")
            
            # Cleanup
            self.agents_client.delete_agent(research_agent.id)
            self.agents_client.delete_agent(writer_agent.id)
            print("\n✅ Exercise 4 complete! Agents deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 4: {e}")
        
        input("\nPress Enter to return to menu...")
    
    def show_architecture(self):
        """Display multi-agent architecture overview."""
        print("\n" + "=" * 70)
        print("MULTI-AGENT ORCHESTRATION ARCHITECTURE")
        print("=" * 70)
        print("""
    🏗️  ARCHITECTURE EVOLUTION

    1️⃣  LOCAL COORDINATION (Exercise 1)
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
    
    
    2️⃣  DISTRIBUTED A2A (Exercise 2)
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
    
    
    3️⃣  VISUAL WORKFLOWS (Exercise 3)
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
        print("  LAB 4: MULTI-AGENT ORCHESTRATION")
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
                self.exercise_1_local_multi_agent()
            elif choice == "2":
                self.exercise_2_a2a_protocol()
            elif choice == "3":
                self.exercise_3_workflow_orchestration()
            elif choice == "4":
                self.exercise_4_interactive_demo()
            elif choice == "5":
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
