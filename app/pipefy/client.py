import logging

from app.pipefy.mutations import (
    CREATE_CARD_MUTATION,
    UPDATE_CARD_PRIORITY_MUTATION,
    UPDATE_CARD_STATUS_MUTATION,
)

logger = logging.getLogger(__name__)

PIPEFY_PIPE_ID = "your_pipe_id_here"


def create_card(nome: str, email: str, patrimonio: float) -> dict:
    variables = {
        "pipe_id": PIPEFY_PIPE_ID,
        "nome": nome,
        "email": email,
        "patrimonio": str(patrimonio),
    }
    logger.info(
        "[PIPEFY SIMULADO] createCard\nMutation: %s\nVariables: %s",
        CREATE_CARD_MUTATION.strip(),
        variables,
    )
    return {"simulated": True, "mutation": "createCard", "variables": variables}


def update_card_status(card_id: str, status: str) -> dict:
    variables = {"card_id": card_id, "status": status}
    logger.info(
        "[PIPEFY SIMULADO] updateCardField (status)\nMutation: %s\nVariables: %s",
        UPDATE_CARD_STATUS_MUTATION.strip(),
        variables,
    )
    return {"simulated": True, "mutation": "updateCardField:status", "variables": variables}


def update_card_priority(card_id: str, prioridade: str) -> dict:
    variables = {"card_id": card_id, "prioridade": prioridade}
    logger.info(
        "[PIPEFY SIMULADO] updateCardField (prioridade)\nMutation: %s\nVariables: %s",
        UPDATE_CARD_PRIORITY_MUTATION.strip(),
        variables,
    )
    return {"simulated": True, "mutation": "updateCardField:prioridade", "variables": variables}
