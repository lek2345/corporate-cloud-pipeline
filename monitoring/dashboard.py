
import streamlit as st
import requests
import time
from datetime import datetime

APP_URL = "https://corporate-cloud-pipeline.onrender.com"
HEALTH_URL = f"{APP_URL}/health"

st.set_page_config(
    page_title="Corporate Cloud Monitoring",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Corporate Cloud Monitoring Dashboard")
st.caption("Live monitoring of your deployed Flask application")

if "history" not in st.session_state:
    st.session_state.history = []

@st.fragment(run_every="30s")
def monitoring_panel():

    start_time = time.perf_counter()

    try:
        response = requests.get(HEALTH_URL, timeout=60)
        response_time = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        success = response.status_code == 200

        if success:
            status = "Online"
            health = response.json().get("status", "Unknown")
        else:
            status = "Error"
            health = "Unhealthy"

        http_code = response.status_code

    except requests.RequestException:
        response_time = None
        status = "Offline"
        health = "Unavailable"
        http_code = "N/A"
        success = False

    checked_at = datetime.now().strftime("%H:%M:%S")

    st.session_state.history.append({
        "Time": checked_at,
        "Response Time (ms)": response_time,
        "Successful": success
    })

    # Keep the latest 50 health checks
    st.session_state.history = st.session_state.history[-50:]

    history = st.session_state.history

    total_checks = len(history)
    successful_checks = sum(
        item["Successful"] for item in history
    )
    failed_checks = total_checks - successful_checks

    uptime = (
        successful_checks / total_checks * 100
        if total_checks else 0
    )

    st.subheader("Application Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Application Status", status)
    col2.metric("Health Check", health)
    col3.metric("HTTP Status", str(http_code))
    col4.metric(
        "Response Time",
        f"{response_time:.2f} ms"
        if response_time is not None else "N/A"
    )

    st.divider()

    st.subheader("Monitoring Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Checks", total_checks)
    col2.metric("Successful Checks", successful_checks)
    col3.metric("Failed Checks", failed_checks)

    st.metric("Observed Uptime", f"{uptime:.2f}%")

    st.caption(
        "Uptime is calculated from checks collected during this dashboard session."
    )

    st.divider()

    st.subheader("Response Time History")

    chart_data = [
        item for item in history
        if item["Response Time (ms)"] is not None
    ]

    if chart_data:
        st.line_chart(
            chart_data,
            x="Time",
            y="Response Time (ms)"
        )
    else:
        st.info("No response-time measurements available yet.")

    st.divider()

    st.subheader("Application Details")

    st.write("Application URL:", APP_URL)
    st.write("Health Endpoint:", HEALTH_URL)
    st.write("Last Checked:", checked_at)

    if success:
        st.success("Your cloud application is healthy!")
    else:
        st.error("Application health check failed.")

    st.caption("Next automatic check in approximately 30 seconds.")

monitoring_panel()
