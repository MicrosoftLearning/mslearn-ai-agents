---
lab:
    title: 'Advanced Tool Calling and Code Interpreter'
    description: 'Master advanced agent capabilities with code interpreter, async functions, and data processing using a unified interactive application.'
    hidden: true
---

# Advanced Tool Calling and Code Interpreter

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
1. Task 1: Data Analysis with Code Interpreter
2. Task 2: Advanced Async Custom Functions
3. Task 3: File Operations and Data Transformation
4. Task 4: Comprehensive Demo (All Tools Combined)
5. View Architecture Overview
0. Exit
```

---

## Setup

### Navigate to the lab directory

1. Open Visual Studio Code.

2. Open the lab folder:
   ```
   C:\repos\mslearn-ai-agents\Labfiles\uplevel\02-advanced-tool-calling\Python
   ```
   
   Use **File > Open Folder** in VS Code.

### Configure environment

1. In the lab folder, locate the provided `.env` and `requirements.txt` files.

1. Open the `.env` file and replace `your_project_endpoint_here` with your actual project endpoint:

    ```
    PROJECT_ENDPOINT=<your_project_endpoint>
    MODEL_DEPLOYMENT_NAME=gpt-4.1
    ```
    
    **To get your project endpoint:** In VS Code, open the **Microsoft Foundry** extension, right-click on your active project, and select **Copy Project Endpoint**.

1. Install dependencies:

    ```powershell
    pip install -r requirements.txt
    ```

### Verify file structure

Ensure you have these files:
- `advanced_tool_lab.py` - Main unified application - `advanced_functions.py` - Custom async functions module
- `data_processor.py` - File processing utilities module
- `requirements.txt`
- `.env` (your configuration)

---

## Data Analysis with Code Interpreter

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

### Run the application

1. **Start the unified application**:

    ```powershell
    python advanced_tool_lab.py
    ```

2. **Select option 1** from the menu: "Task 1: Data Analysis with Code Interpreter"

### Observe code interpreter in action

The application will demonstrate code interpreter with three sample queries:

1. **Analyze key trends** - Agent examines sales data and identifies patterns
2. **Create visualizations** - Agent generates charts showing sales by region
3. **Calculate statistics** - Agent computes mean, median, and totals

**What you'll see:**

```
Created agent: sales-analytics-agent

Uploading ../sales_data.csv...
File uploaded: file-abc123

Testing code interpreter with sample queries:

[Query 1] Analyze the sales data in file file-abc123. What are the key trends?

⏳ Agent generating and executing code...

ANALYSIS:
I've analyzed your sales data. Here are the key findings:

1. Revenue Trends: Total revenue is $145,320 with steady growth...
2. Regional Performance: North region leads with 35% of sales...
3. Product Mix: Software products account for 60% of revenue...

Recommendations:
- Focus on North region expansion
- Increase software product inventory
- Address declining Midwest performance
```

### Understand the architecture

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

agent = project_client.agents.create_agent(
    model="gpt-4.1",
    name="sales-analytics-agent",
    instructions="Use code interpreter to analyze data...",
    tools=[code_interpreter]  # Enable dynamic code generation
)
```

### Key concepts

**Code Interpreter Benefits:**
- **Dynamic**: Agent generates code based on each query
- **Flexible**: Works with any data structure
- **Secure**: Code runs in isolated sandbox
- **Self-correcting**: Can fix errors and retry
- **Powerful**: Full Python capabilities (pandas, matplotlib, numpy)

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

## Advanced Async Custom Functions

In this exercise, you'll explore sophisticated custom function patterns including async operations, function chaining, and error handling.

### What are Advanced Functions?

While code interpreter is great for dynamic analysis, custom functions provide:
- **Specific business logic** (pricing rules, approval workflows)
- **External integrations** (CRM systems, databases, APIs)
- **Controlled operations** (with validation and permissions)
- **Consistent behavior** (repeatable, testable)

### Run the application

1. If the application isn't running, start it:
   ```powershell
   python advanced_tool_lab.py
   ```

2. **Select option 2** from the menu: "Task 2: Advanced Async Custom Functions"

### Observe advanced functions

The exercise demonstrates 4 sophisticated functions from `advanced_functions.py`:

