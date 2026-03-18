import streamlit as st

st.set_page_config(page_title="Supportlytics Dashboard", layout="wide")

st.title("📊 Supportlytics - IT Support Performance Dashboard")

st.write("Power BI Dashboard Embedded Below")

powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiMjlmNTM0OGMtNThhMC00ZTYxLTk2ZjEtMjc1YzJmNzFlOWRhIiwidCI6IjAxMDJhMTE2LWM1NjEtNGM2MS04ZWJmLWUwNzk0YmE5ODY3OSJ9"

st.components.v1.iframe(powerbi_url, height=800, width=1200)