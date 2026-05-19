Feature: Cadastro de Restaurante
  Como um parceiro da plataforma de delivery
  Quero poder cadastrar meu restaurante
  Para que eu possa vender meus produtos pelo aplicativo

  Background:
    Given que o endpoint de "cadastro de restaurante" está "disponível"

  Scenario: Requisição de cadastro processado com sucesso
    Given que o "restaurante" cujo "nome" é "Gosto bom" não existe na tabela "restaurantes" do banco de dados
    When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
      | nome      | endereco  | cnpj               | horario     | tipo         |
      | Gosto bom | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
    Then o sistema deve registrar o restaurante "Gosto bom" na tabela "restaurantes" do banco de dados
    And o restaurante "Gosto bom" deve estar disponível para criar propostas
    And o sistema responde com o código HTTP "201"

    Scenario Outline: Requisição de cadastro processado com erro - dados faltantes
      Given que o "restaurante" cujo "nome" é "Gosto bom" não existe na tabela "restaurantes" do banco de dados
      When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
        | nome    | endereco   | cnpj   | horario   | tipo   |
        | <nome>  | <endereco> | <cnpj> | <horario> | <tipo> |
      Then o sistema responde com o código HTTP "400"
      Examples:
        | nome      | endereco  | cnpj               | horario     | tipo         |
        |           | Rua A, 10 |                    | 08:00-22:00 |              |
        | Gosto bom | Rua A, 10 |                    | 08:00-22:00 | Hamburgueria |
        | Gosto bom | Rua A, 10 |                    |             | Hamburgueria |
        | Gosto bom | Rua A, 10 |                    | 08:00-22:00 |              |

    Scenario: Requisição de cadastro processado com erro - nome já existe
      Given que o "restaurante" cujo "nome" é "Gosto bom" existe na tabela "restaurantes" do banco de dados
      When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
        | nome      | endereco  | cnpj               | horario     | tipo         |
        | Gosto bom | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
      Then o sistema responde com o código HTTP "400"

    Scenario: Requisição de cadastro processado com erro - cnpj já existe
      Given que o "restaurante" cujo "cnpj" é "00.000.000/0001-00" existe na tabela "restaurantes" do banco de dados
      When eu envio uma requisição ao endpoint de "cadastro de restaurante" com os dados:
        | nome      | endereco  | cnpj               | horario     | tipo         |
        | Gosto bom | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
      Then o sistema responde com o código HTTP "400"
