---
lab:
    title: 'Advanced Tool Calling and Code Interpreter'
    description: 'Master advanced agent capabilities with code interpreter, async functions, and data processing.'
---

# Advanced Tool Calling and Code Interpreter

In this exercise, you'll dive deep into advanced agent capabilities by mastering the code interpreter tool for dynamic data analysis, implementing sophisticated async custom functions, and building production-ready file processing workflows. You'll build a Sales Analytics Agent that demonstrates real-world data analysis scenarios.

This exercise takes approximately **60** minutes.

> **Note**: This lab builds on Lab 1. You should have completed Lab 1 or be familiar with basic agent creation and custom functions.

## Learning Objectives

By the end of this exercise, you'll be able to:

1. Use the code interpreter tool for dynamic data analysis and visualization
2. Implement advanced async function patterns with proper error handling
3. Chain multiple functions for complex workflows
4. Process and transform files programmatically
5. Combine code interpreter with custom functions for powerful analytics
6. Apply production-ready patterns (validation, retries, fallbacks)

## Prerequisites

Before starting this exercise, ensure you have:

- Completed Lab 1 (Build AI Agents with Portal and VS Code)
- An Azure AI Foundry project with a deployed model
- Visual Studio Code with Foundry extension installed
- Python 3.12 or later installed
- Familiarity with async/await patterns in Python

## Scenario

You'll build a **Sales Analytics Agent** for Contoso Corporation that helps sales teams analyze data, generate reports, and automate workflows. The agent will:

- Analyze sales data from uploaded CSV files using code interpreter
- Generate visualizations (charts, graphs) dynamically
- Process batch data transformations
- Apply custom business logic with advanced functions
- Handle errors gracefully with retries and fallbacks

---

## Exercise 1: Data Analysis with Code Interpreter

In this exercise, you'll use the code interpreter tool to enable your agent to dynamically generate and execute Python code for data analysis.

### Create the Sales Analytics Agent

1. Open Visual Studio Code and navigate to your lab project folder (or create a new one, e.g., `C:\labs\sales-analytics-agent`).

1. Open this folder in VS Code (**File > Open Folder**).

1. Create a new file named `sales_analytics_agent.py`.

