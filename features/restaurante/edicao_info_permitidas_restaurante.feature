Funcionalidade: Edição de Informações do Restaurante
  Como proprietário de um restaurante
  Quero poder editar informações do meu perfil
  Para manter os dados do meu estabelecimento atualizados

  Background:
    Given que estou logado no sistema
    And que estou na página de perfil do restaurante "Gosto bom"

  Scenario: Edição de informações permitidas
    When eu altero as seguintes informações:
      | campo                    | novo_valor  |
      | endereço                 | Rua B, 20   |
      | horário de funcionamento | 09:00-23:00 |
    Then as informações devem ser atualizadas com sucesso

  Scenario: Bloqueio de alteração de CNPJ
    When eu tento editar o campo "CNPJ"
    Then o campo "CNPJ" deve estar desabilitado para edição

  Scenario: Persistência de dados após edição
    Given que alterei o tipo do restaurante para "Pizzaria"
    When eu atualizo a página de perfil do restaurante
    Then o sistema deve exibir o novo tipo "Pizzaria"
