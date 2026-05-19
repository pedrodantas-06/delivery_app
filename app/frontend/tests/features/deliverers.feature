Feature: Gestão de entregadores e distribuicao de pedidos

    # ==============================
    # Cadastro e gestão básica
    # ==============================

    Scenario: cadastrar entregador com sucesso
        Given nao existe entregador cadastrado
        When um entregador e registrado com nome "Ana", telefone "11999999999" e regiao "Zona Sul"
        Then o entregador "Ana" deve ser criado com status "AVAILABLE" na regiao "Zona Sul"

    Scenario: atualizar status do entregador
        Given existe um entregador "Ana" com status "AVAILABLE" na regiao "Zona Sul"
        When o status do entregador "Ana" e atualizado para "OCCUPIED"
        Then o entregador "Ana" deve possuir status "OCCUPIED"

    Scenario: listar entregadores disponiveis por status
        Given existem entregadores cadastrados com diferentes status
        When a listagem de entregadores e solicitada com filtro "AVAILABLE"
        Then o sistema retorna apenas entregadores com status "AVAILABLE"

    # ==============================
    # Distribuicao (broadcast)
    # ==============================

    Scenario: distribuir pedido para entregadores disponiveis da regiao
        Given existe um pedido "P123" com status "PENDING" na regiao "Zona Sul"
        And existem entregadores "Ana" e "Bruno" com status "AVAILABLE" na regiao "Zona Sul"
        When o sistema inicia a distribuicao do pedido "P123"
        Then o sistema envia notificacao de entrega para "Ana" e "Bruno"
        And o pedido "P123" permanece com status "PENDING"

    # ==============================
    # Aceite de pedido (concorrencia)
    # ==============================

    Scenario: primeiro entregador aceita o pedido com sucesso
        Given existe um pedido "P123" com status "PENDING" na regiao "Zona Sul"
        And o pedido "P123" foi enviado para os entregadores "Ana" e "Bruno"
        And os entregadores "Ana" e "Bruno" possuem status "AVAILABLE"
        When o entregador "Ana" aceita o pedido "P123"
        Then o pedido "P123" deve ser atualizado para status "IN_DELIVERY"
        And o entregador "Ana" deve ser atualizado para status "OCCUPIED"
        And o pedido "P123" deve ser associado ao entregador "Ana"
        And as notificacoes do pedido "P123" devem ser removidas para os demais entregadores

    # ==============================
    # Recusa de pedido
    # ==============================

    Scenario: entregador recusa pedido e outro aceita
        Given existe um pedido "P123" com status "PENDING" na regiao "Zona Sul"
        And o pedido "P123" foi enviado para os entregadores "Ana" e "Bruno"
        And os entregadores "Ana" e "Bruno" possuem status "AVAILABLE"
        When o entregador "Ana" recusa o pedido "P123"
        And o entregador "Bruno" aceita o pedido "P123"
        Then o pedido "P123" deve ser atualizado para status "IN_DELIVERY"
        And o entregador "Bruno" deve ser atualizado para status "OCCUPIED"
        And o pedido "P123" deve ser associado ao entregador "Bruno"

    # ==============================
    # Reatribuicao por falha
    # ==============================

    Scenario: reatribuir pedido apos falha na entrega
        Given existe um pedido "P123" com status "IN_DELIVERY" associado ao entregador "Ana" na regiao "Zona Sul"
        And existe um entregador "Bruno" com status "AVAILABLE" na regiao "Zona Sul"
        When o sistema identifica falha de entrega do pedido "P123"
        Then o entregador "Ana" deve ser atualizado para status "AVAILABLE"
        And o sistema redistribui o pedido "P123" para entregadores disponiveis da regiao
        And o sistema envia notificacao de entrega para "Bruno"

    # ==============================
    # Reatribuicao por cancelamento
    # ==============================

    Scenario: reatribuir pedido apos cancelamento do entregador
        Given existe um pedido "P123" com status "IN_DELIVERY" associado ao entregador "Ana" na regiao "Zona Sul"
        And existe um entregador "Bruno" com status "AVAILABLE" na regiao "Zona Sul"
        When o entregador "Ana" cancela a entrega do pedido "P123"
        Then o entregador "Ana" deve ser atualizado para status "AVAILABLE"
        And o sistema redistribui o pedido "P123" para entregadores disponiveis da regiao
        And o sistema envia notificacao de entrega para "Bruno"