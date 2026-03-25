import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu

# --- Page Configuration ---
st.set_page_config(page_title="Customer Support Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Styling (FIXED: Menu background unified, About section emojis visible) ---
st.markdown("""
    <style>
    /* Sidebar styling - unified dark background */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Fix for option menu items - SAME background as sidebar menu (not white) */
    div[data-testid="stSidebar"] .nav-link {
        background-color: transparent !important;
        color: #e2e8f0 !important;
        border-radius: 8px;
        margin: 4px 0;
    }
    
    div[data-testid="stSidebar"] .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    div[data-testid="stSidebar"] .nav-link-selected {
        background-color: #334155 !important;
        color: white !important;
        border-left: 3px solid #667eea;
    }
    
    /* Ensure the option menu container inherits sidebar background */
    .st-emotion-cache-1y4p8pa {
        background-color: transparent !important;
    }
    
    /* Individual Section Frames */
    .section-frame {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .section-frame:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* Section headers - FIXED: emojis now visible with proper display */
    .section-header {
        font-size: 1.4rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        display: inline-block;
    }
    
    /* Ensure emojis in section headers display properly */
    .section-header emoji, .section-header span, .section-header {
        unicode-bidi: normal;
    }
    
    .section-header-text {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
    .section-emoji {
    font-size: 1.4rem;
    -webkit-text-fill-color: initial;
}
    /* Section content text */
    .section-content {
        color: #4a5568;
        line-height: 1.6;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Horizontal workflow container */
    .workflow-horizontal {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .workflow-step {
        flex: 1;
        min-width: 100px;
        text-align: center;
        padding: 0.75rem 0.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s;
        border: 1px solid #e9ecef;
    }
    
    .workflow-step:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    .step-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .step-title {
        font-weight: 600;
        color: #2d3748;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
    }
    
    .step-desc {
        font-size: 0.7rem;
        color: #718096;
    }
    
    .step-arrow {
        font-size: 1.5rem;
        color: #667eea;
        font-weight: bold;
    }
    
    /* Tools container */
    .tools-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin: 1rem 0;
    }
    
    .tool-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Key insights grid */
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .insight-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border-left: 3px solid #667eea;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .insight-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .insight-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.25rem;
        font-size: 0.9rem;
    }
    
    .insight-value {
        color: #667eea;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    .main-header {
        text-align: left;
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        margin-top: 0;
        padding: 0;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .kpi-card-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .kpi-card-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .kpi-card-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .kpi-card-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
    .kpi-label { color: white; font-size: 0.9rem; font-weight: 500; margin-bottom: 0.5rem; opacity: 0.9; }
    .kpi-value { color: white; font-size: 1.8rem; font-weight: bold; margin-bottom: 0.25rem; }
    
    .filter-section { margin-bottom: 1.5rem; }
    .chart-container { background: transparent; padding: 0.5rem; height: 100%; }
    .chart-title { font-size: 1rem; font-weight: 600; color: #333; margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid #667eea; display: inline-block; }
    .stSelectbox > div { margin-bottom: 0; }
    .element-container { margin-bottom: 0 !important; }
    .stSelectbox label { font-weight: 500; color: #555; }
    .stColumn { display: flex; flex-direction: column; }
    .stPlotlyChart { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation (Unified dark menu background) ---
with st.sidebar:
    st.markdown("### ☰ Menu")
    st.markdown("---")
    
    page = option_menu(
        menu_title=None,
        options=["Dashboard", "About"],
        icons=["house", "info-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#94a3b8", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "4px 0px",
                "color": "#4d2187",
                "background-color": "transparent",
                "hover-color": "rgba(255,255,255,0.1)",
                "border-radius": "8px",
            },
            "nav-link-selected": {
                "background-color": "#334155",
                "color": "white",
                "border-left": "3px solid #667eea"
            },
        }
    )
    
    

# --- Load Data from Excel ---
@st.cache_data
def load_data():
    df = pd.read_excel('data (1).xlsx')
    df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'])
    df['First Response Time'] = pd.to_datetime(df['First Response Time'], errors='coerce')
    df['Time to Resolution'] = pd.to_datetime(df['Time to Resolution'], errors='coerce')
    df['Resolution_Duration_Hours'] = pd.to_numeric(df['Resolution_Duration_Hours'], errors='coerce')
    df['Customer Satisfaction Rating'] = pd.to_numeric(df['Customer Satisfaction Rating'], errors='coerce')
    df['Has Rating'] = df['Customer Satisfaction Rating'] > 0
    
    bins = [0, 18, 30, 45, 60, 100]
    labels = ['0-18', '19-30', '31-45', '46-60', '60+']
    df['Age Group'] = pd.cut(df['Customer Age'], bins=bins, labels=labels, right=False)
    df['Month-Year'] = df['Date of Purchase'].dt.to_period('M').astype(str)
    
    # Create Resolution_category if not exists
    if 'Resolution_category' not in df.columns:
        df['Resolution_category'] = pd.cut(df['Resolution_Duration_Hours'], 
                                            bins=[0, 12, 48, float('inf')], 
                                            labels=['Fast', 'Medium', 'Slow'])
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please make sure the file 'data (1).xlsx' is in the same directory as this script.")
    st.stop()

# --- About Page Content (All emojis now visible in headings) ---
if page == "About":
    st.markdown("""<h1 class="main-header"><span class="main-header-text">About This Project</span></h1>
""", unsafe_allow_html=True)
    
    # --- Frame 1: Project Overview (emoji visible) ---
    st.markdown("""
    <div class="section-frame">
        <div class="section-header"><span class="section-emoji">📋</span>
        <span class="section-header-text">Project Overview</span></div>
        <div class="section-content">
            The objective of this project is to analyze IT support ticket data to identify key performance trends, optimize resolution times, and enhance service efficiency through data analysis and visualization.The goal is to uncover patterns in customer requests, technical issues, and support performance metrics to recommend improvements in workflow and resource allocation.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Frame 2: Dataset Description (emoji visible) ---
    st.markdown("""
    <div class="section-frame">
        <div class="section-header"><span class="section-emoji">📊</span>
        <span class="section-header-text">Dataset Description</span></div>
        <div class="section-content">
            <ul style="list-style-type: circle; padding-left: 20px;">
                <li>Dataset Source from Internal IT Support Ticket System dataset.</li>
                <li>The dataset covers the time period from 2020 to 2021, containing two years of ticket data.</li>
                <li>Total Tickets 8,469 included in the dataset.</li>
                <li>Ticket attributes:Ticket ID,Type,Status,Priority,Channel.</li>
                <li>Customer information:Age,Gender,Country.</li>
                <li>Product information:Product Purchased.</li>
                <li>Performance metrics:First Response Time,Resolution Time,Satisfaction Rating.</li>
            </ul>
        </div>
    </div>
    <style>
.section-content ul li::marker {
    color: black;
}
</style>
    """, unsafe_allow_html=True)
    
    # --- Frame 3: Project Workflow (Horizontal Diagram with visible emojis) ---
    st.markdown("""
    <div class="section-frame">
        <div class="section-header"><span class="section-emoji">🔄</span>      
        <span class="section-header-text">Project Workflow</span></div>
        <div class="workflow-horizontal">
            <div class="workflow-step">
                <div class="step-icon">📥</div>
                <div class="step-title">Data Collection</div>
                <div class="step-desc">Extract 8,469 tickets</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">🧹</div>
                <div class="step-title">Data Preprocessing</div>
                <div class="step-desc">Clean & format</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">⚙️</div>
                <div class="step-title">Feature Engineering</div>
                <div class="step-desc">Create metrics</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">📊</div>
                <div class="step-title">EDA</div>
                <div class="step-desc">Analyze patterns</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">📈</div>
                <div class="step-title">Power BI</div>
                <div class="step-desc">Interactive visuals</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">🌐</div>
                <div class="step-title">Streamlit</div>
                <div class="step-desc">Web dashboard</div>
            </div>
            <div class="step-arrow">→</div>
            <div class="workflow-step">
                <div class="step-icon">📝</div>
                <div class="step-title">Reporting</div>
                <div class="step-desc">Insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Frame 4: Tools & Technologies (emoji visible) ---
    st.markdown("""
    <div class="section-frame">
        <div class="section-header"><span class="section-emoji">🛠️</span>
        <span class="section-header-text">Tools & Technologies</span></div>
        <div class="tools-container">
            <span class="tool-badge">🐍 Python</span>
            <span class="tool-badge">📊 Pandas</span>
            <span class="tool-badge">🔢 NumPy</span>
            <span class="tool-badge">📈 Plotly</span>
            <span class="tool-badge">📊 Power BI</span>
            <span class="tool-badge">🎨 Matplotlib</span>
            <span class="tool-badge">🌊 Streamlit</span>
            <span class="tool-badge">📁 Excel</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Frame 5: Key Insights (emoji visible) ---
    st.markdown("""
    <div class="section-frame">
        <div class="section-header"><span class="section-emoji">💡</span>
        <span class="section-header-text">Key Insights</span></div>
        <div class="insights-grid">
            <div class="insight-card">
                <div class="insight-icon">🎯</div>
                <div class="insight-title">Top Priority</div>
                <div class="insight-value">Medium priority tickets dominate with 2,192 tickets</div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">⏱️</div>
                <div class="insight-title">Average Resolution</div>
                <div class="insight-value">20.17 hours average resolution time</div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">📞</div>
                <div class="insight-title">Channel Preference</div>
                <div class="insight-value">Chat and Email are most used channels</div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">🛍️</div>
                <div class="insight-title">Top Problem Products</div>
                <div class="insight-value">Microsoft Office and GoPro Hero generate highest ticket volume</div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">🌍</div>
                <div class="insight-title">Geographic Distribution</div>
                <div class="insight-value">USA and UK have highest ticket volumes</div>
            </div>
            <div class="insight-card">
                <div class="insight-icon">⭐</div>
                <div class="insight-title">Satisfaction Rating</div>
                <div class="insight-value">Average satisfaction of 0.98/5 - significant improvement needed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# --- Main Dashboard Content ---
if page == "Dashboard":
    st.markdown('<h1 class="main-header"> Customer Support Dashboard</h1>', unsafe_allow_html=True)
    
    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tickets = len(df)
        st.markdown(f"""
            <div class="kpi-card kpi-card-1">
                <div class="kpi-label">Total Tickets</div>
                <div class="kpi-value">{total_tickets:,}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if not df.empty:
            top_priority = df['Ticket Priority'].mode()[0]
            st.markdown(f"""
                <div class="kpi-card kpi-card-2">
                    <div class="kpi-label">Top Priority</div>
                    <div class="kpi-value">{top_priority}</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col3:
        closed_tickets = df[df['Ticket Status'] == 'Closed']
        avg_resolution = closed_tickets['Resolution_Duration_Hours'].mean()
        resolution_text = f"{avg_resolution:.2f} hrs" if pd.notna(avg_resolution) else "N/A"
        st.markdown(f"""
            <div class="kpi-card kpi-card-3">
                <div class="kpi-label">Avg Resolution</div>
                <div class="kpi-value">{resolution_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        rated_tickets = df[df['Has Rating']]
        avg_satisfaction = rated_tickets['Customer Satisfaction Rating'].mean()
        satisfaction_text = f"{avg_satisfaction:.2f}/5" if pd.notna(avg_satisfaction) else "N/A"
        st.markdown(f"""
            <div class="kpi-card kpi-card-4">
                <div class="kpi-label">Avg Satisfaction</div>
                <div class="kpi-value">{satisfaction_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Filters Section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
    
    with col_filter1:
        priorities = ['All'] + sorted(df['Ticket Priority'].unique().tolist())
        selected_priority = st.selectbox("Priority", priorities, key="priority_filter")
    
    with col_filter2:
        countries = ['All'] + sorted(df['country'].unique().tolist())
        selected_country = st.selectbox("Country", countries, key="country_filter")
    
    with col_filter3:
        statuses = ['All'] + sorted(df['Ticket Status'].unique().tolist())
        selected_status = st.selectbox("Status", statuses, key="status_filter")
    
    with col_filter4:
        genders = ['All'] + sorted(df['Customer Gender'].unique().tolist())
        selected_gender = st.selectbox("Gender", genders, key="gender_filter")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_priority != 'All':
        filtered_df = filtered_df[filtered_df['Ticket Priority'] == selected_priority]
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['Ticket Status'] == selected_status]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Customer Gender'] == selected_gender]
    
    # Row 1: Three Charts
    row1_col1, row1_col2, row1_col3 = st.columns([1.2, 1, 1])
    
    with row1_col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Ticket Distribution by Type</div>', unsafe_allow_html=True)
        type_counts = filtered_df['Ticket Type'].value_counts()
        fig_pie = px.pie(values=type_counts.values, names=type_counts.index, hole=0,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=True,
                              pull=[0.02 for _ in range(len(type_counts))])
        fig_pie.update_layout(height=400, width=600, margin=dict(t=30, b=30, l=30, r=30))
        st.plotly_chart(fig_pie, use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Avg Resolution Hours by Country</div>', unsafe_allow_html=True)
        avg_res_by_country = filtered_df[filtered_df['Ticket Status'] == 'Closed'].groupby('country')['Resolution_Duration_Hours'].mean().reset_index()
        avg_res_by_country.columns = ['Country', 'Avg Resolution Hours']
        avg_res_by_country = avg_res_by_country.sort_values('Avg Resolution Hours', ascending=True)
        
        bright_colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#FF9F4A', '#A8E6CF']
        fig_bar = px.bar(avg_res_by_country, x='Country', y='Avg Resolution Hours',
                         text_auto='.2f', color='Country', color_discrete_sequence=bright_colors,
                         labels={'Avg Resolution Hours': 'Hours'})
        fig_bar.update_layout(height=400, xaxis_title="Country", yaxis_title="Average Resolution (Hours)",
                             margin=dict(t=30, b=30, l=30, r=30), showlegend=False)
        fig_bar.update_traces(textposition='outside', textfont=dict(size=10))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Channel Resolution Time Distribution</div>', unsafe_allow_html=True)
        
        boxplot_data = []
        for channel in filtered_df['Ticket Channel'].unique():
            channel_df = filtered_df[(filtered_df['Ticket Channel'] == channel) & (filtered_df['Ticket Status'] == 'Closed')]
            resolution_times = channel_df['Resolution_Duration_Hours'].dropna()
            for rt in resolution_times:
                boxplot_data.append({'Channel': channel, 'Resolution Hours': rt})
        
        boxplot_df = pd.DataFrame(boxplot_data)
        if not boxplot_df.empty:
            fig_box = px.box(boxplot_df, x='Channel', y='Resolution Hours', color='Channel',
                             points='outliers', notched=True, color_discrete_sequence=px.colors.qualitative.Set2)
            fig_box.update_layout(height=400, xaxis_title="Support Channel", yaxis_title="Resolution Time (Hours)",
                                 margin=dict(t=30, b=30, l=30, r=30), showlegend=False)
            fig_box.update_traces(marker=dict(size=6), line=dict(width=2), boxmean='sd')
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Two Charts
    col1_width, col2_width = st.columns([0.35, 0.65])
    
    with col1_width:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Cluster Performance by Priority</div>', unsafe_allow_html=True)
        
        # Ensure Resolution_category exists
        if 'Resolution_category' not in filtered_df.columns:
            filtered_df['Resolution_category'] = pd.cut(filtered_df['Resolution_Duration_Hours'], 
                                                        bins=[0, 12, 48, float('inf')], 
                                                        labels=['Fast', 'Medium', 'Slow'])
        
        res_priority = filtered_df.groupby(['Resolution_category', 'Ticket Priority']).size().reset_index(name='Count')
        res_priority = res_priority[res_priority['Resolution_category'].notna()]
        
        if not res_priority.empty:
            fig_grouped = px.bar(res_priority, x='Resolution_category', y='Count', color='Ticket Priority',
                                 barmode='group', text='Count', color_discrete_sequence=px.colors.qualitative.Set1,
                                 category_orders={'Resolution_category': ['Fast', 'Medium', 'Slow']})
            fig_grouped.update_layout(height=400, xaxis_title="Resolution Category", yaxis_title="Number of Tickets",
                                     margin=dict(t=30, b=30, l=30, r=30))
            st.plotly_chart(fig_grouped, use_container_width=True)
        else:
            st.info("No resolution data available.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2_width:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Product Issue by Top 5 Products</div>', unsafe_allow_html=True)
        
        top_5_products = filtered_df['Product Purchased'].value_counts().head(5).index.tolist()
        issue_types = ['Technical issue', 'Billing inquiry', 'Refund request', 'Cancellation request', 'Product inquiry']
        
        heatmap_data = []
        for product in top_5_products:
            product_df = filtered_df[filtered_df['Product Purchased'] == product]
            total_product_tickets = len(product_df)
            for issue in issue_types:
                issue_count = len(product_df[product_df['Ticket Type'] == issue])
                percentage = (issue_count / total_product_tickets * 100) if total_product_tickets > 0 else 0
                heatmap_data.append({'Product': product, 'Issue Type': issue, 'Percentage': percentage})
        
        heatmap_df = pd.DataFrame(heatmap_data)
        if not heatmap_df.empty:
            fig_heatmap = px.density_heatmap(heatmap_df, x='Product', y='Issue Type', z='Percentage',
                                             text_auto='.1f', color_continuous_scale='RdYlGn_r')
            fig_heatmap.update_layout(height=400, xaxis_title="Product", yaxis_title="Issue Type",
                                     xaxis_tickangle=-45, margin=dict(t=30, b=30, l=30, r=30))
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("No product data available.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 3: Geographic Map
    st.markdown('<div class="chart-container" style="margin-top: 0.5rem;">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Geographic Ticket Distribution</div>', unsafe_allow_html=True)
    
    country_counts = filtered_df['country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Ticket Count']
    
    country_coords = {
        'USA': {'lat': 37.0902, 'lon': -95.7129},
        'Canada': {'lat': 56.1304, 'lon': -106.3468},
        'UK': {'lat': 55.3781, 'lon': -3.4360},
        'Germany': {'lat': 51.1657, 'lon': 10.4515},
        'Australia': {'lat': -25.2744, 'lon': 133.7751}
    }
    
    country_counts['lat'] = country_counts['Country'].map(lambda x: country_coords.get(x, {'lat': 0, 'lon': 0})['lat'])
    country_counts['lon'] = country_counts['Country'].map(lambda x: country_coords.get(x, {'lat': 0, 'lon': 0})['lon'])
    
    if not country_counts.empty:
        fig_map = px.scatter_geo(country_counts, lat='lat', lon='lon', size='Ticket Count',
                                 hover_name='Country', hover_data={'Ticket Count': True},
                                 projection="natural earth", color='Ticket Count',
                                 color_continuous_scale='Viridis', size_max=35)
        fig_map.update_layout(height=400, geo=dict(showframe=False, showcoastlines=True,
                                                   landcolor='rgb(243, 243, 243)',
                                                   countrycolor='rgb(204, 204, 204)'),
                             margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No geographic data available for the selected filters.")
    st.markdown('</div>', unsafe_allow_html=True)