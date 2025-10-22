from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from datetime import datetime

class DomainError(Exception):
    pass


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"

class Money(BaseModel):
    amount_cents: int = Field(ge=0)
    currency: str = "COP"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise DomainError("Monedas distintas")
        return Money(amount_cents=self.amount_cents + other.amount_cents, currency=self.currency)

class OrderItem(BaseModel):
    sku: str
    qty: int = Field(ge=1)
    unit_price: Money

    @property
    def line_total(self) -> Money:
        return Money(amount_cents=self.unit_price.amount_cents * self.qty, currency=self.unit_price.currency)

class Order(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def total(self) -> Money:
        total = Money(amount_cents=0, currency=self.items[0].unit_price.currency if self.items else "COP")
        for it in self.items:
            total = total + it.line_total
        return total

    def mark_paid(self) -> None:
        if self.status == OrderStatus.PAID:
            return
        if self.status != OrderStatus.PENDING:
            raise DomainError("Sólo se pueden pagar pedidos PENDING")
        self.status = OrderStatus.PAID