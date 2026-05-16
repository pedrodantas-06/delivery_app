Funcionalidade: Validação de Acesso do Restaurante
  Como um parceiro da plataforma de delivery
  Quero acessar o painel do meu restaurante
  Para que eu possa gerenciar minhas propostas

Scenario: Validação de acesso ao painel de propostas
    Given que concluí o autocadastro do restaurante “Gosto bom”
    When eu acesso o painel principal
    Then visualizo a opção de cadastrar novas propostas