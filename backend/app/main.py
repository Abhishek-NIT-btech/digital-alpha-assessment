import math
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TransactionListResponse
from app.summary_schemas import TransactionSummaryResponse
from app.transaction import Transaction


app = FastAPI(
    title="Digital Alpha Transactions API",
    version="1.0.0",
)


# -----------------------------
# CORS configuration
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Health check
# -----------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# -----------------------------
# Get transactions
# -----------------------------

@app.get(
    "/api/transactions",
    response_model=TransactionListResponse,
)
def get_transactions(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: Optional[str] = Query(
        default=None,
    ),
    category: Optional[str] = Query(
        default=None,
    ),
    status: Optional[str] = Query(
        default=None,
    ),
    payment_method: Optional[str] = Query(
        default=None,
    ),
    date_from: Optional[datetime] = Query(
        default=None,
    ),
    date_to: Optional[datetime] = Query(
        default=None,
    ),
    sort_by: str = Query(
        default="id",
    ),
    sort_order: str = Query(
        default="asc",
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    # -----------------------------
    # Search by merchant
    # -----------------------------

    if search:
        query = query.filter(
            Transaction.merchant.ilike(
                f"%{search.strip()}%"
            )
        )

    # -----------------------------
    # Filter by category
    # -----------------------------

    if category:
        query = query.filter(
            Transaction.category == category
        )

    # -----------------------------
    # Filter by status
    # -----------------------------

    if status:
        query = query.filter(
            Transaction.status == status.upper()
        )

    # -----------------------------
    # Filter by payment method
    # -----------------------------

    if payment_method:
        query = query.filter(
            Transaction.payment_method == payment_method
        )

    # -----------------------------
    # Filter by starting date
    # -----------------------------

    if date_from:
        query = query.filter(
            Transaction.timestamp >= date_from
        )

    # -----------------------------
    # Filter by ending date
    # -----------------------------

    if date_to:
        query = query.filter(
            Transaction.timestamp <= date_to
        )

    # -----------------------------
    # Sorting
    # -----------------------------

    allowed_sort_fields = {
        "id": Transaction.id,
        "timestamp": Transaction.timestamp,
        "amount": Transaction.amount,
        "merchant": Transaction.merchant,
    }

    sort_column = allowed_sort_fields.get(
        sort_by.lower()
    )

    if sort_column is None:
        sort_column = Transaction.id

    if sort_order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # -----------------------------
    # Total matching records
    # -----------------------------

    total = query.count()

    # -----------------------------
    # Pagination
    # -----------------------------

    offset = (page - 1) * page_size

    transactions = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # -----------------------------
    # Total pages
    # -----------------------------

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    return {
        "items": transactions,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
    }


# -----------------------------
# Transaction summary
# -----------------------------

@app.get(
    "/api/transactions/summary",
    response_model=TransactionSummaryResponse,
)
def get_transaction_summary(
    db: Session = Depends(get_db),
):
    # -----------------------------
    # Total transactions
    # -----------------------------

    total_transactions = (
        db.query(func.count(Transaction.id))
        .scalar()
    )

    # -----------------------------
    # Total amount
    # -----------------------------

    total_amount = (
        db.query(func.sum(Transaction.amount))
        .scalar()
    )

    if total_amount is None:
        total_amount = Decimal("0.00")

    # -----------------------------
    # Successful transactions
    # -----------------------------

    successful_transactions = (
        db.query(func.count(Transaction.id))
        .filter(
            Transaction.status == "SUCCESS"
        )
        .scalar()
    )

    # -----------------------------
    # Failed transactions
    # -----------------------------

    failed_transactions = (
        db.query(func.count(Transaction.id))
        .filter(
            Transaction.status == "FAILED"
        )
        .scalar()
    )

    # -----------------------------
    # Pending transactions
    # -----------------------------

    pending_transactions = (
        db.query(func.count(Transaction.id))
        .filter(
            Transaction.status == "PENDING"
        )
        .scalar()
    )

    # -----------------------------
    # Category breakdown
    # -----------------------------

    category_results = (
        db.query(
            Transaction.category,
            func.count(Transaction.id),
            func.sum(Transaction.amount),
        )
        .filter(
            Transaction.category.isnot(None)
        )
        .group_by(
            Transaction.category
        )
        .order_by(
            func.sum(Transaction.amount).desc()
        )
        .all()
    )

    category_breakdown = [
        {
            "category": category,
            "count": count,
            "amount": amount or Decimal("0.00"),
        }
        for category, count, amount in category_results
    ]

    # -----------------------------
    # Payment method breakdown
    # -----------------------------

    payment_method_results = (
        db.query(
            Transaction.payment_method,
            func.count(Transaction.id),
            func.sum(Transaction.amount),
        )
        .group_by(
            Transaction.payment_method
        )
        .order_by(
            func.sum(Transaction.amount).desc()
        )
        .all()
    )

    payment_method_breakdown = [
        {
            "payment_method": payment_method,
            "count": count,
            "amount": amount or Decimal("0.00"),
        }
        for payment_method, count, amount in payment_method_results
    ]

    # -----------------------------
    # Top 10 merchants
    # -----------------------------

    merchant_results = (
        db.query(
            Transaction.merchant,
            func.count(Transaction.id),
            func.sum(Transaction.amount),
        )
        .group_by(
            Transaction.merchant
        )
        .order_by(
            func.sum(Transaction.amount).desc()
        )
        .limit(10)
        .all()
    )

    top_merchants = [
        {
            "merchant": merchant,
            "count": count,
            "amount": amount or Decimal("0.00"),
        }
        for merchant, count, amount in merchant_results
    ]

    # -----------------------------
    # Return summary
    # -----------------------------

    return {
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions,
        "pending_transactions": pending_transactions,
        "category_breakdown": category_breakdown,
        "payment_method_breakdown": payment_method_breakdown,
        "top_merchants": top_merchants,
    }