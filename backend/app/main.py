import math
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.reward import Reward, RewardRedemption
from app.reward_schemas import (
    RewardBalanceResponse,
    RewardListResponse,
    RewardRedeemRequest,
    RewardRedeemResponse,
)
from app.schemas import TransactionListResponse
from app.summary_schemas import TransactionSummaryResponse
from app.transaction import Base, Transaction


app = FastAPI(
    title="Digital Alpha Transactions API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176",
        "http://localhost:5177",
        "http://127.0.0.1:5177",
        "http://localhost:5178",
        "http://127.0.0.1:5178",
        "http://localhost:5179",
        "http://127.0.0.1:5179",
        "http://localhost:5180",
        "http://127.0.0.1:5180",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# ============================================================
# TRANSACTIONS
# ============================================================

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
    min_amount: Optional[Decimal] = Query(
        default=None,
        ge=0,
    ),
    max_amount: Optional[Decimal] = Query(
        default=None,
        ge=0,
    ),
    sort_by: str = Query(
        default="id",
    ),
    sort_order: str = Query(
        default="asc",
    ),
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Validate amount range
    # --------------------------------------------------------

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="min_amount cannot be greater than max_amount.",
        )

    # --------------------------------------------------------
    # Validate date range
    # --------------------------------------------------------

    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise HTTPException(
            status_code=400,
            detail="date_from cannot be later than date_to.",
        )

    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    query = db.query(Transaction)

    # --------------------------------------------------------
    # Merchant search
    # --------------------------------------------------------

    if search and search.strip():
        query = query.filter(
            Transaction.merchant.ilike(
                f"%{search.strip()}%"
            )
        )

    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    if category:
        query = query.filter(
            Transaction.category == category
        )

    # --------------------------------------------------------
    # Status filter
    # --------------------------------------------------------

    if status:
        query = query.filter(
            Transaction.status == status.upper()
        )

    # --------------------------------------------------------
    # Payment method filter
    # --------------------------------------------------------

    if payment_method:
        query = query.filter(
            Transaction.payment_method == payment_method
        )

    # --------------------------------------------------------
    # Date range filters
    # --------------------------------------------------------

    if date_from:
        query = query.filter(
            Transaction.timestamp >= date_from
        )

    if date_to:
        query = query.filter(
            Transaction.timestamp <= date_to
        )

    # --------------------------------------------------------
    # Amount range filters
    # --------------------------------------------------------

    if min_amount is not None:
        query = query.filter(
            Transaction.amount >= min_amount
        )

    if max_amount is not None:
        query = query.filter(
            Transaction.amount <= max_amount
        )

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

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
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid sort_by. "
                "Use id, timestamp, amount, or merchant."
            ),
        )

    if sort_order.lower() not in {
        "asc",
        "desc",
    }:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc.",
        )

    if sort_order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # --------------------------------------------------------
    # Count matching records
    # --------------------------------------------------------

    total = query.count()

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (page - 1) * page_size

    transactions = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

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


# ============================================================
# TRANSACTION SUMMARY / ANALYTICS
# ============================================================

@app.get(
    "/api/transactions/summary",
    response_model=TransactionSummaryResponse,
)
def get_transaction_summary(
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Overall transaction totals
    # --------------------------------------------------------

    total_transactions = (
        db.query(
            func.count(Transaction.id)
        )
        .scalar()
    )

    total_amount = (
        db.query(
            func.sum(Transaction.amount)
        )
        .scalar()
    )

    if total_amount is None:
        total_amount = Decimal("0.00")

    successful_transactions = (
        db.query(
            func.count(Transaction.id)
        )
        .filter(
            Transaction.status == "SUCCESS"
        )
        .scalar()
    )

    failed_transactions = (
        db.query(
            func.count(Transaction.id)
        )
        .filter(
            Transaction.status == "FAILED"
        )
        .scalar()
    )

    pending_transactions = (
        db.query(
            func.count(Transaction.id)
        )
        .filter(
            Transaction.status == "PENDING"
        )
        .scalar()
    )

    # --------------------------------------------------------
    # Spending by category
    # --------------------------------------------------------

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
            func.sum(
                Transaction.amount
            ).desc()
        )
        .all()
    )

    category_breakdown = [
        {
            "category": category,
            "count": count,
            "amount": amount or Decimal("0.00"),
        }
        for (
            category,
            count,
            amount
        ) in category_results
    ]

    # --------------------------------------------------------
    # Payment method breakdown
    # --------------------------------------------------------

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
            func.sum(
                Transaction.amount
            ).desc()
        )
        .all()
    )

    payment_method_breakdown = [
        {
            "payment_method": payment_method,
            "count": count,
            "amount": amount or Decimal("0.00"),
        }
        for (
            payment_method,
            count,
            amount
        ) in payment_method_results
    ]

    # --------------------------------------------------------
    # Top merchants
    # --------------------------------------------------------

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
            func.sum(
                Transaction.amount
            ).desc()
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
        for (
            merchant,
            count,
            amount
        ) in merchant_results
    ]

    # --------------------------------------------------------
    # MONTHLY SPENDING TREND
    # --------------------------------------------------------
    #
    # IMPORTANT:
    # Do NOT use date_trunc("month", timestamp) in the
    # SELECT/GROUP BY combination here.
    #
    # PostgreSQL was previously returning:
    #
    #   column "transactions.timestamp" must appear
    #   in the GROUP BY clause
    #
    # We avoid that problem by grouping explicitly by
    # extracted year and month.
    #
    # Only successful payments are included in spending.
    # --------------------------------------------------------

    monthly_trend_rows = (
        db.query(
            func.extract(
                "year",
                Transaction.timestamp,
            ).label("year"),
            func.extract(
                "month",
                Transaction.timestamp,
            ).label("month"),
            func.count(
                Transaction.id
            ).label("count"),
            func.sum(
                Transaction.amount
            ).label("amount"),
        )
        .filter(
            Transaction.status == "SUCCESS"
        )
        .group_by(
            func.extract(
                "year",
                Transaction.timestamp,
            ),
            func.extract(
                "month",
                Transaction.timestamp,
            ),
        )
        .order_by(
            func.extract(
                "year",
                Transaction.timestamp,
            ).asc(),
            func.extract(
                "month",
                Transaction.timestamp,
            ).asc(),
        )
        .all()
    )

    monthly_trend = [
        {
            "month": (
                f"{int(year):04d}-"
                f"{int(month):02d}"
            ),
            "count": int(
                count or 0
            ),
            "amount": (
                amount
                or Decimal("0.00")
            ),
        }
        for (
            year,
            month,
            count,
            amount
        ) in monthly_trend_rows
    ]

    # --------------------------------------------------------
    # Return summary
    # --------------------------------------------------------

    return {
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "successful_transactions": successful_transactions,
        "failed_transactions": failed_transactions,
        "pending_transactions": pending_transactions,
        "category_breakdown": category_breakdown,
        "payment_method_breakdown": payment_method_breakdown,
        "top_merchants": top_merchants,
        "monthly_trend": monthly_trend,
    }


