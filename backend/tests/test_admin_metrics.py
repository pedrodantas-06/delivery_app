from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from core.jwt import criar_token
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token():
    return criar_token({"sub": "4", "role": "ADMIN"})


@pytest.fixture
def cliente_token():
    return criar_token({"sub": "1", "role": "CLIENTE"})


def _mock_count_db(monkeypatch, counts: dict[str, int]):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    def execute(query, _params=None):
        mock_cursor._last_query = query

    def fetchone():
        for table, total in counts.items():
            if f"FROM {table}" in mock_cursor._last_query:
                return {"total": total}
        return {"total": 0}

    mock_cursor.execute = execute
    mock_cursor.fetchone = fetchone
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.admin.rotas.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )
    return mock_conn, mock_cursor


def test_metrics_requires_auth(client):
    response = client.get("/api/v1/admin/metrics")
    assert response.status_code == 403


def test_metrics_forbidden_non_admin(client, cliente_token):
    response = client.get(
        "/api/v1/admin/metrics",
        headers={"Authorization": f"Bearer {cliente_token}"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado"


def test_metrics_success(monkeypatch, client, admin_token):
    _mock_count_db(
        monkeypatch,
        {"clientes": 10, "restaurantes": 3, "pedidos": 25},
    )
    monkeypatch.setattr(
        "modulos.admin.rotas.deliverer_service.list_deliverers",
        lambda: [object(), object()],
    )

    response = client.get(
        "/api/v1/admin/metrics",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "total_clientes": 10,
        "total_restaurantes": 3,
        "total_pedidos": 25,
        "total_entregadores": 2,
    }


def test_listar_pedidos_admin_success(monkeypatch, client, admin_token):
    pedidos = [
        {
            "id": 1,
            "id_restaurante": 1,
            "status": "Pendente",
            "cliente_id": "cli_001",
            "valor_total": 50.0,
            "detalhes": "{}",
        },
    ]
    monkeypatch.setattr(
        "modulos.admin.rotas.PedidoControle.listar_todos",
        lambda: {"pedidos": pedidos, "status_code": 200},
    )

    response = client.get(
        "/api/v1/admin/pedidos",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json() == pedidos
