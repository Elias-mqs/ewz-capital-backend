from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.webhook import WebhookPayload, WebhookResponse
from app.services import webhook_service

router = APIRouter(prefix="/webhooks/pipefy", tags=["Webhooks"])


@router.post(
    "/card-updated",
    response_model=WebhookResponse,
    summary="Processar atualização de card do Pipefy",
    responses={
        404: {"description": "Cliente não encontrado."},
        409: {"description": "Evento já processado anteriormente ou cliente já processado."},
    },
)
def card_updated(payload: WebhookPayload, db: Session = Depends(get_db)):
    return webhook_service.processar_webhook(db, payload)
