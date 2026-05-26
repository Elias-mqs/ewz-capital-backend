CREATE_CARD_MUTATION = """
mutation CreateCard($pipe_id: ID!, $nome: String!, $email: String!, $patrimonio: String!) {
  createCard(input: {
    pipe_id: $pipe_id
    fields_attributes: [
      { field_id: "cliente_nome",     field_value: $nome      }
      { field_id: "cliente_email",    field_value: $email     }
      { field_id: "valor_patrimonio", field_value: $patrimonio }
    ]
  }) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_STATUS_MUTATION = """
mutation UpdateCardStatus($card_id: ID!, $status: String!) {
  updateCardField(input: {
    card_id: $card_id
    field_id: "status"
    new_value: $status
  }) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_PRIORITY_MUTATION = """
mutation UpdateCardPriority($card_id: ID!, $prioridade: String!) {
  updateCardField(input: {
    card_id: $card_id
    field_id: "prioridade"
    new_value: $prioridade
  }) {
    card {
      id
      title
    }
  }
}
"""
