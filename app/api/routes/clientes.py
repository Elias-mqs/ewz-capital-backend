from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services import cliente_service

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post(
    "",
    response_model=ClienteResponse,
    status_code=201,
    summary="Cadastrar novo cliente",
    responses={
        409: {"description": "Já existe um cliente cadastrado com este e-mail."},
        422: {"description": "tipo_solicitacao inválido ou dados malformados."},
    },
)
def criar_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    return cliente_service.criar_cliente(db, payload)
