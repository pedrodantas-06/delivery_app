Feature: Status Operacional do Restaurante
  Como proprietário de um restaurante
  Quero gerenciar o status do meu estabelecimento (aberto/fechado)
  Para garantir que os pedidos só sejam recebidos dentro do horário de funcionamento

  Background:
    Given que o endpoint de "restaurantes" está "disponível"
    And o "restaurante" cujo "id" é "123" existe na tabela "restaurantes" do banco de dados

  Scenario: Fechamento automático por horário
    When o horário atual está "fora" do intervalo de "funcionamento do restaurante" "Gosto bom":
    Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados

  Scenario: Abertura automática por horário
    When o horário atual está "dentro" do intervalo de "funcionamento do restaurante" "Gosto bom":
    Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados

  Scenario: Mudança de status manual para aberto
    When eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:
      | id  | campo  | novo_valor |
      | 123 | status | Aberto     |
    Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Aberto" na tabela "restaurantes" do banco de dados
    And o sistema responde com o código HTTP "200"

  Scenario: Mudança de status manual para fechado
    When eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:
      | id  | campo  | novo_valor |
      | 123 | status | Fechado    |
    Then o sistema deve atualizar o "restaurante" de id "123" com o novo "status" para "Fechado" na tabela "restaurantes" do banco de dados
    And o sistema responde com o código HTTP "200"