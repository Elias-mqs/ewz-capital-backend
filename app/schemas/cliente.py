from pydantic import BaseModel, EmailStr, field_validator


class ClienteCreate(BaseModel):
    cliente_nome: str
    cliente_email: EmailStr
    tipo_solicitacao: str
    valor_patrimonio: float

    @field_validator("cliente_nome", "tipo_solicitacao")
    @classmethod
    def nao_pode_ser_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Campo não pode ser vazio")
        return v

    @field_validator("valor_patrimonio")
    @classmethod
    def patrimonio_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("valor_patrimonio deve ser maior que zero")
        return v


class ClienteResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: float
    status: str
    prioridade: str | None

    model_config = {"from_attributes": True}
