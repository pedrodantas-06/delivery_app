from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional
from pydantic import BaseModel
from modulos.cardapio.controle import CardapioControle

router = APIRouter(prefix="", tags=["Cardápio"])

class ItemCardapioCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria: str
    id_restaurante: int
    disponivel: Optional[bool] = True

class ItemCardapioUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    categoria: Optional[str] = None
    disponivel: Optional[bool] = None

# Rota para cadastrar item no cardápio
@router.post("/cardapio/cadastrar", status_code=201)
async def cadastrar_item(item: ItemCardapioCreate):
    resultado = CardapioControle.cadastrar_item(item.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para listar cardápio com filtros
@router.get("/cardapio", status_code=200)
async def listar_cardapio(
    id_restaurante: Optional[int] = None,
    categoria: Optional[str] = None,
    disponivel: Optional[bool] = None,
    nome: Optional[str] = None
):
    filtros = {}
    if id_restaurante: filtros['id_restaurante'] = id_restaurante
    if categoria: filtros['categoria'] = categoria
    if disponivel is not None: filtros['disponivel'] = disponivel
    if nome: filtros['nome'] = nome

    print(f"Recebendo requisição GET para listar cardápio com filtros: {filtros}")
    
    resultado = CardapioControle.listar_cardapio(filtros)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para obter item específico do cardápio
@router.get("/cardapio/{item_id}", status_code=200)
async def obter_item(item_id: int):
    resultado = CardapioControle.obter_item(item_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["item"]

# Rota para obter cardápio completo de um restaurante
@router.get("/restaurantes/{restaurante_id}/cardapio", status_code=200)
async def obter_cardapio_restaurante(restaurante_id: int):
    resultado = CardapioControle.obter_cardapio_por_restaurante(restaurante_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para atualizar item do cardápio
@router.put("/cardapio/{item_id}", status_code=200)
async def atualizar_item(item_id: int, dados: ItemCardapioUpdate):
    # Remove campos nulos para não sobrescrever com None
    dados_atualizacao = {k: v for k, v in dados.model_dump().items() if v is not None}
    resultado = CardapioControle.atualizar_item(item_id, dados_atualizacao)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para deletar item do cardápio
@router.delete("/cardapio/{item_id}", status_code=200)
async def deletar_item(item_id: int):
    resultado = CardapioControle.deletar_item(item_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado
