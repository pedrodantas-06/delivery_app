from modulos.delivery.application.services.deliverers_service import DelivererService
from modulos.delivery.infrastructure.repositories import DelivererRepositoryImpl, OrderRepositoryImpl


deliverer_service = DelivererService(
    deliverer_repo=DelivererRepositoryImpl(),
    order_repo=OrderRepositoryImpl(),
)
