from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==========================
# Transaction Schema
# ==========================
class Transaction(BaseModel):
    transaction_id: str
    timestamp: Optional[datetime] = None
    card_number: str
    amount: float
    merchant: str
    category: str
    latitude: float
    longitude: float
    is_fraud: Optional[bool] = False

    class Config:
        from_attributes = True


# ==========================
# Fraud Alert Schema
# ==========================
class FraudAlert(BaseModel):
    alert_id: str
    transaction_id: str
    timestamp: Optional[datetime] = None
    card_number: str
    amount: float
    merchant: str
    reason: str

    class Config:
        from_attributes = True


# ==========================
# Dashboard Stats
# ==========================
class DashboardStats(BaseModel):
    total_transactions: int
    total_fraud: int
    total_alerts: int
    fraud_rate: float


# ==========================
# Dashboard Response
# ==========================
class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_transactions: list[Transaction]
    recent_alerts: list[FraudAlert]


# ==========================
# Dashboard Summary
# ==========================
class DashboardSummary(BaseModel):
    total_transactions: int
    fraud_transactions: int
    normal_transactions: int
    fraud_rate: float


# ==========================
# API Health
# ==========================
class HealthResponse(BaseModel):
    status: str
    cassandra: str
    kafka: str
    flink: str


# ==========================
# Fraud Statistics
# ==========================
class FraudStats(BaseModel):
    high_amount: int
    velocity: int
    impossible_travel: int


# ==========================
# Card History
# ==========================
class CardHistory(BaseModel):
    card_number: str
    transaction_count: int
    total_amount: float
    fraud_count: int


# ==========================
# Location Statistics
# ==========================
class LocationStats(BaseModel):
    latitude: float
    longitude: float
    transactions: int


# ==========================
# Merchant Statistics
# ==========================
class MerchantStats(BaseModel):
    merchant: str
    transactions: int
    frauds: int


# ==========================
# API Message
# ==========================
class MessageResponse(BaseModel):
    message: str
