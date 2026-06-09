import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from main import app
from modulos.pagamento.controle import PagamentoControle

scenarios("../../bdd/backend/features/pedido/fluxo_completo.feature")

client = TestClient(app)

DEMO_SENHA_HASH = "$2b$12$u8sc6scl1FXhv8gNAaFgVuW4j3GZ1FMAoN.dVs.gY/uuqx.f4O3Ki"

DEMO_USERS = {
    "cliente@yummicious.com": {
        "id": 1,
        "nome": "Cliente Demo",
        "email": "cliente@yummicious.com",
        "senha": DEMO_SENHA_HASH,
        "role": "CLIENTE",
        "referencia_id": "cli_demo_001",
    },
    "burger@burgerhouse.com": {
        "id": 2,
        "nome": "Burger House",
        "email": "burger@burgerhouse.com",
        "senha": DEMO_SENHA_HASH,
        "role": "RESTAURANTE",
        "referencia_id": "1",
    },
    "entregador@yummicious.com": {
        "id": 3,
        "nome": "Entregador Demo",
        "email": "entregador@yummicious.com",
        "senha": DEMO_SENHA_HASH,
        "role": "ENTREGADOR",
        "referencia_id": "del_demo_001",
    },
    "admin@yummicious.com": {
        "id": 4,
        "nome": "Admin Demo",
        "email": "admin@yummicious.com",
        "senha": DEMO_SENHA_HASH,
        "role": "ADMIN",
        "referencia_id": None,
    },
}


@pytest.fixture
def contexto():
    return {}


@pytest.fixture(autouse=True)
def mock_auth_db(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor._email = None

    def execute(_query, params):
        mock_cursor._email = params[0]

    def fetchone():
        return DEMO_USERS.get(mock_cursor._email)

    mock_cursor.execute = execute
    mock_cursor.fetchone = fetchone
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.auth.auth_service.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )


@given(parsers.parse('que o cliente demo "{cliente_id}" está autenticado'))
def cliente_autenticado(contexto, cliente_id):
    contexto["cliente_id"] = cliente_id


@when(parsers.parse('o cliente cria um pedido no restaurante {restaurante_id:d} com item "{item}" por {preco:d} reais'))
def criar_pedido(contexto, restaurante_id, item, preco, monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 2001
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.pedido.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )

    response = client.post(
        "/api/v1/pedidos",
        json={
            "id_restaurante": restaurante_id,
            "cliente_id": contexto["cliente_id"],
            "itens": [{"nome": item, "preco": float(preco), "quantidade": 1}],
            "endereco_entrega": "Campus Central",
        },
    )
    contexto["pedido_id"] = response.json()["id"]
    contexto["criar_response"] = response


@when("o pagamento do pedido é processado")
def processar_pagamento(contexto, monkeypatch):
    pedido_id = contexto["pedido_id"]
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": pedido_id,
        "status": "Pendente",
        "valor_total": 25.0,
    }
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.pagamento.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )

    async def run():
        with patch.object(
            PagamentoControle,
            "processar_pagamento",
            new=AsyncMock(
                return_value={
                    "pedido_id": pedido_id,
                    "status": "Pago",
                    "transaction_id": "mock_bdd",
                    "status_code": 200,
                }
            ),
        ):
            response = client.post(f"/api/v1/pagamento/processar/{pedido_id}")
        contexto["pagamento_response"] = response

    import asyncio

    asyncio.run(run())


@then(parsers.parse('o pedido deve ter status "{status}"'))
def verificar_status_pedido(contexto, status):
    if "pagamento_response" in contexto:
        assert contexto["pagamento_response"].status_code == 200
        assert contexto["pagamento_response"].json()["status"] == status
    elif "decisao_response" in contexto:
        response = contexto["decisao_response"]
        assert response.status_code == 200
        assert status.lower() in response.json()["mensagem"].lower()
    else:
        assert contexto["criar_response"].status_code == 201
        assert contexto["criar_response"].json()["status"] == status


@given(parsers.parse('que existe um pedido {pedido_id:d} com status "{status}" no restaurante {restaurante_id:d}'))
def pedido_existente(contexto, pedido_id, status, restaurante_id, monkeypatch):
    contexto["pedido_id"] = pedido_id
    contexto["restaurante_id"] = restaurante_id

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "id": pedido_id,
        "status": status,
        "id_restaurante": restaurante_id,
        "cliente_id": "cli_demo_001",
        "valor_total": 25.0,
        "detalhes": json.dumps({"itens": []}),
    }
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.restaurante.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )


@when(parsers.parse("o restaurante aceita o pedido {pedido_id:d}"))
def restaurante_aceita(contexto, pedido_id, monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"status": "Aberto"}
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.restaurante.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )

    response = client.post(
        f"/api/v1/pedidos/{pedido_id}/decisao",
        json={
            "id_pedido": pedido_id,
            "id_restaurante": contexto["restaurante_id"],
            "aceitacao": "aceito",
        },
    )
    contexto["decisao_response"] = response


@when(parsers.parse('o usuário faz login com email "{email}" e senha "{senha}"'))
def login_usuario(contexto, email, senha):
    response = client.post("/api/v1/auth/login", json={"email": email, "senha": senha})
    contexto["login_response"] = response


@then(parsers.parse('a autenticação retorna role "{role}"'))
def verificar_role(contexto, role):
    response = contexto["login_response"]
    assert response.status_code == 200
    assert response.json()["user"]["role"] == role
