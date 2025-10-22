from typing import Dict
from app.models import Order, DomainError

class OrderRepository:
    def __init__(self) -> None:
        self._db: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._db[order.id] = order

    def get(self, order_id: str) -> Order:
        if order_id not in self._db:
            raise DomainError("Pedido no encontrado")
        return self._db[order_id]