# EWZ Capital — Client Management API

API de gerenciamento de clientes com integração simulada ao Pipefy via GraphQL.

Desenvolvida com **Python + FastAPI**, banco **PostgreSQL** e orquestração via **Docker Compose**.

---

## Pré-requisitos

- [Docker](https://www.docker.com/) e Docker Compose instalados

---

## Executando o projeto

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd ewz-capital-backend

# Suba os containers (banco + aplicação)
docker compose up --build
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa (Swagger): `http://localhost:8000/docs`

---

## Executando os testes

```bash
# Com os containers rodando, execute em outro terminal:
docker compose exec app pytest tests/ -v
```

---

## Endpoints

### POST /clientes

Cria um novo cliente e simula a criação de um card no Pipefy.

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

**Resposta esperada (201):**
```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000.0,
  "status": "Aguardando Análise",
  "prioridade": null
}
```

---

### POST /webhooks/pipefy/card-updated

Simula o recebimento de um webhook do Pipefy ao atualizar um card. Aplica a regra de prioridade e atualiza o cliente no banco.

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

**Resposta esperada (200):**
```json
{
  "message": "Webhook processado com sucesso.",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "prioridade_alta"
}
```

**Regra de prioridade:**
- `valor_patrimonio >= 200.000` → `prioridade_alta`
- `valor_patrimonio < 200.000` → `prioridade_normal`

**Idempotência:** enviar o mesmo `event_id` duas vezes retorna `409 Conflict`.

---

## Estrutura do projeto

```
ewz-capital-backend/
├── app/
│   ├── api/            # Rotas FastAPI
│   │   └── routes/
│   │       ├── clientes.py
│   │       └── webhooks.py
│   ├── core/           # Configuração e conexão com banco
│   │   ├── config.py
│   │   └── database.py
│   ├── models/         # Modelos ORM (SQLAlchemy)
│   ├── schemas/        # Validação Pydantic
│   ├── services/       # Regras de negócio
│   ├── repositories/   # Acesso ao banco
│   ├── pipefy/         # Mutations GraphQL do Pipefy
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
└── .env
```

---

## Visão de Produção (AWS)

Em produção, essa estrutura escalaria da seguinte forma:

**API Gateway + Lambda (ou ECS Fargate)**
O endpoint `POST /clientes` seria exposto via API Gateway, acionando uma função Lambda (ou container no Fargate) com a lógica do service. O Lambda é stateless e escala automaticamente sob demanda, sem necessidade de gerenciar servidores.

**Processamento de Webhooks com SQS**
Em vez de o Pipefy chamar diretamente o endpoint, o webhook seria recebido por uma fila SQS. Um Lambda consumidor processa as mensagens de forma assíncrona, garantindo que picos de volume não derrubem o sistema e que eventos falhos sejam reprocessados automaticamente (dead-letter queue).

**Banco de dados**
- Para alta escala: **DynamoDB** — tabela `Clientes` com `cliente_email` como partition key e tabela `WebhookEvents` com `event_id` como chave única para idempotência nativa.
- Para necessidade de queries relacionais: **RDS PostgreSQL** com Multi-AZ para alta disponibilidade e read replicas para leitura.

**Idempotência em escala**
No DynamoDB, a verificação de `event_id` duplicado seria feita com `ConditionExpression` garantindo operação atômica — sem race condition em ambientes com múltiplas instâncias.

**Integração Pipefy**
As chamadas GraphQL ao Pipefy sairiam de dentro do Lambda com as credenciais armazenadas no **AWS Secrets Manager**, nunca expostas em variáveis de ambiente diretamente.