| Function | Purpose | Key Pattern |
|----------|---------|-------------|
| `analyze_customer_segment` | Customer behavior analysis | Async/await, validation |
| `calculate_forecast` | Sales forecasting | Data processing, error handling |
| `process_sales_pipeline` | Pipeline analysis | Structured responses |
| `get_comprehensive_recommendations` | Combined insights | Function orchestration |

**Sample interaction:**

```
USER: Analyze the enterprise customer segment for quarterly performance

⏳ Processing with advanced functions...
  Calling: analyze_customer_segment

AGENT: Based on the quarterly analysis of our enterprise segment:

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

### Understand async patterns

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
- **Performance**: Handle multiple operations concurrently
- **Scalability**: Don't block while waiting for I/O
- **Responsiveness**: Agent can process other tasks
- **Real-world**: Matches production API patterns

### Function definition pattern

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

agent = project_client.agents.create_agent(
    model="gpt-4.1",
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

### Key concepts

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

## File Operations and Data Transformation

In this exercise, you'll explore file processing capabilities that complement both code interpreter and custom functions.

### What are File Operations?

File operations enable agents to:
- Load and parse CSV/JSON files
- Transform and aggregate data
- Export results in multiple formats
- Handle data validation
- Process batch operations

### Run the application

1. **Select option 3** from the menu: "Task 3: File Operations and Data Transformation"

### Observe file processing

The exercise demonstrates three operations from `data_processor.py`:

**Test 1: Load CSV File**
```
Loaded ../sales_data.csv
   Successfully loaded 20 rows with 5 columns
   Columns: date, region, product, quantity, revenue
```

**Test 2: Transform and Aggregate**
```
Transformation results:
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
Export result: Successfully exported to analysis_results.json
```

### Understand file processing patterns

**File Operations in Agent Context:**

```python
# Define file operation as a function tool
file_ops = FunctionTool(
    name="transform_sales_data",
    description="Transform and aggregate sales data by region and product",
    parameters={"type": "object", "properties": {}, "required": []}
)

