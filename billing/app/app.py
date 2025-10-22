import requests
import os
from fastapi import APIRouter
from app.dto import CreatePaymentDTO
from app.models import Money
from app.logger import log_info, LOGGER
from app.repo import PaymentRepository
from app.service import BillingService

SALES_URL : str = os.getenv("SALES_URL ")

repo = PaymentRepository()
billing = BillingService(repo)

route = APIRouter(tags=["billing"], prefix="/v1")

route.post("/payments")
def create_payment(dto: CreatePaymentDTO):
    log_info(f"⇢ POST /payments recibido para orden {dto.order_id} monto={dto.amount_cents} {dto.currency}")
    p = billing.register_payment(order_id=dto.order_id, amount=Money(amount_cents=dto.amount_cents, currency=dto.currency))
    log_info(f"Pago {p.id} APROBADO. Notificando a Sales {SALES_URL}/integration/payment-approved")
    evt = {"order_id": p.order_id, "amount_cents": p.amount.amount_cents, "currency": p.amount.currency}
    try:
        resp = requests.post(f"{SALES_URL}/integration/payment-approved", json=evt, timeout=5)
        log_info(f"Respuesta de Sales {resp.status_code}: {resp.text[:120]}")
    except Exception as e:
        LOGGER.error(f"Error notificando a Sales: {e}")
    return {"payment_id": p.id, "status": p.status}

route.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    p = repo.get(payment_id)
    return p