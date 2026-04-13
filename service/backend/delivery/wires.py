from delivery.application.services import DelivererService
from delivery.infrastructure.repositories import DelivererRepositoryImpl, OrderRepositoryImpl


deliverer_service = DelivererService(
    deliverer_repo=DelivererRepositoryImpl(),
    order_repo=OrderRepositoryImpl(),
)
