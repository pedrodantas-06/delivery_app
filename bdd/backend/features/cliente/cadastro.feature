Feature: Cadastro de clientes

  Scenario: falha ao cadastrar cliente com email duplicado
    Given existe um cliente com email "joao@email.com"
    When eu envio uma requisição POST para "/clientes" com email "joao@email.com"
    Then o sistema deve retornar erro "Dados já cadastrados"