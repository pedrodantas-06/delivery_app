import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configurações do Banco de Dados
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "delivery_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "delivery_pass")
    DB_NAME: str = os.getenv("DB_NAME", "yummicious_db")

    # Configurações Gerais
    BACKEND_NAME: str = os.getenv("BACKEND_NAME", "yummicious_back")
    FRONTEND_NAME: str = os.getenv("FRONTEND_NAME", "yummicious_front")
    TZ: str = os.getenv("TZ", "America/Sao_Paulo")

    # Configurações de Segurança
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-it-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Recuperação de senha
    RESET_TOKEN_EXP_MIN: int = int(os.getenv("RESET_TOKEN_EXP_MIN", 30))
    # Em desenvolvimento devolvemos o token na resposta (sem envio real de e-mail).
    DEV_EXPOSE_RESET_TOKEN: bool = os.getenv("DEV_EXPOSE_RESET_TOKEN", "true").lower() == "true"

    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Yummicious"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
