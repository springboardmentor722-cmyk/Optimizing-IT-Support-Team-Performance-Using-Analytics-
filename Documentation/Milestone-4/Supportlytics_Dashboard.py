import os
import time
import warnings

import pandas as pd
import plotly.express as px
import streamlit as st

warnings.filterwarnings("ignore")

# ================================================================
# PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Optimizing IT Support Team Performance Using Analytics (Supportlytics)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================================================
# CSS
# ================================================================
st.markdown(
    """
    <style>
        /* ── Hide Streamlit default branding ── */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }

        /* ── Background ── */
        .stApp { background-color: #F4F6F9; }
        .block-container { padding: 0.8rem 1.8rem 2rem 1.8rem; }

        /* ── Header ── */
        .main-header {
            background: #1B2A3B;
            padding: 24px 36px;
            border-radius: 6px;
            margin-bottom: 18px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.18);
            border-bottom: 3px solid #3A7BD5;
        }
        .main-header h1 {
            color: #FFFFFF !important;
            font-size: 1.55rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: 0.3px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .main-header .subtitle {
            color: #A8BDD0;
            font-size: 0.82rem;
            margin: 6px 0 0 0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .main-header .filter-pill {
            display: inline-block;
            background: rgba(58,123,213,0.25);
            border: 1px solid rgba(58,123,213,0.6);
            border-radius: 3px;
            padding: 3px 12px;
            margin: 8px 3px 0 3px;
            font-size: 0.76rem;
            color: #D0E4F7;
            font-weight: 600;
        }

        /* ── KPI Cards ── */
        .kpi-card {
            background: #FFFFFF;
            border-radius: 6px;
            padding: 16px 10px 14px 10px;
            text-align: center;
            box-shadow: 0 1px 6px rgba(0,0,0,0.08);
            border-top: 4px solid #3A7BD5;
            min-height: 95px;
        }
        .kpi-blue   { border-top-color: #3A7BD5 !important; }
        .kpi-green  { border-top-color: #1E7145 !important; }
        .kpi-orange { border-top-color: #C55A11 !important; }
        .kpi-purple { border-top-color: #5C3D8F !important; }
        .kpi-teal   { border-top-color: #0E6B5E !important; }
        .kpi-red    { border-top-color: #A93226 !important; }

        .kpi-val {
            font-size: 1.65rem;
            font-weight: 700;
            color: #1B2A3B;
            line-height: 1.1;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .kpi-label {
            font-size: 0.66rem;
            color: #6B7A8D;
            margin-top: 6px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.9px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        /* ── Active filter badge ── */
        .active-filter-box {
            background: #EAF0FB;
            border: 1px solid #B0C8EE;
            border-radius: 4px;
            padding: 7px 10px;
            margin-top: 6px;
            font-size: 0.80rem;
            color: #000000 !important;
            font-weight: 600;
        }
        .active-filter-box * { color: #000000 !important; }
        .all-data-box {
            background: #EAF4EE;
            border: 1px solid #A8D5B5;
            border-radius: 4px;
            padding: 7px 10px;
            margin-top: 6px;
            font-size: 0.80rem;
            color: #000000 !important;
            font-weight: 600;
        }
        .all-data-box * { color: #000000 !important; }

        /* ── Section header ── */
        .sec-hdr {
            background: #FFFFFF;
            border-radius: 6px;
            padding: 10px 18px;
            margin: 14px 0 10px 0;
            border-left: 4px solid #3A7BD5;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
        .sec-hdr h3 {
            color: #1B2A3B;
            margin: 0;
            font-size: 0.93rem;
            font-weight: 700;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            background: #FFFFFF;
            border-radius: 6px;
            padding: 4px 6px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.07);
            gap: 3px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 13px;
            font-weight: 600;
            color: #1B2A3B;
            border-radius: 4px;
            padding: 9px 20px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .stTabs [aria-selected="true"] {
            background: #1B2A3B !important;
            color: #FFFFFF !important;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] > div {
            background: #F0F4F8;
            border-right: 1px solid #D4DCE6;
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown *,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] small {
            color: #000000 !important;
        }
        /* ── Dropdown box ── */
        section[data-testid="stSidebar"] .stSelectbox > div > div {
            background-color: #FFFFFF !important;
            border: 1px solid #B0BEC5 !important;
            border-radius: 4px !important;
        }
        section[data-testid="stSidebar"] .stSelectbox > div > div > div {
            color: #000000 !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] .stSelectbox svg {
            fill: #1B2A3B !important;
        }
        div[data-baseweb="popover"] ul li div {
            color: #1B2A3B !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="popover"] { background: white !important; }
        section[data-testid="stSidebar"] .active-filter-box,
        section[data-testid="stSidebar"] .active-filter-box *,
        section[data-testid="stSidebar"] .all-data-box,
        section[data-testid="stSidebar"] .all-data-box * {
            color: #000000 !important;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            padding: 14px;
            color: #8A96A3;
            font-size: 0.76rem;
            margin-top: 14px;
            border-top: 1px solid #D4DCE6;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        /* ── Dataframe ── */
        div[data-testid="stDataFrame"] {
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 1px 6px rgba(0,0,0,0.07);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# LIVE RELOAD HELPERS
# ================================================================
REFRESH_INTERVAL = 10  # seconds between auto-refresh checks

def find_data_file():
    """Locate the dataset file and return (path, type)."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        script_dir = os.getcwd()

    search_dirs = [
        script_dir,
        r"C:\Users\natur\OneDrive\Data visualisation project",
        r"C:\Users\natur\Data visulaization",
        os.getcwd(),
    ]
    file_names = [
        "Supportlytics_Final_Data.csv",
        "Supportlytics_finaldata(CSV).csv",
        "Supportlytics_Final_Data.xlsx",
        "Supportlytics_Final_Data.xls",
        "Supportlytics_Final_Data (1).xlsx",
        "Supportlytics_Final_Data (1).xls",
    ]
    for folder in search_dirs:
        for fname in file_names:
            full = os.path.join(folder, fname)
            if os.path.exists(full):
                ftype = "csv" if fname.endswith(".csv") else "excel"
                return full, ftype
    return None, None


def get_mtime(path):
    """Return file modification time, or 0 if path is None/missing."""
    try:
        return os.path.getmtime(path) if path else 0
    except OSError:
        return 0


# ================================================================
# LOAD DATA  –  cached with TTL; clears automatically on file change
# ================================================================
@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data(file_path: str, _mtime: float):
    """_mtime is a cache-busting argument: any change invalidates cache."""
    found_path = file_path
    found_type = "csv" if file_path.endswith(".csv") else "excel"

    if found_path is None or not os.path.exists(found_path):
        st.error(
            "Data file not found.\n\n"
            "Place **Supportlytics_Final_Data.csv** in the same folder as this script."
        )
        st.stop()

    if found_type == "csv":
        df = pd.read_csv(found_path)
        df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    else:
        raw = pd.read_excel(found_path, header=0)
        if raw.shape[1] == 1:
            col = raw.columns[0]
            rows = raw[col].str.split(",", expand=True)
            rows.columns = col.split(",")
            rows.columns = [
                c.strip().replace(" ", "_").lower() for c in rows.columns
            ]
            df = rows
        else:
            df = raw
            df.columns = (
                df.columns.str.strip().str.replace(" ", "_").str.lower()
            )

    # Type conversions
    num_cols = [
        "resolution_hours", "performance_score",
        "cluster_size", "latitude", "longitude", "resolution_duration",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["date_of_purchase"] = pd.to_datetime(
        df["date_of_purchase"], errors="coerce"
    )
    df["cluster"] = df["ticket_channel"]
    df["similarity_score"] = df["performance_score"]
    df["year_month"] = df["date_of_purchase"].dt.strftime("%Y-%m")
    return df


# ================================================================
# RESOLVE DATA FILE ONCE (path doesn't change between reruns)
# ================================================================
_data_path, _data_type = find_data_file()

if _data_path is None:
    st.error(
        "Data file not found.\n\n"
        "Place **Supportlytics_Final_Data.csv** in the same folder as this script."
    )
    st.stop()

# Detect file changes → bust cache automatically
_current_mtime = get_mtime(_data_path)
if "last_mtime" not in st.session_state:
    st.session_state.last_mtime = _current_mtime

if _current_mtime != st.session_state.last_mtime:
    st.cache_data.clear()
    st.session_state.last_mtime = _current_mtime

df = load_data(_data_path, _current_mtime)

# ================================================================
# SIDEBAR  –  filters + active filter display
# ================================================================
with st.sidebar:
    st.markdown("## Supportlytics")
    st.markdown("### Optimizing IT Support Team Performance Using Analytics")
    st.markdown("---")
    st.markdown("### Dashboard Filters")
    st.markdown("*Use filters to drill down:*")

    sel_region = st.selectbox(
        "Region",
        ["All"] + sorted(df["region"].dropna().unique().tolist()),
    )
    sel_priority = st.selectbox(
        "Priority",
        ["All", "Low", "Medium", "High", "Critical"],
    )
    sel_status = st.selectbox(
        "Ticket Status",
        ["All"] + sorted(df["ticket_status"].dropna().unique().tolist()),
    )
    sel_type = st.selectbox(
        "Ticket Type",
        ["All"] + sorted(df["ticket_type"].dropna().unique().tolist()),
    )
    sel_channel = st.selectbox(
        "Channel",
        ["All"] + sorted(df["ticket_channel"].dropna().unique().tolist()),
    )

    # Show active filters clearly
    st.markdown("---")
    st.markdown("### Active Filters")
    active_filters = {
        "Region": sel_region,
        "Priority": sel_priority,
        "Status": sel_status,
        "Type": sel_type,
        "Channel": sel_channel,
    }
    any_active = False
    for label, val in active_filters.items():
        if val != "All":
            any_active = True
            st.markdown(
                f"<div class='active-filter-box'>{label}: <b>{val}</b></div>",
                unsafe_allow_html=True,
            )
    if not any_active:
        st.markdown(
            "<div class='all-data-box'>Showing <b>All Data</b></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(f"**Total Records:** `{len(df):,}`")
    st.markdown(f"**Date Range:** `2020 – 2021`")
    st.markdown(f"**Regions:** `{df['region'].nunique()}`")
    st.markdown(f"**Channels:** `{df['ticket_channel'].nunique()}`")
    st.markdown(f"**Ticket Types:** `{df['ticket_type'].nunique()}`")

    # ── Live Reload Controls ──────────────────────────────────────
    st.markdown("---")
    st.markdown("### Live Data Refresh")
    if st.button("Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.session_state.last_mtime = get_mtime(_data_path)
        st.rerun()

    auto_refresh = st.toggle("Auto-Refresh (10s)", value=False)
    st.markdown(
        f"<small style='color:#000000;'>Last loaded: "
        f"{time.strftime('%H:%M:%S')}</small>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<small style='color:#000000;'>File: "
        f"<code style='color:#1A3A5C;'>{os.path.basename(_data_path)}</code></small>",
        unsafe_allow_html=True,
    )


# ================================================================
# APPLY FILTERS
# ================================================================
fdf = df.copy()
if sel_region != "All":
    fdf = fdf[fdf["region"] == sel_region]
if sel_priority != "All":
    fdf = fdf[fdf["ticket_priority"] == sel_priority]
if sel_status != "All":
    fdf = fdf[fdf["ticket_status"] == sel_status]
if sel_type != "All":
    fdf = fdf[fdf["ticket_type"] == sel_type]
if sel_channel != "All":
    fdf = fdf[fdf["ticket_channel"] == sel_channel]

closed = fdf[fdf["ticket_status"] == "Closed"].copy()
unresolved = fdf[
    fdf["ticket_priority"].isin(["High", "Critical"])
    & (fdf["ticket_status"] != "Closed")
].copy()

# Geo data — exclude Other Global for cleaner map
geo_df = fdf[fdf["region"] != "Other Global"].dropna(
    subset=["latitude", "longitude"]
).copy()


# ================================================================
# CHART THEME DEFAULTS
# ================================================================
BLUES = px.colors.sequential.Blues_r
LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font=dict(color="#1F4E79", size=13, family="Arial Black"),
    font=dict(color="#444", size=11),
    margin=dict(l=10, r=20, t=42, b=10),
    legend=dict(
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="#DDD",
        borderwidth=1,
        font=dict(size=11),
    ),
)


# ================================================================
# HEADER  –  shows active filters as pills
# ================================================================
pills_html = ""
for label, val in active_filters.items():
    if val != "All":
        pills_html += f"<span class='filter-pill'>{label}: {val}</span>"
if not pills_html:
    pills_html = "<span class='filter-pill'>All Data Selected</span>"

st.markdown(
    f"""
    <div class='main-header'>
        <h1>Optimizing IT Support Team Performance Using Analytics (Supportlytics)</h1>
        <p class='subtitle'>IT Support Analytics Dashboard</p>
        <div>{pills_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================================================
# KPI CARDS  –  recomputed on filtered data
# ================================================================
if len(fdf) > 0:
    avg_res = round(fdf["resolution_hours"].mean(), 2)
    top_cat = fdf["ticket_type"].value_counts().index[0]
    cluster_idx = round(fdf["similarity_score"].mean(), 2)
    top_region = fdf.groupby("region")["resolution_hours"].mean().idxmin()
else:
    avg_res = 0
    top_cat = "N/A"
    cluster_idx = 0
    top_region = "N/A"

kc1, kc2, kc3, kc4, kc5, kc6 = st.columns(6)

kpi_data = [
    (kc1, f"{len(fdf):,}",     "Total Tickets",           "kpi-blue"),
    (kc2, f"{avg_res}h",       "Avg Resolution Time",     "kpi-green"),
    (kc3, top_cat,             "Most Frequent Category",  "kpi-orange"),
    (kc4, f"{cluster_idx}",    "Cluster Similarity Index","kpi-purple"),
    (kc5, top_region,          "Top Performing Region",   "kpi-teal"),
    (kc6, f"{len(unresolved):,}", "High Priority Backlog","kpi-red"),
]

for col, val, label, css in kpi_data:
    fs = "1.75rem" if len(str(val)) < 12 else "0.92rem"
    with col:
        st.markdown(
            f"<div class='kpi-card {css}'>"
            f"<div class='kpi-val' style='font-size:{fs};'>{val}</div>"
            f"<div class='kpi-label'>{label}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ================================================================
# TABS
# ================================================================
tab1, tab2, tab4 = st.tabs(
    [
        "Performance Trends",
        "Geographic Insights",
        "Unresolved Issues",
    ]
)

# ────────────────────────────────────────────────────────────────
# TAB 1 – PERFORMANCE TRENDS
# ────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(
        "<div class='sec-hdr'><h3>"
        "Performance Trend Analysis — Resolution Times, Team Efficiency & Priority Breakdown"
        "</h3></div>",
        unsafe_allow_html=True,
    )

    if len(fdf) == 0:
        st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    else:
        # Row 1
        r1c1, r1c2 = st.columns(2)

        with r1c1:
            pord = [
                p for p in ["Low", "Medium", "High", "Critical"]
                if p in fdf["ticket_priority"].unique()
            ]
            p1 = (
                fdf.groupby("ticket_priority")["resolution_hours"]
                .mean()
                .reindex(pord)
                .reset_index()
                .dropna()
            )
            p1.columns = ["Priority", "Avg Hours"]
            if len(p1) > 0:
                fig = px.bar(
                    p1, x="Avg Hours", y="Priority", orientation="h",
                    color="Priority", color_discrete_sequence=BLUES,
                    title="1. Avg Resolution Time by Priority",
                    text="Avg Hours",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}h",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        with r1c2:
            p2 = (
                fdf.groupby("ticket_type")["resolution_hours"]
                .mean()
                .sort_values()
                .reset_index()
                .dropna()
            )
            p2.columns = ["Ticket Type", "Avg Hours"]
            if len(p2) > 0:
                fig = px.bar(
                    p2, x="Avg Hours", y="Ticket Type", orientation="h",
                    color="Ticket Type", color_discrete_sequence=BLUES,
                    title="2. Avg Resolution Time by Ticket Type",
                    text="Avg Hours",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}h",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        # Row 2
        r2c1, r2c2 = st.columns(2)

        with r2c1:
            p3 = (
                fdf.groupby("cluster")["resolution_hours"]
                .mean()
                .sort_values()
                .reset_index()
                .dropna()
            )
            p3.columns = ["Channel", "Avg Hours"]
            if len(p3) > 0:
                fig = px.bar(
                    p3, x="Avg Hours", y="Channel", orientation="h",
                    color="Channel", color_discrete_sequence=BLUES,
                    title="3. Team Efficiency — Fastest Channels",
                    text="Avg Hours",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}h",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        with r2c2:
            p4 = (
                fdf.groupby("region")["resolution_hours"]
                .mean()
                .sort_values()
                .reset_index()
                .dropna()
            )
            p4.columns = ["Region", "Avg Hours"]
            if len(p4) > 0:
                mean_v = p4["Avg Hours"].mean()
                fig = px.bar(
                    p4, x="Avg Hours", y="Region", orientation="h",
                    color="Region", color_discrete_sequence=BLUES,
                    title="4. Fastest Region by Resolution Time",
                    text="Avg Hours",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}h",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.add_vline(
                    x=mean_v, line_dash="dash", line_color="red",
                    annotation_text=f"Mean: {mean_v:.1f}h",
                    annotation_position="top right",
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        # Row 3
        r3c1, r3c2 = st.columns(2)

        with r3c1:
            monthly = (
                fdf.groupby("year_month")["resolution_hours"]
                .mean()
                .reset_index()
                .dropna()
            )
            monthly.columns = ["Month", "Avg Hours"]
            if len(monthly) > 0:
                fig = px.line(
                    monthly, x="Month", y="Avg Hours",
                    title="5. Monthly Resolution Time Trend",
                    markers=True,
                    color_discrete_sequence=["#2E75B6"],
                )
                fig.add_hline(
                    y=monthly["Avg Hours"].mean(),
                    line_dash="dash", line_color="red",
                    annotation_text=f"Mean: {monthly['Avg Hours'].mean():.2f}h",
                )
                fig.update_traces(line_width=2.5, marker_size=7)
                fig.update_layout(**LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

        with r3c2:
            p6 = (
                fdf.groupby(["ticket_priority", "ticket_status"])["ticket_id"]
                .count()
                .reset_index()
            )
            p6.columns = ["Priority", "Status", "Count"]
            if len(p6) > 0:
                fig = px.bar(
                    p6, x="Priority", y="Count", color="Status",
                    title="6. Ticket Status Distribution by Priority",
                    barmode="stack",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    category_orders={
                        "Priority": ["Low", "Medium", "High", "Critical"]
                    },
                )
                fig.update_layout(**LAYOUT)
                st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────────────────────────────────
# TAB 2 – GEOGRAPHIC INSIGHTS
# ────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        "<div class='sec-hdr'><h3>"
        "Geographic & Category-Level Insights — Heatmaps, World Map & Performance by Region"
        "</h3></div>",
        unsafe_allow_html=True,
    )

    if len(fdf) == 0:
        st.warning("No data matches the selected filters.")
    else:
        g1c1, g1c2 = st.columns(2)

        with g1c1:
            heat1 = pd.crosstab(fdf["region"], fdf["ticket_type"])
            fig = px.imshow(
                heat1, color_continuous_scale="Blues",
                title="1. Heatmap — Region vs Ticket Type",
                text_auto=True, aspect="auto",
            )
            fig.update_layout(**LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with g1c2:
            pord = [
                p for p in ["Low", "Medium", "High", "Critical"]
                if p in fdf["ticket_priority"].unique()
            ]
            heat2 = pd.crosstab(fdf["region"], fdf["ticket_priority"])
            heat2 = heat2[[c for c in pord if c in heat2.columns]]
            fig = px.imshow(
                heat2, color_continuous_scale="Oranges",
                title="2. Heatmap — Region vs Ticket Priority",
                text_auto=True, aspect="auto",
            )
            fig.update_layout(**LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        # World map – Other Global excluded for clarity
        map_src = geo_df if len(geo_df) > 0 else fdf.dropna(subset=["latitude", "longitude"])
        if len(map_src) > 0:
            fig = px.scatter_geo(
                map_src,
                lat="latitude", lon="longitude",
                color="ticket_type", size="cluster_size",
                hover_name="region",
                hover_data={
                    "ticket_priority": True,
                    "resolution_hours": ":.2f",
                    "latitude": False,
                    "longitude": False,
                },
                title="3. Geographic Distribution of IT Support Tickets by Category",
                projection="natural earth",
                color_discrete_sequence=px.colors.qualitative.Set1,
            )
            fig.update_layout(**LAYOUT, height=430)
            st.plotly_chart(fig, use_container_width=True)

        g2c1, g2c2 = st.columns(2)

        with g2c1:
            p3 = (
                fdf.groupby("region")["performance_score"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
                .dropna()
            )
            p3.columns = ["Region", "Avg Score"]
            if len(p3) > 0:
                fig = px.bar(
                    p3, x="Avg Score", y="Region", orientation="h",
                    color="Region", color_discrete_sequence=BLUES,
                    title="4. Avg Performance Score by Region",
                    text="Avg Score",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        with g2c2:
            p4 = (
                fdf.groupby("ticket_type")["performance_score"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
                .dropna()
            )
            p4.columns = ["Ticket Type", "Avg Score"]
            if len(p4) > 0:
                fig = px.bar(
                    p4, x="Avg Score", y="Ticket Type", orientation="h",
                    color="Ticket Type", color_discrete_sequence=BLUES,
                    title="5. Avg Performance Score by Ticket Type",
                    text="Avg Score",
                )
                fig.update_traces(
                    texttemplate="%{text:.2f}",
                    textposition="outside",
                    marker_line_width=0,
                )
                fig.update_layout(**LAYOUT, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        sd = (
            fdf.groupby("region")
            .agg(
                cluster_size=("cluster_size", "mean"),
                performance_score=("performance_score", "mean"),
                ticket_count=("ticket_id", "count"),
            )
            .reset_index()
            .dropna()
        )
        sd.columns = ["Region", "Cluster Size", "Performance Score", "Ticket Count"]
        if len(sd) > 0:
            fig = px.scatter(
                sd, x="Cluster Size", y="Performance Score",
                size="Ticket Count", color="Region", text="Region",
                title="6. Cluster Size vs Performance Score by Region",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_traces(textposition="top center")
            fig.update_layout(**LAYOUT, height=380)
            st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────────────────────────────────
# TAB 4 – UNRESOLVED ISSUES
# ────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        "<div class='sec-hdr'><h3>"
        "High Priority Unresolved Issues — Backlog Analysis & Ticket Details"
        "</h3></div>",
        unsafe_allow_html=True,
    )

    crit_count = len(unresolved[unresolved["ticket_priority"] == "Critical"])
    high_count = len(unresolved[unresolved["ticket_priority"] == "High"])
    top_bl = (
        unresolved["region"].value_counts().index[0]
        if len(unresolved) > 0 else "N/A"
    )

    uk1, uk2, uk3, uk4 = st.columns(4)
    for col, val, label, css in [
        (uk1, f"{len(unresolved):,}", "Total Backlog",          "kpi-red"),
        (uk2, f"{crit_count:,}",      "Critical Tickets",       "kpi-red"),
        (uk3, f"{high_count:,}",      "High Priority Tickets",  "kpi-orange"),
        (uk4, top_bl,                 "Top Backlog Region",      "kpi-blue"),
    ]:
        fs = "1.75rem" if len(str(val)) < 12 else "0.92rem"
        with col:
            st.markdown(
                f"<div class='kpi-card {css}'>"
                f"<div class='kpi-val' style='font-size:{fs};'>{val}</div>"
                f"<div class='kpi-label'>{label}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    if len(unresolved) == 0:
        st.success("No high priority unresolved tickets for the selected filters.")
    else:
        u1c1, u1c2 = st.columns(2)

        with u1c1:
            pend = unresolved["ticket_priority"].value_counts().reset_index()
            pend.columns = ["Priority", "Count"]
            fig = px.bar(
                pend, x="Priority", y="Count",
                color="Priority",
                color_discrete_map={"Critical": "#C0392B", "High": "#E74C3C"},
                title="1. Unresolved Tickets by Priority",
                text="Count",
            )
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
            )
            fig.update_layout(**LAYOUT, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with u1c2:
            pend_r = (
                unresolved.groupby("region")["ticket_id"]
                .count()
                .sort_values()
                .reset_index()
            )
            pend_r.columns = ["Region", "Count"]
            fig = px.bar(
                pend_r, x="Count", y="Region", orientation="h",
                color="Region",
                color_discrete_sequence=px.colors.sequential.Reds_r,
                title="2. Unresolved High Priority by Region",
                text="Count",
            )
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
            )
            fig.update_layout(**LAYOUT, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        u2c1, u2c2 = st.columns(2)

        with u2c1:
            pend_t = (
                unresolved.groupby("ticket_type")["ticket_id"]
                .count()
                .sort_values()
                .reset_index()
            )
            pend_t.columns = ["Ticket Type", "Count"]
            fig = px.bar(
                pend_t, x="Count", y="Ticket Type", orientation="h",
                color="Ticket Type",
                color_discrete_sequence=px.colors.sequential.Reds_r,
                title="3. Unresolved Tickets by Type",
                text="Count",
            )
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
            )
            fig.update_layout(**LAYOUT, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with u2c2:
            pend_c = (
                unresolved.groupby("cluster")["ticket_id"]
                .count()
                .sort_values()
                .reset_index()
            )
            pend_c.columns = ["Channel", "Count"]
            fig = px.bar(
                pend_c, x="Count", y="Channel", orientation="h",
                color="Channel",
                color_discrete_sequence=px.colors.sequential.Reds_r,
                title="4. Unresolved Tickets by Channel",
                text="Count",
            )
            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
            )
            fig.update_layout(**LAYOUT, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # Ticket details table
    st.markdown(
        "<div class='sec-hdr'><h3>Unresolved Ticket Details (Top 100)</h3></div>",
        unsafe_allow_html=True,
    )
    cols_show = [
        "ticket_id", "ticket_type", "ticket_priority",
        "ticket_status", "region", "ticket_channel",
    ]
    avail = [c for c in cols_show if c in unresolved.columns]
    if len(unresolved) > 0:
        disp = (
            unresolved[avail]
            .sort_values("ticket_priority")
            .head(100)
            .reset_index(drop=True)
            .fillna("—")
        )
        st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.success("No unresolved tickets for selected filters.")

# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.markdown(
    "<div class='footer'>"
    "<b>Optimizing IT Support Team Performance Using Analytics (Supportlytics)</b> &nbsp;|&nbsp; "
    "Built with Streamlit &amp; Plotly"
    "</div>",
    unsafe_allow_html=True,
)

# ================================================================
# AUTO-REFRESH  –  triggers rerun every REFRESH_INTERVAL seconds
# ================================================================
if auto_refresh:
    time.sleep(REFRESH_INTERVAL)
    st.rerun()
