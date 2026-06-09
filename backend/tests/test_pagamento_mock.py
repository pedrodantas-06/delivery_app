import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from modulos.pagamento.controle import PagamentoControle
from modulos.pagamento.mock_gateway import MockPaymentGateway


@pytest.fixture
def client():
    return TestClient(app)


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


def test_processar_pagamento_aprova_pedido_pendente(monkeypatch):
    mock_conn, mock_cursor = _mock_pedido_db(
        monkeypatch,
        {"id": 42, "status": "Pendente", "valor_total": 50.0},
    )

    async def run():
        with patch.object(
            MockPaymentGateway,
            "processar",
            new=AsyncMock(
                return_value={"status": "APROVADO", "transaction_id": "mock_test123"}
            ),
        ) as mock_processar:
            resultado = await PagamentoControle.processar_pagamento(42)

        assert resultado == {
            "pedido_id": 42,
            "status": "Pago",
            "transaction_id": "mock_test123",
            "status_code": 200,
        }
        mock_processar.assert_awaited_once_with(50.0)
        assert mock_cursor.execute.call_count == 3
        mock_conn.commit.assert_called_once()

    asyncio.run(run())


def test_mock_gateway_delay():
    async def run():
        start = time.monotonic()
        result = await MockPaymentGateway.processar(50.0)
        elapsed = time.monotonic() - start

        assert result["status"] == "APROVADO"
        assert result["transaction_id"].startswith("mock_")
        assert elapsed >= 0.9

    asyncio.run(run())


def test_pagamento_rejeita_pedido_nao_pendente(monkeypatch):
    _mock_pedido_db(
        monkeypatch,
        {"id": 99, "status": "Pago", "valor_total": 30.0},
    )

    async def run():
        resultado = await PagamentoControle.processar_pagamento(99)
        assert resultado["erro"] == "Pedido não está pendente"
        assert resultado["status_code"] == 400

    asyncio.run(run())
