Funcionalidade: Edição de Informações do Restaurante
  Como proprietário de um restaurante
  Quero poder editar informações do meu perfil
  Para manter os dados do meu estabelecimento atualizados

Scenario: Edição de informações permitidas
    Given que estou na página de perfil do restaurante “Gosto bom”
    And sou o proprietário do restaurante “Gosto bom”
    When eu altero o endereço e o horário de funcionamento
    Then as novas informações são salvas no banco de dados

Scenario: Bloqueio de alteração de CNPJ
    Given que o restaurante “Gosto bom” já possui um “CNPJ” cadastrado
    When eu tento editar o campo de “CNPJ”
    Then o campo deve estar desabilitado para edição

Scenario: Persistência de dados após edição
    Given que alterei o tipo do restaurante “Gosto bom”
    When eu atualizo a página de perfil do restaurante “Gosto bom”
    Then o sistema deve exibir o novo tipo cadastrado
