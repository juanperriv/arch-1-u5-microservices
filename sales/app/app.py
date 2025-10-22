import requests
import os
from fastapi import APIRouter, HTTPException
from app.models import OrderItem, Money, DomainError
from app.dto import CreateOrderDTO, OrderVM, PaymentApprovedDTO
from app.logger import log_info
from app.repo import OrderRepository
from app.service import SalesService

BILLING_URL: str = os.getenv("BILLING_URL")

repo = OrderRepository()
sales = SalesService(repo)

route = APIRouter(tags=["sales"], prefix="/v1")

@route.post("/orders", response_model=OrderVM)
def create_order(dto: CreateOrderDTO):
    log_info(f"⇢ POST /orders recibido para {dto.order_id}")
    items = [OrderItem(sku=i.sku, qty=i.qty, unit_price=Money(amount_cents=i.unit_price_cents, currency=i.currency)) for i in dto.items]
    order = sales.place_order(dto.order_id, dto.customer_id, items)
    total = order.total()
    log_info(f"Pedido {order.id} total {total.amount_cents} {total.currency}")
    payload = {"order_id": order.id, "amount_cents": total.amount_cents, "currency": total.currency}
    try:
        resp = requests.post(f"{BILLING_URL}/payments", json=payload, timeout=5)
        log_info(f"→ Enviado a Billing ({resp.status_code})")
    except Exception as e:
        print("Error al contactar Billing:", e)
    return OrderVM(id=order.id, status=order.status, total_amount_cents=total.amount_cents, currency=total.currency)

# Consulta: obtener estado del pedido
@route.get("/orders/{order_id}", response_model=OrderVM)
def get_order(order_id: str):
    try:
        order = repo.get(order_id)
        total = order.total()
        return OrderVM(id=order.id, status=order.status, total_amount_cents=total.amount_cents, currency=total.currency)
    except DomainError as e:
        # 404 cuando el pedido no existe
        raise HTTPException(status_code=404, detail=str(e))



# Webhook: evento de Billing → Sales (PaymentApproved)
@route.post("/integration/payment-approved")
def on_payment_approved(evt: PaymentApprovedDTO):
    log_info(f"↩ Evento PaymentApproved para orden {evt.order_id}")
    order = repo.get(evt.order_id)
    if evt.amount_cents >= order.total().amount_cents:
        sales.mark_order_as_paid(order.id)
        return {"ok": True, "status": order.status}
    else:
        return {"ok": False, "reason": "Pago insuficiente"}