from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.pipefy import client as pipefy_client
from app.repositories import cliente_repository
from app.schemas.cliente import ClienteCreate


def criar_cliente(db: Session, payload: ClienteCreate) -> Cliente:
    cliente = cliente_repository.criar(
        db=db,
        nome=payload.cliente_nome,
        email=payload.cliente_email,
        tipo_solicitacao=payload.tipo_solicitacao,
        valor_patrimonio=payload.valor_patrimonio,
    )

    pipefy_client.create_card(
        nome=cliente.cliente_nome,
        email=cliente.cliente_email,
        patrimonio=cliente.valor_patrimonio,
    )

    return cliente
