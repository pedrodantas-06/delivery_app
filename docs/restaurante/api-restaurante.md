# Documentação da API de Restaurantes

Esta documentação descreve as rotas da API REST para a funcionalidade de gerenciamento de restaurantes.

## 1. Cadastro de Restaurante
- **Método**: `POST`
- **Rota**: `/restaurantes`
- **Descrição**: Cria um novo restaurante na plataforma.
- **Exemplo de Corpo (JSON)**:
  ```json
  {
    "nome": "Gosto bom",
    "endereço": "Rua A, 10",
    "cnpj": "00.000.000/0001-00",
    "horário": "08:00-22:00",
    "tipo": "Hamburgueria"
  }
  ```
- **Retorno**: `201 Created`
  ```json
  {
    "id": 1,
    "nome": "Gosto bom",
    "status": "Aberto"
  }
  ```

## 2. Listagem e Filtro
- **Método**: `GET`
- **Rota**: `/restaurantes`
- **Parâmetros (Query)**: `categoria` (opcional)
- **Retorno**: `200 OK`
  ```json
  [
    { "id": 1, "nome": "Gosto bom", "tipo": "Hamburgueria" },
    { "id": 2, "nome": "Pizza Rápida", "tipo": "Pizzaria" }
  ]
  ```

## 3. Detalhes do Restaurante
- **Método**: `GET`
- **Rota**: `/restaurantes/{id}`
- **Retorno**: `200 OK`
  ```json
  {
    "id": 1,
    "nome": "Gosto bom",
    "endereço": "Rua A, 10",
    "horário": "08:00-22:00",
    "tipo": "Hamburgueria"
  }
  ```

## 4. Edição de Perfil
- **Método**: `PATCH`
- **Rota**: `/restaurantes/{id}`
- **Exemplo de Corpo (JSON)**:
  ```json
  {
    "endereço": "Rua B, 20"
  }
  ```
- **Retorno**: `200 OK`
  ```json
  {
    "id": 1,
    "endereço": "Rua B, 20"
  }
  ```

## 5. Atualização de Status Operacional
- **Método**: `PATCH`
- **Rota**: `/restaurantes/{id}/status`
- **Exemplo de Corpo (JSON)**:
  ```json
  {
    "status": "Fechado"
  }
  ```
- **Retorno**: `200 OK`

## 6. Aceite de Pedido
- **Método**: `PATCH`
- **Rota**: `/pedidos/{id}/aceitar`
- **Retorno**: `200 OK`

## 7. Recusa de Pedido
- **Método**: `PATCH`
- **Rota**: `/pedidos/{id}/recusar`
- **Retorno**: `200 OK`

## 8. Histórico de Notificações
- **Método**: `GET`
- **Rota**: `/restaurantes/{id}/notificacoes`
- **Retorno**: `200 OK`
  ```json
  [
    { "id": 101, "tipo": "Pedido", "mensagem": "Novo pedido recebido" }
  ]
  ```

## 9. Acesso ao Painel Principal
- **Método**: `GET`
- **Rota**: `/restaurantes/{id}/dashboard`
- **Retorno**: `200 OK`
  ```json
  {
    "pedidos_pendentes": 5,
    "status_atual": "Aberto"
  }
  ```
