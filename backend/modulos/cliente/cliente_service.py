import uuid

from modulos.cliente.cliente_repository import ClienteRepository
from modulos.auth.auth_service import AuthService
from core.seguranca import hash_senha


class ClienteService:

    def cadastrar_cliente(self, dados):
        repo = ClienteRepository()
        try:
            nome = dados["nome"].strip()
            email = dados["email"].strip().lower()
            cpf = dados["cpf"].strip()
            telefone = dados["telefone"].strip()

            if repo.buscar_usuario_por_email(email):
                return {"erro": "Email já cadastrado", "status_code": 400}

            if repo.buscar_cliente_por_cpf(cpf):
                return {"erro": "CPF já cadastrado", "status_code": 400}

            cliente_id = "cli_" + uuid.uuid4().hex[:12]
            senha_hash = hash_senha(dados["senha"])

            repo.cadastrar(cliente_id, nome, email, cpf, telefone, senha_hash)

            return {
                "mensagem": "Cliente cadastrado com sucesso",
                "cliente_id": cliente_id,
            }

        finally:
            repo.fechar()

    def login_cliente(self, dados):
        # Login unificado: a fonte de verdade da autenticação é a tabela `usuarios`.
        return AuthService.login(dados["email"], dados["senha"])

    def obter_perfil(self, usuario_id):
        repo = ClienteRepository()
        try:
            perfil = repo.buscar_perfil(usuario_id)
            if not perfil:
                return {"erro": "Cliente não encontrado", "status_code": 404}
            return {"cliente": perfil}
        finally:
            repo.fechar()

    def listar_clientes(self, filtros=None):
        repo = ClienteRepository()
        try:
            filtros_permitidos = {"id", "nome", "email", "cpf"}

            filtros_filtrados = {
                k: v for k, v in (filtros or {}).items()
                if k in filtros_permitidos
            }

            clientes = repo.listar(filtros_filtrados)

            return {"clientes": clientes}

        finally:
            repo.fechar()

    def atualizar_cliente(self, usuario_id, dados):
        repo = ClienteRepository()
        try:
            usuario = repo.buscar_usuario_por_id(usuario_id)
            if not usuario:
                return {"erro": "Cliente não encontrado", "status_code": 404}

            if not dados:
                return {"erro": "Nenhum dado para atualizar", "status_code": 400}

            if "email" in dados:
                email = dados["email"].strip().lower()
                existente = repo.buscar_usuario_por_email(email)
                if existente and existente["id"] != usuario_id:
                    return {"erro": "Email já cadastrado", "status_code": 400}
                dados["email"] = email

            # Distribui cada campo para a tabela correta.
            dados_usuario = {}
            dados_cliente = {}

            for campo, valor in dados.items():
                if campo == "nome":
                    dados_usuario["nome"] = valor
                    dados_cliente["nome"] = valor
                elif campo == "email":
                    dados_usuario["email"] = valor
                    dados_cliente["email"] = valor
                elif campo == "senha":
                    dados_usuario["senha"] = hash_senha(valor)
                elif campo == "telefone":
                    dados_cliente["telefone"] = valor

            if not dados_usuario and not dados_cliente:
                return {"erro": "Nenhum campo válido para atualização", "status_code": 400}

            repo.atualizar(
                usuario_id, usuario["referencia_id"], dados_usuario, dados_cliente
            )

            return {"mensagem": "Cliente atualizado com sucesso"}

        finally:
            repo.fechar()

    def deletar_cliente(self, usuario_id):
        repo = ClienteRepository()
        try:
            usuario = repo.buscar_usuario_por_id(usuario_id)
            if not usuario:
                return {"erro": "Cliente não encontrado", "status_code": 404}

            repo.deletar(usuario_id, usuario["referencia_id"])

            return {"mensagem": "Cliente deletado com sucesso"}

        finally:
            repo.fechar()

    def estatisticas_pedidos(self, usuario_id):
        repo = ClienteRepository()
        try:
            usuario = repo.buscar_usuario_por_id(usuario_id)
            if not usuario:
                return {"erro": "Cliente não encontrado", "status_code": 404}

            cliente_id = usuario["referencia_id"]
            stats = repo.estatisticas_pedidos(cliente_id) if cliente_id else None

            if not stats:
                stats = {"total": 0, "no_mes": 0, "preco_medio": 0}

            return {
                "total": int(stats["total"]),
                "no_mes": int(stats["no_mes"]),
                "preco_medio": round(float(stats["preco_medio"]), 2),
            }
        finally:
            repo.fechar()
