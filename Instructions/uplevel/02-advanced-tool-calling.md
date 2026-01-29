---
lab:
    title: 'Advanced Tool Calling and Code Interpreter'
    description: 'Master advanced agent capabilities with code interpreter, async functions, and data processing using a unified interactive application.'
---

# Lab 2: Advanced Tool Calling and Code Interpreter

In this lab, you'll master advanced agent capabilities through a unified interactive application. You'll explore the code interpreter tool for dynamic data analysis, implement sophisticated async custom functions, and build production-ready file processing workflows.

This lab takes approximately **60** minutes.

> **Note**: This lab builds on Lab 1. You should have completed Lab 1 or be familiar with basic agent creation and custom functions.

## Learning Objectives

By the end of this lab, you'll be able to:

1. Use the code interpreter tool for dynamic data analysis and visualization
2. Implement advanced async function patterns with proper error handling
3. Chain multiple functions for complex workflows
4. Process and transform files programmatically
5. Combine code interpreter with custom functions for powerful analytics
6. Apply production-ready patterns (validation, retries, fallbacks)

## Prerequisites

Before starting this lab, ensure you have:

- Completed Lab 1 (Build AI Agents with Portal and VS Code)
- An Microsoft Foundry project with a deployed model
- Visual Studio Code with Foundry extension installed
- Python 3.12 or later installed
- Familiarity with async/await patterns in Python

## Scenario

You'll work with a **Sales Analytics Agent** for Contoso Corporation that helps sales teams analyze data, generate reports, and automate workflows. The agent will:

- Analyze sales data from uploaded CSV files using code interpreter
- Generate visualizations (charts, graphs) dynamically
- Process batch data transformations
- Apply custom business logic with advanced functions
- Handle errors gracefully with retries and fallbacks

## Lab Structure

This lab uses a **unified interactive application** (`advanced_tool_lab.py`) that provides a menu-driven interface for all exercises. You'll stay in one application throughout the lab, with each exercise building on the previous one.

```
Menu Options:
1. Exercise 1: Data Analysis with Code Interpreter
2. Exercise 2: Advanced Async Custom Functions
3. Exercise 3: File Operations and Data Transformation
4. Exercise 4: Comprehensive Demo (All Tools Combined)
5. View Architecture Overview
0. Exit
```

---

## Setup

### Task 1: Navigate to the lab directory

1. Open Visual Studio Code.

2. Open the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\uplevel\02-advanced-tool-calling\Python
   ```
   
   Use **File > Open Folder** in VS Code.

### Task 2: Configure environment

1. In the lab folder, locate the provided `.env` and `requirements.txt` files.

1. Open the `.env` file and replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    MODEL_DEPLOYMENT_NAME=gpt-4o
    ```
    
    **To get your project endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

1. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

### Task 3: Verify file structure

Ensure you have these files:
- `advanced_tool_lab.py` - Main unified application ⭐
- `advanced_functions.py` - Custom async functions module
- `data_processor.py` - File processing utilities module
- `requirements.txt`
- `.env` (your configuration)

---

## Exercise 1: Data Analysis with Code Interpreter

In this exercise, you'll explore the code interpreter tool that enables agents to dynamically generate and execute Python code for data analysis.

### What is Code Interpreter?

The code interpreter tool allows agents to:
- Write and execute Python code dynamically
- Process uploaded files (CSV, Excel, JSON, etc.)
- Perform statistical analysis
- Generate charts and visualizations
- Handle data transformations
- Debug and retry code execution

**Key benefit**: No need to pre-define specific analysis functions - the agent adapts to any data structure and query.

### Task 1: Run Exercise 1

1. **Start the unified application**:

    ```powershell
    python advanced_tool_lab.py
    ```

2. **Select option 1** from the menu: "Exercise 1: Data Analysis with Code Interpreter"

### Task 2: Observe code interpreter in action

The application will demonstrate code interpreter with three sample queries:

1. **Analyze key trends** - Agent examines sales data and identifies patterns
2. **Create visualizations** - Agent generates charts showing sales by region
3. **Calculate statistics** - Agent computes mean, median, and totals

**What you'll see:**

```
✅ Created agent: sales-analytics-agent

📤 Uploading ../sales_data.csv...
✅ File uploaded: file-abc123

🔍 Testing code interpreter with sample queries:

[Query 1] Analyze the sales data in file file-abc123. What are the key trends?

⏳ Agent generating and executing code...

📊 ANALYSIS:
I've analyzed your sales data. Here are the key findings:

1. Revenue Trends: Total revenue is $145,320 with steady growth...
2. Regional Performance: North region leads with 35% of sales...
3. Product Mix: Software products account for 60% of revenue...

Recommendations:
- Focus on North region expansion
- Increase software product inventory
- Address declining Midwest performance
```

