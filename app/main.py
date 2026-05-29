from fastapi import FastAPI

from app.api.router import api_router

_openapi_tags = [
    {
        "name": "Clientes",
        "description": (
            "Cadastro de clientes. Ao criar um cliente, um card é aberto "
            "automaticamente no Pipefy via GraphQL."
        ),
    },
    {
        "name": "Webhooks",
        "description": (
            "Recebimento de eventos do Pipefy. Atualiza status e prioridade "
            "dos clientes com base nos cards."
        ),
    },
]

app = FastAPI(
    title="EWZ Capital — Client Management API",
    description="API de gerenciamento de clientes com integração ao Pipefy via GraphQL.",
    version="1.0.0",
    openapi_tags=_openapi_tags,
)

app.include_router(api_router)
