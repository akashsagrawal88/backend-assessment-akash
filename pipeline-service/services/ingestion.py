import requests
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert

from database import SessionLocal
from models.customer import Customer

MOCK_SERVER_URL = "http://mock-server:5000/api/customers"


def ingest_customers():
    db = SessionLocal()
    all_customers = []
    page = 1
    limit = 10

    try:
        while True:
            response = requests.get(MOCK_SERVER_URL, params={"page": page, "limit": limit})
            response.raise_for_status()

            payload = response.json()
            customers = payload.get("data", [])

            if not customers:
                break

            all_customers.extend(customers)

            total = payload.get("total", 0)
            if page * limit >= total:
                break

            page += 1

        for customer in all_customers:
            stmt = insert(Customer).values(
                customer_id=customer["customer_id"],
                first_name=customer["first_name"],
                last_name=customer["last_name"],
                email=customer["email"],
                phone=customer.get("phone"),
                address=customer.get("address"),
                date_of_birth=datetime.strptime(customer["date_of_birth"], "%Y-%m-%d").date()
                if customer.get("date_of_birth")
                else None,
                account_balance=customer.get("account_balance"),
                created_at=datetime.fromisoformat(customer["created_at"])
                if customer.get("created_at")
                else None,
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=["customer_id"],
                set_={
                    "first_name": customer["first_name"],
                    "last_name": customer["last_name"],
                    "email": customer["email"],
                    "phone": customer.get("phone"),
                    "address": customer.get("address"),
                    "date_of_birth": datetime.strptime(customer["date_of_birth"], "%Y-%m-%d").date()
                    if customer.get("date_of_birth")
                    else None,
                    "account_balance": customer.get("account_balance"),
                    "created_at": datetime.fromisoformat(customer["created_at"])
                    if customer.get("created_at")
                    else None,
                },
            )

            db.execute(stmt)

        db.commit()
        return len(all_customers)

    finally:
        db.close()
