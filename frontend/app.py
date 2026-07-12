import os
import time
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:8000"
)

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------

@st.cache_data(ttl=5)
def load_dashboard():

    response = requests.get(
        f"{BACKEND_URL}/dashboard",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=5)
def load_transactions():

    response = requests.get(
        f"{BACKEND_URL}/transactions",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


@st.cache_data(ttl=5)
def load_alerts():

    response = requests.get(
        f"{BACKEND_URL}/alerts",
        timeout=10
    )

    response.raise_for_status()

    return response.json()


# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("💳 Real-Time Financial Fraud Detection Dashboard")

st.caption(
    "Kafka • PyFlink • Cassandra • FastAPI • Streamlit"
)

# ----------------------------------------------------
# Refresh
# ----------------------------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

try:

    dashboard = load_dashboard()

    stats = dashboard["stats"]

    transactions = dashboard["recent_transactions"]

    alerts = dashboard["recent_alerts"]

except Exception as e:

    st.error(f"Backend not available.\n\n{e}")

    st.stop()

# ----------------------------------------------------
# Metrics
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    stats["total_transactions"]
)

col2.metric(
    "Fraud Transactions",
    stats["total_fraud"]
)

col3.metric(
    "Fraud Rate",
    f"{stats['fraud_rate']:.2f}%"
)

col4.metric(
    "Total Alerts",
    stats["total_alerts"]
)

st.divider()

# ----------------------------------------------------
# Transaction Chart
# ----------------------------------------------------

st.subheader("Transaction Amount Distribution")

if len(transactions) > 0:

    df = pd.DataFrame(transactions)

    fig = px.histogram(
        df,
        x="amount",
        nbins=20,
        title="Transaction Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No transactions found.")

# ----------------------------------------------------
# Fraud Pie Chart
# ----------------------------------------------------

st.subheader("Fraud vs Genuine")

fraud = stats["total_fraud"]

normal = stats["total_transactions"] - fraud

pie = px.pie(
    values=[normal, fraud],
    names=["Normal", "Fraud"],
    title="Fraud Distribution"
)

st.plotly_chart(
    pie,
    use_container_width=True
)

# ----------------------------------------------------
# Recent Transactions
# ----------------------------------------------------

st.subheader("Latest Transactions")

if len(transactions):

    df = pd.DataFrame(transactions)

    st.dataframe(
        df,
        use_container_width=True,
        height=350
    )

else:

    st.warning("No transaction data.")

# ----------------------------------------------------
# Fraud Alerts
# ----------------------------------------------------

st.subheader("Fraud Alerts")

if len(alerts):

    alerts_df = pd.DataFrame(alerts)

    st.dataframe(
        alerts_df,
        use_container_width=True,
        height=250
    )

else:

    st.success("No fraud alerts.")

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.divider()

st.write(
    "Pipeline: Generator → Kafka → PyFlink → Cassandra → FastAPI → Streamlit"
)

st.caption("Auto refresh every 5 seconds.")

time.sleep(5)

st.rerun()