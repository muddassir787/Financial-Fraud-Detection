# Real-Time Financial Fraud Detection System using Apache Flink, Kafka, Cassandra & FastAPI
Overview

This project is a complete real-time financial fraud detection platform built using modern Big Data technologies. It continuously generates financial transactions, streams them through Apache Kafka, processes them with Apache Flink, detects fraudulent activities using multiple fraud detection rules, stores results in Apache Cassandra, exposes REST APIs using FastAPI, and visualizes live analytics through a Streamlit dashboard.

The system demonstrates how modern event-driven architectures can be used to detect suspicious financial transactions in real time.

Architecture
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
Features
Real-time transaction generation
Kafka event streaming
Apache Flink stream processing
Multiple fraud detection rules
Cassandra NoSQL database
FastAPI REST API
Streamlit Analytics Dashboard
Docker Compose deployment
Microservice Architecture
Technology Stack
Technology	Purpose
Python	Core Programming
Apache Kafka	Event Streaming
Apache Flink	Stream Processing
Apache Cassandra	NoSQL Database
FastAPI	Backend REST API
Streamlit	Dashboard
Docker	Containerization
Docker Compose	Service Orchestration
Project Structure
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
│   ├── fraud_detector.py
│   ├── fraud_rules.py
│   ├── utils.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── cassandra/
│   └── init.cql
│
├── docker-compose.yml
├── README.md
└── requirements.txt
Fraud Detection Rules

The system currently detects fraud using multiple business rules.

1. High Amount Detection

Transactions exceeding the predefined threshold are marked as suspicious.

Example

Amount > $5000
2. Velocity Check

If a customer performs multiple transactions within a short period, the transaction is considered suspicious.

Example

More than 3 transactions in 60 seconds
3. Impossible Travel Detection

If the same card is used from two geographically distant locations within an impossible travel time, fraud is detected.

Uses the Haversine Distance Formula.

Data Flow
Generator

↓

Kafka Topic

↓

Apache Flink

↓

Fraud Rules

↓

Cassandra Database

↓

FastAPI

↓

Streamlit Dashboard
Dashboard

The dashboard provides:

Total Transactions
Fraud Transactions
Fraud Rate
Total Alerts
Latest Transactions
Fraud Alerts
Transaction Amount Distribution
Fraud vs Genuine Pie Chart
Cassandra Tables
transactions

Stores every processed transaction.

Columns include

Transaction ID
Card Number
Merchant
Amount
Timestamp
Latitude
Longitude
Fraud Status
fraud_alerts

Stores detected fraud alerts.

Includes

Alert ID
Transaction ID
Card Number
Merchant
Amount
Fraud Reason
transactions_by_card

Stores transaction history grouped by card number for velocity and travel detection.

REST API
Health Check
GET /health
Dashboard Statistics
GET /stats
Recent Transactions
GET /transactions
Fraud Alerts
GET /alerts
Dashboard
GET /dashboard
Search by Card
GET /card/{card_number}
Transaction Details
GET /transaction/{transaction_id}
Running the Project
Clone Repository
git clone https://github.com/yourusername/financial-fraud-detection.git

cd financial-fraud-detection
Build Docker Images
docker compose build
Start All Services
docker compose up -d
Verify Running Containers
docker ps

Expected services:

Kafka

Cassandra

Flink JobManager

Flink TaskManager

Generator

Backend

Frontend
Submit Flink Job
docker exec -it flink-jobmanager bash

flink run -py /app/fraud_detector.py
Open Dashboard
Streamlit
http://localhost:8501
FastAPI
http://localhost:8000
Swagger API Documentation
http://localhost:8000/docs
Flink Dashboard
http://localhost:8081
Verify Cassandra Data

Open Cassandra shell

docker exec -it cassandra cqlsh

Use keyspace

USE fraud_detection;

View Transactions

SELECT * FROM transactions LIMIT 10;

View Fraud Alerts

SELECT * FROM fraud_alerts LIMIT 10;
Future Improvements
Machine Learning Fraud Detection
Apache Spark Integration
Redis Caching
Elasticsearch
Kibana Monitoring
Grafana Dashboards
JWT Authentication
Kubernetes Deployment
AWS Deployment
Model Explainability
Email/SMS Fraud Notifications
Learning Outcomes

This project demonstrates practical experience with:

Event-Driven Architecture
Stream Processing
Distributed Systems
Big Data Technologies
Docker Containerization
Microservices
NoSQL Database Design
REST API Development
Real-Time Analytics
Fraud Detection Systems

Author

Muhammad Muddassir Hussain
