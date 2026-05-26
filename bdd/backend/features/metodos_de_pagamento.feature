Feature: Gerenciamento de métodos de pagamento - BACKEND

  Como um sistema
  Eu quero validar as regras de negócio de métodos de pagamento
  Para garantir a integridade dos dados

  # Cenário 1: API de criação
  Scenario: Criar novo método de pagamento via API
    Given existe um cliente cadastrado com ID "cli_123"
    And o cliente "cli_123" não tem métodos de pagamento cadastrados
    When eu envio uma requisição POST para "/api/v1/api/pagamento/metodos" para o cliente "cli_123"
      | campo         | valor                          |
      | tipo          | CREDIT_CARD                    |
      | numero        | 4111111111111111               |
      | nome_titular  | JOAO SILVA                     |
      | validade_mes  | 12                             |
      | validade_ano  | 2028                           |
      | cvv           | 123                            |
    Then o status da resposta deve ser "201 CREATED"
    And o cartão deve estar dentre os métodos de pagamento do cliente "cli_123"

  # Cenário 2: Validação de dados inválidos
  Scenario: Tentar criar método com cartão expirado via API
    Given existe um cliente cadastrado com ID "cli_123"
    When eu envio uma requisição POST para "/api/v1/api/pagamento/metodos" para o cliente "cli_123"
      | campo         | valor                          |
      | tipo          | CREDIT_CARD                    |
      | numero        | 4111111111111111               |
      | nome_titular  | JOAO SILVA                     |
      | validade_mes  | 12                             |
      | validade_ano  | 2024                           |
      | cvv           | 123                            |
    Then o status da resposta deve ser "422 UNPROCESSABLE ENTITY"
    And a mensagem deve ser "Data de validade expirada"

  # Cenário 3: API de remoção
  Scenario: Remover método de pagamento via API
    Given existe um cliente cadastrado com ID "cli_125"
    And o cliente "cli_125" não tem métodos de pagamento cadastrados
    And o cliente "cli_125" possui o método "456" cadastrado
    And o cliente "cli_125" possui o método "457" cadastrado
    When eu envio uma requisição DELETE para "/api/v1/api/pagamento/metodos/456" para o cliente "cli_125"
    Then o status da resposta deve ser "204 NO CONTENT"
    And apenas o método "457" consta como método de pagamento do cliente "cli_125"


  # Cenário 4: API de atualização
  Scenario: Atualizar dados do método de pagamento via API
    Given existe um cliente cadastrado com ID "cli_127"
    Given o cliente "cli_127" possui o método "metodo_458" com validade "12/2025"
    When eu envio uma requisição PUT para "/api/v1/api/pagamento/metodos/458" do cliente "cli_127"
      | campo         | valor    |
      | validade_mes  | 06       |
      | validade_ano  | 2026     |
    Then o status deve ser 200 OK
    And a validade do método "metodo_458" deve ser atualizada para "06/2026"