"""
Testes do fluxo de clientes unificado em `usuarios` + recuperação de senha.

Seguem o padrão de mock de banco usado em test_auth_login.py: substituímos o
repositório/conexão por objetos falsos para validar a lógica de serviço e rotas
sem precisar de um MySQL real.
"""
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app
from core.jwt import criar_token
import modulos.cliente.cliente_service as cs_mod

client = TestClient(app)


def auth_header(sub="1", role="CLIENTE"):
    token = criar_token({"sub": sub, "role": role})
    return {"Authorization": f"Bearer {token}"}


class FakeRepo:
    """Repositório falso configurável via FakeRepo.state."""

    state = {}

    def __init__(self):
        pass

    def fechar(self):
        pass

    def buscar_usuario_por_email(self, email):
        return FakeRepo.state.get("usuario_por_email")

    def buscar_cliente_por_cpf(self, cpf):
        return FakeRepo.state.get("cliente_por_cpf")

    def buscar_usuario_por_id(self, usuario_id):
        return FakeRepo.state.get("usuario_por_id")

    def buscar_perfil(self, usuario_id):
        return FakeRepo.state.get("perfil")

    def listar(self, filtros=None):
        return FakeRepo.state.get("lista", [])

    def estatisticas_pedidos(self, cliente_id):
        FakeRepo.state["stats_cliente_id"] = cliente_id
        return FakeRepo.state.get("stats")

    def cadastrar(self, *args):
        FakeRepo.state["cadastrou"] = args

    def atualizar(self, usuario_id, referencia_id, dados_usuario, dados_cliente):
        FakeRepo.state["atualizou"] = (usuario_id, referencia_id, dados_usuario, dados_cliente)

    def deletar(self, usuario_id, referencia_id):
        FakeRepo.state["deletou"] = (usuario_id, referencia_id)


@pytest.fixture(autouse=True)
def fake_repo(monkeypatch):
    FakeRepo.state = {}
    monkeypatch.setattr(cs_mod, "ClienteRepository", FakeRepo)
    yield


def install_auth_db(monkeypatch, fetch_value):
    conn = MagicMock()
    cur = MagicMock()
    cur.fetchone.return_value = fetch_value
    conn.cursor.return_value = cur
    monkeypatch.setattr(
        "modulos.auth.auth_service.ConexaoBanco.get_connection", lambda: conn
    )
    return cur


# ----------------------------------------------------------------------
# Cadastro
# ----------------------------------------------------------------------
def test_cadastro_cria_usuario_e_cliente():
    FakeRepo.state.update({"usuario_por_email": None, "cliente_por_cpf": None})
    r = client.post("/api/v1/clientes/", json={
        "nome": "Maria",
        "email": "MARIA@email.com",
        "cpf": "98765432100",
        "telefone": "11888888888",
        "senha": "123456",
    })
    assert r.status_code == 201
    body = r.json()
    assert body["cliente_id"].startswith("cli_")
    # cadastrou = (cliente_id, nome, email_normalizado, cpf, telefone, senha_hash)
    cadastro = FakeRepo.state["cadastrou"]
    assert cadastro[2] == "maria@email.com"  # email normalizado
    assert cadastro[1] == "Maria"


def test_cadastro_email_duplicado():
    FakeRepo.state.update({"usuario_por_email": {"id": 1}, "cliente_por_cpf": None})
    r = client.post("/api/v1/clientes/", json={
        "nome": "Maria", "email": "maria@email.com", "cpf": "1",
        "telefone": "1", "senha": "x",
    })
    assert r.status_code == 400
    assert r.json()["detail"] == "Email já cadastrado"


def test_cadastro_cpf_duplicado():
    FakeRepo.state.update({"usuario_por_email": None, "cliente_por_cpf": {"id": "cli_x"}})
    r = client.post("/api/v1/clientes/", json={
        "nome": "Maria", "email": "maria@email.com", "cpf": "1",
        "telefone": "1", "senha": "x",
    })
    assert r.status_code == 400
    assert r.json()["detail"] == "CPF já cadastrado"


# ----------------------------------------------------------------------
# Estatísticas
# ----------------------------------------------------------------------
def test_estatisticas_pedidos():
    FakeRepo.state.update({
        "usuario_por_id": {"id": 1, "referencia_id": "cli_1"},
        "stats": {"total": 3, "no_mes": 1, "preco_medio": 42.5},
    })
    r = client.get("/api/v1/clientes/me/estatisticas", headers=auth_header(sub="1"))
    assert r.status_code == 200
    assert r.json() == {"total": 3, "no_mes": 1, "preco_medio": 42.5}
    assert FakeRepo.state["stats_cliente_id"] == "cli_1"


def test_estatisticas_sem_token():
    r = client.get("/api/v1/clientes/me/estatisticas")
    assert r.status_code in (401, 403)  # HTTPBearer bloqueia sem credenciais


# ----------------------------------------------------------------------
# Atualizar / Deletar (autorização + distribuição de campos)
# ----------------------------------------------------------------------
def test_atualizar_distribui_campos_entre_tabelas():
    FakeRepo.state.update({"usuario_por_id": {"id": 1, "referencia_id": "cli_1"}})
    r = client.put("/api/v1/clientes/1", json={"nome": "Novo", "telefone": "99999"},
                   headers=auth_header(sub="1"))
    assert r.status_code == 200
    usuario_id, ref, dados_usuario, dados_cliente = FakeRepo.state["atualizou"]
    assert usuario_id == 1 and ref == "cli_1"
    assert dados_usuario == {"nome": "Novo"}
    assert dados_cliente == {"nome": "Novo", "telefone": "99999"}


def test_atualizar_outro_usuario_negado():
    r = client.put("/api/v1/clientes/2", json={"nome": "X"}, headers=auth_header(sub="1"))
    assert r.status_code == 403


def test_deletar_dono():
    FakeRepo.state.update({"usuario_por_id": {"id": 1, "referencia_id": "cli_1"}})
    r = client.delete("/api/v1/clientes/1", headers=auth_header(sub="1"))
    assert r.status_code == 200
    assert FakeRepo.state["deletou"] == (1, "cli_1")


def test_deletar_outro_usuario_negado():
    r = client.delete("/api/v1/clientes/2", headers=auth_header(sub="1"))
    assert r.status_code == 403


# ----------------------------------------------------------------------
# Recuperação de senha (modo dev)
# ----------------------------------------------------------------------
def test_forgot_password_devolve_token_em_dev(monkeypatch):
    install_auth_db(monkeypatch, {"id": 1})
    r = client.post("/api/v1/auth/forgot-password", json={"email": "maria@email.com"})
    assert r.status_code == 200
    body = r.json()
    assert "mensagem" in body
    assert body.get("token")  # exposto em modo dev


def test_forgot_password_email_inexistente_sem_token(monkeypatch):
    install_auth_db(monkeypatch, None)
    r = client.post("/api/v1/auth/forgot-password", json={"email": "naoexiste@email.com"})
    assert r.status_code == 200
    assert "token" not in r.json()


def test_reset_password_token_invalido(monkeypatch):
    install_auth_db(monkeypatch, None)
    r = client.post("/api/v1/auth/reset-password", json={"token": "x", "nova_senha": "nova"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Token inválido ou expirado"


def test_reset_password_sucesso(monkeypatch):
    install_auth_db(monkeypatch, {"id": 5, "usuario_id": 1})
    r = client.post("/api/v1/auth/reset-password", json={"token": "validtoken", "nova_senha": "nova"})
    assert r.status_code == 200
    assert r.json()["mensagem"] == "Senha redefinida com sucesso"
