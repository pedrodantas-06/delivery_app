Feature: Processamento de estornos - BACKEND

  Scenario: Scenario name: Processar estorno total via API
    Given o pedido "123" do cliente "Ana Vitória" está com status "Pago"
    And o valor pago foi "100,00"
    And o cliente "Ana Vitória" tem "0,00" no saldo do app
    When eu envio uma requisição POST para "/api/v1/api/pagamento/estornar/123" para o cliente "cli_ana_vitória"
    Then o status da resposta deve ser "200 OK"
    And o pedido "123" deve ter status "Cancelado"
    And o saldo do cliente deve ser "100,00"

  Scenario: Impedir estorno após aceite do restaurante
    Given o pedido "124" do cliente "Ana Vitória" está com status "Em preparo"
    When eu envio uma requisição POST para "/api/v1/api/pagamento/estornar/124" para o cliente "cli_ana_vitória"
    Then o status da resposta deve ser "400 BAD REQUEST"
    And a mensagem deve ser "Pedido não pode ser cancelado após aceite do restaurante"
    And o status do pedido "124" deve permanecer "Em preparo"
