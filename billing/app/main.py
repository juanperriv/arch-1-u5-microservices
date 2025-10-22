from fastapi import FastAPI

import app.logger
from app.app import route


app = FastAPI(title="Billing Service")
app.include_router(route)

app.get("/health")
def health():
    return {"service": "billing", "status": "ok"}

