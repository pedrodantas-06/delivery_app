Funcionalidade: Cadastro de Restaurante
  Como um parceiro da plataforma de delivery
  Quero poder cadastrar meu restaurante
  Para que eu possa vender meus produtos pelo aplicativo

Scenario: Cadastro realizado com sucesso pelo proprietário
    Given que eu sou o proprietário do restaurante “Gosto bom”
    And o restaurante “Gosto bom” não existe no sistema
    When eu preencho os dados de cadastro e finalizo o processo
    Then o restaurante “Gosto bom” está disponível para criar propostas imediatamente