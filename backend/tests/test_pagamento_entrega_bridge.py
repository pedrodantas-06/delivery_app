import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import NAMESPACE_URL, uuid5

from fastapi.testclient import TestClient

from main import app
from modulos.delivery.wires import reset_delivery_state
from modulos.pagamento.controle import PagamentoControle
from modulos.pagamento.mock_gateway import MockPaymentGateway

pedido_pendente_id = 123


def _mock_pedido_db(monkeypatch, pedido):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = pedido
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr(
        "modulos.pagamento.controle.ConexaoBanco.get_connection",
        lambda: mock_conn,
    )
    return mock_conn, mock_cursor


def test_pagamento_bridge_assigns_delivery(monkeypatch):
    reset_delivery_state()
    client = TestClient(app)

    created = client.post(
        "/api/v1/deliverers/",
        json={"name": "Demo", "phone": "11999990001", "region": "Zona Sul"},
    )
    assert created.status_code == 201

    _mock_pedido_db(
        monkeypatch,
        {"id": pedido_pendente_id, "status": "Pendente", "valor_total": 50.0},
    )

    async def run():
        with patch.object(
            MockPaymentGateway,
            "processar",
            new=AsyncMock(
                return_value={"status": "APROVADO", "transaction_id": "mock_bridge"}
            ),
        ):
            resultado = await PagamentoControle.processar_pagamento(pedido_pendente_id)

        assert resultado["status"] == "Pago"
        assert resultado["pedido_id"] == pedido_pendente_id

    asyncio.run(run())

    listed = client.get("/api/v1/orders/", params={"region": "Zona Sul"})
    assert listed.status_code == 200

    items = listed.json()["items"]
    assert len(items) >= 1

    order_uuid = str(uuid5(NAMESPACE_URL, str(pedido_pendente_id)))
    match = next((item for item in items if item["order_id"] == order_uuid), None)
    assert match is not None
    assert match["region"] == "Zona Sul"
    assert match["assigned_deliverer_id"] == created.json()["id"]
