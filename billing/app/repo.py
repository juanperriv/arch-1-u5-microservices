from typing import Dict
from app.models import Payment

class PaymentRepository:
    def __init__(self) -> None:
        self._db: Dict[str, Payment] = {}

    def save(self, p: Payment) -> None:
        self._db[p.id] = p

    def get(self, pid: str) -> Payment:
        return self._db[pid]