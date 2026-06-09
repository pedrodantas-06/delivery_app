import asyncio
import uuid


class MockPaymentGateway:
    @staticmethod
    async def processar(valor: float) -> dict:
        await asyncio.sleep(1)
        return {
            "status": "APROVADO",
            "transaction_id": f"mock_{uuid.uuid4().hex[:8]}",
        }
