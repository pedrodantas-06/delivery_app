#language: pt

Feature: Cadastro e manutenção de métodos de pagamento

  Como um usuário do app de delivery de comida
  Eu quero gerenciar meus métodos de pagamento (inserir, remover, atualizar)
  Para que eu tenha flexibilidade e segurança na hora de pagar meus pedidos

  Scenario: Inserir novo método de pagamento com sucesso
    Given que o usuário "cliente"  está logado no app
    When ele acessar a área "Meus Pagamentos"
    And clicar em "Adicionar novo método de pagamento"
    And preencher os dados de um cartão de crédito válido
    And clicar em "Salvar"
    Then o sistema deve exibir a mensagem "Método de pagamento adicionado com sucesso"
    And o novo cartão deve aparecer na lista de métodos de pagamento

  Scenario: Remover um método de pagamento existente
    Given que o usuário "cliente" possui o cartão "Visa final 1234" cadastrado
    When ele selecionar o cartao "Visa final 1234" na lista de métodos de pagamento
    And clicar em "Remover"
    And confirmar a remoção
    Then o cartao "Visa final 1234" deve ser removido da lista de métodos de pagamento
    And o sistema deve exibir "Método de pagamento removido"

  Scenario: Atualizar dados de um método de pagamento
    Given que o usuário "cliente" possui um cartão salvo como "Visa final 1234"
    When ele editar a data de validade desse cartão para "12/2026"
    And salvar as alterações
    Then o sistema deve exibir "Método de pagamento atualizado com sucesso"
    And o cartão "Visa final 1234" deve ter a data de validade "12/2026" na lista de métodos de pagamento


Feature: Cadastro e manutenção de promoções

  Como um administrador do app de delivery de comida
  Eu quero gerenciar promoções (inserir, remover, atualizar)
  Para que eu possa oferecer descontos e incentivar os usuários a realizarem pedidos

  Scenario: Inserir nova promoção
    Given que o usuário logado possui perfil de administrador
    When ele acessar a área "Gestão de Promoções"
    And clicar em "Nova Promoção"
    And preencher os campos: código promocional, desconto, data de início e fim
    And clicar em "Ativar Promoção"
    Then a promoção deve ser listada como "Ativa"
    And todos os usuários devem conseguir aplicar o código na finalização do pedido

  Scenario: Remover uma promoção ativa
    Given que existe uma promoção ativa chamada "FRETEGRATIS"
    When o administrador clicar em "Remover" ao lado da promoção
    And confirmar a remoção
    Then a promoção não deve mais ser aceita pelo sistema
    And ao tentar aplicar o código "FRETEGRATIS", o sistema deve exibir "Promoção inválida"

  Scenario: Atualizar uma promoção
    Given que existe uma promoção "DESCONTO10" com validade até 10/12/2025
    When o administrador editar a data de fim para 20/12/2025
    And salvar
    Then a promoção deve ficar vigente até a nova data
    And o sistema deve refletir essa mudança ao validar o código


Feature: Disparo de emails para usuários com comprovante de pedido

  Como um usuário do app de delivery de comida
  Eu quero receber um comprovante do meu pedido por email
  Para que eu tenha uma confirmação oficial da minha compra

  Scenario: Após pedido finalizado, enviar comprovante por email
    Given que o usuário selecionou itens no carrinho
    And escolheu um método de pagamento válido
    When ele finalizar o pedido com sucesso
    Then o sistema deve gerar um comprovante
    And enviar um email para o endereço do usuário com assunto "Comprovante do seu pedido"
    And o email deve conter: número do pedido, itens, valor total, forma de pagamento e dados do restaurante


Feature: Aplicação de cupom de desconto

  Como um cliente do app de delivery de comida
  Eu quero aplicar cupons de desconto nos meus pedidos
  Para que eu possa pagar menos pelas minhas compras

  Scenario: Aplicar cupom de desconto válido
    Given que existe um pedido com ID "PEDIDO123" e valor total de "100,00"
    And o pedido está com status "aguardando pagamento"
    And existe um cupom "DESCE20" que oferece "20%" de desconto dentro do prazo de validade
    When o cliente insere o cupom "DESCE20" na tela de pagamento
    Then o valor final da compra é atualizado para "80,00"
    And o cliente recebe uma mensagem de confirmação do desconto aplicado

  Scenario: Aplicar cupom de desconto inválido
    Given que existe um pedido com ID "PEDIDO124" e valor total de "100,00"
    And o pedido está com status "aguardando pagamento"
    And existe um cupom "DESCE20" que oferece "20%" de desconto fora do prazo de validade
    When o cliente insere o cupom "DESCE20" na tela de pagamento
    Then o cliente recebe uma mensagem de erro indicando que o cupom é inválido
    And o valor final da compra permanece "100,00"


Feature: Estorno de saldo ao cancelar pedido

  Como um cliente do app de delivery de comida
  Eu quero cancelar meu pedido e receber estorno do valor pago
  Para que eu não seja prejudicado financeiramente quando o pedido ainda não foi aceito

  Scenario: Realizar estorno de saldo ao cancelar pedido antes do restaurante aceitar
    Given que existe um pedido com ID "PEDIDO123" e valor total de "100,00"
    And o pedido está com status "pago"
    When o cliente solicita cancelamento do pedido antes do restaurante aceitar
    Then o status do pedido deve ser atualizado para "Cancelado"
    And o saldo de "100,00" deve ser estornado para o método de pagamento original
    And o cliente recebe uma mensagem de confirmação do cancelamento

  Scenario: Tentar cancelar pedido depois do restaurante aceitar
    Given que existe um pedido com ID "PEDIDO123" e valor total de "100,00"
    And o pedido está com status "pago"
    When o cliente solicita cancelamento do pedido depois do restaurante aceitar
    Then o status do pedido deve permanecer como "Pago"
    And nenhum estorno deve ser realizado
    And o cliente recebe uma mensagem de erro indicando que o pedido não pode ser cancelado
