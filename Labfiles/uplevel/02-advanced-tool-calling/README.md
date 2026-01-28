# Lab 2: Advanced Tool Calling and Code Interpreter

This lab demonstrates advanced agent capabilities including code interpreter for dynamic data analysis, sophisticated async custom functions, and production-ready file processing workflows.

**⭐ This lab uses a unified menu-driven application for the best learning experience.**

## Contents

### Main Application

- **`advanced_tool_lab.py`** ⭐ - Unified interactive application with menu interface

### Supporting Modules

- **`advanced_functions.py`** - Async custom functions (imported by main app)
- **`data_processor.py`** - File processing utilities (imported by main app)

### Individual Examples (Optional)

- **`sales_analytics_agent.py`** - Standalone code interpreter example
- **`remote_mcp_agent.py`** - Additional reference implementation

### Configuration

- **`requirements.txt`** - Python package dependencies
- **`.env.example`** - Template for environment configuration

### Data Files

- **`../sales_data.csv`** - Sample sales data for analysis (20 records)
- **`../inventory_data.csv`** - Sample inventory data for practice (9 records)

## Setup Instructions

### 1. Prerequisites

- Completed Lab 1 (or have Microsoft Foundry project configured)
- Python 3.12 or later
- Azure subscription with AI Foundry access
- VS Code with Foundry extension (optional but recommended)

### 2. Install Dependencies

```powershell
cd Python
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
   ```powershell
   cp .env.example .env
   ```

2. Edit `.env` and add your Microsoft Foundry project endpoint:
   ```
   PROJECT_ENDPOINT=<your_project_endpoint>
   ```

   **To get your endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Endpoint**.

### 4. Authenticate with Azure

Ensure you're authenticated with Azure:

```powershell
az login
```

## Running the Lab

### ⭐ Recommended: Use the Unified Application

```powershell
python advanced_tool_lab.py
```

You'll see an interactive menu:

```
═══════════════════════════════════════════════════════════
   LAB 2: ADVANCED TOOL CALLING AND CODE INTERPRETER
═══════════════════════════════════════════════════════════

📚 Choose an exercise:

  1. Exercise 1: Data Analysis with Code Interpreter
     (Upload CSV, generate visualizations, statistical analysis)

  2. Exercise 2: Advanced Async Custom Functions
     (Customer segmentation, forecasting, pipeline processing)

  3. Exercise 3: File Operations and Data Transformation
     (Load CSV, transform data, export results)

  4. Exercise 4: Comprehensive Demo (All Tools Combined)
     (Interactive agent with all capabilities)

  5. View Architecture Overview

  0. Exit
```

**Benefits of the Unified App:**
- ✅ Stay in one application for entire lab
- ✅ Natural progression through exercises
- ✅ Interactive demos with real-time feedback
- ✅ Architecture overview included
- ✅ Less context switching

### Alternative: Run Individual Files

If you prefer standalone examples:

```powershell
# Exercise 1 (code interpreter)
python sales_analytics_agent.py

# Test Exercise 2 functions
python -c "import asyncio; from advanced_functions import analyze_customer_segment; print(asyncio.run(analyze_customer_segment('enterprise', 'quarterly')))"

# Test Exercise 3 functions
python -c "import asyncio; from data_processor import transform_sales_data; print(asyncio.run(transform_sales_data()))"
```

## Lab Structure

### Exercise 1: Data Analysis with Code Interpreter (20 min)

Explore dynamic code generation and execution:
- Upload and analyze CSV files
- Generate visualizations (charts, graphs)
- Perform statistical analysis
- See code generated in real-time

**Key Learning**: Code interpreter enables agents to adapt to any data structure without pre-defined functions.

### Exercise 2: Advanced Async Custom Functions (20 min)

Master sophisticated function patterns:
- Async/await for concurrent operations
- Parameter validation and error handling
- Function chaining and composition
- Structured responses

**Key Learning**: Custom functions provide controlled, validated business logic.

### Exercise 3: File Operations and Data Transformation (20 min)

Production-ready file processing:
- Load and parse CSV files
- Transform and aggregate data
- Export results in multiple formats
- Handle errors gracefully

**Key Learning**: File operations integrate seamlessly with agent workflows.

### Exercise 4: Comprehensive Interactive Demo

Combine all tools in an interactive agent:
- Ask any question
- Agent selects appropriate tool
- See tool decision-making in action
- Experiment with combined capabilities

**Key Learning**: Agents intelligently choose tools based on query type.

## Architecture

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
│ • Generate code │ │ • Async    │ │ • Load CSV            │
│ • Execute Python│ │ • Chaining │ │ • Transform data      │
│ • Create charts │ │ • Error    │ │ • Export results      │
│ • Statistics    │ │   handling │ │ • Validation          │
└─────────────────┘ └────────────┘ └───────────────────────┘
```

