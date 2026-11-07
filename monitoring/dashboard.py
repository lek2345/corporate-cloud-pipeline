
import time
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


# -------------------- CONFIGURATION --------------------

APP_URL = "http://100.31.99.241"
HEALTH_URL = f"{APP_URL}/health"

REFRESH_INTERVAL = 30
REQUEST_TIMEOUT = 60
MAX_HISTORY = 50
LATENCY_THRESHOLD = 1000


st.set_page_config(
    page_title="NEXUS CLOUDOPS | Command Center",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------- THEME --------------------

st.markdown("""
<style>
.stApp {
    background: #101512;
    color: #E6F0E9;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label, span {
    color: #E6F0E9;
}

[data-testid="stSidebar"] {
    background: #171F1A;
    border-right: 1px solid #304438;
}

[data-testid="stSidebar"] h2 {
    color: #8BE0A6;
    letter-spacing: 2px;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #A9BCAF;
}

.hero {
    background: linear-gradient(120deg, #1B3023, #203B2B, #15291F);
    border: 1px solid #41694D;
    border-radius: 18px;
    padding: 28px;
    margin: 12px 0 24px;
}

.hero-tag, .section-tag {
    color: #8BE0A6;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    color: #F1FFF4;
    font-size: 34px;
    font-weight: 800;
    margin-top: 9px;
}

.hero-subtitle {
    color: #B6CFBD;
    font-size: 14px;
    margin-top: 9px;
    line-height: 1.8;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1D2B22, #17231B);
    border: 1px solid #355441;
    border-radius: 15px;
    padding: 20px 18px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #A8C2AE;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #E9FFEF;
    font-size: 27px;
    font-weight: 750;
}

.info-panel {
    background: #1A261E;
    border: 1px solid #344E3B;
    border-radius: 14px;
    padding: 20px;
    min-height: 190px;
    margin-bottom: 12px;
}

.info-title {
    color: #91DDA7;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 12px;
}

.info-content {
    color: #D0DFD3;
    font-size: 14px;
    line-height: 2;
}

div.stButton > button {
    background: #287A49;
    color: white;
    border: 1px solid #4DA76B;
    border-radius: 9px;
    font-weight: 650;
}

div.stButton > button:hover {
    background: #35945A;
    color: white;
    border-color: #75D493;
}

div.stDownloadButton > button {
    background: #234B32;
    color: #DFFFE8;
    border: 1px solid #4B8D60;
}

[data-testid="stRadio"] label {
    color: #C5D8CA;
}

hr {
    border-color: #344B3A;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

.status-line {
    background: #1C2D21;
    border: 1px solid #42674B;
    border-radius: 11px;
    padding: 14px 18px;
    color: #B8E9C5;
    font-size: 14px;
    font-weight: 650;
    margin-bottom: 18px;
}

.endpoint-request {
    background: #17231B !important;
    color: #B8E9C5 !important;
    border: 1px solid #355441;
    border-radius: 10px;
    padding: 16px;
    font-family: monospace;
    overflow-wrap: anywhere;
}

.nexus-table-wrap {
    width: 100%;
    overflow-x: auto;
    background: #17231B !important;
    border: 1px solid #355441;
    border-radius: 12px;
    margin-top: 10px;
    margin-bottom: 18px;
}

table.nexus-table {
    width: 100%;
    border-collapse: collapse;
    background: #17231B !important;
    color: #E6F0E9 !important;
    font-size: 14px;
}

table.nexus-table thead th {
    background: #203B2B !important;
    color: #8BE0A6 !important;
    padding: 14px;
    text-align: left;
    border-bottom: 1px solid #41694D;
    white-space: nowrap;
}

table.nexus-table tbody td {
    background: #17231B !important;
    color: #E6F0E9 !important;
    padding: 13px 14px;
    border-bottom: 1px solid #304438;
}

table.nexus-table tbody tr:nth-child(even) td {
    background: #1A261E !important;
}

table.nexus-table tbody tr:hover td {
    background: #294332 !important;
    color: #FFFFFF !important;
}

.footer {
    text-align: center;
    color: #809987;
    font-size: 11px;
    letter-spacing: 1px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- DARK TABLE FUNCTION --------------------

def render_dark_table(dataframe):

    table_html = dataframe.to_html(
        index=False,
        escape=True,
        border=0,
        classes="nexus-table"
    )

    st.markdown(
        f"""
        <div class="nexus-table-wrap">
            {table_html}
        </div>
        """,
        unsafe_allow_html=True
    )



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
    st.caption("Hosting Platform: AWS EC2")
    st.caption("Application: Flask")
    st.caption("Dashboard: Streamlit")

    st.divider()

    st.markdown("**Monitoring interval**")
    st.caption("Automatic check every 30 seconds")

# -------------------- SESSION STATE --------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "last_error" not in st.session_state:
    st.session_state.last_error = None


if "history" not in st.session_state:
    st.session_state.history = []

if "last_error" not in st.session_state:
    st.session_state.last_error = "None"

if "last_checked" not in st.session_state:
    st.session_state.last_checked = "Not checked yet"


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.markdown("## 🟢 NEXUS")
    st.caption("EMERALD CLOUD INTELLIGENCE")

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "NAVIGATION",
        [
            "Application Overview",
            "Performance Analytics",
            "Service Diagnostics",
            "Activity History"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### DEPLOYMENT PROFILE")

    st.caption("CLOUD PLATFORM")
    st.markdown("**Render Cloud**")

    st.caption("BACKEND FRAMEWORK")
    st.markdown("**Python Flask**")

    st.caption("DASHBOARD ENGINE")
    st.markdown("**Streamlit**")

    st.caption("CI/CD AUTOMATION")
    st.markdown("**GitHub Actions**")

    st.divider()

    st.markdown("### MONITORING ENGINE")
    st.markdown("🟢 Automatic health checks")

    st.caption(
        f"Refresh interval: {REFRESH_INTERVAL} seconds"
    )

    st.caption(
        f"History retention: {MAX_HISTORY} checks"
    )

    st.divider()

    st.markdown("### ENVIRONMENT")
    st.markdown("🟢 Production endpoint")
    st.caption("HTTPS connection")
    st.caption("NEXUS CLOUDOPS v3.0")


# -------------------- MAIN HEADER --------------------

st.markdown(
    '<div class="section-tag">'
    'INFRASTRUCTURE INTELLIGENCE / DEVOPS / OBSERVABILITY'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero">
    <div class="hero-tag">ENTERPRISE CLOUD OPERATIONS</div>
    <div class="hero-title">🟢 NEXUS CLOUDOPS</div>
    <div class="hero-subtitle">
        Intelligent Infrastructure Command Center<br>
        Application monitoring &nbsp; | &nbsp;
        Performance intelligence &nbsp; | &nbsp;
        Service reliability
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- MONITORING ENGINE --------------------

@st.fragment(run_every=f"{REFRESH_INTERVAL}s")
def monitoring_engine():

    # Make one request to the Flask health endpoint.

    start_time = time.perf_counter()

    try:

        response = requests.get(
            HEALTH_URL,
            timeout=REQUEST_TIMEOUT
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        http_code = response.status_code

        try:
            data = response.json()
        except ValueError:
            data = {}

        success = (
            http_code == 200
            and data.get("status") == "healthy"
        )

        status = "ONLINE" if success else "ERROR"
        health = "HEALTHY" if success else "UNHEALTHY"

        error_message = (
            "None"
            if success
            else f"HTTP {http_code}: Health check failed"
        )

    except requests.RequestException as error:

        response = None
        response_time = None
        http_code = "N/A"
        success = False
        status = "OFFLINE"
        health = "UNAVAILABLE"

        error_message = str(error)[:200]

    # Save this check in the current Streamlit session.

    now = datetime.now()

    st.session_state.last_checked = now.strftime(
        "%d %b %Y | %H:%M:%S"
    )

    st.session_state.last_error = error_message

    st.session_state.history.append({

        "Timestamp": now,
        "Date": now.strftime("%d-%m-%Y"),
        "Time": now.strftime("%H:%M:%S"),
        "Response Time (ms)": response_time,
        "HTTP Status": http_code,
        "Result": "SUCCESS" if success else "FAILED",
        "Successful": success

    })

    st.session_state.history = (
        st.session_state.history[-MAX_HISTORY:]
    )

    history = st.session_state.history

    # Calculate statistics.

    total = len(history)

    passed = sum(
        row["Successful"] for row in history
    )

    failed = total - passed

    uptime = (
        passed / total * 100
        if total
        else 0
    )

    valid_times = [
        row["Response Time (ms)"]
        for row in history
        if row["Response Time (ms)"] is not None
    ]

    avg_latency = (
        sum(valid_times) / len(valid_times)
        if valid_times else 0
    )

    fastest = min(valid_times) if valid_times else 0
    slowest = max(valid_times) if valid_times else 0

    p95 = (
        pd.Series(valid_times).quantile(0.95)
        if valid_times else 0
    )

    # Status bar and manual refresh.

    left, right = st.columns([5, 1])

    with left:
<<<<<<< HEAD
        st.markdown("### Flask Application")
        st.write("**Platform:** AWS EC2")
        st.write("**Framework:** Flask")
        st.write("**Service:** Corporate Cloud Pipeline")
        st.write("**Status:**", status)

        st.markdown(
            f"[Open Application]({APP_URL})"
=======

        st.markdown(
            f"**LAST SYSTEM CHECK:** "
            f"{st.session_state.last_checked}"
>>>>>>> 0816ab0 (Fix monitoring dashboard errors and UI)
        )

    with right:

        if st.button(
            "↻ Refresh Now",
            use_container_width=True
        ):
            st.rerun()

    if success:

        st.markdown(
<<<<<<< HEAD
           f"[Test Health Endpoint]({HEALTH_URL})"
=======
            '<div class="status-line">'
            '🟢 SYSTEM OPERATIONAL — '
            'Application health verification successful'
            '</div>',
            unsafe_allow_html=True
>>>>>>> 0816ab0 (Fix monitoring dashboard errors and UI)
        )

    else:

        st.error(
            "🔴 SYSTEM ALERT — "
            "Application health verification failed"
        )

    # ==================== APPLICATION OVERVIEW ====================

    if page == "Application Overview":

        st.markdown("## ◈ Application Overview")

        st.caption(
            "Real-time status of your deployed corporate application"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Application Status",
            status,
            "Live endpoint check"
        )

        c2.metric("Health Status", health)

        c3.metric("HTTP Response Code", str(http_code))

        c4.metric(
            "Response Latency",
            f"{response_time:.2f} ms"
            if response_time is not None
            else "N/A"
        )

        st.divider()

        st.markdown("## ◈ Operational Summary")

        a, b, c, d = st.columns(4)

        a.metric("Total Checks", total)
        b.metric("Successful Checks", passed)
        c.metric("Failed Checks", failed)
        d.metric("Observed Uptime", f"{uptime:.2f}%")

        st.caption(
            f"Observed uptime uses the latest {MAX_HISTORY} "
            "checks in this dashboard session. "
            "It is not lifetime production uptime."
        )

        st.divider()

        st.markdown("## ◈ Infrastructure Overview")

        left, right = st.columns(2)

        with left:

            st.markdown("""
            <div class="info-panel">
                <div class="info-title">
                    ☁️ APPLICATION SERVICE
                </div>
                <div class="info-content">
                    <b>Application:</b> Corporate Cloud Pipeline<br>
                    <b>Framework:</b> Python Flask<br>
                    <b>Cloud Hosting:</b> Render<br>
                    <b>Protocol:</b> HTTPS<br>
                    <b>Service:</b> Production Application
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"[↗ Open Deployed Application]({APP_URL})"
            )

        with right:

            st.markdown(f"""
            <div class="info-panel">
                <div class="info-title">
                    🔗 HEALTH MONITORING
                </div>
                <div class="info-content">
                    <b>Endpoint:</b> /health<br>
                    <b>HTTP Status:</b> {http_code}<br>
                    <b>Health:</b> {health}<br>
                    <b>Last Verified:</b> {st.session_state.last_checked}<br>
                    <b>Monitoring:</b> Automatic
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"[↗ Test Health Endpoint]({HEALTH_URL})"
            )

        st.divider()

        st.markdown("## ◈ Recent Monitoring Events")

        if history:

            recent = pd.DataFrame(history[::-1])

            render_dark_table(
                recent[
                    [
                        "Date",
                        "Time",
                        "Response Time (ms)",
                        "HTTP Status",
                        "Result"
                    ]
                ].head(5)
            )

        else:

            st.info("Waiting for monitoring activity.")

    # ==================== PERFORMANCE ANALYTICS ====================

    elif page == "Performance Analytics":

        st.markdown("## ◈ Performance Intelligence")

        st.caption(
            "Analyze application latency and response performance"
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Average Latency",
            f"{avg_latency:.2f} ms"
        )

        b.metric(
            "Fastest Response",
            f"{fastest:.2f} ms"
        )

        c.metric(
            "Slowest Response",
            f"{slowest:.2f} ms"
        )

        d.metric(
            "P95 Latency",
            f"{p95:.2f} ms"
        )

        st.divider()

        st.markdown("### ⚡ Response Time Analysis")

        st.caption(
            "Historical response time across recent health checks"
        )

        if valid_times:

            chart_data = pd.DataFrame([
                {
                    "Timestamp": row["Timestamp"],
                    "Response Time (ms)": row["Response Time (ms)"]
                }
                for row in history
                if row["Response Time (ms)"] is not None
            ]).sort_values("Timestamp")

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=chart_data["Timestamp"],
                    y=chart_data["Response Time (ms)"],
                    mode="lines+markers",
                    name="Response Time",
                    line=dict(
                        color="#65D995",
                        width=3
                    ),
                    marker=dict(size=7)
                )
            )

            fig.add_hline(
                y=LATENCY_THRESHOLD,
                line_dash="dash",
                line_color="#FF5C5C",
                annotation_text=(
                    f"{LATENCY_THRESHOLD} ms Threshold"
                ),
                annotation_position="top right"
            )

            fig.update_layout(
                title="Application Response Performance",
                xaxis_title="Monitoring Time",
                yaxis_title="Response Time (ms)",
                template="plotly_dark",
                paper_bgcolor="#101512",
                plot_bgcolor="#17231B",
                font=dict(color="#E6F0E9"),
                height=420,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=30
                ),
                yaxis=dict(rangemode="tozero"),
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Waiting for performance measurements."
            )

        st.divider()

        st.markdown("### ◈ Latency Assessment")

        if response_time is None:

            st.error(
                "Latency unavailable. Health request failed."
            )

        elif response_time < 300:

            st.success(
                "EXCELLENT — Application response is very fast."
            )

        elif response_time < LATENCY_THRESHOLD:

            st.info(
                "MODERATE — Application response is acceptable."
            )

        else:

            st.warning(
                "HIGH LATENCY — Investigate application performance."
            )

        st.caption(
            "Performance thresholds: Excellent < 300 ms, "
            "Moderate < 1000 ms, High Latency >= 1000 ms."
        )

        st.markdown("### ◈ Performance Health Indicator")

        if response_time is None:

            st.progress(0)

            st.error(
                "Performance data unavailable."
            )

        else:

            score = max(
                0,
                min(100, int(100 - response_time / 20))
            )

            st.progress(score / 100)

            st.metric(
                "Performance Score",
                f"{score}/100"
            )

        st.divider()

        st.markdown("### ◈ Performance Samples")

        if history:

            performance = pd.DataFrame(history[::-1])

            render_dark_table(
                performance[
                    [
                        "Time",
                        "Response Time (ms)",
                        "HTTP Status",
                        "Result"
                    ]
                ]
            )

    # ==================== SERVICE DIAGNOSTICS ====================

    elif page == "Service Diagnostics":

        st.markdown("## ◈ Service Diagnostics")

        st.caption(
            "Inspect application connectivity and endpoint health"
        )

        left, right = st.columns(2)

        with left:

            st.markdown("""
            <div class="info-panel">
                <div class="info-title">
                    ☁️ DEPLOYMENT CONFIGURATION
                </div>
                <div class="info-content">
                    <b>Cloud Platform:</b> Render<br>
                    <b>Backend:</b> Python Flask<br>
                    <b>Dashboard:</b> Streamlit<br>
                    <b>CI/CD:</b> GitHub Actions<br>
                    <b>Protocol:</b> HTTPS<br>
                    <b>Request Method:</b> GET
                </div>
            </div>
            """, unsafe_allow_html=True)

        with right:

            response_time_display = (
                f"{response_time:.2f} ms"
                if response_time is not None
                else "N/A"
            )

            connection_text = (
                "Successful"
                if response is not None
                else "Failed"
            )

            st.markdown(f"""
            <div class="info-panel">
                <div class="info-title">
                    🟢 LIVE DIAGNOSTIC RESULT
                </div>
                <div class="info-content">
                    <b>Application:</b> {status}<br>
                    <b>Health:</b> {health}<br>
                    <b>HTTP Code:</b> {http_code}<br>
                    <b>Response Time:</b> {response_time_display}<br>
                    <b>Connection:</b> {connection_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### ◈ Endpoint Verification")

        st.caption("Health monitoring request")

        st.markdown(
            f"""
            <div class="endpoint-request">
                <span style="color:#65D995;font-weight:bold;">
                    GET
                </span>
                {HEALTH_URL}
            </div>
            """,
            unsafe_allow_html=True
        )

        if success:

            st.success(
                "Endpoint verification passed. "
                "HTTP 200 and expected healthy status received."
            )

        else:

            st.error(
                "Endpoint verification failed."
            )

            st.caption(
                f"Diagnostic details: "
                f"{st.session_state.last_error}"
            )

        st.markdown("### ◈ Application Links")

        st.markdown(
            f"[↗ Open Application]({APP_URL})"
        )

        st.markdown(
            f"[↗ Verify Health Endpoint]({HEALTH_URL})"
        )

        st.divider()

        st.markdown("### ◈ Monitoring Configuration")

        st.write(
            f"Automatic refresh: Every {REFRESH_INTERVAL} seconds"
        )

        st.write(
            f"Request timeout: {REQUEST_TIMEOUT} seconds"
        )

        st.write(
            f"Maximum history: {MAX_HISTORY} records"
        )

    # ==================== ACTIVITY HISTORY ====================

    elif page == "Activity History":

        st.markdown("## ◈ Monitoring Event Journal")

        st.caption(
            "Historical records of application health verification"
        )

        a, b, c = st.columns(3)

        a.metric("Total Events", total)
        b.metric("Successful Events", passed)
        c.metric("Failed Events", failed)

        st.divider()

        if history:

            logs = pd.DataFrame(history[::-1])

            st.markdown("### Recent Event Records")

            render_dark_table(
                logs[
                    [
                        "Date",
                        "Time",
                        "HTTP Status",
                        "Response Time (ms)",
                        "Result"
                    ]
                ]
            )

            csv_data = logs.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇ Download Monitoring Report",
                data=csv_data,
                file_name="nexus_cloudops_monitoring.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.info(
                "No monitoring records are available yet."
            )

        st.divider()

        st.markdown("### ◈ Session Management")

        if st.button("Clear Monitoring History"):

            st.session_state.history = []

            st.rerun()

        st.caption(
            "Clearing history removes the records stored "
            "in the current dashboard session."
        )

    # -------------------- FOOTER --------------------

    st.divider()

    st.markdown("""
    <div class="footer">
        NEXUS CLOUDOPS &nbsp; | &nbsp;
        CORPORATE CLOUD DEPLOYMENT PIPELINE
        <br><br>
        ENTERPRISE INFRASTRUCTURE MONITORING
        &nbsp; • &nbsp; VERSION 3.0
    </div>
    """, unsafe_allow_html=True)


# -------------------- START DASHBOARD --------------------

monitoring_engine()
