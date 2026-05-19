Funcionalidade: Status Operacional do Restaurante
  Como proprietário de um restaurante
  Quero gerenciar o status do meu estabelecimento (aberto/fechado)
  Para garantir que os pedidos só sejam recebidos dentro do horário de funcionamento

  Background:
    Given que estou logado no sistema

  Scenario: Fechamento automático por horário
    Given que o horário atual está fora do intervalo de funcionamento do restaurante "Gosto bom"
    When o cliente visualiza a lista de restaurantes
    Then o restaurante "Gosto bom" deve aparecer com o status "Fechado"

  Scenario: Bloqueio de pedidos fora do horário
    Given que o restaurante está com status "Fechado"
    When um cliente tenta realizar um pedido
    Then o sistema deve exibir "Restaurante indisponível"

  Scenario: Reabertura baseada no cronograma
    Given que o horário de abertura do restaurante chegou
    When o sistema processa a atualização de status
    Then o restaurante deve ficar disponível para receber pedidos

  Scenario: Alteração visual de status para o cliente
    Given que o restaurante mudou seu status para "Fechado"
    When o cliente visualiza o card do restaurante
    Then deve haver um indicador visual de "Fechado"

  Scenario: Mudança manual de status
    Given que eu altero a chave de status para "Fechado" no painel
    Then o sistema deve exibir "Restaurante fechado" e interromper o recebimento de pedidos

  Scenario: Verificação de status na finalização do pedido
    Given que um cliente iniciou a montagem de um carrinho
    When o restaurante muda para "Fechado" antes do checkout ser concluído
    Then o sistema deve informar "Restaurante não aceita mais pedidos"
