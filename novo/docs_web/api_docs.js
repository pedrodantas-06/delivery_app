const apiDados = {
    "menus": [
      {
        "categoria": "Account",
        "endpoints": [
          {
            "titulo": "Details",
            "descricao_geral": "Obtenha os detalhes de uma conta específica.",
            "metodo": "GET",
            "url": "/account/{account_id}",
            "path_params": [
              {
                "nome": "account_id",
                "obrigatorio": true,
                "tipo": "integer",
                "descricao": "O ID da conta que você deseja buscar os detalhes."
              }
            ],
            "query_params": [
              {
                "nome": "session_id",
                "obrigatorio": false,
                "tipo": "string",
                "descricao": "O ID da sessão válida do usuário para autenticação."
              },
              {
                "nome": "language",
                "obrigatorio": false,
                "tipo": "string",
                "descricao": "O código ISO 639-1 para traduzir os dados (ex: pt-BR). Padrão: en-US."
              }
            ],
            "resposta_status": "200 OK",
            "resposta_exemplo": {
              "id": 548,
              "name": "Gabriel",
              "username": "gabriel_dev",
              "include_adult": false
            }
          }
        ]
      },
      {
        "categoria": "Account",
        "endpoints": [
          {
            "titulo": "Details",
            "descricao_geral": "Obtenha os detalhes de uma conta específica.",
            "metodo": "GET",
            "url": "/account/{account_id}",
            "path_params": [
              {
                "nome": "account_id",
                "obrigatorio": true,
                "tipo": "integer",
                "descricao": "O ID da conta que você deseja buscar os detalhes."
              }
            ],
            "query_params": [
              {
                "nome": "session_id",
                "obrigatorio": false,
                "tipo": "string",
                "descricao": "O ID da sessão válida do usuário para autenticação."
              },
              {
                "nome": "language",
                "obrigatorio": false,
                "tipo": "string",
                "descricao": "O código ISO 639-1 para traduzir os dados (ex: pt-BR). Padrão: en-US."
              }
            ],
            "resposta_status": "200 OK",
            "resposta_exemplo": {
              "id": 548,
              "name": "Gabriel",
              "username": "gabriel_dev",
              "include_adult": false
            }
          }
        ]
      }
    ]
  };