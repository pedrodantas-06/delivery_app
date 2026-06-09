import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from main import app

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


@pytest.fixture(autouse=True)
def mock_usuarios_db(monkeypatch):
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


@pytest.fixture
def client():
    return TestClient(app)


def test_login_cliente_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "cliente@yummicious.com",
        "senha": "123456",
    })
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["user"]["role"] == "CLIENTE"
    assert body["user"]["email"] == "cliente@yummicious.com"
    assert body["user"]["referencia_id"] == "cli_demo_001"


def test_login_restaurante_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "burger@burgerhouse.com",
        "senha": "123456",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["user"]["role"] == "RESTAURANTE"
    assert body["user"]["referencia_id"] == "1"


def test_login_entregador_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "entregador@yummicious.com",
        "senha": "123456",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["user"]["role"] == "ENTREGADOR"
    assert body["user"]["referencia_id"] == "del_demo_001"


def test_login_admin_demo(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "admin@yummicious.com",
        "senha": "123456",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["user"]["role"] == "ADMIN"
    assert body["user"]["referencia_id"] is None


def test_login_credenciais_invalidas(client):
    r = client.post("/api/v1/auth/login", json={
        "email": "cliente@yummicious.com",
        "senha": "senha_errada",
    })
    assert r.status_code == 401
    assert r.json()["detail"] == "Credenciais inválidas"
