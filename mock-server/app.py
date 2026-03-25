 from __future__ import annotations

import json
from math import ceil
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "customers.json"

app = Flask(__name__)


def load_customers() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_pagination() -> tuple[int, int]:
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError as exc:
        raise ValueError("page and limit must be integers") from exc

    if page < 1 or limit < 1:
        raise ValueError("page and limit must be positive integers")
    return page, limit


@app.get("/api/health")
def health() -> tuple[Any, int]:
    return jsonify({"status": "healthy"}), 200


@app.get("/api/customers")
def get_customers() -> tuple[Any, int]:
    try:
        page, limit = parse_pagination()
        customers = load_customers()
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500

    total = len(customers)
    start = (page - 1) * limit
    end = start + limit
    paginated = customers[start:end]

    return jsonify(
        {
            "data": paginated,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": ceil(total / limit) if total else 0,
        }
    ), 200


@app.get("/api/customers/<customer_id>")
def get_customer(customer_id: str) -> tuple[Any, int]:
    try:
        customers = load_customers()
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500

    customer = next((item for item in customers if str(item["customer_id"]) == customer_id), None)
    if customer is None:
        return jsonify({"error": f"Customer {customer_id} not found"}), 404
    return jsonify(customer), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
