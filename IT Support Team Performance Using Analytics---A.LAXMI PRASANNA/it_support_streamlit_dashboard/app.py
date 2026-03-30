import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Supportlytics: IT Support Dashboard", layout="wide")

# -------------------------------------------------
# COLORS
# -------------------------------------------------
PRIMARY = "#4A6FA5"
BACKGROUND = "#F7F9FC"

priority_colors = {
    "High": "#F28B82",
    "Medium": "#FBCB8B",
    "Low": "#A8D5BA"
}

type_colors = {
    "Software": "#A7C7E7",
    "Hardware": "#D7BDE2",
    "Network": "#A3E4D7"
}

# -------------------------------------------------
# CSS
# -------------------------------------------------
st.markdown(f"""
<style>

.kpi-box {{
    padding:18px;
    border-radius:10px;
    text-align:center;
    border-left:4px solid {PRIMARY};
}}
.kpi-title {{
    font-size:13px;
    color:#7b8a97;
}}
.kpi-value {{
    font-size:26px;
    font-weight:bold;
    color:{PRIMARY};
}}
.badge {{
    padding:6px 12px;
    border-radius:20px;
    font-size:12px;
    color:#2C3E50;
    font-weight:600;
}}
.high {{ background:{priority_colors["High"]}; }}
.medium {{ background:{priority_colors["Medium"]}; }}
.low {{ background:{priority_colors["Low"]}; }}
.software {{ background:{type_colors["Software"]}; }}
.hardware {{ background:{type_colors["Hardware"]}; }}
.network {{ background:{type_colors["Network"]}; }}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv("fina123.csv")

# -------------------------------------------------
# DATA PREPARATION
# -------------------------------------------------
df["First Response Time"] = pd.to_datetime(df["First Response Time"], errors="coerce")
df["Time to Resolution"] = pd.to_datetime(df["Time to Resolution"], errors="coerce")
df["Resolution Hours"] = (df["Time to Resolution"] - df["First Response Time"]).dt.total_seconds() / 3600
df["Resolution Hours"] = df["Resolution Hours"].clip(lower=0)

# Fix country names
country_mapping = {"USA": "United States", "US": "United States", "U.S.A": "United States",
                   "UK": "United Kingdom", "U.K": "United Kingdom"}
df["Country"] = df["Country"].replace(country_mapping)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(f"""
<h1 style='text-align:center;color:{PRIMARY}'>
Supportlytics: Optimizing IT Support Team Performance
</h1>
""", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#2C3E50'>Monitor KPIs, trends, and global ticket distribution</h4>", unsafe_allow_html=True)

# -------------------------------------------------
# INITIALIZE SESSION STATE
# -------------------------------------------------
if 'type_filter' not in st.session_state:
    st.session_state.type_filter = "All"
if 'priority_filter' not in st.session_state:
    st.session_state.priority_filter = "All"
if 'country_filter' not in st.session_state:
    st.session_state.country_filter = "All"

# -------------------------------------------------
# RESET FUNCTION
# -------------------------------------------------
def reset_filters():
    st.session_state.type_filter = "All"
    st.session_state.priority_filter = "All"
    st.session_state.country_filter = "All"

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
st.markdown("### 🔎 Filters")
f1, f2, f3, f4 = st.columns([2,2,2,1])

with f1:
    st.session_state.type_filter = st.selectbox("🎫 Ticket Type", ["All"] + list(df["Ticket Type"].dropna().unique()), index=0, key="type_box")
with f2:
    st.session_state.priority_filter = st.selectbox("⚡ Priority", ["All"] + list(df["Ticket Priority"].dropna().unique()), index=0, key="priority_box")
with f3:
    st.session_state.country_filter = st.selectbox("🌍 Country", ["All"] + list(df["Country"].dropna().unique()), index=0, key="country_box")
with f4:
    if st.button("🔄 Reset Filters"):
        reset_filters()

# -------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------
def get_filtered_df():
    filtered = df.copy()
    if st.session_state.type_filter != "All":
        filtered = filtered[filtered["Ticket Type"] == st.session_state.type_filter]
    if st.session_state.priority_filter != "All":
        filtered = filtered[filtered["Ticket Priority"] == st.session_state.priority_filter]
    if st.session_state.country_filter != "All":
        filtered = filtered[filtered["Country"] == st.session_state.country_filter]
    return filtered

filtered_df = get_filtered_df()
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters")
    st.stop()

# -------------------------------------------------
# KPIs
# -------------------------------------------------
total_tickets = filtered_df["Ticket ID"].count()
avg_resolution = round(filtered_df["Resolution Hours"].mean(), 2)
most_category = filtered_df["Ticket Type"].mode()[0]
cluster_similarity = round(filtered_df["Customer Satisfaction Rating"].mean(), 2)
top_region = filtered_df["Country"].value_counts().idxmax()

st.markdown("### 📊 Performance KPIs")
k1, k2, k3, k4, k5 = st.columns(5)
def kpi(title, value):
    return f"""
    <div class="kpi-box">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """
k1.markdown(kpi("Total Tickets", total_tickets), unsafe_allow_html=True)
k2.markdown(kpi("Avg Resolution Time", f"{avg_resolution} hrs"), unsafe_allow_html=True)
k3.markdown(kpi("Most Frequent Category", most_category), unsafe_allow_html=True)
k4.markdown(kpi("Cluster Similarity Index", cluster_similarity), unsafe_allow_html=True)
k5.markdown(kpi("Top Region", top_region), unsafe_allow_html=True)

# -------------------------------------------------
# CHARTS
# -------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    fig1 = px.bar(filtered_df, x="Ticket Type", color="Ticket Priority",
                  color_discrete_map=priority_colors, title="Tickets by Type")
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.pie(filtered_df, names="Ticket Priority", hole=0.5,
                  color="Ticket Priority", color_discrete_map=priority_colors, title="Priority Distribution")
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    fig3 = px.scatter(filtered_df, x="Resolution Hours", y="Customer Satisfaction Rating",
                      color="Ticket Priority", size="Resolution Hours",
                      color_discrete_map=priority_colors, title="Cluster Analysis")
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    avg_res = filtered_df.groupby("Ticket Priority")["Resolution Hours"].mean().reset_index()
    fig4 = px.bar(avg_res, x="Ticket Priority", y="Resolution Hours",
                  color="Ticket Priority", color_discrete_map=priority_colors, title="Avg Resolution Time by Priority")
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# MAP
# -------------------------------------------------
st.markdown("### 🌍 Global Ticket Distribution by Priority")
location_data = {
    "United States": (37.0902, -95.7129),
    "United Kingdom": (55.3781, -3.4360),
    "India": (20.5937, 78.9629),
    "Canada": (56.1304, -106.3468),
    "Germany": (51.1657, 10.4515),
    "Australia": (-25.2744, 133.7751)
}
filtered_df["Latitude"] = filtered_df["Country"].map(lambda x: location_data.get(x, [None, None])[0])
filtered_df["Longitude"] = filtered_df["Country"].map(lambda x: location_data.get(x, [None, None])[1])
map_df = filtered_df.groupby(["Country","Latitude","Longitude","Ticket Priority"]).size().reset_index(name="Tickets")

fig_map = px.scatter_mapbox(map_df, lat="Latitude", lon="Longitude",
                            size="Tickets", color="Ticket Priority",
                            hover_name="Country", hover_data=["Ticket Priority","Tickets"],
                            size_max=50, zoom=1, height=500,
                            color_discrete_map=priority_colors,
                            title="🌍 Global Ticket Distribution by Priority")
fig_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0,r=0,t=40,b=0))
st.plotly_chart(fig_map, use_container_width=True)