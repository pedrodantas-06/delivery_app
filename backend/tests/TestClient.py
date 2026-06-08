from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_cadastrar_cliente():
    response = client.post("/api/v1/clientes", json={
    "nome": "Romulo Teste",
    "email": "[romulo_teste@email.com](mailto:romulo_teste@email.com)",
    "cpf": "12345678900",
    "telefone": "81999999999",
    "senha": "123456"
    })


    assert response.status_code in [200, 201]
