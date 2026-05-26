from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.pipefy import client as pipefy_client
from app.repositories import cliente_repository
from app.schemas.cliente import ClienteCreate

TIPOS_SOLICITACAO_PERMITIDOS = {
    "Atualização cadastral",
    "Abertura de conta",
    "Encerramento de conta",
    "Transferência de custódia",
    "Aporte",
    "Resgate",
}


def criar_cliente(db: Session, payload: ClienteCreate) -> Cliente:
    if payload.tipo_solicitacao not in TIPOS_SOLICITACAO_PERMITIDOS:
        raise HTTPException(
            status_code=422,
            detail=(
                f"tipo_solicitacao '{payload.tipo_solicitacao}' não é permitido. "
                f"Valores aceitos: {sorted(TIPOS_SOLICITACAO_PERMITIDOS)}"
            ),
        )

    if cliente_repository.buscar_por_email(db, str(payload.cliente_email)):
        raise HTTPException(
            status_code=409,
            detail=f"Já existe um cliente cadastrado com o e-mail '{payload.cliente_email}'.",
        )

    cliente = cliente_repository.criar(
        db=db,
        nome=payload.cliente_nome,
        email=str(payload.cliente_email),
        tipo_solicitacao=payload.tipo_solicitacao,
        valor_patrimonio=payload.valor_patrimonio,
    )

    pipefy_client.create_card(
        nome=cliente.cliente_nome,
        email=cliente.cliente_email,
        patrimonio=cliente.valor_patrimonio,
    )

    return cliente
