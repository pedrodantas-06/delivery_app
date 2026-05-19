Feature: Gestão de clientes - Autenticação

    # ==============================
    # Cadastro
    # ==============================

    Scenario: cadastrar cliente com sucesso
        Given nao existe cliente cadastrado com email "joao@email.com"
        When um cliente e registrado com nome "João Silva", email "joao@email.com", senha "123456", cpf "12345678900" e telefone "11999999999"
        Then o cliente "João Silva" deve ser criado com email "joao@email.com"

    Scenario: falha ao cadastrar cliente com email duplicado
        Given existe um cliente "João Silva" com email "joao@email.com"
        When um cliente e registrado com nome "Maria Souza", email "joao@email.com", senha "abc123", cpf "98765432100" e telefone "11888888888"
        Then o sistema deve rejeitar o cadastro com erro "Email já cadastrado"

    Scenario: falha ao cadastrar cliente com cpf duplicado
        Given existe um cliente "João Silva" com cpf "12345678900"
        When um cliente e registrado com nome "Maria Souza", email "maria@email.com", senha "abc123", cpf "12345678900" e telefone "11888888888"
        Then o sistema deve rejeitar o cadastro com erro "CPF já cadastrado"

    Scenario: falha ao cadastrar cliente com email invalido
        Given nao existe cliente cadastrado com email "email-invalido"
        When um cliente e registrado com nome "Maria Souza", email "email-invalido", senha "123456", cpf "98765432100" e telefone "11888888888"
        Then o sistema deve rejeitar o cadastro com erro "Email inválido"

    Scenario: falha ao cadastrar cliente com senha invalida
        Given nao existe cliente cadastrado com email "maria@email.com"
        When um cliente e registrado com nome "Maria", email "maria@email.com", senha "123", cpf "98765432100" e telefone "11888888888"
        Then o sistema deve rejeitar o cadastro com erro "Senha deve ter no mínimo 6 caracteres"

    # ==============================
    # Login
    # ==============================

    Scenario: cliente autenticado com credenciais validas
        Given existe um cliente "João Silva" com email "joao@email.com" e senha "123456"
        When o cliente tenta autenticar com email "joao@email.com" e senha "123456"
        Then o cliente "João Silva" deve ser autenticado com sucesso

    Scenario: falha na autenticacao por senha incorreta
        Given existe um cliente "João Silva" com email "joao@email.com" e senha "123456"
        When o cliente tenta autenticar com email "joao@email.com" e senha "senhaerrada"
        Then o sistema deve rejeitar a autenticacao com erro "Senha incorreta"

    Scenario: falha na autenticacao por email inexistente
        Given nao existe cliente cadastrado com email "inexistente@email.com"
        When o cliente tenta autenticar com email "inexistente@email.com" e senha "123456"
        Then o sistema deve rejeitar a autenticacao com erro "Cliente não encontrado"

    # ==============================
    # Recuperacao de senha
    # ==============================

    Scenario: solicitar recuperacao de senha com sucesso
        Given existe um cliente "João Silva" com email "joao@email.com"
        When o cliente solicita recuperacao de senha para o email "joao@email.com"
        Then o sistema envia um email de recuperacao para "joao@email.com"

    Scenario: falha ao solicitar recuperacao com email inexistente
        Given nao existe cliente cadastrado com email "inexistente@email.com"
        When o cliente solicita recuperacao de senha para o email "inexistente@email.com"
        Then o sistema deve rejeitar a solicitacao com erro "Cliente não encontrado"

    Scenario: redefinir senha com sucesso
        Given existe um cliente "João Silva" com email "joao@email.com"
        And existe um token de recuperacao valido para o cliente "João Silva"
        When o cliente redefine a senha para "novaSenha123"
        Then a senha do cliente "João Silva" deve ser atualizada