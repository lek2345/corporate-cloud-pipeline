
import streamlit as st
import requests
import time
from datetime import datetime

# ---------------- CONFIGURATION ----------------

APP_URL = "https://corporate-cloud-pipeline.onrender.com"
HEALTH_URL = f"{APP_URL}/health"

st.set_page_config(
    page_title="Corporate Cloud Control Center",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #0B1120;
    color: #F8FAFC;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1, h2, h3, p, label {
    color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background: #111827;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1E293B, #172554);
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC;
}

div.stButton > button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
}

div.stButton > button:hover {
    background: #1D4ED8;
    color: white;
}

hr {
    border-color: #334155;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
# ☁️ CORPORATE CLOUD CONTROL CENTER

### Infrastructure Monitoring & Application Health

Monitor your deployed Flask application through your cloud dashboard.
""")

st.divider()

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## ☁️ CLOUD CONTROL")
    st.caption("DevOps Monitoring Platform")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("🟢 Application Overview")
    st.markdown("📊 Performance Analytics")
    st.markdown("🛡️ Service Health")
    st.markdown("⚙️ Configuration")

    st.divider()

    st.markdown("### Deployment")
    st.caption("Hosting Platform: Render")
    st.caption("Application: Flask")
    st.caption("Dashboard: Streamlit")

    st.divider()

    st.markdown("**Monitoring interval**")
    st.caption("Automatic check every 30 seconds")

# ---------------- MONITORING ----------------

if "history" not in st.session_state:
    st.session_state.history = []

@st.fragment(run_every="30s")
def monitoring_panel():

    start_time = time.perf_counter()

    try:
        response = requests.get(
            HEALTH_URL,
            timeout=60
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000, 2
        )

        http_code = response.status_code
        success = (
            response.status_code == 200
            and response.json().get("status") == "healthy"
        )

        if success:
            status = "ONLINE"
            health = "HEALTHY"
        else:
            status = "ERROR"
            health = "UNHEALTHY"

    except requests.RequestException:
        response_time = None
        http_code = "N/A"
        success = False
        status = "OFFLINE"
        health = "UNAVAILABLE"

    checked_at = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Response Time (ms)": response_time,
        "Successful": success
    })

    st.session_state.history = (
        st.session_state.history[-50:]
    )

    history = st.session_state.history

    total = len(history)
    passed = sum(item["Successful"] for item in history)
    failed = total - passed

    uptime = (passed / total * 100) if total else 0

    # ---------------- STATUS BANNER ----------------

    if success:
        st.success("● ALL SYSTEMS OPERATIONAL")
    else:
        st.error("● APPLICATION HEALTH CHECK FAILED")

    st.markdown("## 📊 Application Overview")

    # ---------------- KPI CARDS ----------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Application Status", status)

    with c2:
        st.metric("Health Check", health)

    with c3:
        st.metric("HTTP Status", str(http_code))

    with c4:
        st.metric(
            "Response Time",
            f"{response_time:.2f} ms"
            if response_time is not None else "N/A"
        )

    st.divider()

    # ---------------- MONITORING STATISTICS ----------------

    st.markdown("## 📈 Monitoring Statistics")

    a, b, c = st.columns(3)

    a.metric("Total Health Checks", total)
    b.metric("Successful Checks", passed)
    c.metric("Failed Checks", failed)

    st.metric("Observed Uptime", f"{uptime:.2f}%")

    st.caption(
        "Uptime is based on checks collected during this dashboard session."
    )

    st.divider()

    # ---------------- PERFORMANCE GRAPH ----------------

    st.markdown("## ⚡ Performance Analytics")
    st.markdown("### Response Time History")

    chart_data = [
        item for item in history
        if item["Response Time (ms)"] is not None
    ]

    if chart_data:
        st.line_chart(
            chart_data,
            x="Time",
            y="Response Time (ms)",
            color="#38BDF8"
        )
    else:
        st.info("Waiting for response-time measurements.")

    st.divider()

    # ---------------- SERVICE DETAILS ----------------

    st.markdown("## 🛡️ Service Health")

    left, right = st.columns(2)

    with left:
        st.markdown("### Flask Application")
        st.write("**Platform:** Render Cloud")
        st.write("**Framework:** Flask")
        st.write("**Service:** Corporate Cloud Pipeline")
        st.write("**Status:**", status)

        st.markdown(
            "[Open Application](https://corporate-cloud-pipeline.onrender.com)"
        )

    with right:
        st.markdown("### Health Endpoint")
        st.write("**Endpoint:** `/health`")
        st.write("**HTTP Code:**", http_code)
        st.write("**Health:**", health)
        st.write("**Last Checked:**", checked_at)

        st.markdown(
            "[Test Health Endpoint](https://corporate-cloud-pipeline.onrender.com/health)"
        )

    st.divider()

    st.caption(
        "Corporate Cloud Deployment Pipeline | "
        "DevOps & CI/CD Monitoring | 2026"
    )

# ---------------- RUN DASHBOARD ----------------

monitoring_panel()
