Feature: Edição de Informações do Restaurante
  Como proprietário de um restaurante
  Quero poder editar informações do meu perfil
  Para manter os dados do meu estabelecimento atualizados

  Background:
    Given que o endpoint de "edição de restaurante" está "disponível"
    And eu sou o proprietário do "restaurante" de id "123"
    And que o "restaurante" cujo "id" é "123" "existe" na tabela "restaurantes" do banco de dados

  Scenario: Edição de informações permitidas
    When eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:
      | id  | campo | novo_valor      |
      | 123 | nome  | Gosto Muito Bom |
    Then o sistema deve atualizar o "restaurante" cujo "id" é "123" com o novo "nome" para "Gosto Muito Bom" na tabela "restaurantes" do banco de dados
    And o sistema responde com o código HTTP "200"

  Scenario: Edição de informações proibidas
    When eu envio uma requisição ao endpoint de "edição de restaurante" com os dados:
      | id  | campo | novo_valor         |
      | 123 | cnpj  | 00.000.000/0001-00 |
    Then o sistema responde com o código HTTP "400"
