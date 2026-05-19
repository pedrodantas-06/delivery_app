Funcionalidade: Validação de Acesso do Restaurante
  Como um parceiro da plataforma de delivery
  Quero acessar o painel do meu restaurante
  Para que eu possa gerenciar minhas propostas

  Background:
    Given que estou logado no sistema

  Scenario: Acesso ao painel de propostas
    Given que concluí o cadastro do restaurante "Gosto bom"
    When eu acesso o painel principal
    Then eu devo visualizar a opção de "Cadastrar propostas"
