Feature: Gestão de Clientes

# ==============================
# CADASTRO
# ==============================

Scenario: Cadastrar cliente com sucesso
    Given não existe usuário com esse email
    And não existe cliente com esse cpf
    When faço POST para "/api/v1/clientes/" com nome "João", email "joao@email.com", cpf "12345678900", telefone "81999999999" e senha "123456"
    Then status deve ser 201
    And cliente deve ser cadastrado
    And deve retornar cliente_id


Scenario: Não permitir cadastro com email duplicado
    Given não existe cliente com esse cpf
    And existe usuário com esse email
    When faço POST para "/api/v1/clientes/" com nome "João", email "joao@email.com", cpf "12345678900", telefone "81999999999" e senha "123456"
    Then status deve ser 400


Scenario: Não permitir cadastro com cpf duplicado
    Given não existe usuário com esse email
    And existe cliente com esse cpf
    When faço POST para "/api/v1/clientes/" com nome "João", email "outro@email.com", cpf "12345678900", telefone "81999999999" e senha "123456"
    Then status deve ser 400


# ==============================
# ATUALIZAÇÃO
# ==============================

Scenario: Atualizar cliente sendo o próprio dono
    Given estou autenticado como usuário "1"
    And existe usuário dono do recurso
    When faço PUT para "/api/v1/clientes/1" alterando nome para "João Atualizado"
    Then status deve ser 200
    And cliente deve ser atualizado


Scenario: Impedir atualização de outro usuário
    Given estou autenticado como usuário "1"
    When faço PUT para "/api/v1/clientes/2" alterando nome para "Hack"
    Then status deve ser 403


# ==============================
# REMOÇÃO
# ==============================

Scenario: Deletar cliente sendo o próprio dono
    Given estou autenticado como usuário "1"
    And existe usuário dono do recurso
    When faço DELETE para "/api/v1/clientes/1"
    Then status deve ser 200
    And cliente deve ser removido


Scenario: Impedir deletar cliente sem permissão
    Given estou autenticado como usuário "1"
    When faço DELETE para "/api/v1/clientes/2"
    Then status deve ser 403