# Agent can call it during conversation
agent = project_client.agents.create_agent(
    model="gpt-4.1",
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

### File operation patterns

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

### Key concepts

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

## Comprehensive Interactive Demo

In this exercise, you'll interact with an agent that combines ALL the capabilities you've learned.

### Run the application

1. **Select option 4** from the menu: "Task 4: Comprehensive Demo"

2. The agent now has access to:
   - Code interpreter (dynamic analysis)
   - Advanced async functions (business logic)
   - File operations (data processing)

### Experiment with combined capabilities

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

### Observe tool selection

The agent intelligently selects tools based on the query:

```
Query: "Show me sales trends"
  → Uses code interpreter (dynamic visualization)

Query: "Analyze enterprise customers"
  → Uses custom function (specific business logic)

Query: "Export data by region"
  → Uses file operations (structured transformation)
```

### Explore agent decision-making

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

## Architecture Overview

### View architecture

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

- Validate all function parameters
- Implement comprehensive error handling
- Add retry logic for transient failures
- Log tool usage and performance
- Test with edge cases
- Monitor token usage (code interpreter can be expensive)
- Set appropriate timeouts
- Implement rate limiting for external APIs

### Next Steps

**Option A**: In **Lab 3: MCP Integration**, you'll learn how to extend agents even further by connecting to external MCP servers, enabling access to specialized tools and data sources without writing custom function wrappers.

**Option B**: Continue with **Exercise 5** below to learn how to build a web UI for your agent using Streamlit.

---

## Interactive Web Dashboard

In this bonus exercise, you'll build a production-ready web interface for your Sales Analytics Agent using Streamlit, demonstrating how to create user-facing applications powered by AI agents.

**Duration**: 30 minutes (optional)

### What is Streamlit?

**Streamlit** is a Python framework for building interactive web applications without JavaScript:
- Beautiful UI with minimal code
- Built-in charts and visualizations
- File upload widgets
- Chat interfaces
- Fast development (under 200 lines)

### Why Add a Web UI?

**Benefits:**
1. **Better User Experience** - Non-technical users can interact via web browser
2. **Visual Results** - Charts, graphs, and dashboards instead of terminal output
3. **Production Ready** - Real-world deployment pattern
4. **Accessibility** - Share link, no Python installation required
5. **Interactive** - Upload files, chat, explore data in real-time

### Install Streamlit

The dependency is already in `requirements.txt`. If you haven't installed it yet:

```powershell
pip install streamlit plotly
```

This installs:
- `streamlit` - Web framework
- `plotly` - Interactive visualizations

### Understand the application

The `streamlit_app.py` file provides a complete web UI with 4 tabs:

**Tab 1: Upload Data** - Drag-and-drop CSV upload
- Data preview and statistics
- Agent initialization

**Tab 2: Chat with Agent** - Interactive chat interface
- Ask questions about data
- Get AI-powered insights
- Chat history

**Tab 3: Dashboard** - Automatic visualizations
- Key metrics
- Interactive charts
- Data export

**Tab 4: Help** ℹ️
- Getting started guide
- Sample questions
- Troubleshooting
- Technical details

### Run the Streamlit application

1. **Navigate to the lab directory** (if not already there):
   ```powershell
   cd C:\repos\mslearn-ai-agents\Labfiles\uplevel\02-advanced-tool-calling\Python
   ```

2. **Ensure your `.env` file is configured** with your PROJECT_ENDPOINT

3. **Start the Streamlit server**:
   ```powershell
   streamlit run streamlit_app.py
   ```

4. **Open in browser**:
   - Streamlit automatically opens your browser
   - Or navigate to: `http://localhost:8501`

5. **You should see**:
   - Clean web interface with sidebar
   - Sales Analytics Agent title
   - Four tabs for different features

### Upload and analyze data

**Step-by-step walkthrough:**

1. **Go to "Upload Data" tab**

2. **Click "Choose a CSV file"**
   - Select: `../sales_data.csv` (or use your own data)
   - See automatic data preview
   - View summary statistics

3. **Click "Initialize Agent"**
   - Agent connects to Microsoft Foundry
   - File uploads to agent
   - Thread created for conversation

4. **Wait for confirmation**:
   ```
   Agent initialized! Go to the Chat tab to start analyzing.
   [balloons animation]
   ```

### Chat with your agent

1. **Switch to "Chat with Agent" tab**

2. **Try these questions**:

   **Trend Analysis:**
   ```
   What are the sales trends in my data?
   ```

   **Regional Performance:**
   ```
   Which region has the highest sales?
   ```

   **Top Performers:**
   ```
   Show me the top 5 products by revenue
   ```

   **Forecasting:**
   ```
   Can you predict next month's sales based on the trends?
   ```

3. **Observe the interaction**:
   - Your message appears with avatar
   - Agent response appears with avatar
   - "Analyzing..." spinner shows while processing
   - Agent uses code interpreter for analysis

4. **Continue the conversation**:
   - Ask follow-up questions
   - Build on previous responses
   - Context is maintained in the thread

### Explore the dashboard

1. **Switch to "Dashboard" tab**

2. **See automatic visualizations**:
   - **Key Metrics**: Total sales, average sale, record count
   - **Sales Trend Chart**: Line chart showing trends over time
   - **Regional Breakdown**: Bar chart by region
   - **Complete Data Table**: Interactive, sortable data

3. **Interact with visualizations**:
   - Hover over charts for details
   - Use slider to adjust rows displayed
   - Sort by different columns
   - Download data as CSV

### Understand the architecture

**Streamlit Application Flow:**

```
┌────────────────────────────────────────┐
│    User's Web Browser                  │
│    (http://localhost:8501)             │
└───────────────┬────────────────────────┘
                │
                │ HTTP
                ▼
┌────────────────────────────────────────┐
│    Streamlit Server                    │
│    (streamlit_app.py)                  │
└───────────┬─────────────┬──────────────┘
            │             │
            │ Azure AI    │ File I/O
            │ SDK         │
            ▼             ▼
┌─────────────────┐  ┌──────────────┐
│ Microsoft       │  │ Local CSV    │
│ Foundry         │  │ Files        │
│                 │  │              │
│ • Create Agent  │  │ • Upload     │
│ • Upload Files  │  │ • Preview    │
│ • Chat Thread   │  │ • Transform  │
│ • Get Responses │  │              │
└─────────────────┘  └──────────────┘
```

### Key code patterns

**File Upload Pattern:**
```python
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head(10))
```

**Chat Interface Pattern:**
```python
if prompt := st.chat_input("Ask about your data..."):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = query_agent(prompt)
            st.write(response)
```

**Visualization Pattern:**
```python
# Create interactive chart
fig = px.line(df, x='date', y='sales', title='Sales Trend')
st.plotly_chart(fig, use_container_width=True)
```

**Session State Pattern:**
```python
# Store data across interactions
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Access later
for msg in st.session_state.messages:
    st.write(msg)
```

### Production considerations

**When deploying to production:**

1. **Authentication**
   ```python
   # Add user authentication
   import streamlit_authenticator as stauth
   
   authenticator = stauth.Authenticate(...)
   name, authentication_status, username = authenticator.login('Login', 'main')
   ```

2. **Error Handling**
   ```python
   try:
       response = agent.run(query)
   except Exception as e:
       st.error(f"Error: {str(e)}")
       # Log error
       logger.error(f"Agent error: {e}")
   ```

3. **Rate Limiting**
   ```python
   # Limit queries per user
   if st.session_state.query_count > MAX_QUERIES:
       st.warning("Query limit reached. Please try again later.")
       st.stop()
   ```

4. **Data Privacy**
   ```python
   # Don't store sensitive data
   # Clear after session
   if st.button("Clear Data"):
       st.session_state.clear()
   ```

5. **Deployment Options**
   - **Streamlit Cloud**: `streamlit deploy streamlit_app.py`
   - **Azure App Service**: Deploy as web app
   - **Docker**: Containerize for any platform
   - **Internal Server**: Run behind corporate firewall

### Extend the application

**Ideas for enhancement:**

1. **Multi-file Upload**
   ```python
   uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
   for file in uploaded_files:
       process_file(file)
   ```

2. **Advanced Charts**
   ```python
   # Add more visualization types
   chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
   if chart_type == "Line":
       st.line_chart(data)
   ```

3. **Export Options**
   ```python
   # Export to different formats
   export_format = st.radio("Format", ["CSV", "Excel", "JSON"])
   if export_format == "Excel":
       df.to_excel("export.xlsx")
   ```

4. **Real-time Updates**
   ```python
   # Auto-refresh data
   if st.checkbox("Auto-refresh"):
       time.sleep(5)
       st.rerun()
   ```

### Compare CLI vs Web UI

| Aspect | CLI (advanced_tool_lab.py) | Web UI (streamlit_app.py) |
|--------|---------------------------|---------------------------|
| **Setup** | `python advanced_tool_lab.py` | `streamlit run streamlit_app.py` |
| **Interface** | Terminal menu | Web browser |
| **Visualizations** | Text only | Interactive charts |
| **File Upload** | File path | Drag-and-drop |
| **Chat** | Text input/output | Rich chat interface |
| **Sharing** | Share code | Share URL |
| **Best For** | Developers, debugging | End users, demos |

**Recommendation**: Use both!
- **Development**: CLI for testing and debugging
- **Production**: Web UI for end users

### Key Concepts Summary

**What you learned:**
1. How to build web UIs for AI agents
2. Streamlit framework basics
3. File upload and data preview
4. Chat interface patterns
5. Interactive visualizations
6. Production deployment considerations

**When to add a web UI:**
- Non-technical users need access
- Want visual, interactive results
- Building demos or prototypes
- Need to share with stakeholders
- Production user-facing applications

---

## Summary (Updated with Exercise 5)

Congratulations! You've completed Lab 2 including the bonus web UI exercise.

### Complete Skills Acquired

1. **Code Interpreter** - Dynamic data analysis
2. **Advanced Async Functions** - Business logic
3. **File Operations** - Data transformation
4. **Tool Selection** - Intelligent agent decisions
5. **Web UI Development** NEW - User-facing applications

### Next Steps

**Continue to**: [Lab 3 - MCP Integration](./03-mcp-integration.md)

---

## Clean Up

All agents created in this lab were automatically deleted after each exercise. No additional cleanup required.

## Additional Resources

- [Microsoft Foundry Code Interpreter Documentation](https://learn.microsoft.com/azure/ai-foundry/agents/tools/code-interpreter)
- [Custom Functions Best Practices](https://learn.microsoft.com/azure/ai-foundry/agents/tools/functions)
- [Async Programming in Python](https://docs.python.org/3/library/asyncio.html)
- [Pandas Data Analysis](https://pandas.pydata.org/docs/)
