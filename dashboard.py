import streamlit as st
import sqlite3
import pandas as pd
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Self-Healing Data Pipeline",
    page_icon="🔧",
    layout="wide"
)

# ==========================================
# PIPELINE CONTROL
# ==========================================

if st.button("Run Pipeline", type="primary"):

    with st.spinner("Running AI Self-Healing Data Pipeline..."):

        result = subprocess.run(
            ["cmd", "/c", str(BASE_DIR / "run_pipeline.bat")],
            capture_output=True,
            text=True
        )

    if result.returncode == 0:

        st.success("Pipeline executed successfully.")
        st.rerun()

    else:

        st.error("Pipeline execution failed.")

    with st.expander("View Pipeline Output"):

        st.code(
            result.stdout + result.stderr
        )

# ==========================================
# TITLE
# ==========================================

st.title("🔧 AI Self-Healing Data Pipeline")
st.subheader("Pipeline Monitoring Dashboard")


# ==========================================
# DATABASE PATH
# ==========================================

DB_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customer_database.db"
)


# ==========================================
# LOAD CUSTOMER DATA
# ==========================================

def load_customer_data():

    if not DB_PATH.exists():
        return pd.DataFrame()

    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM customers",
        connection
    )

    connection.close()

    return df


# ==========================================
# LOAD FAILURE LOGS
# ==========================================

def load_failure_logs():
    
    if not DB_PATH.exists():
        return pd.DataFrame()

    connection = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT
            id AS "Log ID",
            failure_id AS "Failure ID",
            failure_type AS "Failure Type",
            severity AS "Severity",
            root_cause_type AS "Root Cause",
            confidence AS "Confidence",
            healing_action AS "Healing Action",
            status AS "Status",
            detected_at AS "Detected At"
        FROM failure_logs
        ORDER BY id
        """,
        connection
    )

    connection.close()

    return df


# ==========================================
# LOAD DATA
# ==========================================

customer_df = load_customer_data()

failure_df = load_failure_logs()


# ==========================================
# PIPELINE STATUS
# ==========================================

if not customer_df.empty:

    pipeline_status = "SUCCESS"

else:

    pipeline_status = "NO DATA"


# ==========================================
# TOP METRICS
# ==========================================

total_failures = len(failure_df)

total_healed = len(
    failure_df[
        failure_df["Status"] == "HEALED"
    ]
) if not failure_df.empty else 0

total_failed = len(
    failure_df[
        failure_df["Status"] == "FAILED"
    ]
) if not failure_df.empty else 0

total_rows = len(customer_df)

failures_requiring_attention = len(
    failure_df[
        failure_df["Status"] == "FAILED"
    ]
) if not failure_df.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Pipeline Status",
        pipeline_status
    )


with col2:

    st.metric(
        "Total Failures",
        total_failures
    )


with col3:

    st.metric(
        "Failures Healed",
        total_healed
    )


with col4:

    st.metric(
        "Rows Processed",
        total_rows
    )

with col5:

    st.metric(
        "Needs Attention",
        failures_requiring_attention
    )

# ==========================================
# FAILURE SUMMARY
# ==========================================

st.divider()

st.header("Failure Summary")


if not failure_df.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Failures by Type")

        failure_counts = (
            failure_df["Failure Type"]
            .value_counts()
        )

        st.bar_chart(
            failure_counts
        )


    with col2:

        st.subheader("Failure Status")

        status_counts = (
            failure_df["Status"]
            .value_counts()
        )

        st.bar_chart(
            status_counts
        )

else:

    st.info(
        "No failure records available."
    )

# ==========================================
# LATEST AI FAILURE ANALYSIS
# ==========================================

st.divider()

st.header("Latest AI Failure Analysis")

if not failure_df.empty:

    latest_failure = failure_df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Latest Failure",
            latest_failure["Failure Type"]
        )

    with col2:
        st.metric(
            "Severity",
            latest_failure["Severity"]
        )

    with col3:
        st.metric(
            "Status",
            latest_failure["Status"]
        )

    st.subheader("Root Cause Analysis")

    st.write(
        f"**Root Cause:** {latest_failure['Root Cause']}"
    )

    st.write(
        f"**Confidence:** {latest_failure['Confidence']}"
    )

    st.write(
        f"**Healing Action:** {latest_failure['Healing Action']}"
    )

    st.write(
        f"**Detected At:** {latest_failure['Detected At']}"
    )

else:

    st.info(
        "No failure analysis available."
    )

# ==========================================
# FAILURE HISTORY
# ==========================================

st.divider()

st.header("Failure History")


if not failure_df.empty:
    
    # ==========================================
    # FAILURE FILTERS
    # ==========================================

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        failure_type_filter = st.selectbox(
            "Filter by Failure Type",
            ["All"] + sorted(
                failure_df["Failure Type"].dropna().unique().tolist()
            )
        )

    with filter_col2:

        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + sorted(
                failure_df["Status"].dropna().unique().tolist()
            )
        )

    filtered_df = failure_df.copy()

    if failure_type_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Failure Type"] == failure_type_filter
        ]

    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Status"] == status_filter
        ]

    display_columns = [
        "Failure ID",
        "Failure Type",
        "Severity",
        "Root Cause",
        "Confidence",
        "Healing Action",
        "Status",
        "Detected At"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in failure_df.columns
    ]

    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No failure history available."
    )

# ==========================================
# FAILURE REPORT DOWNLOAD
# ==========================================

st.divider()

st.header("Failure Report")

if not failure_df.empty:

    report_df = failure_df.copy()

    csv_data = report_df.to_csv(index=False)

    st.download_button(
        label="Download Failure Report",
        data=csv_data,
        file_name="failure_report.csv",
        mime="text/csv"
    )

else:

    st.info("No failure records available for download.")

# ==========================================
# CUSTOMER DATA
# ==========================================

st.divider()

st.header("Current Customer Data")

if not customer_df.empty:

    st.dataframe(
        customer_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "Customer database is empty or unavailable."
    )
