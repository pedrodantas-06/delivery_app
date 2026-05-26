from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from modulos.pagamento.controle import PagamentoControle

router = APIRouter(prefix="", tags=["Pagamento"])

class MetodoPagamentoCreate(BaseModel):
    tipo: str
    numero: str
    nome_titular: str
    validade_mes: int
    validade_ano: int
    cvv: str

class MetodoPagamentoUpdate(BaseModel):
    validade_mes: Optional[int] = None
    validade_ano: Optional[int] = None

@router.post("/api/pagamento/estornar/{pedido_id}")
async def estornar_pedido(pedido_id: int):
    resultado = PagamentoControle.processar_estorno(pedido_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.post("/api/pagamento/metodos", status_code=201)
async def criar_metodo_pagamento(
    cliente_id: str,
    metodo: MetodoPagamentoCreate
):
    resultado = PagamentoControle.criar_metodo(cliente_id, metodo.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.put("/api/pagamento/metodos/{metodo_id}")
async def atualizar_metodo_pagamento(
    metodo_id: int,
    cliente_id: str,
    dados: MetodoPagamentoUpdate
):
    dados_atualizacao = {k: v for k, v in dados.model_dump().items() if v is not None}
    resultado = PagamentoControle.atualizar_metodo(metodo_id, cliente_id, dados_atualizacao)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.delete("/api/pagamento/metodos/{metodo_id}", status_code=204)
async def remover_metodo_pagamento(
    metodo_id: int,
    cliente_id: str
):
    resultado = PagamentoControle.remover_metodo(metodo_id, cliente_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return None