### Task 3: Understand the architecture

**Code Interpreter Flow:**
```
User Query
    ↓
Agent receives request
    ↓
Agent generates Python code
    ↓
Code executes in sandbox
    ↓
Results returned to agent
    ↓
Agent formats response
```

**Agent Configuration** (from `advanced_tool_lab.py`):
```python
code_interpreter = CodeInterpreterTool()

agent = agents_client.create_agent(
    model="gpt-4o",
    name="sales-analytics-agent",
    instructions="Use code interpreter to analyze data...",
    tools=[code_interpreter]  # Enable dynamic code generation
)
```

### Task 4: Key concepts

**Code Interpreter Benefits:**
- ✅ **Dynamic**: Agent generates code based on each query
- ✅ **Flexible**: Works with any data structure
- ✅ **Secure**: Code runs in isolated sandbox
- ✅ **Self-correcting**: Can fix errors and retry
- ✅ **Powerful**: Full Python capabilities (pandas, matplotlib, numpy)

**When to use Code Interpreter:**
- Data analysis with unknown/varying structure
- Statistical computations
- Chart and graph generation
- File format conversions
- Complex calculations

**When to use Custom Functions instead:**
- Specific business logic
- External API calls
- Database operations
- Consistent, repeatable operations

---

## Exercise 2: Advanced Async Custom Functions

In this exercise, you'll explore sophisticated custom function patterns including async operations, function chaining, and error handling.

### What are Advanced Functions?

While code interpreter is great for dynamic analysis, custom functions provide:
- **Specific business logic** (pricing rules, approval workflows)
- **External integrations** (CRM systems, databases, APIs)
- **Controlled operations** (with validation and permissions)
- **Consistent behavior** (repeatable, testable)

### Task 1: Run Exercise 2

1. If the application isn't running, start it:
   ```powershell
   python advanced_tool_lab.py
   ```

2. **Select option 2** from the menu: "Exercise 2: Advanced Async Custom Functions"

### Task 2: Observe advanced functions

The exercise demonstrates 4 sophisticated functions from `advanced_functions.py`:

| Function | Purpose | Key Pattern |
|----------|---------|-------------|
| `analyze_customer_segment` | Customer behavior analysis | Async/await, validation |
| `calculate_forecast` | Sales forecasting | Data processing, error handling |
| `process_sales_pipeline` | Pipeline analysis | Structured responses |
| `get_comprehensive_recommendations` | Combined insights | Function orchestration |

**Sample interaction:**

```
💬 USER: Analyze the enterprise customer segment for quarterly performance

⏳ Processing with advanced functions...
  🔧 Calling: analyze_customer_segment

🤖 AGENT: Based on the quarterly analysis of our enterprise segment:

Revenue: $1.2M (↑ 15% QoQ)
Customer Count: 45 active accounts
Growth Rate: 15%
Retention: 92%

Key Insights:
- Strong quarter-over-quarter growth driven by upsells
- High retention indicates satisfied customers
- Average deal size increased 12%

Recommendations:
- Focus on expanding successful accounts
- Identify upsell opportunities in stable accounts
```

### Task 3: Understand async patterns

**Why Async?**
```python
# From advanced_functions.py
async def analyze_customer_segment(segment: str, time_period: str) -> str:
    # Simulates concurrent operations (API calls, database queries)
    await asyncio.sleep(0.5)  # Non-blocking wait
    
    # Process data
    results = {
        "segment": segment,
        "metrics": calculate_metrics(segment),
        "insights": generate_insights(segment)
    }
    
    return json.dumps(results, indent=2)
```

**Benefits of Async Functions:**
- ⚡ **Performance**: Handle multiple operations concurrently
- 🔄 **Scalability**: Don't block while waiting for I/O
- 🎯 **Responsiveness**: Agent can process other tasks
- 💪 **Real-world**: Matches production API patterns

### Task 4: Function definition pattern

**How the agent knows about functions** (from `advanced_tool_lab.py`):

```python
functions = [
    FunctionTool(
        name="analyze_customer_segment",
        description="Analyze customer behavior for a specific segment",
        parameters={
            "type": "object",
            "properties": {
                "segment": {
                    "type": "string",
                    "enum": ["enterprise", "mid-market", "small-business"]
                },
                "time_period": {
                    "type": "string",
                    "enum": ["monthly", "quarterly", "yearly"]
                }
            },
            "required": ["segment", "time_period"]
        }
    ),
    # More functions...
]

agent = agents_client.create_agent(
    model="gpt-4o",
    tools=functions  # Agent knows these are available
)
```

**Function Calling Flow:**
```
1. User asks a question
2. Agent determines which function(s) to call
3. Agent extracts parameters from user query
4. Function executes (async)
5. Results returned as JSON
6. Agent synthesizes natural language response
```

