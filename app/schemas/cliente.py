from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator


class ClienteCreate(BaseModel):
    cliente_nome: str = Field(min_length=1, max_length=255)
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(min_length=1, max_length=255)
    valor_patrimonio: Decimal = Field(gt=0, decimal_places=2)

    @field_validator("cliente_nome", "tipo_solicitacao")
    @classmethod
    def normalizar_string(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Campo não pode ser vazio ou conter apenas espaços")
        return v


class ClienteResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: str
    tipo_solicitacao: str
    valor_patrimonio: Decimal
    status: str
    prioridade: str | None

    model_config = {"from_attributes": True}
