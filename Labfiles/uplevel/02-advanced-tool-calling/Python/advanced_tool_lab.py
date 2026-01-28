"""
Lab 2: Advanced Tool Calling and Code Interpreter - Unified Interactive Application

This application provides a menu-driven interface to explore advanced agent capabilities:
- Code interpreter for dynamic data analysis
- Advanced async custom functions
- File operations and data transformation

Run this single file to complete all exercises.
The advanced_functions.py and data_processor.py modules are imported as needed.
"""

import os
import time
import asyncio
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import (
    CodeInterpreterTool,
    FilePurpose,
    FunctionTool
)

# Import our custom modules
try:
    from advanced_functions import (
        analyze_customer_segment,
        calculate_forecast,
        process_sales_pipeline,
        get_comprehensive_recommendations
    )
    from data_processor import (
        load_csv_file,
        transform_sales_data,
        export_results
    )
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    print("⚠️  Warning: advanced_functions.py or data_processor.py not found")
    print("   Some exercises will have limited functionality")

# Load environment variables
load_dotenv()

class AdvancedToolLab:
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
        print("     LAB 2: ADVANCED TOOL CALLING AND CODE INTERPRETER")
        print("=" * 70)
        print("\n📚 Choose an exercise:\n")
        print("  1. Exercise 1: Data Analysis with Code Interpreter")
        print("     (Upload CSV, generate visualizations, statistical analysis)")
        print()
        print("  2. Exercise 2: Advanced Async Custom Functions")
        print("     (Customer segmentation, forecasting, pipeline processing)")
        print()
        print("  3. Exercise 3: File Operations and Data Transformation")
        print("     (Load CSV, transform data, export results)")
        print()
        print("  4. Exercise 4: Comprehensive Demo (All Tools Combined)")
        print("     (Interactive agent with all capabilities)")
        print()
        print("  5. View Architecture Overview")
        print()
        print("  0. Exit")
        print("\n" + "=" * 70)
    
    def exercise_1_code_interpreter(self):
        """Exercise 1: Code interpreter for data analysis."""
        print("\n" + "=" * 70)
        print("EXERCISE 1: DATA ANALYSIS WITH CODE INTERPRETER")
        print("=" * 70)
        print("\nThe code interpreter tool allows agents to generate and execute")
        print("Python code dynamically for data analysis and visualization.\n")
        
        # Check if sales_data.csv exists
        csv_file = "../sales_data.csv"
        if not os.path.exists(csv_file):
            print(f"⚠️  Warning: {csv_file} not found")
            print("   Using demo queries without file upload\n")
            csv_file = None
        
        try:
            # Create agent with code interpreter
            code_interpreter = CodeInterpreterTool()
            
            agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="sales-analytics-agent",
                instructions="""You are a sales analytics assistant.
                Use the code interpreter to analyze data, generate visualizations,
                and provide statistical insights.
                
                Always explain your analysis clearly with actionable recommendations.""",
                tools=[code_interpreter]
            )
            
            print(f"✅ Created agent: {agent.name}\n")
            
            # Create thread
            thread = self.agents_client.create_thread()
            
            # Upload file if available
            file_id = None
            if csv_file:
                print(f"📤 Uploading {csv_file}...")
                with open(csv_file, "rb") as f:
                    file = self.agents_client.upload_file(
                        file=f,
                        purpose=FilePurpose.AGENTS
                    )
                    file_id = file.id
                print(f"✅ File uploaded: {file_id}\n")
            
            # Sample queries
            if file_id:
                queries = [
                    f"Analyze the sales data in file {file_id}. What are the key trends?",
                    f"Create a chart showing sales by region from file {file_id}",
                    f"Calculate basic statistics (mean, median, total) from file {file_id}"
                ]
            else:
                queries = [
                    "Generate a sample sales dataset with 5 products and calculate total revenue",
                    "Create a bar chart showing hypothetical sales by quarter",
                    "Demonstrate calculating statistics (mean, median, std dev) on sample data"
                ]
            
            print("🔍 Testing code interpreter with sample queries:\n")
            print("=" * 70)
            
            for i, query in enumerate(queries, 1):
                print(f"\n[Query {i}] {query}\n")
                
                self.agents_client.create_message(
                    thread_id=thread.id,
                    role="user",
                    content=query
                )
                
                print("⏳ Agent generating and executing code...")
                run = self.agents_client.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=agent.id
                )
                
                # Wait for completion
                while run.status in ["queued", "in_progress"]:
                    time.sleep(1)
                    run = self.agents_client.runs.get(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                
                if run.status == "completed":
                    # Get response
                    messages = self.agents_client.messages.list(thread_id=thread.id)
                    for msg in messages:
                        if msg.role == "assistant" and msg.text_messages:
                            response = msg.text_messages[-1].text.value
                            print(f"\n📊 ANALYSIS:\n{response}\n")
                            break
                else:
                    print(f"⚠️  Run status: {run.status}")
                
                print("-" * 70)
                
                if i < len(queries):
                    time.sleep(1)
            
            # Cleanup
            self.agents_client.delete_agent(agent.id)
            print("\n✅ Exercise 1 complete! Agent deleted.\n")
            
            print("💡 Key Takeaways:")
            print("  • Agent generates Python code dynamically")
            print("  • Code is executed in secure sandbox")
            print("  • Can create visualizations and perform complex analysis")
            print("  • No need to pre-define analysis functions\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 1: {e}")
        
        input("\nPress Enter to return to menu...")
    
    def exercise_2_async_functions(self):
        """Exercise 2: Advanced async custom functions."""
        print("\n" + "=" * 70)
        print("EXERCISE 2: ADVANCED ASYNC CUSTOM FUNCTIONS")
        print("=" * 70)
        print("\nThis exercise demonstrates sophisticated function patterns:")
        print("  • Async/await for concurrent operations")
        print("  • Function chaining and composition")
        print("  • Error handling and retries")
        print("  • Structured data processing\n")
        
        if not MODULES_AVAILABLE:
            print("❌ Error: advanced_functions.py not found")
            print("Please ensure advanced_functions.py is in the same directory\n")
            input("Press Enter to return to menu...")
            return
        
        try:
            # Define function tools
            functions = [
                FunctionTool(
                    name="analyze_customer_segment",
                    description="Analyze customer behavior for a specific segment",
                    parameters={
                        "type": "object",
                        "properties": {
                            "segment": {
                                "type": "string",
                                "description": "Customer segment (enterprise, mid-market, small-business)",
                                "enum": ["enterprise", "mid-market", "small-business"]
                            },
                            "time_period": {
                                "type": "string",
                                "description": "Time period (monthly, quarterly, yearly)",
                                "enum": ["monthly", "quarterly", "yearly"]
                            }
                        },
                        "required": ["segment", "time_period"]
                    }
                ),
                FunctionTool(
                    name="calculate_forecast",
                    description="Calculate sales forecast based on historical data",
                    parameters={
                        "type": "object",
                        "properties": {
                            "product_category": {
                                "type": "string",
                                "description": "Product category"
                            },
                            "forecast_months": {
                                "type": "integer",
                                "description": "Number of months to forecast"
                            }
                        },
                        "required": ["product_category", "forecast_months"]
                    }
                ),
                FunctionTool(
                    name="process_sales_pipeline",
                    description="Process and analyze the sales pipeline",
                    parameters={
                        "type": "object",
                        "properties": {
                            "pipeline_stage": {
                                "type": "string",
                                "description": "Pipeline stage to analyze",
                                "enum": ["prospecting", "qualification", "proposal", "negotiation", "closed"]
                            }
                        },
                        "required": ["pipeline_stage"]
                    }
                ),
                FunctionTool(
                    name="get_comprehensive_recommendations",
                    description="Get comprehensive recommendations combining all analyses",
                    parameters={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
            
            # Create agent
            agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="advanced-analytics-agent",
                instructions="""You are an advanced sales analytics assistant.
                Use your functions to provide deep insights and actionable recommendations.
                Always explain your analysis clearly.""",
                tools=functions
            )
            
            print(f"✅ Created agent with {len(functions)} advanced functions\n")
            
            # Create thread
            thread = self.agents_client.create_thread()
            
            # Test queries
            test_queries = [
                "Analyze the enterprise customer segment for quarterly performance",
                "Calculate a 6-month forecast for the software category",
                "What's happening in the proposal stage of our pipeline?",
                "Give me comprehensive recommendations based on all available data"
            ]
            
            print("🔍 Testing async functions:\n")
            print("=" * 70)
            
            for query in test_queries:
                print(f"\n💬 USER: {query}\n")
                
                self.agents_client.create_message(
                    thread_id=thread.id,
                    role="user",
                    content=query
                )
                
                print("⏳ Processing with advanced functions...")
                run = self.agents_client.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=agent.id
                )
                
                # Wait for completion
                while run.status in ["queued", "in_progress", "requires_action"]:
                    time.sleep(1)
                    run = self.agents_client.runs.get(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                    
                    # Handle function calls
                    if run.status == "requires_action":
                        tool_calls = run.required_action.submit_tool_outputs.tool_calls
                        tool_outputs = []
                        
                        for tool_call in tool_calls:
                            function_name = tool_call.function.name
                            arguments = eval(tool_call.function.arguments)
                            
                            print(f"  🔧 Calling: {function_name}")
                            
                            # Call the appropriate function
                            if function_name == "analyze_customer_segment":
                                result = asyncio.run(analyze_customer_segment(
                                    arguments.get("segment"),
                                    arguments.get("time_period")
                                ))
                            elif function_name == "calculate_forecast":
                                result = asyncio.run(calculate_forecast(
                                    arguments.get("product_category"),
                                    arguments.get("forecast_months")
                                ))
                            elif function_name == "process_sales_pipeline":
                                result = asyncio.run(process_sales_pipeline(
                                    arguments.get("pipeline_stage")
                                ))
                            elif function_name == "get_comprehensive_recommendations":
                                result = asyncio.run(get_comprehensive_recommendations())
                            else:
                                result = '{"error": "Unknown function"}'
                            
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": result
                            })
                        
                        # Submit tool outputs
                        run = self.agents_client.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs
                        )
                
                if run.status == "completed":
                    messages = self.agents_client.messages.list(thread_id=thread.id)
                    for msg in messages:
                        if msg.role == "assistant" and msg.text_messages:
                            response = msg.text_messages[-1].text.value
                            print(f"\n🤖 AGENT: {response}\n")
                            break
                else:
                    print(f"⚠️  Run status: {run.status}")
                
                print("-" * 70)
            
            # Cleanup
            self.agents_client.delete_agent(agent.id)
            print("\n✅ Exercise 2 complete! Agent deleted.\n")
            
            print("💡 Key Takeaways:")
            print("  • Async functions enable concurrent operations")
            print("  • Function chaining builds complex workflows")
            print("  • Structured responses improve agent understanding")
            print("  • Error handling ensures reliability\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 2: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_3_file_operations(self):
        """Exercise 3: File operations and data transformation."""
        print("\n" + "=" * 70)
        print("EXERCISE 3: FILE OPERATIONS AND DATA TRANSFORMATION")
        print("=" * 70)
        print("\nThis exercise demonstrates file processing capabilities:")
        print("  • Load and parse CSV files")
        print("  • Transform and aggregate data")
        print("  • Export results in multiple formats")
        print("  • Handle data validation and errors\n")
        
        if not MODULES_AVAILABLE:
            print("❌ Error: data_processor.py not found")
            print("Please ensure data_processor.py is in the same directory\n")
            input("Press Enter to return to menu...")
            return
        
        # Check if sales_data.csv exists
        csv_file = "../sales_data.csv"
        if not os.path.exists(csv_file):
            print(f"⚠️  Warning: {csv_file} not found")
            print("   Exercise will demonstrate with mock data\n")
            csv_file = None
        
        try:
            print("🔍 Testing file operations:\n")
            print("=" * 70)
            
            # Test 1: Load CSV
            print("\n[Test 1] Load CSV File\n")
            if csv_file:
                result = asyncio.run(load_csv_file(csv_file))
                print(f"📂 Loaded {csv_file}")
                print(f"   {result}\n")
            else:
                print("   Skipped (no CSV file available)\n")
            
            # Test 2: Transform data
            print("[Test 2] Transform and Aggregate Sales Data\n")
            result = asyncio.run(transform_sales_data())
            print("📊 Transformation results:")
            print(f"   {result}\n")
            
            # Test 3: Export results
            print("[Test 3] Export Results to JSON\n")
            result = asyncio.run(export_results({"test": "data"}))
            print(f"💾 Export result: {result}\n")
            
            print("-" * 70)
            print("\n✅ Exercise 3 complete!\n")
            
            print("💡 Key Takeaways:")
            print("  • File operations integrate seamlessly with agents")
            print("  • Data transformation enables rich analysis")
            print("  • Multiple export formats support various workflows")
            print("  • Error handling ensures data integrity\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 3: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to return to menu...")
    
    def exercise_4_comprehensive_demo(self):
        """Exercise 4: Interactive demo combining all capabilities."""
        print("\n" + "=" * 70)
        print("EXERCISE 4: COMPREHENSIVE INTERACTIVE DEMO")
        print("=" * 70)
        print("\nThis agent combines ALL capabilities:")
        print("  📊 Code interpreter")
        print("  🔧 Advanced async functions")
        print("  📁 File operations")
        print("\nType 'quit' to exit this exercise.\n")
        print("=" * 70 + "\n")
        
        if not MODULES_AVAILABLE:
            print("⚠️  Warning: Some modules not available")
            print("   Demo will have limited functionality\n")
        
        try:
            # Create comprehensive agent
            tools = [CodeInterpreterTool()]
            
            # Add custom functions if available
            if MODULES_AVAILABLE:
                tools.extend([
                    FunctionTool(
                        name="analyze_customer_segment",
                        description="Analyze customer behavior for a specific segment",
                        parameters={
                            "type": "object",
                            "properties": {
                                "segment": {"type": "string"},
                                "time_period": {"type": "string"}
                            },
                            "required": ["segment", "time_period"]
                        }
                    ),
                    FunctionTool(
                        name="transform_sales_data",
                        description="Transform and aggregate sales data",
                        parameters={"type": "object", "properties": {}, "required": []}
                    )
                ])
            
            agent = self.agents_client.create_agent(
                model=self.model_deployment,
                name="comprehensive-analytics-agent",
                instructions="""You are a comprehensive sales analytics assistant.
                You have access to multiple tools:
                - Code interpreter for dynamic analysis
                - Custom functions for business logic
                - File operations for data processing
                
                Use the most appropriate tool for each request.""",
                tools=tools
            )
            
            print(f"✅ Created comprehensive agent with {len(tools)} tools\n")
            
            thread = self.agents_client.create_thread()
            
            print("💡 Try asking:")
            print("   • 'Generate a sample sales dataset and analyze it'")
            print("   • 'Analyze the enterprise customer segment monthly'")
            print("   • 'Transform our sales data by region'\n")
            
            while True:
                user_input = input("YOU: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nExiting comprehensive demo...")
                    break
                
                if not user_input:
                    continue
                
                self.agents_client.create_message(
                    thread_id=thread.id,
                    role="user",
                    content=user_input
                )
                
                print("\n⏳ Processing...\n")
                run = self.agents_client.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=agent.id
                )
                
                # Wait and handle function calls
                while run.status in ["queued", "in_progress", "requires_action"]:
                    time.sleep(1)
                    run = self.agents_client.runs.get(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                    
                    if run.status == "requires_action" and MODULES_AVAILABLE:
                        tool_calls = run.required_action.submit_tool_outputs.tool_calls
                        tool_outputs = []
                        
                        for tool_call in tool_calls:
                            function_name = tool_call.function.name
                            arguments = eval(tool_call.function.arguments)
                            
                            if function_name == "analyze_customer_segment":
                                result = asyncio.run(analyze_customer_segment(
                                    arguments.get("segment"),
                                    arguments.get("time_period")
                                ))
                            elif function_name == "transform_sales_data":
                                result = asyncio.run(transform_sales_data())
                            else:
                                result = '{"error": "Unknown function"}'
                            
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": result
                            })
                        
                        run = self.agents_client.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs
                        )
                
                if run.status == "completed":
                    messages = self.agents_client.messages.list(thread_id=thread.id)
                    for msg in messages:
                        if msg.role == "assistant" and msg.text_messages:
                            response = msg.text_messages[-1].text.value
                            print(f"AGENT: {response}\n")
                            break
                else:
                    print(f"⚠️  Run status: {run.status}\n")
                
                print("-" * 70 + "\n")
            
            # Cleanup
            self.agents_client.delete_agent(agent.id)
            print("\n✅ Exercise 4 complete! Agent deleted.\n")
            
        except Exception as e:
            print(f"❌ Error in Exercise 4: {e}")
        
        input("\nPress Enter to return to menu...")
    
    def show_architecture(self):
        """Display architecture overview."""
        print("\n" + "=" * 70)
        print("ADVANCED TOOL CALLING ARCHITECTURE")
        print("=" * 70)
        print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                   Your AI Agent                             │
    │         (Microsoft Foundry Project)                          │
    └────────┬────────────────┬────────────────┬──────────────────┘
             │                 │                │
             │                 │                │
    ┌────────▼────────┐ ┌─────▼──────┐ ┌──────▼────────────────┐
    │ Code Interpreter│ │  Custom    │ │  File Operations      │
    │                 │ │  Functions │ │                       │
    │ • Generate code │ │            │ │ • Load CSV            │
    │ • Execute Python│ │ • Async    │ │ • Transform data      │
    │ • Create charts │ │ • Chaining │ │ • Export results      │
    │ • Statistics    │ │ • Error    │ │ • Validation          │
    │                 │ │   handling │ │                       │
    └─────────────────┘ └────────────┘ └───────────────────────┘

