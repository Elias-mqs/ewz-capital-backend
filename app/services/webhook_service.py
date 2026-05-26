from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.pipefy import client as pipefy_client
from app.repositories import cliente_repository, webhook_event_repository
from app.schemas.webhook import WebhookPayload, WebhookResponse

LIMITE_PRIORIDADE_ALTA = 200_000


def _calcular_prioridade(valor_patrimonio: float) -> str:
    if valor_patrimonio >= LIMITE_PRIORIDADE_ALTA:
        return "prioridade_alta"
    return "prioridade_normal"


def processar_webhook(db: Session, payload: WebhookPayload) -> WebhookResponse:
    if webhook_event_repository.evento_ja_processado(db, payload.event_id):
        raise HTTPException(status_code=409, detail="Evento já processado anteriormente.")

    cliente = cliente_repository.buscar_por_email(db, str(payload.cliente_email))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    prioridade = _calcular_prioridade(cliente.valor_patrimonio)
    novo_status = "Processado"

    cliente_repository.atualizar_status_e_prioridade(db, cliente, novo_status, prioridade)
    webhook_event_repository.registrar_evento(db, payload.event_id, payload.card_id, str(payload.cliente_email))

    pipefy_client.update_card_status(card_id=payload.card_id, status=novo_status)
    pipefy_client.update_card_priority(card_id=payload.card_id, prioridade=prioridade)

    return WebhookResponse(
        message="Webhook processado com sucesso.",
        cliente_email=str(payload.cliente_email),
        status=novo_status,
        prioridade=prioridade,
    )
