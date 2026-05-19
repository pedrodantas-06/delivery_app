Feature: clientes

Scenario: Cadastro de cliente com dados válidos
  Given que o usuário não possui cadastro
  When ele informa nome, email e senha válidos
  Then o cliente é cadastrado com sucesso

Scenario: Cadastro com email já existente
  Given que já existe um cliente com o email informado
  When o usuário tenta se cadastrar novamente com esse email
  Then o sistema deve exibir uma mensagem de erro

Scenario: Cadastro com dados inválidos
  Given que o usuário está na tela de cadastro
  When ele informa um email inválido
  Then o sistema deve rejeitar o cadastro

Scenario: Remoção de cliente existente
  Given que o cliente está autenticado
  When ele solicita a exclusão da conta
  Then o cliente deve ser removido do sistema

Scenario: Remoção sem autenticação
  Given que o usuário não está autenticado
  When tenta remover uma conta
  Then o sistema deve negar a operação

Scenario: Atualização de dados do cliente
  Given que o cliente está autenticado
  When ele atualiza seus dados pessoais
  Then as informações devem ser salvas com sucesso

Scenario: Atualização com dados inválidos
  Given que o cliente está autenticado
  When ele informa dados inválidos
  Then o sistema deve exibir erro e não salvar

Scenario: Visualizar histórico de pedidos
  Given que o cliente está autenticado
  When ele acessa seu histórico
  Then o sistema deve exibir a lista de pedidos

Scenario: Histórico vazio
  Given que o cliente não possui pedidos
  When ele acessa o histórico
  Then o sistema deve informar que não há pedidos

Scenario: Visualizar estatísticas do mês
  Given que o cliente possui pedidos registrados
  When ele acessa as estatísticas
  Then o sistema deve mostrar quantidade total, quantidade no mês e preço médio

Scenario: Estatísticas sem pedidos
  Given que o cliente não possui pedidos no mês
  When acessa as estatísticas
  Then os valores devem ser zero ou vazios

Scenario: Solicitar recuperação de senha com email válido
  Given que o cliente possui conta cadastrada
  When ele solicita recuperação com email válido
  Then o sistema deve enviar um email de recuperação

Scenario: Recuperação com email inexistente
  Given que o email não está cadastrado
  When o usuário solicita recuperação
  Then o sistema deve exibir mensagem de erro

Scenario: Redefinir senha com sucesso
  Given que o cliente recebeu o link de recuperação
  When ele define uma nova senha válida
  Then a senha deve ser atualizada com sucesso