1. Add the following code:

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects.models import CodeInterpreterTool
    
    def main():
        # Initialize the project client
        project_endpoint = os.environ.get("PROJECT_ENDPOINT")
        
        if not project_endpoint:
            print("Error: PROJECT_ENDPOINT environment variable not set")
            print("Please set it in your .env file")
            return
        
        print("Connecting to Azure AI Foundry project...")
        credential = DefaultAzureCredential()
        project_client = AIProjectClient.from_connection_string(
            conn_str=project_endpoint,
            credential=credential
        )
        
        print("Creating Sales Analytics Agent with code interpreter...")
        
        # Create agent with code interpreter tool
        agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="sales-analytics-agent",
            instructions="""You are a Sales Analytics Agent for Contoso Corporation.
            You help sales teams analyze data, generate insights, and create visualizations.
            
            When analyzing data:
            - Always examine the data structure first
            - Provide clear explanations of your findings
            - Create visualizations when appropriate
            - Highlight key trends and anomalies
            - Suggest actionable recommendations
            
            You have access to Python code interpreter for data analysis.""",
            tools=[CodeInterpreterTool()]
        )
        
        print(f"✅ Agent created with ID: {agent.id}")
        
        # Create a thread for conversation
        thread = project_client.agents.create_thread()
        print(f"✅ Thread created with ID: {thread.id}\n")
        
        # Interactive chat loop
        print("="*70)
        print("Sales Analytics Agent Ready!")
        print("Upload data files and ask analysis questions.")
        print("Type 'exit' to quit.")
        print("="*70 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using Sales Analytics Agent!")
                break
            
            if not user_input:
                continue
            
            # Add user message to thread
            project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run the agent
            print("\n🔄 Analyzing...")
            run = project_client.agents.create_run(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            # Wait for completion
            import time
            while run.status in ["queued", "in_progress"]:
                time.sleep(1)
                run = project_client.agents.get_run(
                    thread_id=thread.id,
                    run_id=run.id
                )
            
            # Check for errors
            if run.status == "failed":
                print(f"❌ Error: {run.last_error}")
                continue
            
            # Get the response
            messages = project_client.agents.list_messages(thread_id=thread.id)
            
            # Display the latest assistant message
            for message in messages:
                if message.role == "assistant":
                    for content in message.content:
                        if hasattr(content, 'text'):
                            print(f"\nAgent: {content.text.value}\n")
                        # Display images if generated
                        elif hasattr(content, 'image_file'):
                            print(f"📊 Chart generated: {content.image_file.file_id}")
                    break
    
    if __name__ == "__main__":
        main()
    ```

### Upload and Analyze Sales Data

1. Download the sample sales data file. Create a new file named `sales_data.csv` in your project folder with the following content:

    ```csv
    Date,Region,Product,Units_Sold,Revenue,Sales_Rep
    2024-01-15,North,Widget A,150,7500,John Smith
    2024-01-15,South,Widget B,200,12000,Jane Doe
    2024-01-15,East,Widget A,175,8750,Bob Johnson
    2024-01-15,West,Widget C,125,8125,Alice Williams
    2024-02-15,North,Widget A,165,8250,John Smith
    2024-02-15,South,Widget B,220,13200,Jane Doe
    2024-02-15,East,Widget A,190,9500,Bob Johnson
    2024-02-15,West,Widget C,140,9100,Alice Williams
    2024-03-15,North,Widget A,180,9000,John Smith
    2024-03-15,South,Widget B,240,14400,Jane Doe
    2024-03-15,East,Widget A,205,10250,Bob Johnson
    2024-03-15,West,Widget C,155,10075,Alice Williams
    ```

1. Set up your environment configuration. Create a `.env` file (if you don't already have one):

    ```
    PROJECT_ENDPOINT=<your_endpoint_from_lab_1>
    ```

1. Run the agent:

    ```bash
    python sales_analytics_agent.py
    ```

1. Upload the CSV file. When prompted, you can use the agent's file upload capability:

    > **Note**: The agent can accept file uploads through the API. For now, you'll ask the agent to analyze data you describe.

1. Try these analysis prompts:

    ```
    Can you analyze the sales trends by region over the three months?
    ```

    ```
    Create a bar chart showing total revenue by product
    ```

    ```
    Which sales representative has the highest average revenue per month?
    ```

    ```
    Are there any concerning trends I should know about?
    ```

1. Observe how the agent:
   - Generates Python code dynamically
   - Analyzes the data structure
   - Creates visualizations
   - Provides insights and recommendations

### Understanding Code Interpreter

The code interpreter tool enables agents to:

- ✅ Write and execute Python code dynamically
- ✅ Process uploaded files (CSV, Excel, JSON, etc.)
- ✅ Perform statistical analysis
- ✅ Generate charts and visualizations
- ✅ Handle data transformations
- ✅ Debug and retry code execution

**Key Benefits**:
- No need to pre-define specific analysis functions
- Agent adapts to any data structure
- Handles edge cases automatically
- Can fix errors and retry

---

## Exercise 2: Advanced Custom Function Patterns

Now you'll implement sophisticated custom functions with async patterns, error handling, and parameter validation.

### Create Advanced Functions Module

1. Create a new file named `advanced_functions.py`:

    ```python
    import asyncio
    from typing import List, Dict, Optional
    from datetime import datetime, timedelta
    import json
    
    # Simulated data store (in production, this would be a database)
    SALES_CACHE = {}
    
    
    async def analyze_customer_segment(
        segment: str,
        time_period: str = "30d",
        metrics: Optional[List[str]] = None
    ) -> dict:
        """
        Analyze customer segment with async data fetching.
        
        Args:
            segment: Customer segment ('enterprise', 'smb', 'consumer')
            time_period: Analysis period ('7d', '30d', '90d')
            metrics: Optional list of metrics to calculate
        
        Returns:
            dict: Analysis results with metrics
        """
        # Validate parameters
        valid_segments = ["enterprise", "smb", "consumer"]
        if segment not in valid_segments:
            return {
                "status": "error",
                "error": f"Invalid segment. Must be one of: {', '.join(valid_segments)}"
            }
        
        valid_periods = ["7d", "30d", "90d"]
        if time_period not in valid_periods:
            return {
                "status": "error",
                "error": f"Invalid period. Must be one of: {', '.join(valid_periods)}"
            }
        
        # Default metrics if none provided
        if metrics is None:
            metrics = ["revenue", "growth", "retention"]
        
        try:
            # Simulate async data fetching
            print(f"  📊 Fetching {segment} data for {time_period}...")
            await asyncio.sleep(0.5)  # Simulate API call
            
            # Simulate data processing
            results = {
                "segment": segment,
                "time_period": time_period,
                "timestamp": datetime.now().isoformat(),
                "metrics": {}
            }
            
            # Calculate requested metrics
            for metric in metrics:
                if metric == "revenue":
                    results["metrics"]["revenue"] = {
                        "total": 125000 + (5000 * len(segment)),
                        "currency": "USD"
                    }
                elif metric == "growth":
                    results["metrics"]["growth"] = {
                        "percentage": 15.5,
                        "trend": "increasing"
                    }
                elif metric == "retention":
                    results["metrics"]["retention"] = {
                        "rate": 0.92,
                        "cohort_size": 450
                    }
            
            results["status"] = "success"
            return results
            
        except Exception as e:
            # Graceful error handling
            return {
                "status": "error",
                "error": str(e),
                "fallback_data": await get_cached_segment_data(segment)
            }
    
    
    async def get_cached_segment_data(segment: str) -> dict:
        """Fallback function to retrieve cached data."""
        await asyncio.sleep(0.1)
        return {
            "cached": True,
            "segment": segment,
            "last_updated": (datetime.now() - timedelta(hours=1)).isoformat()
        }
    
    
    async def calculate_forecast(
        product: str,
        months: int = 3,
        include_confidence: bool = True
    ) -> dict:
        """
        Calculate sales forecast with confidence intervals.
        
        Args:
            product: Product name
            months: Number of months to forecast
            include_confidence: Include confidence intervals
        
        Returns:
            dict: Forecast results
        """
        # Validate parameters
        if months < 1 or months > 12:
            return {
                "status": "error",
                "error": "Months must be between 1 and 12"
            }
        
        try:
            print(f"  🔮 Calculating {months}-month forecast for {product}...")
            await asyncio.sleep(0.3)
            
            # Simulate forecast calculation
            base_value = 10000
            forecast = []
            
            for month in range(1, months + 1):
                prediction = {
                    "month": month,
                    "predicted_units": base_value + (month * 500),
                    "predicted_revenue": (base_value + (month * 500)) * 50
                }
                
                if include_confidence:
                    prediction["confidence_interval"] = {
                        "lower": prediction["predicted_units"] * 0.85,
                        "upper": prediction["predicted_units"] * 1.15
                    }
                
                forecast.append(prediction)
            
            return {
                "status": "success",
                "product": product,
                "forecast": forecast,
                "model": "linear_regression",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    
    async def process_sales_pipeline(data: Dict) -> dict:
        """
        Chain multiple analysis functions together.
        
        Args:
            data: Input data with segments and products
        
        Returns:
            dict: Combined analysis results
        """
        try:
            print("  🔄 Processing sales pipeline...")
            
            # Step 1: Analyze segments (parallel)
            segments = data.get("segments", ["enterprise", "smb"])
            segment_tasks = [
                analyze_customer_segment(seg, "30d")
                for seg in segments
            ]
            segment_results = await asyncio.gather(*segment_tasks)
            
            # Step 2: Calculate forecasts (parallel)
            products = data.get("products", ["Widget A", "Widget B"])
            forecast_tasks = [
                calculate_forecast(prod, 3)
                for prod in products
            ]
            forecast_results = await asyncio.gather(*forecast_tasks)
            
            # Step 3: Combine results
            return {
                "status": "success",
                "pipeline_completed": datetime.now().isoformat(),
                "segment_analysis": segment_results,
                "forecasts": forecast_results,
                "recommendations": generate_recommendations(
                    segment_results,
                    forecast_results
                )
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    
    def generate_recommendations(segments, forecasts) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Check growth trends
        for seg in segments:
            if seg.get("status") == "success":
                metrics = seg.get("metrics", {})
                growth = metrics.get("growth", {})
                if growth.get("percentage", 0) > 10:
                    recommendations.append(
                        f"Strong growth in {seg['segment']} segment - consider expanding"
                    )
        
        # Check forecast trends
        for forecast in forecasts:
            if forecast.get("status") == "success":
                predictions = forecast.get("forecast", [])
                if len(predictions) > 0:
                    last_month = predictions[-1]["predicted_revenue"]
                    if last_month > 600000:
                        recommendations.append(
                            f"High revenue forecast for {forecast['product']} - increase inventory"
                        )
        
        return recommendations if recommendations else ["Continue monitoring trends"]
    
    
    # For testing
    async def test_functions():
        """Test all async functions."""
        print("\n=== Testing Async Functions ===\n")
        
        # Test 1: Segment analysis
        result1 = await analyze_customer_segment("enterprise", "30d")
        print(f"✅ Segment analysis: {result1['status']}")
        
        # Test 2: Forecast
        result2 = await calculate_forecast("Widget A", 3)
        print(f"✅ Forecast: {result2['status']}")
        
        # Test 3: Pipeline
        result3 = await process_sales_pipeline({
            "segments": ["enterprise", "smb"],
            "products": ["Widget A", "Widget B"]
        })
        print(f"✅ Pipeline: {result3['status']}")
        print(f"\nRecommendations:")
        for rec in result3.get("recommendations", []):
            print(f"  • {rec}")
    
    
    if __name__ == "__main__":
        asyncio.run(test_functions())
    ```

### Test Advanced Functions

1. Run the test script to verify all functions work:

    ```bash
    python advanced_functions.py
    ```

1. You should see output like:

    ```
    === Testing Async Functions ===

    📊 Fetching enterprise data for 30d...
    ✅ Segment analysis: success
    🔮 Calculating 3-month forecast for Widget A...
    ✅ Forecast: success
    🔄 Processing sales pipeline...
    📊 Fetching enterprise data for 30d...
    📊 Fetching smb data for 30d...
    🔮 Calculating 3-month forecast for Widget A...
    🔮 Calculating 3-month forecast for Widget B...
    ✅ Pipeline: success

    Recommendations:
      • Strong growth in enterprise segment - consider expanding
      • Strong growth in smb segment - consider expanding
      • High revenue forecast for Widget A - increase inventory
      • High revenue forecast for Widget B - increase inventory
    ```

### Key Advanced Patterns Demonstrated

1. **Async/Await**: Non-blocking operations for better performance
2. **Parameter Validation**: Input checking with clear error messages
3. **Error Handling**: Try-catch with graceful fallbacks
4. **Function Chaining**: Pipeline pattern for complex workflows
5. **Parallel Execution**: Multiple async operations with `gather()`
6. **Type Hints**: Clear function signatures
7. **Fallback Data**: Cached data when live calls fail

---

## Exercise 3: File Operations and Data Transformation

In this exercise, you'll build a comprehensive file processing system that combines code interpreter with custom functions.

### Create Data Processor Module

1. Create a new file named `data_processor.py`:

    ```python
    import csv
    import json
    from typing import List, Dict
    from pathlib import Path
    from datetime import datetime
    
    
    def load_csv_file(file_path: str) -> List[Dict]:
        """
        Load CSV file and return as list of dictionaries.
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            List of dictionaries with CSV data
        """
        try:
            data = []
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            print(f"✅ Loaded {len(data)} rows from {Path(file_path).name}")
            return data
            
        except FileNotFoundError:
            print(f"❌ Error: File not found: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return []
    
    
    def transform_sales_data(data: List[Dict]) -> Dict:
        """
        Transform sales data with aggregations and calculations.
        
        Args:
            data: List of sales records
        
        Returns:
            Transformed data with summaries
        """
        if not data:
            return {"error": "No data to transform"}
        
        try:
            # Initialize aggregators
            by_region = {}
            by_product = {}
            by_rep = {}
            
            # Process each record
            for record in data:
                region = record.get("Region", "Unknown")
                product = record.get("Product", "Unknown")
                rep = record.get("Sales_Rep", "Unknown")
                
                # Convert numeric values
                units = int(record.get("Units_Sold", 0))
                revenue = float(record.get("Revenue", 0))
                
                # Aggregate by region
                if region not in by_region:
                    by_region[region] = {"units": 0, "revenue": 0, "count": 0}
                by_region[region]["units"] += units
                by_region[region]["revenue"] += revenue
                by_region[region]["count"] += 1
                
                # Aggregate by product
                if product not in by_product:
                    by_product[product] = {"units": 0, "revenue": 0, "count": 0}
                by_product[product]["units"] += units
                by_product[product]["revenue"] += revenue
                by_product[product]["count"] += 1
                
                # Aggregate by rep
                if rep not in by_rep:
                    by_rep[rep] = {"units": 0, "revenue": 0, "count": 0}
                by_rep[rep]["units"] += units
                by_rep[rep]["revenue"] += revenue
                by_rep[rep]["count"] += 1
            
            # Calculate averages
            for region_data in by_region.values():
                region_data["avg_revenue"] = region_data["revenue"] / region_data["count"]
            
            return {
                "status": "success",
                "total_records": len(data),
                "by_region": by_region,
                "by_product": by_product,
                "by_sales_rep": by_rep,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    
    def process_multiple_files(file_paths: List[str]) -> Dict:
        """
        Process multiple CSV files and combine results.
        
        Args:
            file_paths: List of paths to CSV files
        
        Returns:
            Combined analysis
        """
        print(f"\n🔄 Processing {len(file_paths)} file(s)...\n")
        
        all_data = []
        file_summaries = []
        
        for file_path in file_paths:
            # Load file
            data = load_csv_file(file_path)
            if data:
                all_data.extend(data)
                
                # Transform individual file
                transformed = transform_sales_data(data)
                file_summaries.append({
                    "file": Path(file_path).name,
                    "records": len(data),
                    "summary": transformed
                })
        
        # Transform combined data
        combined_transform = transform_sales_data(all_data)
        
        return {
            "status": "success",
            "files_processed": len(file_paths),
            "total_records": len(all_data),
            "individual_files": file_summaries,
            "combined_analysis": combined_transform
        }
    
    
    def export_results(data: Dict, output_path: str, format: str = "json") -> bool:
        """
        Export analysis results to file.
        
        Args:
            data: Data to export
            output_path: Output file path
            format: Export format ('json' or 'csv')
        
        Returns:
            Success status
        """
        try:
            if format == "json":
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"✅ Exported to {output_path}")
                return True
                
            elif format == "csv":
                # Export summary as CSV
                with open(output_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Metric", "Value"])
                    
                    if "combined_analysis" in data:
                        writer.writerow(["Total Records", data["total_records"]])
                        writer.writerow(["Files Processed", data["files_processed"]])
                
                print(f"✅ Exported to {output_path}")
                return True
            else:
                print(f"❌ Unsupported format: {format}")
                return False
                
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    
    # For testing
    def main():
        """Test data processing functions."""
        print("\n=== Testing Data Processing ===\n")
        
        # Test with sales_data.csv if it exists
        if Path("sales_data.csv").exists():
            # Test 1: Load and transform
            data = load_csv_file("sales_data.csv")
            if data:
                transformed = transform_sales_data(data)
                print(f"\n📊 Analysis Complete:")
                print(f"  • Total records: {transformed.get('total_records', 0)}")
                print(f"  • Regions: {len(transformed.get('by_region', {}))}")
                print(f"  • Products: {len(transformed.get('by_product', {}))}")
                
                # Test 2: Export results
                export_results(
                    transformed,
                    "analysis_results.json",
                    "json"
                )
        else:
            print("⚠️  sales_data.csv not found. Create it first.")
    
    
    if __name__ == "__main__":
        main()
    ```

### Test File Processing

1. Run the data processor:

    ```bash
    python data_processor.py
    ```

1. You should see output analyzing your sales_data.csv file.

1. Check the generated `analysis_results.json` file to see the structured output.

### Combine Code Interpreter with File Processing

Now you'll integrate everything into a comprehensive analytics workflow.

1. Create a new file named `comprehensive_agent.py` that combines code interpreter with your custom functions:

    ```python
    import os
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects.models import CodeInterpreterTool, FunctionTool
    import asyncio
    import json
    
    # Import your custom functions
    from advanced_functions import (
        analyze_customer_segment,
        calculate_forecast,
        process_sales_pipeline
    )
    from data_processor import (
        load_csv_file,
        transform_sales_data,
        export_results
    )
    
    
    # Function schemas for agent
    functions = [
        FunctionTool(
            name="analyze_customer_segment",
            description="Analyze customer segment with metrics",
            parameters={
                "type": "object",
                "properties": {
                    "segment": {
                        "type": "string",
                        "description": "Customer segment",
                        "enum": ["enterprise", "smb", "consumer"]
                    },
                    "time_period": {
                        "type": "string",
                        "description": "Analysis period",
                        "enum": ["7d", "30d", "90d"],
                        "default": "30d"
                    }
                },
                "required": ["segment"]
            }
        ),
        FunctionTool(
            name="calculate_forecast",
            description="Calculate sales forecast for a product",
            parameters={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name"
                    },
                    "months": {
                        "type": "integer",
                        "description": "Number of months to forecast",
                        "default": 3
                    }
                },
                "required": ["product"]
            }
        )
    ]
    
    
    def main():
        # Initialize project client
        project_endpoint = os.environ.get("PROJECT_ENDPOINT")
        
        if not project_endpoint:
            print("Error: PROJECT_ENDPOINT not set")
            return
        
        print("Creating Comprehensive Analytics Agent...")
        credential = DefaultAzureCredential()
        project_client = AIProjectClient.from_connection_string(
            conn_str=project_endpoint,
            credential=credential
        )
        
        # Create agent with BOTH code interpreter AND custom functions
        agent = project_client.agents.create_agent(
            model="gpt-4o",
            name="comprehensive-analytics-agent",
            instructions="""You are an advanced Sales Analytics Agent.
            
            You have access to:
            1. Code Interpreter - for dynamic data analysis and visualization
            2. Custom Functions - for specific business analytics
            
            Use code interpreter for:
            - Analyzing uploaded files
            - Creating visualizations
            - Statistical analysis
            
            Use custom functions for:
            - Customer segment analysis
            - Sales forecasting with confidence intervals
            
            Always provide clear insights and actionable recommendations.""",
            tools=[CodeInterpreterTool()] + functions
        )
        
        print(f"✅ Agent created with ID: {agent.id}")
        print("✅ Tools: Code Interpreter + 2 Custom Functions\n")
        
        # Create thread
        thread = project_client.agents.create_thread()
        
        # Function map for execution
        function_map = {
            "analyze_customer_segment": lambda **kwargs: asyncio.run(analyze_customer_segment(**kwargs)),
            "calculate_forecast": lambda **kwargs: asyncio.run(calculate_forecast(**kwargs))
        }
        
        # Interactive loop
        print("="*70)
        print("Comprehensive Analytics Agent Ready!")
        print("I can analyze data, create forecasts, and generate insights.")
        print("Type 'exit' to quit.")
        print("="*70 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input:
                continue
            
            # Add message
            project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run agent
            print("\n🔄 Processing...")
            run = project_client.agents.create_run(
                thread_id=thread.id,
                agent_id=agent.id
            )
            
            # Handle function calls and code execution
            while run.status in ["queued", "in_progress", "requires_action"]:
                run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)
                
                if run.status == "requires_action":
                    tool_outputs = []
                    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"  ⚡ Calling: {function_name}")
                        
                        if function_name in function_map:
                            result = function_map[function_name](**function_args)
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(result)
                            })
                    
                    project_client.agents.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                
                import time
                time.sleep(1)
            
            # Get response
            messages = project_client.agents.list_messages(thread_id=thread.id)
            for message in messages:
                if message.role == "assistant":
                    for content in message.content:
                        if hasattr(content, 'text'):
                            print(f"\nAgent: {content.text.value}\n")
                    break
    
    
    if __name__ == "__main__":
        main()
    ```

1. Test the comprehensive agent:

    ```bash
    python comprehensive_agent.py
    ```

1. Try combining code interpreter with custom functions:

    ```
    Analyze the enterprise segment for the last 30 days and create a 3-month forecast for Widget A
    ```

    The agent will call both the custom function AND use code interpreter as needed!

---

## Summary

In this exercise, you:

✅ Mastered code interpreter for dynamic data analysis  
✅ Implemented advanced async function patterns  
✅ Built production-ready error handling and validation  
✅ Created file processing and transformation workflows  
✅ Combined code interpreter with custom functions  
✅ Applied real-world analytics patterns  

You now have the skills to build powerful, production-ready analytics agents!

## Next Steps

Continue your learning journey:

- **Lab 3: MCP Integration** - Extend agents with external tools via Model Context Protocol
- **Lab 4: Multi-Agent Orchestration** - Coordinate multiple specialized agents
- **Lab 5: M365 & Teams Integration** - Deploy to production in Microsoft Teams

### Additional Resources

- [Code Interpreter Documentation](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
- [Azure AI Projects SDK Reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
