"""
Lab 2: Advanced Tool Calling - Streamlit Web UI
Exercise 5: Interactive Web Dashboard for Sales Analytics Agent

This application provides a web-based interface for the Sales Analytics Agent,
demonstrating how to create user-facing applications powered by AI agents.

IMPORTANT: This app imports and reuses the lab's existing modules:
- advanced_functions.py - Custom async functions
- data_processor.py - File operations
- Same agent patterns as CLI app

This demonstrates production best practices: one codebase, multiple frontends.

UPDATED: Now uses the new AIProjectClient pattern with endpoint parameter (Lab 09 style)

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import CodeInterpreterTool, FunctionTool
import plotly.express as px
import plotly.graph_objects as go

# Import our existing lab modules (code reuse!)
try:
    from advanced_functions import (
        analyze_customer_segment,
        calculate_forecast,
        process_sales_pipeline,
        generate_recommendations
    )
    from data_processor import (
        load_csv_file,
        transform_sales_data,
        export_results
    )
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    st.warning("⚠️ Lab modules not found. Some features will be limited.")

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'data_uploaded' not in st.session_state:
    st.session_state.data_uploaded = False
if 'agent_client' not in st.session_state:
    st.session_state.agent_client = None
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None
if 'current_thread' not in st.session_state:
    st.session_state.current_thread = None

@st.cache_resource
def init_agent_client():
    """Initialize the AI Projects client."""
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    if not project_endpoint:
        st.error("❌ PROJECT_ENDPOINT not found in .env file")
        st.stop()
    
    try:
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            credential=credential,
            endpoint=project_endpoint
        )
        return client
    except Exception as e:
        st.error(f"❌ Failed to connect to Microsoft Foundry: {str(e)}")
        st.stop()

def create_agent_with_file(client, file_id):
    """Create an agent with code interpreter, custom functions, and uploaded file."""
    try:
        # Define tools: code interpreter + custom functions from our lab modules
        tools = [CodeInterpreterTool()]
        
        # Add custom functions if modules are available
        if MODULES_AVAILABLE:
            custom_functions = [
                FunctionTool(analyze_customer_segment),
                FunctionTool(calculate_forecast),
                FunctionTool(process_sales_pipeline),
                FunctionTool(get_comprehensive_recommendations)
            ]
            tools.extend(custom_functions)
        
        agent = client.agents.create_agent(
            model=os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4.1"),
            name="sales-analytics-web-agent",
            instructions="""You are a sales analytics expert helping users analyze their sales data.

When analyzing data:
1. Use code interpreter for exploratory analysis and visualizations
2. Use custom functions (analyze_customer_segment, calculate_forecast, etc.) for specific business queries
3. Provide clear, concise insights
4. Explain trends and patterns
5. Offer actionable recommendations
6. Always cite specific numbers from the data

You have access to:
- Code interpreter: For dynamic analysis, charts, and statistics
- Custom business functions: For segment analysis, forecasting, and recommendations
- File operations: The uploaded sales data

