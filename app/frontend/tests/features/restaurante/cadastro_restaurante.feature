Funcionalidade: Cadastro de Restaurante
  Como um parceiro da plataforma de delivery
  Quero poder cadastrar meu restaurante
  Para que eu possa vender meus produtos pelo aplicativo

  Background:
    Given que estou na página de cadastro

  Scenario: Cadastro realizado com sucesso
    Given que o restaurante "Gosto bom" não existe no sistema
    When eu preencho o cadastro com os dados:
      | nome      | endereço  | cnpj               | horário     | tipo         |
      | Gosto bom | Rua A, 10 | 00.000.000/0001-00 | 08:00-22:00 | Hamburgueria |
    And eu finalizo o processo de cadastro
    Then o restaurante "Gosto bom" deve estar disponível para criar propostas

  Scenario Schema: Validação de campos obrigatórios
    When eu preencho o cadastro com dados incompletos:
      | nome   | endereço   | cnpj   | horário   | tipo   |
      | <nome> | <endereço> | <cnpj> | <horário> | <tipo> |
    And eu finalizo o processo de cadastro
    Then o sistema deve exibir "Campo obrigatório não preenchido" e impedir o envio

    Exemplos:
      | nome      | endereço  | cnpj               | horário     | tipo         |
      | Gosto bom | Rua A, 10 |                    | 08:00-22:00 | Hamburgueria |
      | Gosto bom | Rua A, 10 | 00.000.000/0001-00 |             | Hamburgueria |

  Scenario: Validação de formato de documento (CNPJ)
    When eu informo um CNPJ inválido "123"
    Then o sistema deve exibir "Formato de documento inválido"
