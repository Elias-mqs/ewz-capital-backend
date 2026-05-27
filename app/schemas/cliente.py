from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class ClienteCreate(BaseModel):
    cliente_nome: str = Field(
        min_length=1,
        max_length=255,
        description="Nome completo do cliente.",
        examples=["João da Silva"],
    )
    cliente_email: EmailStr = Field(
        description="E-mail único do cliente.",
        examples=["joao.silva@email.com"],
    )
    tipo_solicitacao: str = Field(
        min_length=1,
        max_length=255,
        description=(
            "Tipo de solicitação. Valores aceitos: 'Abertura de conta', 'Aporte', "
            "'Atualização cadastral', 'Encerramento de conta', 'Resgate', "
            "'Transferência de custódia'."
        ),
        examples=["Abertura de conta"],
    )
    valor_patrimonio: Decimal = Field(
        gt=0,
        decimal_places=2,
        description="Valor do patrimônio do cliente em reais (deve ser maior que zero).",
        examples=[150000.00],
    )

    @field_validator("cliente_nome", "tipo_solicitacao")
    @classmethod
    def normalizar_string(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Campo não pode ser vazio ou conter apenas espaços")
        return v


class ClienteResponse(BaseModel):
    id: int = Field(description="Identificador único do cliente.")
    cliente_nome: str = Field(description="Nome completo do cliente.")
    cliente_email: str = Field(description="E-mail do cliente.")
    tipo_solicitacao: str = Field(description="Tipo de solicitação cadastrada.")
    valor_patrimonio: Decimal = Field(description="Valor do patrimônio do cliente em reais.")
    status: Literal["Aguardando Análise", "Processado"] = Field(
        description="Status atual do cliente no fluxo de análise."
    )
    prioridade: Literal["prioridade_alta", "prioridade_normal"] | None = Field(
        description=(
            "Prioridade atribuída via webhook do Pipefy. "
            "'prioridade_alta' para patrimônio >= R$ 200.000; "
            "'prioridade_normal' para os demais. Nulo enquanto não processado."
        )
    )

    model_config = {"from_attributes": True}
