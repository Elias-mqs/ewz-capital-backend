from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class WebhookPayload(BaseModel):
    event_id: str = Field(
        min_length=1,
        max_length=255,
        description="Identificador único do evento Pipefy. Usado para garantir idempotência.",
        examples=["evt_abc123"],
    )
    card_id: str = Field(
        min_length=1,
        max_length=255,
        description="Identificador do card no Pipefy.",
        examples=["card_456"],
    )
    cliente_email: EmailStr = Field(
        description="E-mail do cliente associado ao card.",
        examples=["joao.silva@email.com"],
    )
    timestamp: datetime = Field(
        description="Data e hora em que o evento ocorreu no Pipefy (ISO 8601).",
        examples=["2024-01-15T10:30:00Z"],
    )


class WebhookResponse(BaseModel):
    message: str = Field(description="Mensagem de confirmação do processamento.")
    cliente_email: str = Field(description="E-mail do cliente processado.")
    status: Literal["Processado"] = Field(description="Status atualizado do cliente.")
    prioridade: Literal["prioridade_alta", "prioridade_normal"] = Field(
        description="Prioridade atribuída: 'prioridade_alta' para patrimônio >= R$ 200.000."
    )
