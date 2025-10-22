from typing import List
from app.models import Money, Payment, PaymentStatus
from app.repo import PaymentRepository

class BillingService:
    def __init__(self, repo: PaymentRepository) -> None:
        self.repo = repo

    def register_payment(self, order_id: str, amount: Money) -> Payment:
        # PoC: aprobamos siempre. Aquí podrías validar con pasarela/fraude/etc.
        pid = f"PAY-{order_id}"
        payment = Payment(id=pid, order_id=order_id, amount=amount, status=PaymentStatus.APPROVED)
        self.repo.save(payment)
        return payment