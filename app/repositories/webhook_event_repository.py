from sqlalchemy.orm import Session

from app.models.webhook_event import WebhookEvent


def evento_ja_processado(db: Session, event_id: str) -> bool:
    return db.query(WebhookEvent).filter(WebhookEvent.event_id == event_id).first() is not None


def registrar_evento(db: Session, event_id: str, card_id: str, cliente_email: str) -> None:
    evento = WebhookEvent(
        event_id=event_id,
        card_id=card_id,
        cliente_email=cliente_email,
    )
    db.add(evento)
