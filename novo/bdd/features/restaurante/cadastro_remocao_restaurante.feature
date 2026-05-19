Feature: Cadastro e Remoção de Restaurante
  Como um parceiro da plataforma de delivery
  Quero poder cadastrar ou remover meu restaurante
  Para que eu possa vender meus produtos pelo aplicativo

  Background:
    Given que o endpoint de "cadastro de restaurante" está "disponível"

  Scenario: Requisição de cadastro processado com sucesso
    Given que o "restaurante" cujo "nome" é "Gosto Legal" "não existe" na tabela "restaurantes" do banco de dados
    And que o "restaurante" cujo "cnpj" é "00.000.000/0001-00" "não existe" na tabela "restaurantes" do banco de dados
    When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
      | nome        | endereco  | cnpj               | horario     | tipo         |
      | Gosto Legal | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
    Then o sistema deve registrar o restaurante "Gosto Legal" na tabela "restaurantes" do banco de dados
    And o restaurante "Gosto Legal" deve estar "disponível" para criar propostas
    And o sistema responde com o código HTTP "201"

  Scenario Outline: Requisição de cadastro processado com erro - dados faltantes
    Given que o "restaurante" cujo "nome" é "Gosto ruim" "não existe" na tabela "restaurantes" do banco de dados
    When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
      | nome    | endereco   | cnpj   | horario   | tipo   |
      | <nome>  | <endereco> | <cnpj> | <horario> | <tipo> |
    Then o sistema responde com o código HTTP "400"
    Examples:
      | nome       | endereco  | cnpj               | horario     | tipo         |
      |            | Rua A, 10 |                    | 08:00-22:00 |              |
      | Gosto ruim | Rua A, 10 |                    | 08:00-22:00 | Hamburgueria |
      | Gosto ruim | Rua A, 10 |                    |             | Hamburgueria |
      | Gosto ruim | Rua A, 10 |                    | 08:00-22:00 |              |

  Scenario: Requisição de cadastro processado com erro - nome já existe
    Given que o "restaurante" cujo "nome" é "Gosto bom" "existe" na tabela "restaurantes" do banco de dados
    When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
      | nome      | endereco  | cnpj               | horario     | tipo         |
      | Gosto bom | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
    Then o sistema responde com o código HTTP "400"

  Scenario: Requisição de cadastro processado com erro - cnpj já existe
    Given que o "restaurante" cujo "cnpj" é "12.345.678/0001-99" "existe" na tabela "restaurantes" do banco de dados
    When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
      | nome      | endereco  | cnpj               | horario     | tipo         |
      | Gosto bom | Rua A, 10 | 12.345.678/0001-99 | 08:00-22:00 | Hamburgueria |
    Then o sistema responde com o código HTTP "400"

  Scenario: Requisição de remoção processado com sucesso
    Given que o "restaurante" cujo "id" é "1" "existe" na tabela "restaurantes" do banco de dados
    And eu sou o proprietário do "restaurante" de id "1"
    When eu envio uma requisição ao endpoint de "remoção de restaurante" com os dados:
      | id  |
      | 1 |
    Then o sistema deve remover o restaurante "1" na tabela "restaurantes" do banco de dados
    And o restaurante "1" deve estar "indisponível" para criar propostas
    And o sistema responde com o código HTTP "200"

    Scenario: Requisição de remoção processado com erro
    Given que o "restaurante" cujo "id" é "123" "não existe" na tabela "restaurantes" do banco de dados
    And eu sou o proprietário do "restaurante" de id "123"
    When eu envio uma requisição ao endpoint de "remoção de restaurante" com os dados:
      | id  |
      | 123 |
    Then o sistema deve remover o restaurante "123" na tabela "restaurantes" do banco de dados
    And o restaurante "123" deve estar "indisponível" para criar propostas
    And o sistema responde com o código HTTP "404"