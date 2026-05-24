from uuid import uuid4

from modulos.delivery.application.services.deliverers_service import DelivererService
from modulos.delivery.domain.enums import DelivererStatus
from modulos.delivery.infrastructure.memory_repositories import (
    InMemoryDelivererRepository,
    InMemoryOrderRepository,
)


def test_deliverer_status_available_to_occupied():
    service = DelivererService(InMemoryDelivererRepository(), InMemoryOrderRepository())

    deliverer = service.register_deliverer('Ana', '11999999999', 'Zona Sul')
    updated = service.update_status(deliverer.id, DelivererStatus.OCCUPIED)

    assert updated.status == DelivererStatus.OCCUPIED


def test_assigns_deliverer_automatically_in_same_region():
    service = DelivererService(InMemoryDelivererRepository(), InMemoryOrderRepository())
    deliverer = service.register_deliverer('Ana', '11999999999', 'Zona Sul')

    order = service.assign_deliverer(uuid4(), 'Zona Sul')

    assert order.status.value == 'IN_DELIVERY'
    assert order.assigned_deliverer_id == deliverer.id