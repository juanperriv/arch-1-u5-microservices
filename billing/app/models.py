from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class DomainError(Exception):
    pass


class PaymentStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Money(BaseModel):
    amount_cents: int = Field(ge=0)
    currency: str = "COP"

class Payment(BaseModel):
    id: str
    order_id: str
    amount: MoneyB
    status: PaymentStatus
    processed_at: datetime = Field(default_factory=datetime.utcnow)