Choose the most appropriate tool for each query.""",
            tools=tools,
            tool_resources={
                "code_interpreter": {
                    "file_ids": [file_id]
                }
            }
        )
        return agent
    except Exception as e:
        st.error(f"Failed to create agent: {str(e)}")
        return None

def analyze_dataframe(df):
    """Generate basic statistics and insights from the dataframe."""
    insights = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': list(df.columns),
        'numeric_columns': list(df.select_dtypes(include=['int64', 'float64']).columns),
        'date_columns': list(df.select_dtypes(include=['datetime64']).columns)
    }
    
    # Check for common sales columns
    if 'amount' in df.columns or 'sales' in df.columns:
        amount_col = 'amount' if 'amount' in df.columns else 'sales'
        insights['total_sales'] = df[amount_col].sum()
        insights['avg_sales'] = df[amount_col].mean()
        insights['max_sales'] = df[amount_col].max()
        insights['min_sales'] = df[amount_col].min()
    
    return insights

def create_visualizations(df):
    """Create default visualizations from the dataframe."""
    charts = []
    
    # Sales over time (if date column exists)
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    amount_cols = [col for col in df.columns if any(x in col.lower() for x in ['amount', 'sales', 'revenue'])]
    
    if date_cols and amount_cols:
        date_col = date_cols[0]
        amount_col = amount_cols[0]
        
        # Convert to datetime if needed
        if df[date_col].dtype == 'object':
            df[date_col] = pd.to_datetime(df[date_col])
        
        # Group by date and sum
        daily_sales = df.groupby(pd.Grouper(key=date_col, freq='D'))[amount_col].sum().reset_index()
        
        fig = px.line(daily_sales, x=date_col, y=amount_col,
                     title='Sales Trend Over Time',
                     labels={date_col: 'Date', amount_col: 'Sales Amount'})
        fig.update_traces(line_color='#1f77b4', line_width=3)
        charts.append(('line', fig))
    
    # Sales by category (if category column exists)
    category_cols = [col for col in df.columns if any(x in col.lower() for x in ['region', 'product', 'category', 'type'])]
    
    if category_cols and amount_cols:
        category_col = category_cols[0]
        amount_col = amount_cols[0]
        
        category_sales = df.groupby(category_col)[amount_col].sum().reset_index()
        category_sales = category_sales.sort_values(amount_col, ascending=False).head(10)
        
        fig = px.bar(category_sales, x=category_col, y=amount_col,
                    title=f'Top Sales by {category_col.title()}',
                    labels={category_col: category_col.title(), amount_col: 'Sales Amount'})
        fig.update_traces(marker_color='#2ca02c')
        charts.append(('bar', fig))
    
    return charts

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=80)
    st.title("Sales Analytics Agent")
    st.markdown("---")
    
    st.header("ℹ️ About")
    st.write("""
    This AI-powered dashboard helps you:
    - 📊 Analyze sales data
    - 📈 Generate insights
    - 🤖 Chat with your data
    - 💡 Get recommendations
    """)
    
    st.markdown("---")
    
    st.header("💡 Sample Questions")
    st.write("""
    Try asking:
    - "What are the sales trends?"
    - "Which region has highest sales?"
    - "Show me top 10 products"
    - "Create a sales forecast"
    - "Compare Q1 vs Q2 sales"
    """)
    
    st.markdown("---")
    
    st.header("🔧 Status")
    if st.session_state.data_uploaded:
        st.success("✅ Data uploaded")
        if st.session_state.current_agent:
            st.success("✅ Agent ready")
    else:
        st.info("📁 Upload data to start")
    
    st.markdown("---")
    
    # Show module status
    st.header("📦 Modules")
    if MODULES_AVAILABLE:
        st.success("✅ Lab modules loaded")
        with st.expander("Loaded functions"):
            st.write("• analyze_customer_segment")
            st.write("• calculate_forecast")
            st.write("• process_sales_pipeline")
            st.write("• get_comprehensive_recommendations")
            st.write("• load_csv_file")
            st.write("• transform_sales_data")
    else:
        st.warning("⚠️ Lab modules not found")
        st.caption("Using code interpreter only")
    
    st.markdown("---")
    st.caption("Lab 2: Advanced Tool Calling")
    st.caption("Powered by Microsoft Foundry")

# Main content
st.title("📊 Sales Analytics Agent - Interactive Dashboard")
st.markdown("Upload your sales data and chat with an AI agent for instant insights!")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📁 Upload Data", "💬 Chat with Agent", "📊 Dashboard", "ℹ️ Help"])

with tab1:
    st.header("📁 Upload Your Sales Data")
    st.write("Upload a CSV file containing your sales data to get started.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your sales data in CSV format. The file should contain columns like date, amount, region, product, etc."
    )
    
    if uploaded_file is not None:
        try:
            # Load and display data
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df
            st.session_state.data_uploaded = True
            
            st.success(f"✅ Successfully loaded {len(df):,} rows and {len(df.columns)} columns")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            insights = analyze_dataframe(df)
            
            with col1:
                st.metric("Total Rows", f"{insights['total_rows']:,}")
            with col2:
                st.metric("Columns", insights['total_columns'])
            with col3:
                if 'total_sales' in insights:
                    st.metric("Total Sales", f"${insights['total_sales']:,.2f}")
            with col4:
                if 'avg_sales' in insights:
                    st.metric("Average Sale", f"${insights['avg_sales']:,.2f}")
            
            # Data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column info
            with st.expander("📊 Column Details"):
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Non-Null': df.count().values,
                    'Null': df.isnull().sum().values
                })
                st.dataframe(col_info, use_container_width=True)
            
            # Initialize agent
            if st.button("🚀 Initialize Agent with This Data", type="primary"):
                with st.spinner("Setting up your agent..."):
                    # Initialize client
                    if not st.session_state.agent_client:
                        st.session_state.agent_client = init_agent_client()
                    
                    client = st.session_state.agent_client
                    
                    # Save and upload file
                    temp_file = "temp_upload.csv"
                    df.to_csv(temp_file, index=False)
                    
                    try:
                        # Upload file to agent
                        file = client.agents.upload_file(
                            file_path=temp_file,
                        )
                        
                        # Create agent
                        agent = create_agent_with_file(client, file.id)
                        
                        if agent:
                            st.session_state.current_agent = agent
                            st.session_state.file_id = file.id
                            
                            # Create thread
                            thread = client.agents.create_thread()
                            st.session_state.current_thread = thread
                            
                            st.success("✅ Agent initialized! Go to the Chat tab to start analyzing.")
                            st.balloons()
                        
                    except Exception as e:
                        st.error(f"Error initializing agent: {str(e)}")
                    finally:
                        # Cleanup temp file
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.write("Please ensure your CSV file is properly formatted.")

with tab2:
    st.header("💬 Chat with Your Sales Agent")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload data in the 'Upload Data' tab first")
    elif not st.session_state.current_agent:
        st.warning("⚠️ Please initialize the agent in the 'Upload Data' tab")
    else:
        st.write("Ask questions about your sales data and get AI-powered insights!")
        
        # Display chat history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(message["content"])
        
        # Chat input
        prompt = st.chat_input("Ask about your sales data...", key="chat_input")
        
        if prompt:
            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.write(prompt)
            
            # Get agent response
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Analyzing..."):
                    try:
                        client = st.session_state.agent_client
                        agent = st.session_state.current_agent
                        thread = st.session_state.current_thread
                        
                        # Create message
                        message = client.agents.create_message(
                            thread_id=thread.id,
                            role="user",
                            content=prompt
                        )
                        
                        # Run agent
                        run = client.agents.create_and_process_run(
                            thread_id=thread.id,
                            agent_id=agent.id
                        )
                        
                        # Get response
                        messages = client.agents.list_messages(thread_id=thread.id)
                        response_content = messages.data[0].content[0].text.value
                        
                        # Display response
                        st.write(response_content)
                        
                        # Add to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_content
                        })
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

with tab3:
    st.header("📊 Sales Dashboard")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload data first")
    else:
        df = st.session_state.data
        
        st.subheader("📈 Key Metrics")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        insights = analyze_dataframe(df)
        
        with col1:
            st.metric("📊 Total Records", f"{insights['total_rows']:,}")
        
        with col2:
            st.metric("📋 Columns", insights['total_columns'])
        
        with col3:
            if 'total_sales' in insights:
                st.metric("💰 Total Sales", f"${insights['total_sales']:,.2f}")
        
        with col4:
            if 'avg_sales' in insights:
                st.metric("📊 Avg Sale", f"${insights['avg_sales']:,.2f}")
        
        st.markdown("---")
        
        # Create visualizations
        st.subheader("📈 Visualizations")
        
        charts = create_visualizations(df)
        
        if charts:
            for chart_type, fig in charts:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Upload data with date and amount columns to see automatic visualizations")
        
        st.markdown("---")
        
        # Data table
        st.subheader("📋 Complete Data")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            if insights['numeric_columns']:
                sort_column = st.selectbox("Sort by", insights['numeric_columns'])
                sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
                
                if sort_order == "Descending":
                    df_display = df.sort_values(sort_column, ascending=False)
                else:
                    df_display = df.sort_values(sort_column, ascending=True)
            else:
                df_display = df
        
        with col2:
            num_rows = st.slider("Rows to display", 10, len(df), min(50, len(df)))
        
        st.dataframe(df_display.head(num_rows), use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="sales_data_export.csv",
            mime="text/csv"
        )

with tab4:
    st.header("ℹ️ Help & Getting Started")
    
    st.markdown("""
    ## 🚀 Quick Start Guide
    
    ### Important: Code Reuse Architecture
    
    **This web UI imports and reuses the same code from the CLI exercises!**
    
    - ✅ **advanced_functions.py** - Custom async functions (Exercise 2)
    - ✅ **data_processor.py** - File operations (Exercise 3)
    - ✅ **Same agent patterns** - Consistent backend
    
    This demonstrates production best practices:
    - **One codebase, multiple frontends** (CLI + Web)
    - **Code reuse** across interfaces
    - **Consistent behavior** regardless of UI
    
    ### Step 1: Upload Your Data
    1. Go to the **Upload Data** tab
    2. Click "Choose a CSV file" and select your sales data
    3. Review the data preview
    4. Click "Initialize Agent" to prepare the AI
    
    ### Step 2: Chat with Your Agent
    1. Go to the **Chat with Agent** tab
    2. Ask questions about your data (see examples below)
    3. Get instant insights and analysis
    4. Continue the conversation naturally
    
    ### Step 3: View Dashboard
    1. Go to the **Dashboard** tab
    2. See automatic visualizations
    3. Explore your data interactively
    4. Download results
    
    ---
    
    ## 💡 Example Questions
    
    **Trend Analysis:**
    - "Show me the sales trend over the last 6 months"
    - "How do sales compare month-over-month?"
    - "Are sales increasing or decreasing?"
    
    **Performance Analysis:**
    - "Which product/region has the highest sales?"
    - "What are the top 10 performing items?"
    - "Show me the best and worst performing categories"
    
    **Forecasting:**
    - "Predict next month's sales"
    - "What's the sales forecast for Q4?"
    - "Create a 3-month sales projection"
    
    **Comparisons:**
    - "Compare sales by region"
    - "How does this year compare to last year?"
    - "Which month had the highest revenue?"
    
    ---
    
    ## 📊 Data Format Requirements
    
    Your CSV file should contain:
    - **Date column**: For time-based analysis (e.g., 'date', 'order_date')
    - **Amount column**: For sales figures (e.g., 'amount', 'sales', 'revenue')
    - **Category columns**: For grouping (e.g., 'region', 'product', 'category')
    
    **Example structure:**
    ```
    date,product,region,amount
    2024-01-15,Laptop,North,1200.00
    2024-01-16,Monitor,South,450.00
    ...
    ```
    
    ---
    
    ## 🔧 Troubleshooting
    
    **Agent not responding?**
    - Check your internet connection
    - Verify PROJECT_ENDPOINT in .env file
    - Try re-initializing the agent
    
    **Charts not showing?**
    - Ensure your data has date and amount columns
    - Check for null values in key columns
    - Try different column names
    
    **Upload failed?**
    - Verify CSV format (no special characters)
    - Check file size (< 10MB recommended)
    - Ensure proper encoding (UTF-8)
    
    ---
    
    ## 🎓 Learning Objectives
    
    This exercise demonstrates:
    - ✅ Building web UIs for AI agents
    - ✅ Real-time data analysis with code interpreter
    - ✅ Interactive chat interfaces
    - ✅ Data visualization with AI insights
    - ✅ Production-ready agent applications
    
    ---
    
    ## 🛠️ Technical Details
    
    **Architecture: Shared Backend, Multiple Frontends**
    
    ```
    ┌─────────────────────────────────────────┐
    │     Shared Python Modules               │
    │                                         │
    │  • advanced_functions.py                │
    │  • data_processor.py                    │
    │  • Common agent patterns                │
    └──────────┬────────────────┬─────────────┘
               │                │
               │                │
    ┌──────────▼──────┐  ┌─────▼────────────┐
    │   CLI App       │  │   Web UI         │
    │   (Terminal)    │  │   (Browser)      │
    │                 │  │                  │
    │ advanced_tool_  │  │ streamlit_app.py │
    │ lab.py          │  │                  │
    └─────────────────┘  └──────────────────┘
    ```
    
    **Key Benefit:** Both interfaces use identical:
    - ✅ Custom functions
    - ✅ File operations
    - ✅ Agent configuration
    - ✅ Business logic
    
    **Result:** Consistency and code reuse!
    
    ---
    
    **Powered by:**
    - Microsoft Foundry (AI Agent Service)
    - Streamlit (Web Framework)
    - Plotly (Visualizations)
    - Code Interpreter Tool (Data Analysis)
    
    **Agent Capabilities:**
    - Natural language understanding
    - Python code generation & execution
    - Data analysis & statistics
    - Chart generation
    - Contextual conversations
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("🤖 Powered by Microsoft Foundry | 📚 Lab 2: Advanced Tool Calling - Exercise 5")