### Task 5: Key concepts

**Advanced Function Patterns:**

1. **Parameter Validation**
   ```python
   if segment not in ["enterprise", "mid-market", "small-business"]:
       return {"status": "error", "message": "Invalid segment"}
   ```

2. **Error Handling**
   ```python
   try:
       result = await fetch_data(segment)
   except Exception as e:
       return {"status": "error", "details": str(e)}
   ```

3. **Structured Responses**
   ```python
   return json.dumps({
       "status": "success",
       "data": results,
       "timestamp": datetime.now().isoformat()
   })
   ```

4. **Function Chaining**
   ```python
   segment_data = await analyze_customer_segment(...)
   forecast = await calculate_forecast(segment_data...)
   recommendations = combine_insights(segment_data, forecast)
   ```

---

## Exercise 3: File Operations and Data Transformation

In this exercise, you'll explore file processing capabilities that complement both code interpreter and custom functions.

### What are File Operations?

File operations enable agents to:
- Load and parse CSV/JSON files
- Transform and aggregate data
- Export results in multiple formats
- Handle data validation
- Process batch operations

### Task 1: Run Exercise 3

1. **Select option 3** from the menu: "Exercise 3: File Operations and Data Transformation"

### Task 2: Observe file processing

The exercise demonstrates three operations from `data_processor.py`:

**Test 1: Load CSV File**
```
📂 Loaded ../sales_data.csv
   Successfully loaded 20 rows with 5 columns
   Columns: date, region, product, quantity, revenue
```

**Test 2: Transform and Aggregate**
```
📊 Transformation results:
   By Region: {
       "North": {"count": 7, "total_revenue": 45000},
       "South": {"count": 5, "total_revenue": 32000},
       "East": {"count": 8, "total_revenue": 38000}
   }
   
   By Product: {
       "Software": {"count": 12, "total_revenue": 75000},
       "Hardware": {"count": 8, "total_revenue": 40000}
   }
```

**Test 3: Export Results**
```
💾 Export result: Successfully exported to analysis_results.json
```

### Task 3: Understand file processing patterns

**File Operations in Agent Context:**

```python
# Define file operation as a function tool
file_ops = FunctionTool(
    name="transform_sales_data",
    description="Transform and aggregate sales data by region and product",
    parameters={"type": "object", "properties": {}, "required": []}
)

# Agent can call it during conversation
agent = agents_client.create_agent(
    model="gpt-4o",
    tools=[code_interpreter, *custom_functions, file_ops]
)
```

**When agent calls the function:**
```
User: "Show me sales by region"
  ↓
Agent: Calls transform_sales_data()
  ↓
Function: Loads CSV, aggregates by region, returns JSON
  ↓
Agent: "Here's the breakdown:
        North: $45,000 (35%)
        South: $32,000 (25%)
        East: $38,000 (30%)"
```

### Task 4: File operation patterns

**From `data_processor.py`:**

```python
async def load_csv_file(file_path: str) -> str:
    """
    Patterns demonstrated:
    • Async file I/O
    • Error handling (file not found, parse errors)
    • Data validation
    • Structured error responses
    """
    try:
        data = pd.read_csv(file_path)
        return json.dumps({
            "status": "success",
            "rows": len(data),
            "columns": list(data.columns)
        })
    except FileNotFoundError:
        return json.dumps({
            "status": "error",
            "error": "File not found"
        })
```

### Task 5: Key concepts

**File Operations vs Code Interpreter:**

| Aspect | File Operations Function | Code Interpreter |
|--------|-------------------------|------------------|
| **Control** | Predefined logic | Dynamic code generation |
| **Validation** | Built-in validation | Agent-generated validation |
| **Performance** | Optimized for specific tasks | Flexible but may be slower |
| **Security** | Controlled file access | Sandboxed execution |
| **Use Case** | Consistent, repeatable transformations | Ad-hoc, exploratory analysis |

**Best Practice**: Use both together!
- File operations for structured, validated data loading
- Code interpreter for exploratory analysis on loaded data

---

## Exercise 4: Comprehensive Interactive Demo

In this exercise, you'll interact with an agent that combines ALL the capabilities you've learned.

### Task 1: Run Exercise 4

1. **Select option 4** from the menu: "Exercise 4: Comprehensive Demo"

2. The agent now has access to:
   - 📊 Code interpreter (dynamic analysis)
   - 🔧 Advanced async functions (business logic)
   - 📁 File operations (data processing)

### Task 2: Experiment with combined capabilities

**Try these queries:**

1. **Code interpreter query:**
   ```
   Generate a sample sales dataset and analyze it
   ```

2. **Custom function query:**
   ```
   Analyze the enterprise customer segment monthly
   ```

3. **File operation query:**
   ```
   Transform our sales data by region and product
   ```

