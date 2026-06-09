from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from modulos.pedido.controle import PedidoControle

router = APIRouter(prefix="", tags=["Pedidos"])


class ItemPedido(BaseModel):
    nome: str
    preco: float
    quantidade: int


class PedidoCreate(BaseModel):
    id_restaurante: int
    cliente_id: str
    itens: list[ItemPedido]
    endereco_entrega: str


@router.post("/pedidos", status_code=201)
async def criar_pedido(pedido: PedidoCreate):
    resultado = PedidoControle.criar(pedido.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return {
        "id": resultado["id"],
        "status": resultado["status"],
        "valor_total": resultado["valor_total"],
        "mensagem": resultado["mensagem"],
    }


@router.get("/pedidos", status_code=200)
async def listar_pedidos(
    cliente_id: Optional[str] = None,
    restaurante_id: Optional[int] = None,
):
    if cliente_id:
        resultado = PedidoControle.listar_por_cliente(cliente_id)
    elif restaurante_id is not None:
        resultado = PedidoControle.listar_por_restaurante(restaurante_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Informe cliente_id ou restaurante_id",
        )

    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["pedidos"]


@router.get("/pedidos/{pedido_id}", status_code=200)
async def obter_pedido(pedido_id: int):
    resultado = PedidoControle.obter(pedido_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["pedido"]
