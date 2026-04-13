Feature: Gestão de entregadores

    Scenario: cadastrar entregador com sucesso
        Given nenhum entregador existe
        When o cliente registra um entregador com nome "Ana" telefone "11999999999" região "Zona Sul"
        Then o entregador "Ana" deve ser criado com status "AVAILABLE" na região "Zona Sul"

    Scenario: atualizar status do entregador
        Given um entregador existente com nome "Ana" e região "Zona Sul"
        When o entregador for atualizado para status "OCCUPIED"
        Then o entregador deve ter status "OCCUPIED"

    Scenario: atribuir entregador automaticamente
        Given uma ordem pendente na região "Zona Sul"
        And um entregador disponível na região "Zona Sul"
        When a atribuição automática for solicitada para a ordem
        Then a ordem deve ser marcada como "IN_DELIVERY"
        And o entregador deve ser marcado como "OCCUPIED"

    Scenario: reatribuir pedido após recusa
        Given uma ordem em entrega na região "Zona Sul" atribuída ao entregador "Ana"
        And outro entregador disponível na região "Zona Sul"
        When a reatribuição for solicitada para a ordem
        Then a nova atribuição deve escolher outro entregador disponível
        And a ordem deve continuar em "IN_DELIVERY"