4. **Combined query:**
   ```
   Load our sales data, calculate quarterly forecasts for each product category, 
   and create a visualization showing trends
   ```

### Task 3: Observe tool selection

The agent intelligently selects tools based on the query:

```
Query: "Show me sales trends"
  → Uses code interpreter (dynamic visualization)

Query: "Analyze enterprise customers"
  → Uses custom function (specific business logic)

Query: "Export data by region"
  → Uses file operations (structured transformation)
```

### Task 4: Explore agent decision-making

**How does the agent choose?**

The agent considers:
1. **Function descriptions** - Matches query intent to tool purpose
2. **Parameter requirements** - Checks if query provides needed inputs
3. **Tool capabilities** - Selects most appropriate tool for task
4. **Context** - Considers previous messages and results

**Example:**
```
USER: "I need a forecast for software products, next 6 months"

AGENT REASONING:
- Query mentions "forecast" → matches calculate_forecast function
- Query specifies "software" → matches product_category parameter
- Query specifies "6 months" → matches forecast_months parameter
→ Calls: calculate_forecast("software", 6)
```

---

## Exercise 5: Architecture Overview

### Task 1: View architecture

**Select option 5** from the menu to see the complete architecture diagram.

### Comprehensive Architecture

```
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
```

### Tool Decision Matrix

| User Need | Recommended Tool | Why |
|-----------|------------------|-----|
| "Analyze this CSV" | Code Interpreter | Dynamic, exploratory |
| "Calculate quarterly forecast" | Custom Function | Specific business logic |
| "Export data by region" | File Operations | Structured transformation |
| "Create a chart" | Code Interpreter | Visualization generation |
| "Check enterprise segment" | Custom Function | Validated business queries |

### Production Patterns

**Error Handling:**
```python
try:
    result = await function_call()
except ValidationError as e:
    return {"status": "error", "message": "Invalid input"}
except TimeoutError:
    return {"status": "error", "message": "Operation timed out"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"status": "error", "message": "Internal error"}
```

**Performance Optimization:**
```python
# Batch operations
results = await asyncio.gather(
    analyze_segment("enterprise"),
    analyze_segment("mid-market"),
    analyze_segment("small-business")
)

# Caching
if cache_key in CACHE:
    return CACHE[cache_key]
result = await expensive_operation()
CACHE[cache_key] = result
```

**Testing:**
```python
# Unit test functions
async def test_analyze_segment():
    result = await analyze_customer_segment("enterprise", "quarterly")
    assert result["status"] == "success"
    assert "metrics" in result

# Integration test agent
def test_agent_with_functions():
    response = query_agent("Analyze enterprise customers")
    assert "revenue" in response.lower()
```

---

## Summary

Congratulations! You've completed Lab 2 and mastered advanced tool calling patterns.

### What You've Learned

1. **Code Interpreter**
   - Dynamic Python code generation
   - Data analysis and visualization
   - Adaptive to any data structure

2. **Advanced Async Functions**
   - Async/await patterns for performance
   - Function chaining and composition
   - Error handling and validation

3. **File Operations**
   - CSV/JSON parsing and transformation
   - Data aggregation and export
   - Integration with agent workflows

4. **Tool Selection**
   - When to use each tool type
   - How agents decide which tool to call
   - Combining tools for powerful solutions

### Key Takeaways

| Pattern | Use When | Benefit |
|---------|----------|---------|
| **Code Interpreter** | Exploratory analysis, unknown data | Maximum flexibility |
| **Custom Functions** | Specific business logic | Control and validation |
| **File Operations** | Structured data processing | Performance and reliability |
| **Combined Approach** | Complex workflows | Best of all worlds |

### Production Checklist

Before deploying advanced tool agents:

- ✅ Validate all function parameters
- ✅ Implement comprehensive error handling
- ✅ Add retry logic for transient failures
- ✅ Log tool usage and performance
- ✅ Test with edge cases
- ✅ Monitor token usage (code interpreter can be expensive)
- ✅ Set appropriate timeouts
- ✅ Implement rate limiting for external APIs

### Next Steps

In **Lab 3: MCP Integration**, you'll learn how to extend agents even further by connecting to external MCP servers, enabling access to specialized tools and data sources without writing custom function wrappers.

**Continue to**: [Lab 3 - MCP Integration](./03-mcp-integration.md)

---

## Clean Up

All agents created in this lab were automatically deleted after each exercise. No additional cleanup required.

## Additional Resources

- [Microsoft Foundry Code Interpreter Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/tools/code-interpreter)
- [Custom Functions Best Practices](https://learn.microsoft.com/azure/ai-foundry/agents/tools/functions)
- [Async Programming in Python](https://docs.python.org/3/library/asyncio.html)
- [Pandas Data Analysis](https://pandas.pydata.org/docs/)
