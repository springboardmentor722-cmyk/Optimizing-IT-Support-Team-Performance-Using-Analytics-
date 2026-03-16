import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IT Support Performance Dashboard", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>IT Support Real-Time Monitoring Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

df = pd.read_excel("dashboard_dataset.xlsx")

df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"])

# ----------------------
# Sidebar Filters
# ----------------------

st.sidebar.header("Filters")

priority = st.sidebar.multiselect(
    "Ticket Priority",
    options=df["Ticket Priority"].unique(),
    default=df["Ticket Priority"].unique()
)

status = st.sidebar.multiselect(
    "Ticket Status",
    options=df["Ticket Status"].unique(),
    default=df["Ticket Status"].unique()
)

channel = st.sidebar.multiselect(
    "Ticket Channel",
    options=df["Ticket Channel"].unique(),
    default=df["Ticket Channel"].unique()
)

df = df[
    (df["Ticket Priority"].isin(priority)) &
    (df["Ticket Status"].isin(status)) &
    (df["Ticket Channel"].isin(channel))
]

# ----------------------
# KPI Metrics
# ----------------------

total_tickets = df["Ticket ID"].count()
closed_tickets = df[df["Ticket Status"] == "Closed"]["Ticket ID"].count()
avg_resolution = round(df["Resolution_Time_Hours"].mean(),2)

sla_met = df[df["Resolution_Time_Hours"] <= 12]["Ticket ID"].count()
sla_performance = round((sla_met / total_tickets) * 100,2)

col1,col2,col3,col4 = st.columns(4, gap="large")

col1.metric("Total Tickets", total_tickets)
col2.metric("Closed Tickets", closed_tickets)
col3.metric("Avg Resolution Time", avg_resolution)
col4.metric("SLA Performance %", sla_performance)

st.markdown("---")

# ----------------------
# Ticket Status Distribution
# ----------------------

col1,col2 = st.columns(2)

status_dist = df["Ticket Status"].value_counts().reset_index()
status_dist.columns = ["Status","Count"]

fig_status = px.pie(
    status_dist,
    names="Status",
    values="Count",
    title="Ticket Status Distribution"
)

col1.plotly_chart(fig_status,use_container_width=True)

# ----------------------
# Ticket Distribution by Priority
# ----------------------

priority_dist = df["Ticket Priority"].value_counts().reset_index()
priority_dist.columns = ["Priority","Count"]

fig_priority = px.pie(
    priority_dist,
    names="Priority",
    values="Count",
    title="Ticket Distribution by Priority"
)

col2.plotly_chart(fig_priority,use_container_width=True)

st.markdown("---")

# ----------------------
# Avg Resolution Time by Priority
# ----------------------

avg_res_priority = df.groupby("Ticket Priority")["Resolution_Time_Hours"].mean().reset_index()

fig_avg_res = px.bar(
    avg_res_priority,
    x="Ticket Priority",
    y="Resolution_Time_Hours",
    color="Ticket Priority",
    text_auto=True,
    title="Average Resolution Time by Priority"
)

fig_avg_res.update_traces(textposition="outside")

st.plotly_chart(fig_avg_res, use_container_width=True)

st.markdown("---")


# ----------------------
# Ticket Status by Channel
# ----------------------

channel_status = df.groupby(["Ticket Channel","Ticket Status"]).size().reset_index(name="Count")

fig_channel = px.bar(
    channel_status,
    x="Ticket Channel",
    y="Count",
    color="Ticket Status",
    text="Count",
    barmode="group",
    title="Ticket Status by Service Channel"
)

fig_channel.update_traces(textposition="outside")

st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# ----------------------
# Global Ticket Channel Distribution
# ----------------------

channel_locations = {
    "Email": {"lat": 40.7128, "lon": -74.0060},      # New York
    "Phone": {"lat": 51.5074, "lon": -0.1278},       # London
    "Chat": {"lat": 28.6139, "lon": 77.2090},        # Delhi
    "Social media": {"lat": -33.8688, "lon": 151.2093}  # Sydney
}

geo_data = df["Ticket Channel"].value_counts().reset_index()
geo_data.columns = ["Ticket Channel", "Count"]

geo_data["lat"] = geo_data["Ticket Channel"].map(lambda x: channel_locations[x]["lat"])
geo_data["lon"] = geo_data["Ticket Channel"].map(lambda x: channel_locations[x]["lon"])

fig_map = px.scatter_mapbox(
    geo_data,
    lat="lat",
    lon="lon",
    size="Count",
    color="Ticket Channel",
    hover_name="Ticket Channel",
    size_max=40,
    zoom=1,
    title="Global Ticket Channel Distribution"
)

fig_map.update_layout(
    mapbox_style="open-street-map",
)

st.plotly_chart(fig_map, use_container_width=True)