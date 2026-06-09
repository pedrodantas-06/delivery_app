import json
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def _mock_pedido_db(monkeypatch, fetchone=None, fetchall=None, lastrowid=42):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fetchone
    mock_cursor.fetchall.return_value = fetchall or []
    mock_cursor.lastrowid = lastrowid
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.pedido.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )
    return mock_conn, mock_cursor


def test_criar_pedido_com_itens(monkeypatch, client):
    mock_conn, mock_cursor = _mock_pedido_db(monkeypatch, lastrowid=42)

    payload = {
        "id_restaurante": 1,
        "cliente_id": "cli_demo_001",
        "itens": [
            {"nome": "X-Burguer", "preco": 25.0, "quantidade": 2},
            {"nome": "Coca-Cola", "preco": 8.0, "quantidade": 1},
        ],
        "endereco_entrega": "Campus Central, Bloco A",
    }

    response = client.post("/api/v1/pedidos", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "Pendente"
    assert data["valor_total"] == 58.0
    assert data["id"] == 42

    insert_call = mock_cursor.execute.call_args_list[0]
    assert "INSERT INTO pedidos" in insert_call[0][0]
    insert_vals = insert_call[0][1]
    assert insert_vals[0] == 1
    assert insert_vals[1] == "Pendente"
    assert insert_vals[2] == "cli_demo_001"
    assert insert_vals[3] == 58.0

    detalhes = json.loads(insert_vals[4])
    assert detalhes["endereco_entrega"] == "Campus Central, Bloco A"
    assert len(detalhes["itens"]) == 2
    mock_conn.commit.assert_called_once()


def test_listar_por_cliente(monkeypatch, client):
    pedidos = [
        {
            "id": 1,
            "status": "Pendente",
            "cliente_id": "cli_001",
            "valor_total": 50.0,
            "id_restaurante": 1,
        },
        {
            "id": 2,
            "status": "Pago",
            "cliente_id": "cli_001",
            "valor_total": 30.0,
            "id_restaurante": 1,
        },
    ]
    _mock_pedido_db(monkeypatch, fetchall=pedidos)

    response = client.get("/api/v1/pedidos?cliente_id=cli_001")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["cliente_id"] == "cli_001"


def test_listar_por_restaurante(monkeypatch, client):
    pedidos = [
        {
            "id": 1,
            "id_restaurante": 1,
            "status": "Pendente",
            "cliente_id": "cli_001",
            "valor_total": 25.0,
        },
    ]
    _mock_pedido_db(monkeypatch, fetchall=pedidos)

    response = client.get("/api/v1/pedidos?restaurante_id=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id_restaurante"] == 1
