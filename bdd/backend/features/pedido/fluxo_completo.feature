Feature: Fluxo completo de pedido demo

    Scenario: cliente cria pedido e pagamento é aprovado
        Given que o cliente demo "cli_demo_001" está autenticado
        When o cliente cria um pedido no restaurante 1 com item "X-Burguer" por 25 reais
        And o pagamento do pedido é processado
        Then o pedido deve ter status "Pago"

    Scenario: restaurante aceita pedido pago
        Given que existe um pedido 100 com status "Pago" no restaurante 1
        When o restaurante aceita o pedido 100
        Then o pedido deve ter status "Em preparo"

    Scenario: fluxo demo autentica todas as roles
        When o usuário faz login com email "cliente@yummicious.com" e senha "123456"
        Then a autenticação retorna role "CLIENTE"
        When o usuário faz login com email "burger@burgerhouse.com" e senha "123456"
        Then a autenticação retorna role "RESTAURANTE"
        When o usuário faz login com email "entregador@yummicious.com" e senha "123456"
        Then a autenticação retorna role "ENTREGADOR"
        When o usuário faz login com email "admin@yummicious.com" e senha "123456"
        Then a autenticação retorna role "ADMIN"
