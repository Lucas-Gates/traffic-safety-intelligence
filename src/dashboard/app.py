import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE_URL = "localhost/api"

st.set_page_config(
    page_title="Traffic Safety Intelligence Platform",
    layout="wide",
)

st.title("Traffic Safety Intelligence Platform")
st.caption("Nationwide Fatal Crash Analysis using NHTSA FARS Data & FastAPI")

@st.cache_data(ttl=60)
def fetch_overview():
    res = requests.get(f"{API_BASE_URL}/stats/overview")
    return res.json() if res.status_code == 200 else None

overview = fetch_overview()

if overview:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fatal Crashes", f"{overview['total_crashes']:,}")
    col2.metric("Total Fatalities", f"{overview['total_fatalities']:,}")
    col3.metric("Vehicles Involved", f"{overview['total_vehicles']:,}")
    col4.metric("Persons Involved", f"{overview['total_people']:,}")
else:
    st.error("Failed to connect to the FastAPI backend. Ensure Uvicorn is running on port 8000.")

st.markdown("---")

st.subheader("State Rankings & Cumulative Fatality Share")

limit = st.slider("Top N States to display:", min_value=5, max_value=50, value=15)
res_states = requests.get(f"{API_BASE_URL}/analytics/state-rankings", params={"limit": limit})

if res_states.status_code == 200:
    df_states = pd.DataFrame(res_states.json())
    
    fig_states = px.bar(
        df_states,
        x="statename",
        y="total_fatal_crashes",
        color="total_fatalities",
        labels={"statename": "State", "total_fatal_crashes": "Fatal Crashes", "total_fatalities": "Fatalities"},
        title="Top States by Total Fatal Crashes",
        template="plotly_white"
    )
    st.plotly_chart(fig_states, use_container_width=True)