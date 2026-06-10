import pytest
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from main import app
import modulos.cliente.cliente_service as cs_mod
from core.jwt import criar_token

scenarios("../../bdd/backend/features/cliente/cliente.feature")

# =========================
# CLIENT
# =========================

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def context():
    return {}


# =========================
# AUTH HEADER (igual ao unificado)
# =========================

def auth_header(sub="1", role="CLIENTE"):
    token = criar_token({"sub": sub, "role": role})
    return {"Authorization": f"Bearer {token}"}


# =========================
# FAKE REPOSITORY
# =========================

class FakeRepo:
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

    def cadastrar(self, *args):
        FakeRepo.state["cadastrou"] = args

    def atualizar(self, usuario_id, referencia_id, dados_usuario, dados_cliente):
        FakeRepo.state["atualizou"] = (
            usuario_id,
            referencia_id,
            dados_usuario,
            dados_cliente,
        )

    def deletar(self, usuario_id, referencia_id):
        FakeRepo.state["deletou"] = (usuario_id, referencia_id)


@pytest.fixture(autouse=True)
def fake_repo(monkeypatch):
    FakeRepo.state = {}
    monkeypatch.setattr(cs_mod, "ClienteRepository", FakeRepo)
    yield


# =========================
# GIVEN
# =========================

@given(parsers.parse('estou autenticado como usuário "{user_id}"'))
def usuario_autenticado(context, user_id):
    context["headers"] = auth_header(sub=user_id)


@given("não existe usuário com esse email")
def email_livre():
    FakeRepo.state["usuario_por_email"] = None


@given("não existe cliente com esse cpf")
def cpf_livre():
    FakeRepo.state["cliente_por_cpf"] = None


@given("existe usuário dono do recurso")
def usuario_existe():
    FakeRepo.state["usuario_por_id"] = {"id": 1, "referencia_id": "cli_1"}
    
@given("existe usuário com esse email")
def usuario_existe_email():
    FakeRepo.state["usuario_por_email"] = {"id": 1}

@given("existe cliente com esse cpf")
def cliente_existe_cpf():
    FakeRepo.state["cliente_por_cpf"] = {"id": "cli_1"}



# =========================
# WHEN
# =========================

@when(
    parsers.parse(
        'faço POST para "{endpoint}" com nome "{nome}", email "{email}", cpf "{cpf}", telefone "{telefone}" e senha "{senha}"'
    )
)
def cadastrar_cliente(client, context, endpoint, nome, email, cpf, telefone, senha):
    response = client.post(
        endpoint,
        json={
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "telefone": telefone,
            "senha": senha,
        },
    )
    context["response"] = response


@when(
    parsers.parse(
        'faço PUT para "{endpoint}" alterando nome para "{nome}"'
    )
)
def atualizar_cliente(client, context, endpoint, nome):
    response = client.put(
        endpoint,
        json={"nome": nome},
        headers=context["headers"],
    )
    context["response"] = response


@when(
    parsers.parse(
        'faço DELETE para "{endpoint}"'
    )
)
def deletar_cliente(client, context, endpoint):
    response = client.delete(endpoint, headers=context["headers"])
    context["response"] = response


# =========================
# THEN
# =========================

@then(parsers.parse('status deve ser {status:d}'))
def verificar_status(context, status):
    assert context["response"].status_code == status


@then("cliente deve ser cadastrado")
def verificar_cadastro():
    assert "cadastrou" in FakeRepo.state


@then("cliente deve ser atualizado")
def verificar_update():
    assert "atualizou" in FakeRepo.state


@then("cliente deve ser removido")
def verificar_delete():
    assert "deletou" in FakeRepo.state


@then("deve retornar cliente_id")
def verificar_cliente_id(context):
    assert "cliente_id" in context["response"].json()