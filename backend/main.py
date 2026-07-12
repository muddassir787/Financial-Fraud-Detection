from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import CassandraDB
from schemas import (
    Transaction,
    FraudAlert,
    DashboardStats,
    DashboardResponse,
)

app = FastAPI(
    title="Financial Fraud Detection API",
    version="1.0.0",
    description="Backend API for Real-Time Financial Fraud Detection Dashboard"
)

# -------------------------------
# Enable CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Cassandra Connection
# -------------------------------
db = CassandraDB()


# =====================================================
# Home
# =====================================================
@app.get("/")
def home():
    return {
        "message": "Financial Fraud Detection Backend Running",
        "status": "OK"
    }


# =====================================================
# Health Check
# =====================================================
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }


# =====================================================
# Dashboard Statistics
# =====================================================
@app.get("/stats", response_model=DashboardStats)
def get_stats():
    return db.get_dashboard_stats()


# =====================================================
# Recent Transactions
# =====================================================
@app.get(
    "/transactions",
    response_model=list[Transaction]
)
def get_transactions(limit: int = 20):
    return db.get_recent_transactions(limit)


# =====================================================
# Fraud Alerts
# =====================================================
@app.get(
    "/alerts",
    response_model=list[FraudAlert]
)
def get_alerts(limit: int = 20):
    return db.get_recent_alerts(limit)


# =====================================================
# Dashboard Data
# =====================================================
@app.get(
    "/dashboard",
    response_model=DashboardResponse
)
def dashboard():

    stats = db.get_dashboard_stats()

    transactions = db.get_recent_transactions(20)

    alerts = db.get_recent_alerts(20)

    return DashboardResponse(
        stats=stats,
        recent_transactions=transactions,
        recent_alerts=alerts
    )


# =====================================================
# Search by Card Number
# =====================================================
@app.get("/card/{card_number}")
def search_card(card_number: str):

    return {
        "card_number": card_number,
        "transactions": db.get_card_transactions(card_number)
    }


# =====================================================
# Search Transaction
# =====================================================
@app.get("/transaction/{transaction_id}")
def transaction(transaction_id: str):

    return db.get_transaction(transaction_id)


# =====================================================
# Manual Refresh Endpoint
# =====================================================
@app.get("/refresh")
def refresh():

    return {
        "message": "Dashboard refreshed successfully."
    }


# =====================================================
# Run Server
# =====================================================
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )