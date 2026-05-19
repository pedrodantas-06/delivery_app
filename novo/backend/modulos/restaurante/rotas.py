from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional
from pydantic import BaseModel
from modulos.restaurante.controle import RestauranteControle

router = APIRouter(prefix="", tags=["Restaurantes"])

class RestauranteCreate(BaseModel):
    nome: str
    endereco: str
    cnpj: str
    horario: str
    tipo: str

class RestauranteUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cnpj: Optional[str] = None
    horario: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None

class PedidoAcao(BaseModel):
    id_pedido: int
    id_restaurante: int
    aceitacao: str # "aceito" ou "rejeitado"

@router.post("/restaurantes/cadastrar", status_code=201)
async def cadastrar_restaurante(restaurante: RestauranteCreate):
    resultado = RestauranteControle.cadastrar_restaurante(restaurante.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.get("/restaurantes", status_code=200)
async def listar_restaurantes(
    nome: Optional[str] = None, 
    endereco: Optional[str] = None, 
    cnpj: Optional[str] = None, 
    horario: Optional[str] = None, 
    tipo: Optional[str] = None, 
    status: Optional[str] = None
):
    filtros = {}
    if nome: filtros['nome'] = nome
    if endereco: filtros['endereco'] = endereco
    if cnpj: filtros['cnpj'] = cnpj
    if horario: filtros['horario'] = horario
    if tipo: filtros['tipo'] = tipo
    if status: filtros['status'] = status

    print(f"Recebendo requisição GET para listar restaurantes com filtros: {nome}, {tipo}, {status}")
    
    resultado = RestauranteControle.listar_restaurantes(filtros)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["restaurantes"]

@router.put("/restaurantes/atualizar/{restaurante_id}")
async def atualizar_restaurante(restaurante_id: int, dados: RestauranteUpdate):
    # Remove campos nulos para não sobrescrever com None
    dados_atualizacao = {k: v for k, v in dados.model_dump().items() if v is not None}
    resultado = RestauranteControle.atualizar_restaurante(restaurante_id, dados_atualizacao)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para gerenciar pedidos (Notificação)
@router.post("/pedidos/{acao.id_pedido}/decisao")
async def gerenciar_pedido(acao: PedidoAcao):
    resultado = RestauranteControle.gerenciar_pedido(
        acao.id_pedido, 
        acao.id_restaurante, 
        acao.aceitacao
    )
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# Rota para trigger manual de atualização de status (simulando o automático do BDD)
@router.post("/restaurantes/status")
async def sincronizar_horarios():
    RestauranteControle.verificar_horarios_e_atualizar_status()
    return {"mensagem": "Horários sincronizados com sucesso"}
