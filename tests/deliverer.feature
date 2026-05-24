Feature: Deliverer BDD

  Scenario: cadastrar entregador com sucesso
    Given nenhum entregador existe
    When eu cadastro um entregador com nome "Ana" telefone "11999999999" regiao "Zona Sul"
    Then o entregador "Ana" deve ficar com status "AVAILABLE"