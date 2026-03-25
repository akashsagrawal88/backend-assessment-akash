from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models.customer import Customer
from services.ingestion import ingest_customers

app = FastAPI()

Base.metadata.create_all(bind=engine)


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
    try:
        offset = (page - 1) * limit
        customers = db.query(Customer).offset(offset).limit(limit).all()
        total = db.query(Customer).count()

        return {
            "data": [
                {k: v for k, v in c.__dict__.items() if k != "_sa_instance_state"}
                for c in customers
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }
    finally:
        db.close()


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db: Session = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {k: v for k, v in customer.__dict__.items() if k != "_sa_instance_state"}
    finally:
        db.close()
