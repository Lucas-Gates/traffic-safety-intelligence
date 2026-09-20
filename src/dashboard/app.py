import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")

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
    total_crashes = overview.get("total_crashes") or 0
    total_fatalities = overview.get("total_fatalities") or 0
    total_vehicles = overview.get("total_vehicles") or 0
    total_people = overview.get("total_people") or 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fatal Crashes", f"{int(total_crashes):,}")
    col2.metric("Total Fatalities", f"{int(total_fatalities):,}")
    col3.metric("Vehicles Involved", f"{int(total_vehicles):,}")
    col4.metric("Persons Involved", f"{int(total_people):,}")
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

st.subheader("Crash Distribution by Hour: Rural vs. Urban")
res_hourly = requests.get(f"{API_BASE_URL}/analytics/hourly-trends")
if res_hourly.status_code == 200:
    df_hourly = pd.DataFrame(res_hourly.json())
    
    fig_hourly = px.line(
        df_hourly,
        x="hour",
        y=["rural_crashes", "urban_crashes"],
        labels={"hour": "Hour of Day (0-23)", "value": "Crash Count", "variable": "Area Type"},
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

st.subheader("Contributing Factors by Vehicle Make")
min_inv = st.number_input("Minimum Crash Involvements:", min_value=100, max_value=2000, value=500, step=100)
res_makes = requests.get(f"{API_BASE_URL}/analytics/factors/vehicle-makes", params={"min_involvements": min_inv})
if res_makes.status_code == 200:
    df_makes = pd.DataFrame(res_makes.json())
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_speed = px.bar(
            df_makes.sort_values(by="pct_speed_related", ascending=False).head(10),
            x="pct_speed_related",
            y="makename",
            orientation="h",
            labels={"pct_speed_related": "% Speed-Related", "makename": "Vehicle Make"},
            title="Top 10 Makes by Speeding Rate (%)",
            template="plotly_white"
        )
        st.plotly_chart(fig_speed, use_container_width=True)
        
    with col_b:
        fig_alc = px.bar(
            df_makes.sort_values(by="pct_alcohol_involved", ascending=False).head(10),
            x="pct_alcohol_involved",
            y="makename",
            orientation="h",
            labels={"pct_alcohol_involved": "% Alcohol-Involved", "makename": "Vehicle Make"},
            title="Top 10 Makes by Alcohol Involvement Rate (%)",
            template="plotly_white"
        )
        st.plotly_chart(fig_alc, use_container_width=True)