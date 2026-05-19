Funcionalidade: Gerenciamento do Carrinho
    Como um cliente da plataforma de delivery.
    Quero poder adicionar, remover e visualizar itens no meu carrinho de compras
    Para que eu possa revisar meu pedido antes de finalizar a compra

Scenario: Adição bem-sucedida de item com customizações ao carrinho
    Given que o usuário "João Silva" está autenticado no sistema
    And o carrinho do usuário "João Silva" está aberto para o restaurante "McDonalds"
    And o item "X-Burguer" do restaurante "McDonalds" está no carrinho
    And o adicional "Bacon Extra" é adicionado ao carrinho
    When o serviço recebe uma requisição para adicionar ao carrinho:
    Then o carrinho do usuário "João Silva" passa a conter o item "X-Burguer" com o adicional "Bacon Extra"
    And o subtotal do carrinho passa a ser "R$ 32,00"
    And o sistema exibe a mensagem "Item adicionado ao carrinho com sucesso"


Scenario: Remoção bem-sucedida de item do carrinho com seus adicionais
    Given que o usuário "João Silva" está autenticado no sistema
    And o carrinho do usuário "João Silva" está aberto para o restaurante "McDonalds"
    And o item "X-Burguer" do restaurante "McDonalds" está no carrinho com o adicional "Bacon Extra"
    And o item "Coca-Cola 350ml" do restaurante "McDonalds" está no carrinho
    And o subtotal do carrinho é "R$ 40,00"
    And o carrinho contém 2 itens
    When o serviço recebe uma requisição para remover o item "X-Burguer" do carrinho
    Then o carrinho do usuário "João Silva" não contém mais o item "X-Burguer"
    And o adicional "Bacon Extra" também é removido do carrinho
    And o carrinho do usuário "João Silva" continua contendo o item "Coca-Cola 350ml"
    And o carrinho passa a conter 1 item
    And o subtotal do carrinho passa a ser "R$ 8,00"
    And o sistema exibe a mensagem "Item removido do carrinho com sucesso"


Scenario: Tentativa de remoção de item inexistente no carrinho
    Given que o usuário "João Silva" está autenticado no sistema
    And o carrinho do usuário "João Silva" está aberto para o restaurante "McDonalds"
    And o item "Coca-Cola 350ml" do restaurante "McDonalds" está no carrinho
    And o subtotal do carrinho é "R$ 8,00"
    When o serviço recebe uma requisição para remover o item "Batata Frita" do carrinho
    Then o sistema exibe a mensagem "Item não encontrado no carrinho"
    And o carrinho do usuário "João Silva" continua contendo o item "Coca-Cola 350ml"
    And o subtotal do carrinho permanece "R$ 8,00"