📊 Tool Categories:

1. CODE INTERPRETER
   • Dynamic code generation and execution
   • Data analysis and visualization
   • Statistical computations
   • No pre-defined functions needed
   • Sandboxed Python environment

2. CUSTOM ASYNC FUNCTIONS
   • Business logic implementation
   • Concurrent operations (async/await)
   • Function composition and chaining
   • Structured data processing
   • Error handling and retries

3. FILE OPERATIONS
   • CSV/JSON parsing
   • Data transformation pipelines
   • Aggregation and filtering
   • Export in multiple formats
   • Data validation

🔑 Key Patterns:

  ✅ Progressive Enhancement
     Start simple → Add complexity → Combine tools

  ✅ Tool Selection
     Agent chooses appropriate tool for each task

  ✅ Error Resilience
     Graceful degradation with fallbacks

  ✅ Data Flow
     Load → Process → Analyze → Export

💡 Production Considerations:

  • Performance: Cache results, batch operations
  • Security: Validate inputs, limit code execution
  • Monitoring: Track tool usage and latency
  • Testing: Unit test functions, integration test agent
  • Documentation: Clear function descriptions
""")
        print("=" * 70)
        input("\nPress Enter to return to menu...")
    
    def run(self):
        """Main application loop."""
        print("\n" + "=" * 70)
        print("  LAB 2: ADVANCED TOOL CALLING AND CODE INTERPRETER")
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
                self.exercise_1_code_interpreter()
            elif choice == "2":
                self.exercise_2_async_functions()
            elif choice == "3":
                self.exercise_3_file_operations()
            elif choice == "4":
                self.exercise_4_comprehensive_demo()
            elif choice == "5":
                self.show_architecture()
            elif choice == "0":
                print("\n👋 Exiting Lab 2. Great work!")
                print("Continue to Lab 3: MCP Integration\n")
                break
            else:
                print("\n⚠️  Invalid choice. Please select 0-5.")
                time.sleep(1)

def main():
    """Entry point."""
    try:
        lab = AdvancedToolLab()
        lab.run()
    except KeyboardInterrupt:
        print("\n\n👋 Lab interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
