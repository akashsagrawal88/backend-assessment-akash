# Backend Assessment – Data Pipeline

## 🚀 Overview
This project implements a data pipeline using:
- Flask (Mock API)
- FastAPI (Ingestion Service)
- PostgreSQL (Database)
- Docker (Containerization)

Flow:
Flask → FastAPI → PostgreSQL

---

## 📦 Setup Instructions

### 1. Start Services
```bash
docker-compose up -d --build
```
### 2. Test Flask API (Mock Server)
```bash
curl http://localhost:5000/api/customers?page=1&limit=5
```

### 3. Ingest Data into Database
```bash
curl -X POST http://localhost:8000/api/ingest
```

### 4. Fetch Data from Database
```bash
curl http://localhost:8000/api/customers?page=1&limit=5
