import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>

/* Main background */
.main {
    background-color: #f3f4f7;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #8e44ad, #e056fd);
    color: white;
}

/* KPI Cards */
div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    text-align: center;
}

/* KPI label */
div[data-testid="stMetricLabel"] {
    color: gray;
    font-size: 14px;
}

/* KPI value */
div[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: black;
}

/* Titles */
h1 {
    text-align: center;
    color: #333;
}

</style>
""", unsafe_allow_html=True)

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=5000, key="refresh")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("final_master_dataset_cleaned.csv")

# ---------------- TITLE ----------------
st.title("Customer Support Dashboard")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("Filters")

priority = st.sidebar.selectbox("Priority", ["All"] + list(df["Ticket Priority"].unique()))
location = st.sidebar.selectbox("Location", ["All"] + list(df["Location"].unique()))
channel = st.sidebar.selectbox("Channel", ["All"] + list(df["Ticket Channel"].unique()))
cluster = st.sidebar.selectbox("Issue Cluster", ["All"] + list(df["Cluster"].unique()))

# ---------------- FILTER LOGIC ----------------
filtered_df = df.copy()

if priority != "All":
    filtered_df = filtered_df[filtered_df["Ticket Priority"] == priority]
if location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location]
if channel != "All":
    filtered_df = filtered_df[filtered_df["Ticket Channel"] == channel]
if cluster != "All":
    filtered_df = filtered_df[filtered_df["Cluster"] == cluster]

# ---------------- KPI ----------------
st.markdown("### ")

k1, k2, k3, k4 = st.columns(4)

total = len(filtered_df)
top_priority = filtered_df["Ticket Priority"].mode()[0]
top_count = len(filtered_df[filtered_df["Ticket Priority"] == top_priority])
avg_time = round(filtered_df["First_Response_Minutes"].mean(), 2)

k1.metric("Total Tickets", total)
k2.metric("Top Priority", top_priority)
k3.metric("Top Priority Count", top_count)
k4.metric("Avg Response Time", avg_time)

# ---------------- TREND (AREA CHART) ----------------
st.subheader("Tickets Trend")

trend = filtered_df.groupby("Date of Purchase").size().reset_index(name="Tickets")

fig_trend = px.area(
    trend,
    x="Date of Purchase",
    y="Tickets"
)

fig_trend.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ---------------- GRAPHS ----------------
c1, c2 = st.columns(2)

# Donut Chart
with c1:
    fig1 = px.pie(
        filtered_df,
        names="Ticket Channel",
        hole=0.5,
        title="Channel Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Bar Chart
with c2:
    fig2 = px.bar(
        filtered_df["Ticket Priority"].value_counts(),
        title="Priority Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- RESPONSE ANALYSIS ----------------
c3, c4 = st.columns(2)

# Box Plot
with c3:
    fig3 = px.box(
        filtered_df,
        x="Location",
        y="First_Response_Minutes",
        color="Location",
        title="Response Time by Location"
    )
    st.plotly_chart(fig3, use_container_width=True)

# Cluster Graph
with c4:
    cluster_data = filtered_df.groupby("Cluster")["First_Response_Minutes"].mean().reset_index()

    fig4 = px.bar(
        cluster_data,
        x="Cluster",
        y="First_Response_Minutes",
        color="First_Response_Minutes",
        title="Response Time by Issue Cluster"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------------- MAP ----------------
st.subheader("Geographical View")

map_data = filtered_df.groupby(
    ["Location", "Latitude", "Longitude"]
).size().reset_index(name="Tickets")

fig_map = px.scatter_mapbox(
    map_data,
    lat="Latitude",
    lon="Longitude",
    size="Tickets",
    color="Location",
    zoom=1
)

fig_map.update_layout(
    mapbox_style="carto-positron",
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig_map, use_container_width=True)