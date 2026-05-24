Feature: GUI de entregadores

  Scenario: cadastrar entregador com sucesso
    Given eu estou na tela de entregadores
    When eu cadastro o entregador "Ana"
    Then vejo "Ana" na lista de entregadores