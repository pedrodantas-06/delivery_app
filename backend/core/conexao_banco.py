from mysql.connector import pooling, Error
from core.config import settings
import logging

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConexaoBanco:
    _connection_pool = None

    @classmethod
    def get_pool(cls):
        if cls._connection_pool is None:
            try:
                logger.info("Iniciando pool de conexões com MySQL...")
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="delivery_pool",
                    pool_size=10,
                    pool_reset_session=True,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    charset="utf8mb4",
                    init_command="SET NAMES utf8mb4"
                )
                logger.info("Pool de conexões criado com sucesso.")
            except Error as err:
                logger.error(f"Erro ao criar pool de conexões: {err}")
                raise
        return cls._connection_pool

    @classmethod
    def get_connection(cls):
        return cls.get_pool().get_connection()

def get_db():
    """Helper para obter uma conexão do pool e garantir que ela seja fechada"""
    connection = ConexaoBanco.get_connection()
    try:
        yield connection
    finally:
        if connection.is_connected():
            connection.close()
