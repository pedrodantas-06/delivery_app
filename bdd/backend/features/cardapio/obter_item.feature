Feature: Cardápio API
    Scenario: Obter item do cardápio por ID
        Given o CardapioService retorna um item com id "101", nome "Pizza Calabresa" e preço "45.90"
        When uma requisição "GET" for enviada para "/api/v1/cardapio/101"
        Then o status da resposta deve ser "200"
        And o JSON da resposta deve conter id "101"
        And o JSON da resposta deve conter nome "Pizza Calabresa"
        And o JSON da resposta deve conter preço "45.90"
