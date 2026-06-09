from core.conexao_banco import ConexaoBanco
from core.jwt import criar_token
from core.seguranca import verificar_senha


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
