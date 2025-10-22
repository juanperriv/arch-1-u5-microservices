from fastapi import FastAPI

import app.logger
from app.app import route


app = FastAPI(title="Sales Service")
app.include_router(route)

app.get("/health")
def health():
    return {"service": "sales", "status": "ok"}

