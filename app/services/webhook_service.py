from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.pipefy import client as pipefy_client
from app.repositories import cliente_repository, webhook_event_repository
from app.schemas.webhook import WebhookPayload, WebhookResponse

LIMITE_PRIORIDADE_ALTA = 200_000
STATUS_PROCESSADO = "Processado"


def _calcular_prioridade(valor_patrimonio: float) -> str:
    if valor_patrimonio >= LIMITE_PRIORIDADE_ALTA:
        return "prioridade_alta"
    return "prioridade_normal"


def processar_webhook(db: Session, payload: WebhookPayload) -> WebhookResponse:
    email = str(payload.cliente_email)

    if webhook_event_repository.evento_ja_processado(db, payload.event_id):
        raise HTTPException(status_code=409, detail="Evento já processado anteriormente.")

    cliente = cliente_repository.buscar_por_email(db, email)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if cliente.status == STATUS_PROCESSADO:
        raise HTTPException(
            status_code=409,
            detail="Cliente já foi processado anteriormente.",
        )

    prioridade = _calcular_prioridade(cliente.valor_patrimonio)

    cliente_repository.atualizar_status_e_prioridade(db, cliente, STATUS_PROCESSADO, prioridade)
    webhook_event_repository.registrar_evento(db, payload.event_id, payload.card_id, email)
    db.commit()
    db.refresh(cliente)

    pipefy_client.update_card_status(card_id=payload.card_id, status=STATUS_PROCESSADO)
    pipefy_client.update_card_priority(card_id=payload.card_id, prioridade=prioridade)

    return WebhookResponse(
        message="Webhook processado com sucesso.",
        cliente_email=email,
        status=STATUS_PROCESSADO,
        prioridade=prioridade,
    )
