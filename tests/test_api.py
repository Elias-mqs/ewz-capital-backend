from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.cliente import Cliente

_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def _override_get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db():
    session = _SessionLocal()
    yield session
    session.close()


# ── payloads base ─────────────────────────────────────────────────────────────

_CLIENTE = {
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Abertura de conta",
    "valor_patrimonio": 250000.00,
}

_WEBHOOK = {
    "event_id": "evt_001",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2024-01-15T10:30:00Z",
}


# ── helpers ───────────────────────────────────────────────────────────────────

def _criar_cliente(client, patrimonio: float = 250_000.00):
    payload = {**_CLIENTE, "valor_patrimonio": patrimonio}
    with patch("app.pipefy.client.create_card"):
        client.post("/clientes", json=payload)


# ── POST /clientes ────────────────────────────────────────────────────────────

class TestCriarCliente:
    @patch("app.pipefy.client.create_card")
    def test_cria_cliente_com_payload_valido(self, _mock, client, db):
        response = client.post("/clientes", json=_CLIENTE)

        assert response.status_code == 201
        body = response.json()
        assert body["cliente_email"] == _CLIENTE["cliente_email"]
        assert body["status"] == "Aguardando Análise"
        assert body["prioridade"] is None

        salvo = db.query(Cliente).filter_by(cliente_email=_CLIENTE["cliente_email"]).first()
        assert salvo is not None
        assert salvo.cliente_nome == _CLIENTE["cliente_nome"]
        assert salvo.status == "Aguardando Análise"

    @patch("app.pipefy.client.create_card")
    def test_rejeita_email_duplicado(self, _mock, client):
        client.post("/clientes", json=_CLIENTE)
        response = client.post("/clientes", json=_CLIENTE)

        assert response.status_code == 409

    @patch("app.pipefy.client.create_card")
    def test_rejeita_tipo_solicitacao_invalido(self, _mock, client):
        payload = {**_CLIENTE, "tipo_solicitacao": "Tipo Inexistente"}
        response = client.post("/clientes", json=payload)

        assert response.status_code == 422


# ── POST /webhooks/pipefy/card-updated ────────────────────────────────────────

class TestWebhook:
    @patch("app.pipefy.client.update_card_status")
    @patch("app.pipefy.client.update_card_priority")
    def test_atribui_prioridade_alta_para_patrimonio_alto(self, _mp, _ms, client, db):
        _criar_cliente(client, patrimonio=200_000.00)

        response = client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)

        assert response.status_code == 200
        body = response.json()
        assert body["prioridade"] == "prioridade_alta"
        assert body["status"] == "Processado"

        cliente = db.query(Cliente).filter_by(cliente_email=_CLIENTE["cliente_email"]).first()
        assert cliente.prioridade == "prioridade_alta"
        assert cliente.status == "Processado"

    @patch("app.pipefy.client.update_card_status")
    @patch("app.pipefy.client.update_card_priority")
    def test_atribui_prioridade_normal_para_patrimonio_baixo(self, _mp, _ms, client):
        _criar_cliente(client, patrimonio=199_999.99)

        response = client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)

        assert response.status_code == 200
        assert response.json()["prioridade"] == "prioridade_normal"

    @patch("app.pipefy.client.update_card_status")
    @patch("app.pipefy.client.update_card_priority")
    def test_bloqueia_event_id_duplicado(self, _mp, _ms, client):
        _criar_cliente(client, patrimonio=250_000.00)

        client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)
        response = client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)

        assert response.status_code == 409

    @patch("app.pipefy.client.update_card_status")
    @patch("app.pipefy.client.update_card_priority")
    def test_retorna_404_para_cliente_inexistente(self, _mp, _ms, client):
        response = client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)

        assert response.status_code == 404

    @patch("app.pipefy.client.update_card_status")
    @patch("app.pipefy.client.update_card_priority")
    def test_bloqueia_cliente_ja_processado(self, _mp, _ms, client):
        _criar_cliente(client, patrimonio=250_000.00)

        client.post("/webhooks/pipefy/card-updated", json=_WEBHOOK)

        segundo_evento = {**_WEBHOOK, "event_id": "evt_002"}
        response = client.post("/webhooks/pipefy/card-updated", json=segundo_evento)

        assert response.status_code == 409
