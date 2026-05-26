from fastapi import FastAPI

from app.api.router import api_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EWZ Capital — Client Management API",
    description="API de gerenciamento de clientes com integração ao Pipefy via GraphQL.",
    version="1.0.0",
)

app.include_router(api_router)
