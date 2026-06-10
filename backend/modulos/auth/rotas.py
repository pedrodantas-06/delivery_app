from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from modulos.auth.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    senha: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    nova_senha: str


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


@router.post("/forgot-password")
async def forgot_password(body: ForgotPasswordRequest):
    return AuthService.solicitar_reset(body.email)


@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest):
    resultado = AuthService.redefinir_senha(body.token, body.nova_senha)
    if "erro" in resultado:
        raise HTTPException(
            status_code=resultado["status_code"],
            detail=resultado["erro"],
        )
    return resultado
