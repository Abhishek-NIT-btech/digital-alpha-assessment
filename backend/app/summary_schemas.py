from decimal import Decimal
from typing import List

from pydantic import BaseModel


class CategorySummary(BaseModel):
    category: str
    count: int
    amount: Decimal


class PaymentMethodSummary(BaseModel):
    payment_method: str
    count: int
    amount: Decimal


class MerchantSummary(BaseModel):
    merchant: str
    count: int
    amount: Decimal


class TransactionSummaryResponse(BaseModel):
    total_transactions: int
    total_amount: Decimal

    successful_transactions: int
    failed_transactions: int
    pending_transactions: int

    category_breakdown: List[CategorySummary]
    payment_method_breakdown: List[PaymentMethodSummary]
    top_merchants: List[MerchantSummary]