from modulos.cliente.cliente_repository import ClienteRepository
from core.seguranca import hash_senha, verificar_senha
from core.jwt import criar_token


class ClienteService:

    def cadastrar_cliente(self, dados):
        repo = ClienteRepository()
        try:
            email = dados['email'].strip().lower()
            cpf = dados['cpf'].strip()

            if repo.buscar_por_email(email):
                return {"erro": "Email já cadastrado", "status_code": 400}

            if repo.buscar_por_cpf(cpf):
                return {"erro": "CPF já cadastrado", "status_code": 400}

            senha_hash = hash_senha(dados['senha'])

            valores = (
                dados['nome'],
                email,
                cpf,
                dados['telefone'],
                senha_hash,
                "cliente"
            )

            cliente_id = repo.inserir_cliente(valores)

            return {
                "mensagem": "Cliente cadastrado com sucesso",
                "cliente_id": cliente_id
            }

        finally:
            repo.fechar()

    def login_cliente(self, dados):
        repo = ClienteRepository()
        try:
            email = dados['email'].strip().lower()
            senha = dados['senha']

            cliente = repo.buscar_por_email(email)

            if not cliente:
                return {"erro": "Credenciais inválidas", "status_code": 401}

            if not verificar_senha(senha, cliente['senha']):
                return {"erro": "Credenciais inválidas", "status_code": 401}

            token = criar_token({
                "sub": str(cliente['id']),
                "email": cliente['email'],
                "role": cliente['role']
            })

            return {"access_token": token}

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

    def atualizar_cliente(self, cliente_id, dados):
        repo = ClienteRepository()
        try:
            cliente = repo.buscar_por_id(cliente_id)

            if not cliente:
                return {"erro": "Cliente não encontrado", "status_code": 404}

            if not dados:
                return {"erro": "Nenhum dado para atualizar", "status_code": 400}

            campos = []
            valores = []

            for campo, valor in dados.items():
                if campo in {"cpf", "role"}:
                    continue

                if campo == "senha":
                    valor = hash_senha(valor)

                campos.append(campo)
                valores.append(valor)

            if not campos:
                return {"erro": "Nenhum campo válido para atualização", "status_code": 400}

            repo.atualizar(cliente_id, campos, valores)

            return {"mensagem": "Cliente atualizado com sucesso"}

        finally:
            repo.fechar()

    def deletar_cliente(self, cliente_id):
        repo = ClienteRepository()
        try:
            cliente = repo.buscar_por_id(cliente_id)

            if not cliente:
                return {"erro": "Cliente não encontrado", "status_code": 404}

            repo.deletar(cliente_id)

            return {"mensagem": "Cliente deletado com sucesso"}

        finally:
            repo.fechar()