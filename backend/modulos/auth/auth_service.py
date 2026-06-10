import hashlib
import logging
import secrets

from core.conexao_banco import ConexaoBanco
from core.config import settings
from core.jwt import criar_token
from core.seguranca import verificar_senha, hash_senha

logger = logging.getLogger(__name__)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class AuthService:
    @staticmethod
    def login(email: str, senha: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM usuarios WHERE email = %s",
                (email.strip().lower(),),
            )
            user = cursor.fetchone()
            if not user or not verificar_senha(senha, user["senha"]):
                return {"erro": "Credenciais inválidas", "status_code": 401}

            token = criar_token({
                "sub": str(user["id"]),
                "role": user["role"],
            })

            return {
                "access_token": token,
                "user": {
                    "id": user["id"],
                    "nome": user["nome"],
                    "email": user["email"],
                    "role": user["role"],
                    "referencia_id": user["referencia_id"],
                },
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def solicitar_reset(email: str):
        """
        Gera um token de recuperação de senha.

        Por segurança a resposta é sempre genérica (não revela se o e-mail existe).
        Em modo dev (DEV_EXPOSE_RESET_TOKEN) o token volta na resposta e é logado,
        já que não há envio real de e-mail.
        """
        mensagem = {
            "mensagem": "Se o e-mail estiver cadastrado, enviaremos instruções de recuperação."
        }

        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM usuarios WHERE email = %s",
                (email.strip().lower(),),
            )
            user = cursor.fetchone()
            if not user:
                return mensagem

            token = secrets.token_urlsafe(32)
            cursor.execute(
                """
                INSERT INTO password_reset_tokens (usuario_id, token_hash, expira_em)
                VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL %s MINUTE))
                """,
                (user["id"], _hash_token(token), settings.RESET_TOKEN_EXP_MIN),
            )
            conn.commit()

            logger.info("Token de recuperação gerado para usuario_id=%s", user["id"])

            if settings.DEV_EXPOSE_RESET_TOKEN:
                resposta = dict(mensagem)
                resposta["token"] = token
                return resposta

            return mensagem
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def redefinir_senha(token: str, nova_senha: str):
        conn = ConexaoBanco.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, usuario_id FROM password_reset_tokens
                WHERE token_hash = %s AND usado = FALSE AND expira_em > NOW()
                ORDER BY id DESC LIMIT 1
                """,
                (_hash_token(token),),
            )
            registro = cursor.fetchone()
            if not registro:
                return {"erro": "Token inválido ou expirado", "status_code": 400}

            cursor.execute(
                "UPDATE usuarios SET senha = %s WHERE id = %s",
                (hash_senha(nova_senha), registro["usuario_id"]),
            )
            cursor.execute(
                "UPDATE password_reset_tokens SET usado = TRUE WHERE id = %s",
                (registro["id"],),
            )
            conn.commit()

            return {"mensagem": "Senha redefinida com sucesso"}
        finally:
            cursor.close()
            conn.close()
