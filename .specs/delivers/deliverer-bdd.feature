Feature: Entregador e fluxo de entrega
  Como entregador
  Quero gerenciar meu status e aceitar/realizar entregas
  Para cumprir pedidos atribuídos sem alterar domínio Orders

  Background:
    Given que existem entregadores cadastrados na região "Zona Sul"

  Scenario: Registrar novo entregador
    When eu envio um pedido para criar um entregador com nome "Ana" e telefone "11999999999"
    Then a API responde 201 e retorna o id do entregador

  Scenario: Entregador fica disponível e recebe atribuição automática
    Given um order criado na região "Zona Sul" com id "order-123"
    And existem entregadores AVAILABLE na região "Zona Sul"
    When o sistema tenta atribuir o delivery para order "order-123"
    Then o delivery fica com status ASSIGNED e um deliverer_id é preenchido

  Scenario: Entregador aceita (race) — somente um ganha
    Given um delivery ASSIGNED para order "order-xyz"
    When dois entregadores enviam accept simultâneo
    Then apenas o primeiro acceptante tem a atribuição confirmada

  Scenario: Coletar pedido
    Given um delivery ASSIGNED com deliverer_id "d-1"
    When o entregador faz pickup
    Then delivery.status é PICKED_UP e picked_up_at é registrado

  Scenario: Confirmar entrega
    Given um delivery PICKED_UP com deliverer_id "d-1"
    When o entregador envia deliver
    Then delivery.status é DELIVERED e delivered_at é registrado e evento DeliveryCompleted é publicado