# ============================================================
# TRANSACTION DETAIL
# ============================================================

@app.get(
    "/api/transactions/{transaction_id}",
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id
        )
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found.",
        )

    return transaction


# ============================================================
# REWARDS
# ============================================================

# One coin is earned for every ₹100 of successful spending.
# Maximum 100 coins can be earned from one transaction.

COINS_PER_HUNDRED_RUPEES = 1
MAX_COINS_PER_TRANSACTION = 100


def calculate_transaction_coins(
    amount: Decimal,
) -> int:
    if amount <= 0:
        return 0

    coins = int(
        amount // Decimal("100")
    )

    return min(
        coins * COINS_PER_HUNDRED_RUPEES,
        MAX_COINS_PER_TRANSACTION,
    )


def get_earned_coins(
    db: Session,
) -> int:
    successful_transactions = (
        db.query(
            Transaction.amount
        )
        .filter(
            Transaction.status == "SUCCESS"
        )
        .all()
    )

    return sum(
        calculate_transaction_coins(
            amount
        )
        for (
            amount,
        ) in successful_transactions
    )


def get_redeemed_coins(
    db: Session,
) -> int:
    total = (
        db.query(
            func.coalesce(
                func.sum(
                    RewardRedemption.coin_cost
                ),
                0,
            )
        )
        .scalar()
    )

    return int(
        total or 0
    )


# ============================================================
# REWARD BALANCE
# ============================================================

@app.get(
    "/api/rewards/balance",
    response_model=RewardBalanceResponse,
)
def get_reward_balance(
    db: Session = Depends(get_db),
):
    earned_coins = get_earned_coins(db)
    redeemed_coins = get_redeemed_coins(db)

    balance = max(
        earned_coins - redeemed_coins,
        0,
    )

    return {
        "balance": balance,
        "earned_coins": earned_coins,
        "redeemed_coins": redeemed_coins,
    }


# ============================================================
# REWARD CATALOGUE
# ============================================================

@app.get(
    "/api/rewards",
    response_model=RewardListResponse,
)
def get_rewards(
    db: Session = Depends(get_db),
):
    rewards = (
        db.query(Reward)
        .filter(
            Reward.active.is_(True)
        )
        .order_by(
            Reward.coin_cost.asc()
        )
        .all()
    )

    return {
        "items": rewards
    }


# ============================================================
# REDEEM REWARD
# ============================================================

@app.post(
    "/api/rewards/redeem",
    response_model=RewardRedeemResponse,
)
def redeem_reward(
    request: RewardRedeemRequest,
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Find reward
    # --------------------------------------------------------

    reward = (
        db.query(Reward)
        .filter(
            Reward.id == request.reward_id,
            Reward.active.is_(True),
        )
        .first()
    )

    if reward is None:
        raise HTTPException(
            status_code=404,
            detail="Reward not found.",
        )

    # --------------------------------------------------------
    # Calculate current balance
    # --------------------------------------------------------

    earned_coins = get_earned_coins(db)
    redeemed_coins = get_redeemed_coins(db)

    current_balance = max(
        earned_coins - redeemed_coins,
        0,
    )

    # --------------------------------------------------------
    # Validate balance
    # --------------------------------------------------------

    if current_balance < reward.coin_cost:
        raise HTTPException(
            status_code=400,
            detail="Insufficient coin balance.",
        )

    # --------------------------------------------------------
    # Create redemption
    # --------------------------------------------------------

    redemption = RewardRedemption(
        reward_id=reward.id,
        coin_cost=reward.coin_cost,
    )

    db.add(redemption)
    db.commit()

    # --------------------------------------------------------
    # Remaining balance
    # --------------------------------------------------------

    remaining_balance = (
        current_balance
        - reward.coin_cost
    )

    return {
        "success": True,
        "message": "Reward redeemed successfully.",
        "reward": reward,
        "coins_spent": reward.coin_cost,
        "remaining_balance": remaining_balance,
    }