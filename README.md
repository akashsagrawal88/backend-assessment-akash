# Backend Developer Technical Assessment

## 📌 Overview
This project implements a **Dockerized backend data pipeline** using Flask, FastAPI, and PostgreSQL.

It simulates a real-world microservices architecture where data is fetched from one service, processed, stored, and exposed via APIs.

---

## 🔄 Data Flow

Flask API (JSON) → FastAPI Ingestion → PostgreSQL → FastAPI APIs

---

## 🏗️ Tech Stack

- Python (Flask, FastAPI)
- PostgreSQL
- SQLAlchemy ORM
- Docker & Docker Compose

---

## 📂 Project Structure

```bash
backend-assessment-akash/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── data/customers.json
└── pipeline-service/
    ├── main.py
    ├── database.py
    ├── requirements.txt
    ├── Dockerfile
    ├── models/customer.py
    └── services/ingestion.py
```

---

## 🚀 How to Run

```bash
docker compose up -d --build
```

---

## 🔍 API Endpoints

### 🔹 Flask Mock Server (Port 5000)

#### Health Check
```bash
curl http://localhost:5000/api/health
```

#### Get Customers (Paginated)
```bash
curl "http://localhost:5000/api/customers?page=1&limit=5"
```

#### Get Single Customer
```bash
curl http://localhost:5000/api/customers/CUST001
```

---

### 🔹 FastAPI Pipeline Service (Port 8000)

#### 1. Ingest Data from Flask → PostgreSQL
```bash
curl -X POST http://localhost:8000/api/ingest
```

✅ Expected Response:
```json
{"status":"success","records_processed":20}
```

---

#### 2. Get Customers from Database
```bash
curl "http://localhost:8000/api/customers?page=1&limit=5"
```

---

#### 3. Get Single Customer from Database
```bash
curl http://localhost:8000/api/customers/CUST001
```

---

## 📊 API Documentation

Open Swagger UI:

```
http://localhost:8000/docs
```

---

## ⚙️ Key Features

- JSON-based data source (no hardcoding)
- Pagination support (Flask + FastAPI)
- Automatic pagination handling during ingestion
- Upsert logic (prevents duplicate records)
- Clean modular architecture
- Dockerized multi-service setup

---

## 🧠 Design Highlights

- Microservices-based architecture
- Separation of concerns (API, ingestion, DB)
- RESTful API design
- Scalable and containerized setup

---

## ✅ Conclusion

This project demonstrates:
- Backend API development
- Data pipeline implementation
- Database integration with PostgreSQL
- Docker-based microservices architecture

---
