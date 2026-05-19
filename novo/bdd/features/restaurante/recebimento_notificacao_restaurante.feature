Feature: Recebimento de notificação do pedido
  Como proprietário de um restaurante
  Quero poder receber notificação do recebimento de novo pedido
  Para poder confeccioná-los e entregá-los

  Background:
    Given que o endpoint de "pedidos" está "disponível"
    And que o "restaurante" cujo "id" é "123" "existe" na tabela "restaurantes" do banco de dados
    And eu sou o proprietário do "restaurante" de id "123"
    And estou autenticado no sistema
    And que o "pedido" cujo "id" é "987" "existe" na tabela "pedidos" do banco de dados
    And que o "restaurante" cujo "id" é "123" está "aberto"
    And eu recebo uma requisição do sistema informando "novo pedido" com id "987"

  Scenario: Aceite de pedido
    When eu envio um requisição de ao endpoint "pedidos" com os dados:
      | id_pedido  | id_restaurante | aceitacao  |
      | 987        | 123            | aceito     |
    Then o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Em preparo" na tabela "pedidos" do banco de dados
    And o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "id_restaurante" para "123" na tabela "pedidos" do banco de dados
    And o sistema responde com o código HTTP "200"

  Scenario: Recusa de pedido
    When eu envio um requisição de ao endpoint "pedidos" com os dados:
      | id_pedido  | id_restaurante | aceitacao  |
      | 987        | 123            | rejeitado  |
    Then o sistema deve atualizar o "pedido" cujo "id" é "987" com o novo "status" para "Rejeitado" na tabela "pedidos" do banco de dados
    And o sistema responde com o código HTTP "200"
