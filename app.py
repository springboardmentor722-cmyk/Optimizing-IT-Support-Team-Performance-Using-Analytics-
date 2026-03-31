import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="IT Support Dashboard", layout="wide")

# -------------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    text-align: center;
}
.kpi-title {
    font-size: 14px;
    color: gray;
}
.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: #2E86C1;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h1 style='text-align:center;'>📊 IT Support Performance Dashboard</h1>", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_excel("final_data.xlsx")

# -------------------------------
# CLEAN DATA
# -------------------------------
df["Resolution_Duration_Minutes"] = pd.to_numeric(df["Resolution_Duration_Minutes"], errors="coerce").fillna(0)
df["Customer Satisfaction Rating"] = pd.to_numeric(df["Customer Satisfaction Rating"], errors="coerce").fillna(0)

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔎 Filters")

country = st.sidebar.selectbox("Country", ["All"] + list(df["Country"].dropna().unique()))
priority = st.sidebar.selectbox("Priority", ["All"] + list(df["Ticket Priority"].dropna().unique()))
status = st.sidebar.selectbox("Status", ["All"] + list(df["Ticket Status"].dropna().unique()))

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]

if priority != "All":
    filtered_df = filtered_df[filtered_df["Ticket Priority"] == priority]

if status != "All":
    filtered_df = filtered_df[filtered_df["Ticket Status"] == status]

# -------------------------------
# KPI CARDS hema_dashboard/final_data.xlsx
# -------------------------------
st.markdown("### 📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_tickets = filtered_df["Ticket ID"].count()
avg_satisfaction = round(filtered_df["Customer Satisfaction Rating"].mean(), 2)
avg_resolution = round(filtered_df["Resolution_Duration_Minutes"].mean(), 2)
top_country = filtered_df["Country"].value_counts().idxmax() if not filtered_df.empty else "N/A"

def kpi(title, value):
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """

col1.markdown(kpi("Total Tickets", total_tickets), unsafe_allow_html=True)
col2.markdown(kpi("Avg Satisfaction", avg_satisfaction), unsafe_allow_html=True)
col3.markdown(kpi("Avg Resolution (mins)", avg_resolution), unsafe_allow_html=True)
col4.markdown(kpi("Top Country", top_country), unsafe_allow_html=True)

# -------------------------------
# CHARTS
# -------------------------------
st.markdown("### 📊 Insights")

col1, col2 = st.columns(2)

# Donut Chart
with col1:
    fig1 = px.pie(filtered_df,
                  names="Ticket Priority",
                  hole=0.6,
                  color_discrete_sequence=px.colors.sequential.Blues,
                  title="Priority Distribution")
    st.plotly_chart(fig1, use_container_width=True)

# Channel Chart
with col2:
    channel_data = filtered_df["Ticket Channel"].value_counts().reset_index()
    channel_data.columns = ["Channel", "Count"]

    fig2 = px.bar(channel_data,
                  x="Channel",
                  y="Count",
                  text="Count",
                  color="Channel",
                  title="Tickets by Channel")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

# Ticket Type
with col3:
    type_data = filtered_df["Ticket Type"].value_counts().reset_index()
    type_data.columns = ["Type", "Count"]

    fig3 = px.bar(type_data,
                  x="Count",
                  y="Type",
                  orientation="h",
                  color="Type",
                  title="Tickets by Type")
    st.plotly_chart(fig3, use_container_width=True)

# Country Chart
with col4:
    country_data = filtered_df["Country"].value_counts().reset_index()
    country_data.columns = ["Country", "Count"]

    fig4 = px.bar(country_data,
                  x="Country",
                  y="Count",
                  color="Country",
                  title="Tickets by Country")
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# TABLE
# -------------------------------
st.markdown("### 📄 Data Preview")
st.dataframe(filtered_df)