-- ============================================
-- Create Keyspace
-- ============================================

CREATE KEYSPACE IF NOT EXISTS fraud_detection
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE fraud_detection;

-- ============================================
-- Transactions Table
-- ============================================

CREATE TABLE IF NOT EXISTS transactions (

    bucket int,

    timestamp timestamp,

    transaction_id uuid,

    card_number text,

    amount double,

    merchant text,

    category text,

    latitude double,

    longitude double,

    is_fraud boolean,

    PRIMARY KEY ((bucket), timestamp, transaction_id)

) WITH CLUSTERING ORDER BY (timestamp DESC);



-- ============================================
-- Transactions By Card
-- ============================================

CREATE TABLE IF NOT EXISTS transactions_by_card (

    card_number text,

    timestamp timestamp,

    transaction_id uuid,

    amount double,

    latitude double,

    longitude double,

    PRIMARY KEY ((card_number), timestamp)

) WITH CLUSTERING ORDER BY (timestamp DESC);



-- ============================================
-- Fraud Alerts
-- ============================================

CREATE TABLE IF NOT EXISTS fraud_alerts (

    bucket int,

    timestamp timestamp,

    alert_id uuid,

    transaction_id uuid,

    card_number text,

    amount double,

    merchant text,

    reason text,

    PRIMARY KEY ((bucket), timestamp, alert_id)

) WITH CLUSTERING ORDER BY (timestamp DESC);



-- ============================================
-- Indexes
-- ============================================

CREATE INDEX IF NOT EXISTS idx_transactions_card
ON transactions(card_number);


CREATE INDEX IF NOT EXISTS idx_transactions_fraud
ON transactions(is_fraud);


CREATE INDEX IF NOT EXISTS idx_alert_card
ON fraud_alerts(card_number);



-- ============================================
-- Verify Tables
-- ============================================

DESCRIBE TABLE transactions;

DESCRIBE TABLE transactions_by_card;

DESCRIBE TABLE fraud_alerts;