## Key Concepts

### When to Use Each Tool

| Tool Type | Use Case | Example |
|-----------|----------|---------|
| **Code Interpreter** | Dynamic, exploratory analysis | "Analyze this CSV and find trends" |
| **Custom Function** | Specific business logic | "Calculate enterprise customer forecast" |
| **File Operations** | Structured data processing | "Export sales data by region" |

### Code Interpreter Benefits

- ✅ **Dynamic**: Agent writes Python code on-the-fly
- ✅ **Adaptive**: Works with any data structure
- ✅ **Powerful**: Full Python ecosystem (pandas, matplotlib, numpy)
- ✅ **Secure**: Runs in isolated sandbox
- ✅ **Self-correcting**: Can debug and retry

### Advanced Function Patterns

**Async/Await**:
```python
async def analyze_segment(segment: str):
    data = await fetch_data(segment)  # Non-blocking
    return await process_data(data)
```

**Parameter Validation**:
```python
if segment not in ["enterprise", "mid-market", "small-business"]:
    return {"status": "error", "error": "Invalid segment"}
```

**Error Handling**:
```python
try:
    result = await risky_operation()
except Exception as e:
    return {"error": str(e), "fallback": await get_cached_data()}
```

**Function Chaining**:
```python
async def pipeline(data):
    analyzed = await analyze(data)
    forecast = await predict(analyzed)
    return await recommend(forecast)
```

## Module Descriptions

### advanced_functions.py

Contains 4 production-ready async functions:

1. **`analyze_customer_segment()`**
   - Analyzes customer behavior for specific segments
   - Includes metrics: revenue, growth, retention
   - Async data fetching simulation

2. **`calculate_forecast()`**
   - Generates sales forecasts with confidence intervals
   - Multiple time periods (monthly, quarterly, yearly)
   - Historical trend analysis

3. **`process_sales_pipeline()`**
   - Analyzes pipeline stages
   - Conversion rates and bottlenecks
   - Stage-specific insights

4. **`get_comprehensive_recommendations()`**
   - Combines all analyses
   - Actionable recommendations
   - Prioritized by impact

### data_processor.py

File processing utilities:

- **`load_csv_file()`** - Load CSV with validation
- **`transform_sales_data()`** - Aggregate and calculate metrics
- **`export_results()`** - Export to JSON/CSV

## Troubleshooting

### "Cannot import advanced_functions"

Make sure you're in the Python directory:
```powershell
cd C:\repos\mslearn-ai-agents\Labfiles\uplevel\02-advanced-tool-calling\Python
```

### "Code interpreter execution failed"

1. Check CSV file format (headers, no special characters)
2. Verify file is in correct location
3. Try simpler queries first

### "Async function errors"

Ensure you're using `asyncio.run()` to run async functions:
```python
result = asyncio.run(analyze_customer_segment("enterprise", "quarterly"))
```

### "Module not found"

Reinstall dependencies:
```powershell
pip install -r requirements.txt --upgrade
```

## Production Checklist

Before deploying agents with advanced tools:

- ✅ Validate all function parameters
- ✅ Implement comprehensive error handling
- ✅ Add retry logic for transient failures
- ✅ Log tool usage and performance
- ✅ Test with edge cases
- ✅ Monitor token usage (code interpreter can be expensive)
- ✅ Set appropriate timeouts
- ✅ Implement rate limiting

## Learn More

- [Code Interpreter Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/tools/code-interpreter)
- [Custom Functions Best Practices](https://learn.microsoft.com/azure/ai-foundry/agents/tools/functions)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
- [Azure AI Projects SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)

## Next Steps

After completing this lab:
- **Lab 3**: MCP Integration - Connect agents to external tools and servers
- **Lab 4**: Multi-Agent Orchestration - Coordinate multiple specialized agents
- **Lab 5**: M365 & Teams Integration - Deploy to production environments

## License

This code is provided as part of Microsoft Learn training materials.
