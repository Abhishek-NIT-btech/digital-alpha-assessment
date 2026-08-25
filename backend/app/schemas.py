from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    timestamp: datetime
    merchant: str
    category: Optional[str]
    amount: Decimal
    currency: str
    status: str
    payment_method: str

    model_config = ConfigDict(from_attributes=True)


class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]
    page: int
    page_size: int
    total: int
    total_pages: int