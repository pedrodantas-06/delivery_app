from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel

from modulos.cliente.cliente_service import ClienteService
from core.deps import get_current_user

router = APIRouter(prefix="/clientes", tags=["Clientes"])

service = ClienteService()


# ==============================
# SCHEMAS
# ==============================

class ClienteCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    telefone: str
    senha: str


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    senha: Optional[str] = None


class ClienteLogin(BaseModel):
    email: str
    senha: str


# ==============================
# DEPENDÊNCIAS DE AUTORIZAÇÃO
# ==============================

def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


# ==============================
# ROTAS
# ==============================

# Cadastro
@router.post("/", status_code=201)
async def cadastrar_cliente(cliente: ClienteCreate):
    resultado = service.cadastrar_cliente(cliente.model_dump())

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    return resultado


# Login
@router.post("/login")
async def login_cliente(dados: ClienteLogin):
    resultado = service.login_cliente(dados.model_dump())

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    return resultado


# Listar TODOS (somente admin)
@router.get("/", status_code=200)
async def listar_clientes(
    nome: Optional[str] = None,
    email: Optional[str] = None,
    cpf: Optional[str] = None,
    user: dict = Depends(require_admin)
):
    filtros = {
        k: v for k, v in {
            "nome": nome,
            "email": email,
            "cpf": cpf
        }.items() if v is not None
    }

    resultado = service.listar_clientes(filtros)

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    return resultado.get("clientes", [])


# Obter próprio usuário
@router.get("/me", status_code=200)
async def obter_meu_cliente(user: dict = Depends(get_current_user)):
    cliente_id = int(user["sub"])

    resultado = service.listar_clientes({"id": cliente_id})

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    clientes = resultado.get("clientes", [])

    if not clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return clientes[0]


# Atualizar cliente (admin OU dono)
@router.put("/{cliente_id}")
async def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    user: dict = Depends(get_current_user)
):
    if user.get("role") != "admin" and str(cliente_id) != user["sub"]:
        raise HTTPException(status_code=403, detail="Acesso negado")

    dados_atualizacao = {
        k: v for k, v in dados.model_dump().items() if v is not None
    }

    resultado = service.atualizar_cliente(cliente_id, dados_atualizacao)

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    return resultado


# Debug / info do token
@router.get("/token-info")
async def token_info(user: dict = Depends(get_current_user)):
    return user

# Deletar cliente (admin OU dono)
@router.delete("/{cliente_id}")
async def deletar_cliente(
    cliente_id: int,
    user: dict = Depends(get_current_user)
):
    if user.get("role") != "admin" and str(cliente_id) != user["sub"]:
        raise HTTPException(status_code=403, detail="Acesso negado")

    resultado = service.deletar_cliente(cliente_id)

    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"]
        )

    return resultado