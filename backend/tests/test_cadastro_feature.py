import pytest
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then
from main import app

scenarios("../../bdd/backend/features/cliente/cadastro.feature")

client = TestClient(app)


@pytest.fixture
def contexto():
    return {}


def mock_cadastrar_cliente(*args, **kwargs):
    return {
        "erro": "Dados já cadastrados",
        "status_code": 400
    }


@given('existe um cliente com email "joao@email.com"')
def cliente_existente(monkeypatch):
    monkeypatch.setattr(
        "modulos.cliente.controle.ClienteControle.cadastrar_cliente",
        mock_cadastrar_cliente
    )


@when('eu envio uma requisição POST para "/clientes" com email "joao@email.com"')
def enviar_requisicao(contexto):
    response = client.post("/clientes/", json={
        "nome": "Maria",
        "email": "joao@email.com",
        "cpf": "98765432100",
        "telefone": "11888888888",
        "senha": "123456"
    })

    contexto["response"] = response


@then('o sistema deve retornar erro "Dados já cadastrados"')
def verificar_erro(contexto):
    response = contexto["response"]

    print(response.status_code)
    print(response.json())

    assert response.status_code == 400
    assert response.json()["detail"] == "Dados já cadastrados"