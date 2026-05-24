from modulos.delivery.application.services.deliverers_service import DelivererService
from modulos.delivery.infrastructure.memory_repositories import (
    InMemoryDelivererRepository,
    InMemoryOrderRepository,
)


deliverer_repository = InMemoryDelivererRepository()
order_repository = InMemoryOrderRepository()

deliverer_service = DelivererService(
    deliverer_repo=deliverer_repository,
    order_repo=order_repository,
)


def reset_delivery_state() -> None:
    deliverer_repository.clear()
    order_repository.clear()
