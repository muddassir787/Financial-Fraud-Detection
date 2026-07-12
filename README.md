# 🚀 Real-Time Financial Fraud Detection System using Apache Flink, Kafka, Cassandra & FastAPI

## 📖 Overview

This project is a complete **real-time financial fraud detection platform** built using modern Big Data technologies.

It continuously generates financial transactions, streams them through **Apache Kafka**, processes them using **Apache Flink**, detects fraudulent activities with multiple fraud detection rules, stores the processed data in **Apache Cassandra**, exposes REST APIs using **FastAPI**, and visualizes live analytics through a **Streamlit Dashboard**.

The system demonstrates how modern **event-driven architectures** can be used to detect suspicious financial transactions in real time.

---

# 🏗️ Architecture

```text
                    +----------------------+
                    | Transaction Generator|
                    +----------+-----------+
                               |
                               | Kafka Producer
                               v
                     +----------------------+
                     |    Apache Kafka      |
                     +----------+-----------+
                                |
                                |
                     Kafka Consumer (PyFlink)
                                |
                                v
                    +-----------------------+
                    | Apache Flink Stream   |
                    | Fraud Detection Job   |
                    +-----------+-----------+
                                |
                                |
                +---------------+----------------+
                |                                |
                |                                |
                v                                v
        Transactions Table               Fraud Alerts
                |                                |
                +---------------+----------------+
                                |
                         Apache Cassandra
                                |
                                |
                       FastAPI Backend API
                                |
                                |
                         Streamlit Dashboard
```

---

# ✨ Features

- Real-time Transaction Generation
- Apache Kafka Event Streaming
- Apache Flink Stream Processing
- Multiple Fraud Detection Rules
- Apache Cassandra NoSQL Database
- FastAPI REST API
- Streamlit Analytics Dashboard
- Docker Compose Deployment
- Microservice Architecture

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Apache Kafka | Event Streaming |
| Apache Flink | Stream Processing |
| Apache Cassandra | NoSQL Database |
| FastAPI | Backend REST API |
| Streamlit | Dashboard |
| Docker | Containerization |
| Docker Compose | Service Orchestration |

---

# 📂 Project Structure

```text
Financial-Fraud-Detection/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── generator/
│   ├── generator.py
│   ├── transaction_generator.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── flink/
│   ├── Dockerfile
│   ├── fraud_detector.py
│   ├── fraud_rules.py
│   ├── utils.py
│   └── requirements.txt
│
├── cassandra/
│   └── init.cql
│
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

# 🔍 Fraud Detection Rules

## 1️⃣ High Amount Detection

Transactions exceeding the predefined threshold are marked as suspicious.

**Example**

```text
Amount > $5000
```

---

## 2️⃣ Velocity Check

If a customer performs multiple transactions within a short period, the transaction is considered suspicious.

**Example**

```text
More than 3 transactions within 60 seconds
```

---

## 3️⃣ Impossible Travel Detection

If the same card is used from two geographically distant locations within an impossible travel time, fraud is detected.

Uses the **Haversine Distance Formula** to calculate travel distance.

---

# 🔄 Data Flow

```text
Transaction Generator
        │
        ▼
Apache Kafka
        │
        ▼
Apache Flink
        │
        ▼
Fraud Detection Rules
        │
        ▼
Apache Cassandra
        │
        ▼
FastAPI Backend
        │
        ▼
Streamlit Dashboard
```

---

# 📊 Dashboard

The dashboard displays:

- Total Transactions
- Fraud Transactions
- Fraud Rate
- Total Fraud Alerts
- Latest Transactions
- Fraud Alerts
- Transaction Amount Distribution
- Fraud vs Genuine Pie Chart

---

# 🗄 Cassandra Database Schema

## transactions

Stores every processed transaction.

Columns:

- Transaction ID
- Card Number
- Merchant
- Amount
- Timestamp
- Latitude
- Longitude
- Fraud Status

---

## fraud_alerts

Stores detected fraud alerts.

Columns:

- Alert ID
- Transaction ID
- Card Number
- Merchant
- Amount
- Fraud Reason

---

## transactions_by_card

Stores transaction history grouped by card number.

Used for:

- Velocity Detection
- Impossible Travel Detection

---

# 🌐 REST API

## Health Check

```http
GET /health
```

---

## Dashboard Statistics

```http
GET /stats
```

---

## Recent Transactions

```http
GET /transactions
```

---

## Fraud Alerts

```http
GET /alerts
```

---

## Dashboard Data

```http
GET /dashboard
```

---

## Search by Card Number

```http
GET /card/{card_number}
```

---

## Transaction Details

```http
GET /transaction/{transaction_id}
```

---

# ▶ Running the Project

## Clone Repository

```bash
git clone https://github.com/muddassir787/Financial-Fraud-Detection.git

cd Financial-Fraud-Detection
```

---

## Build Docker Images

```bash
docker compose build
```

---

## Start All Services

```bash
docker compose up -d
```

---

## Verify Running Containers

```bash
docker ps
```

Expected Containers:

- Kafka
- Cassandra
- Flink JobManager
- Flink TaskManager
- Generator
- Backend
- Frontend

---

## Submit the PyFlink Job

```bash
docker exec -it flink-jobmanager bash

flink run -py /app/fraud_detector.py
```

---

# 🌍 Open the Application

## Streamlit Dashboard

```
http://localhost:8501
```

---

## FastAPI Backend

```
http://localhost:8000
```

---

## Swagger API Documentation

```
http://localhost:8000/docs
```

---

## Apache Flink Dashboard

```
http://localhost:8081
```

---

# 🗃 Verify Cassandra Data

Open Cassandra Shell

```bash
docker exec -it cassandra cqlsh
```

Select Keyspace

```sql
USE fraud_detection;
```

View Transactions

```sql
SELECT * FROM transactions LIMIT 10;
```

View Fraud Alerts

```sql
SELECT * FROM fraud_alerts LIMIT 10;
```

---

# 🚀 Future Improvements

- Machine Learning Based Fraud Detection
- Apache Spark Streaming
- Redis Cache
- Elasticsearch Integration
- Kibana Dashboard
- Grafana Monitoring
- JWT Authentication
- Kubernetes Deployment
- AWS Cloud Deployment
- Explainable AI (XAI)
- Email & SMS Fraud Notifications

---

# 📚 Learning Outcomes

This project demonstrates practical knowledge of:

- Event-Driven Architecture
- Stream Processing
- Distributed Systems
- Big Data Technologies
- Docker Containerization
- Microservices
- Apache Kafka
- Apache Flink
- Apache Cassandra
- REST API Development
- Real-Time Analytics
- Financial Fraud Detection Systems

---

# 👨‍💻 Author

**Muhammad Muddassir Hussain**
