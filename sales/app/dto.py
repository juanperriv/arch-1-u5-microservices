from pydantic import BaseModel, Field
from typing import List
from app.models import OrderStatus

class CreateOrderItemDTO(BaseModel):
    sku: str
    qty: int = Field(ge=1)
    unit_price_cents: int = Field(ge=0)
    currency: str = "COP"

class CreateOrderDTO(BaseModel):
    order_id: str
    customer_id: str
    items: List[CreateOrderItemDTO]

class OrderVM(BaseModel):
    id: str
    status: OrderStatus
    total_amount_cents: int
    currency: str

class PaymentApprovedDTO(BaseModel):
    order_id: str
    amount_cents: int
    currency: str