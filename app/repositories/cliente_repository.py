from sqlalchemy.orm import Session

from app.models.cliente import Cliente


def criar(db: Session, nome: str, email: str, tipo_solicitacao: str, valor_patrimonio: float) -> Cliente:
    cliente = Cliente(
        cliente_nome=nome,
        cliente_email=email,
        tipo_solicitacao=tipo_solicitacao,
        valor_patrimonio=valor_patrimonio,
        status="Aguardando Análise",
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def buscar_por_email(db: Session, email: str) -> Cliente | None:
    return db.query(Cliente).filter(Cliente.cliente_email == email).first()


def atualizar_status_e_prioridade(db: Session, cliente: Cliente, status: str, prioridade: str) -> Cliente:
    cliente.status = status
    cliente.prioridade = prioridade
    db.commit()
    db.refresh(cliente)
    return cliente
