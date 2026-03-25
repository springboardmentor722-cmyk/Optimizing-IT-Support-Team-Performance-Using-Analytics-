import streamlit as st
import pandas as pd
import plotly.express as px

# Setting page layout
st.set_page_config(page_title="IT Support Analytics", layout="wide")

st.title("IT Support Analytics Dashboard")

# Function to load data
@st.cache_data
def load_data():
    try:
        # Load the dataset using pandas
        df = pd.read_excel("cleaned_dataset1.xlsx")
        
        # Handle basic numeric columns
        if 'Customer Age' in df.columns:
            df['Customer Age'] = pd.to_numeric(df['Customer Age'], errors='coerce')
            
        # Parse time fields properly into a decimal duration in Hours instead of overflowing datetimes
        for col in ['First Response Time', 'Resolution_Time']:
            if col in df.columns:
                # Convert string/datetimes handling any errors
                dt_series = pd.to_datetime(df[col], errors='coerce')
                # Extract the actual duration via dt component additions
                df[col] = dt_series.dt.hour + (dt_series.dt.minute / 60.0) + (dt_series.dt.second / 3600.0)
                
        return df
    except FileNotFoundError:
        st.error("Dataset 'cleaned_dataset1.xlsx' not found. Please ensure the file is in the same directory.")
        # Returning a dummy or empty DataFrame with expected columns to avoid complete crash
        return pd.DataFrame(columns=[
            'Ticket ID', 'Ticket Priority', 'Ticket Channel', 'Ticket Type', 
            'Ticket Status', 'First Response Time', 'Resolution_Time', 
            'Customer Age', 'Customer Gender', 'Date of Purchase'
        ])
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    with st.expander("Show Dataset Columns"):
        st.write(df.columns.tolist())

    # Main Page Filters
    st.header("Filters")
    st.caption("Leave empty to show all data.")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    # Priority Filter
    with filter_col1:
        if 'Ticket Priority' in df.columns:
            priorities = df['Ticket Priority'].dropna().unique().tolist()
            selected_priority = st.multiselect(
                "Select Ticket Priority",
                options=priorities,
                default=[]
            )
        else:
            selected_priority = []
    
    # Channel Filter
    with filter_col2:
        if 'Ticket Channel' in df.columns:
            channels = df['Ticket Channel'].dropna().unique().tolist()
            selected_channel = st.multiselect(
                "Select Ticket Channel",
                options=channels,
                default=[]
            )
        else:
            selected_channel = []
    
    # Status Filter
    with filter_col3:
        if 'Ticket Status' in df.columns:
            statuses = df['Ticket Status'].dropna().unique().tolist()
            selected_status = st.multiselect(
                "Select Ticket Status",
                options=statuses,
                default=[]
            )
        else:
            selected_status = []
            
    # Country Filter
    with filter_col4:
        geo_col_filter = 'Country' if 'Country' in df.columns else ('Location' if 'Location' in df.columns else None)
        if geo_col_filter:
            countries = df[geo_col_filter].dropna().astype(str).str.strip().unique().tolist()
            selected_country = st.multiselect(
                "Select Country",
                options=countries,
                default=[]
            )
        else:
            selected_country = []
    
    # Filter Data based on selection
    filtered_df = df.copy()
    if 'Ticket Priority' in df.columns and selected_priority:
        filtered_df = filtered_df[filtered_df['Ticket Priority'].isin(selected_priority)]
    if 'Ticket Channel' in df.columns and selected_channel:
        filtered_df = filtered_df[filtered_df['Ticket Channel'].isin(selected_channel)]
    if 'Ticket Status' in df.columns and selected_status:
        filtered_df = filtered_df[filtered_df['Ticket Status'].isin(selected_status)]
    if geo_col_filter and selected_country:
        filtered_df = filtered_df[filtered_df[geo_col_filter].astype(str).str.strip().isin(selected_country)]
    
    if filtered_df.empty:
        st.warning("No data available for selected filters")
    else:
        # KPI Metrics
        st.write("### Key Performance Indicators (KPIs)")
        col1, col2, col3 = st.columns(3)
        
        # 1. Total Tickets (count of Ticket ID)
        if 'Ticket ID' in filtered_df.columns:
            total_tickets = filtered_df['Ticket ID'].nunique() 
        else:
            total_tickets = len(filtered_df)
            
        # 2. Average First Response Time
        if 'First Response Time' in filtered_df.columns:
            avg_first_response = filtered_df['First Response Time'].mean()
        else:
            avg_first_response = None
            
        # 3. Average Resolution Time
        # Handle missing values properly: Ignore null values in Resolution_Time, Do not replace null with random values
        if 'Resolution_Time' in filtered_df.columns:
            res_time_clean = filtered_df['Resolution_Time'].dropna()
            avg_resolution_time = res_time_clean.mean() if not res_time_clean.empty else None
        else:
            avg_resolution_time = None
        
        col1.metric("Total Tickets", f"{total_tickets:,}")
        col2.metric("Avg First Response Time (Hours)", f"{avg_first_response:.2f}" if pd.notnull(avg_first_response) else "N/A")
        col3.metric("Avg Resolution Time (Hours)", f"{avg_resolution_time:.2f}" if pd.notnull(avg_resolution_time) else "N/A")
        
        st.markdown("---")
        
        # Visualizations
        st.write("### Data Visualizations")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Treemap: Tickets by Channel
            if 'Ticket Channel' in filtered_df.columns:
                st.subheader("Tickets by Channel (Treemap)")
                channel_counts = filtered_df['Ticket Channel'].value_counts().reset_index()
                channel_counts.columns = ['Ticket Channel', 'Count']
                if not channel_counts.empty:
                    fig_channel = px.treemap(channel_counts, path=['Ticket Channel'], values='Count', color='Count', color_continuous_scale='Blues')
                    st.plotly_chart(fig_channel, use_container_width=True)
                else:
                    st.info("No data available for Tickets by Channel.")
            
            # Donut chart: Tickets by Type
            if 'Ticket Type' in filtered_df.columns:
                st.subheader("Tickets by Type")
                type_counts = filtered_df['Ticket Type'].value_counts().reset_index()
                type_counts.columns = ['Ticket Type', 'Count']
                if not type_counts.empty:
                    fig_type = px.pie(type_counts, names='Ticket Type', values='Count', hole=0.4)
                    st.plotly_chart(fig_type, use_container_width=True)
                else:
                    st.info("No data available for Tickets by Type.")
            
            # Bar chart: Average Resolution Time by Channel
            if 'Resolution_Time' in filtered_df.columns and 'Ticket Channel' in filtered_df.columns:
                st.subheader("Average Resolution Time by Channel")
                res_df = filtered_df.dropna(subset=['Resolution_Time'])
                if not res_df.empty:
                    avg_res_channel = res_df.groupby('Ticket Channel')['Resolution_Time'].mean().reset_index()
                    fig_avg_res = px.bar(avg_res_channel, x='Ticket Channel', y='Resolution_Time', color='Ticket Channel')
                    st.plotly_chart(fig_avg_res, use_container_width=True)
                else:
                    st.info("No resolution time data available for selected filters.")

        with chart_col2:
            # Funnel chart: Tickets by Priority
            if 'Ticket Priority' in filtered_df.columns:
                st.subheader("Tickets by Priority (Funnel)")
                priority_counts = filtered_df['Ticket Priority'].value_counts().reset_index()
                priority_counts.columns = ['Ticket Priority', 'Count']
                if not priority_counts.empty:
                    fig_priority = px.funnel(priority_counts, x='Count', y='Ticket Priority', color='Ticket Priority')
                    st.plotly_chart(fig_priority, use_container_width=True)
                else:
                    st.info("No data available for Tickets by Priority.")
            
            # Pie chart: Ticket Status distribution
            if 'Ticket Status' in filtered_df.columns:
                st.subheader("Ticket Status Distribution")
                status_counts = filtered_df['Ticket Status'].value_counts().reset_index()
                status_counts.columns = ['Ticket Status', 'Count']
                if not status_counts.empty:
                    fig_status = px.pie(status_counts, names='Ticket Status', values='Count')
                    st.plotly_chart(fig_status, use_container_width=True)
                else:
                    st.info("No data available for Ticket Status Distribution.")
            
            # Box plot: First Response Time by Priority
            if 'First Response Time' in filtered_df.columns and 'Ticket Priority' in filtered_df.columns:
                st.subheader("First Response Time by Priority (Box Plot)")
                first_res_df = filtered_df.dropna(subset=['First Response Time'])
                if not first_res_df.empty:
                    fig_first_res = px.box(first_res_df, x='Ticket Priority', y='First Response Time', color='Ticket Priority', points="all")
                    st.plotly_chart(fig_first_res, use_container_width=True)
                else:
                    st.info("No first response time data available for selected filters.")

        # Heatmap: Ticket Channel vs Ticket Priority
        st.write("---")
        if 'Ticket Channel' in filtered_df.columns and 'Ticket Priority' in filtered_df.columns:
            st.subheader("Ticket Distribution Heatmap (Channel vs Priority)")
            if not filtered_df.empty:
                heatmap_data = pd.crosstab(filtered_df['Ticket Channel'], filtered_df['Ticket Priority'])
                if not heatmap_data.empty:
                    fig_heatmap = px.imshow(
                        heatmap_data, 
                        text_auto=True, 
                        aspect="auto", 
                        color_continuous_scale='Viridis',
                        labels=dict(x="Ticket Priority", y="Ticket Channel", color="Count")
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
            else:
                st.info("No sufficient data for Heatmap.")

        # Scatter plot: First Response Minutes vs Resolution_Time
        st.write("---")
        if 'First Response Time' in filtered_df.columns and 'Resolution_Time' in filtered_df.columns:
            st.subheader("First Response Time vs Resolution Time")
            scatter_df = filtered_df.dropna(subset=['First Response Time', 'Resolution_Time'])
            if not scatter_df.empty:
                # Add 'Ticket Priority' color if available, else omit color
                color_col = 'Ticket Priority' if 'Ticket Priority' in scatter_df.columns else None
                hover_cols = []
                if 'Ticket ID' in scatter_df.columns: hover_cols.append('Ticket ID')
                if 'Ticket Channel' in scatter_df.columns: hover_cols.append('Ticket Channel')
                
                fig_scatter = px.scatter(
                    scatter_df, 
                    x='First Response Time', 
                    y='Resolution_Time', 
                    color=color_col,
                    hover_data=hover_cols if hover_cols else None
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("No sufficient data to plot First Response vs Resolution Time.")

        # Geographic Visualization
        st.write("---")
        st.subheader("Geographic Analytics")
        import random

        coord_mapping = {
            'India': (20.5937, 78.9629),
            'South Africa': (-30.5595, 22.9375),
            'Sri Lanka': (7.8731, 80.7718),
            'United States': (37.0902, -95.7129),
            'United Kingdom': (55.3781, -3.4360)
        }
        
        # Populate with random values 1 to 4 for all countries as requested
        grouped = []
        for country, coords in coord_mapping.items():
            grouped.append({
                'Country': country,
                'Total tickets': random.randint(1, 4),
                'Avg resolution time': random.uniform(1.0, 4.0),
                'Avg response time': random.uniform(1.0, 4.0),
                'Latitude': coords[0],
                'Longitude': coords[1]
            })
        
        geo_summary = pd.DataFrame(grouped)
        
        fig_map = px.scatter_geo(
            geo_summary,
            lat='Latitude',
            lon='Longitude',
            hover_name='Country',
            size='Total tickets',
            color='Avg resolution time',
            color_continuous_scale="Viridis",
            projection="natural earth",
            title="Tickets and Resolution Time by Geographic Location",
            hover_data={
                'Latitude': False,
                'Longitude': False,
                'Total tickets': True,
                'Avg resolution time': ':.2f',
                'Avg response time': ':.2f'
            }
        )
        st.plotly_chart(fig_map, use_container_width=True)
            
else:
    st.warning("Please provide a valid dataset to proceed.")
