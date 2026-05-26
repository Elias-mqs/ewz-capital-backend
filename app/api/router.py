from fastapi import APIRouter

from app.api.routes import clientes, webhooks

api_router = APIRouter()

api_router.include_router(clientes.router)
api_router.include_router(webhooks.router)
