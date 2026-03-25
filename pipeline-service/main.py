from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
import requests

from database import SessionLocal, engine
from models.customer import Base, Customer
from services.ingestion import ingest_customers

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post("/api/ingest")
def ingest():
    try:
        records = ingest_customers()
        return {"status": "success", "records_processed": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10):
    db: Session = SessionLocal()
    offset = (page - 1) * limit

    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()

    return {
        "data": [c.__dict__ for c in customers],
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db: Session = SessionLocal()

    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.__dict__
