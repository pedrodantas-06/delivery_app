from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from modulos.delivery.http.api import router as deliverers_router
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from modulos.cardapio.rotas import router as cardapio_router
from modulos.cliente.rotas import router as cliente_router
from modulos.auth.rotas import router as auth_router
from modulos.pagamento.rotas import router as pagamento_router


try:
    from modulos.restaurante.rotas import router as restaurante_router
    from modulos.restaurante.controle import RestauranteControle
except ModuleNotFoundError:
    restaurante_router = None
    RestauranteControle = None

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuração de CORS para segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especificar as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agendador global
scheduler = BackgroundScheduler()

# Inclusão das rotas modulares
app.include_router(deliverers_router, prefix=settings.API_V1_STR)
app.include_router(cardapio_router, prefix=settings.API_V1_STR)
app.include_router(cliente_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(pagamento_router, prefix=settings.API_V1_STR)
if restaurante_router is not None:
    app.include_router(restaurante_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API do Yummicious",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando a aplicação...")
    if RestauranteControle is not None:
        scheduler.add_job(RestauranteControle.verificar_horarios_e_atualizar_status, 'interval', seconds=60)
        scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Encerrando a aplicação...")
    scheduler.shutdown()
