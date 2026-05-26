from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class WebhookPayload(BaseModel):
    event_id: str = Field(min_length=1, max_length=255)
    card_id: str = Field(min_length=1, max_length=255)
    cliente_email: EmailStr
    timestamp: datetime


class WebhookResponse(BaseModel):
    message: str
    cliente_email: str
    status: str
    prioridade: str
