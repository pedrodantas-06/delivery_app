Funcionalidade: Recebimento de notificação do pedido
  Como proprietário de um restaurante
  Quero poder receber notificação do recebimento de novo pedido
  Para poder confeccioná-los e entregá-los

  Background:
    Given que o restaurante está logado no sistema
    And que o restaurante está conectado via Socket

  Scenario: Recebimento de novo pedido
    When um cliente finaliza um novo pedido
    Then o restaurante deve receber uma notificação do tipo "toast"

  Scenario: Aceite de pedido via notificação
    Given que um aviso de novo pedido apareceu na interface
    When eu seleciono a opção "Aceitar"
    Then o status do pedido deve ser atualizado para "Aceito"

  Scenario: Recusa de pedido via notificação
    Given que uma notificação de pedido está visível
    When eu seleciono a opção "Recusar"
    Then a notificação deve ser fechada e o pedido cancelado

  Scenario: Notificação persistente no painel
    Given que um novo pedido foi disparado via Socket
    When o alerta "toast" é exibido na tela
    Then o pedido deve ser listado no painel de gerenciamento

  Scenario: Atualização automática do painel de pedidos
    Given que o restaurante está visualizando a lista de pedidos pendentes
    When um novo pedido é aceito
    Then a lista de pedidos deve ser atualizada automaticamente com esse novo pedido

  Scenario: Histórico de alertas recebidos
    Given que o restaurante recebeu múltiplos pedidos simultâneos
    When eu acesso o log de notificações
    Then cada pedido deve ser exibido com detalhes para ação
