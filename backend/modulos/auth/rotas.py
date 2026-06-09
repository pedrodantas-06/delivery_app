from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from modulos.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
async def login(body: LoginRequest):
    resultado = AuthService.login(body.email, body.senha)
    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"],
        )
    return {
        "access_token": resultado["access_token"],
        "user": resultado["user"],
    }
