Feature: Gestão de entregadores

    Scenario: cadastrar entregador com sucesso
        Given nenhum entregador existe
        When o cliente registra um entregador com nome "Ana" telefone "11999999999" regiao "Zona Sul"
        Then o entregador "Ana" deve ser criado com status "AVAILABLE" na regiao "Zona Sul"

    Scenario: atualizar status do entregador
        Given um entregador existente com nome "Ana" e regiao "Zona Sul"
        When o entregador for atualizado para status "OCCUPIED"
        Then o entregador deve ter status "OCCUPIED"

    Scenario: listar entregadores por status
        Given entregadores com status diferentes cadastrados
        When a listagem de entregadores for solicitada com filtro de status "AVAILABLE"
        Then apenas entregadores com status "AVAILABLE" devem ser retornados

    Scenario: atribuir entregador automaticamente
        Given uma ordem pendente na regiao "Zona Sul"
        And um entregador disponivel na regiao "Zona Sul"
        When a atribuicao automatica for solicitada para a ordem
        Then a ordem deve ser marcada como "IN_DELIVERY"
        And o entregador deve ser marcado como "OCCUPIED"

    Scenario: atribuir entregador manualmente
        Given uma ordem pendente na regiao "Zona Sul"
        And um entregador com nome "Bruno" disponivel na regiao "Zona Sul"
        When a atribuicao manual for solicitada para a ordem com o entregador "Bruno"
        Then a ordem deve ser atribuida ao entregador "Bruno"

    Scenario: nao atribuir quando nao ha entregador disponivel
        Given uma ordem pendente na regiao "Centro"
        And nao existe entregador disponivel na regiao "Centro"
        When a atribuicao automatica for solicitada para a ordem
        Then o sistema deve retornar erro "No available deliverer in region"

    Scenario: impedir atribuicao para entregador ocupado
        Given uma ordem pendente na regiao "Zona Norte"
        And um entregador com nome "Leo" ocupado na regiao "Zona Norte"
        When a atribuicao manual for solicitada para a ordem com o entregador "Leo"
        Then o sistema deve retornar erro "Deliverer is not available"

    Scenario: reatribuir pedido apos recusa
        Given uma ordem em entrega na regiao "Zona Sul" atribuida ao entregador "Ana"
        And outro entregador disponivel na regiao "Zona Sul"
        When a reatribuicao for solicitada para a ordem por motivo "refused"
        Then a nova atribuicao deve escolher outro entregador disponivel
        And a ordem deve continuar em "IN_DELIVERY"
