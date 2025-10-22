from pydantic import BaseModel, Field
from typing import List
from app.models import OrderStatus

class CreatePaymentDTO(BaseModel):
    order_id: str
    amount_cents: int = Field(ge=0)
    currency: str = "COP"