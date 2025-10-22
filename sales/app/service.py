from typing import List
from app.models import Order, OrderItem, DomainError
from app.repo import OrderRepository

class SalesService:
    def __init__(self, repo: OrderRepository) -> None:
        self.repo = repo

    def place_order(self, order_id: str, customer_id: str, items: List[OrderItem]) -> Order:
        if not items:
            raise DomainError("Pedido requiere al menos un ítem")
        order = Order(id=order_id, customer_id=customer_id, items=items)
        self.repo.save(order)
        return order

    def mark_order_as_paid(self, order_id: str) -> Order:
        order = self.repo.get(order_id)
        order.mark_paid()
        self.repo.save(order)
        return order