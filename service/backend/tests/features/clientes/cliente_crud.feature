Feature: Gestão de clientes - Manutenção

    # ==============================
    # Atualização
    # ==============================

    Scenario: atualizar dados do cliente com sucesso
        Given existe um cliente "João Silva" com email "joao@email.com"
        When o cliente "João Silva" atualiza seus dados com:
            | campo    | valor       |
            | telefone | 11988888888 |
        Then o cliente "João Silva" deve ter telefone "11988888888"

    Scenario: falha ao atualizar cliente para email ja cadastrado
        Given existe um cliente "João Silva" com email "joao@email.com"
        And existe um cliente "Maria Souza" com email "maria@email.com"
        When o cliente "João Silva" atualiza seus dados com:
            | campo | valor             |
            | email | maria@email.com   |
        Then o sistema deve rejeitar a operacao com erro "Email já cadastrado"

    Scenario: falha ao atualizar cliente inexistente
        Given nao existe cliente cadastrado com email "inexistente@email.com"
        When o cliente com email "inexistente@email.com" atualiza seus dados
        Then o sistema deve rejeitar a operacao com erro "Cliente não encontrado"

    # ==============================
    # Remoção
    # ==============================

    Scenario: remover cliente com sucesso
        Given existe um cliente "João Silva" com email "joao@email.com"
        When o cliente "João Silva" solicita a exclusao da conta
        Then o cliente "João Silva" nao deve mais existir no sistema

    Scenario: falha ao remover cliente inexistente
        Given nao existe cliente cadastrado com email "inexistente@email.com"
        When o cliente com email "inexistente@email.com" solicita a exclusao da conta
        Then o sistema deve rejeitar a operacao com erro "Cliente não encontrado"