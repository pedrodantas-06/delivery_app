from fastapi import APIRouter, Depends, HTTPException

from core.conexao_banco import ConexaoBanco
from core.deps import get_current_user
from modulos.delivery.wires import deliverer_service
from modulos.pedido.controle import PedidoControle

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


def _count_table(cursor, table: str) -> int:
    cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")
    row = cursor.fetchone()
    return int(row["total"]) if row else 0


@router.get("/metrics")
async def metrics(user: dict = Depends(require_admin)):
    conn = ConexaoBanco.get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        total_clientes = _count_table(cursor, "clientes")
        total_restaurantes = _count_table(cursor, "restaurantes")
        total_pedidos = _count_table(cursor, "pedidos")
    finally:
        cursor.close()
        conn.close()

    total_entregadores = len(deliverer_service.list_deliverers())

    return {
        "total_clientes": total_clientes,
        "total_restaurantes": total_restaurantes,
        "total_pedidos": total_pedidos,
        "total_entregadores": total_entregadores,
    }


@router.get("/pedidos")
async def listar_pedidos_admin(user: dict = Depends(require_admin)):
    resultado = PedidoControle.listar_todos()
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["pedidos"]
