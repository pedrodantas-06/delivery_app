from typing import Optional
from uuid import UUID

from modulos.delivery.domain.entities import Deliverer, Order
from modulos.delivery.domain.enums import DelivererStatus
from modulos.delivery.domain.ports import DelivererRepository, OrderRepository


class InMemoryDelivererRepository(DelivererRepository):
    def __init__(self):
        self._deliverers: dict[UUID, Deliverer] = {}

    def clear(self) -> None:
        self._deliverers.clear()

    def save(self, deliverer: Deliverer) -> Deliverer:
        self._deliverers[deliverer.id] = deliverer
        return deliverer

    def get_by_id(self, deliverer_id: UUID) -> Optional[Deliverer]:
        return self._deliverers.get(deliverer_id)

    def list_deliverers(self, status: Optional[str] = None, region: Optional[str] = None) -> list[Deliverer]:
        items = list(self._deliverers.values())
        if status:
            items = [deliverer for deliverer in items if deliverer.status.value == status]
        if region:
            items = [deliverer for deliverer in items if deliverer.region == region]
        return sorted(items, key=lambda deliverer: deliverer.name)

    def find_available_by_region(self, region: str, exclude_id: Optional[UUID] = None) -> Optional[Deliverer]:
        candidates = [
            deliverer
            for deliverer in self._deliverers.values()
            if deliverer.region == region and deliverer.status == DelivererStatus.AVAILABLE
        ]
        if exclude_id is not None:
            candidates = [deliverer for deliverer in candidates if deliverer.id != exclude_id]
        return sorted(candidates, key=lambda deliverer: deliverer.name)[0] if candidates else None


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders: dict[UUID, Order] = {}

    def clear(self) -> None:
        self._orders.clear()

    def save(self, order: Order) -> Order:
        self._orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return self._orders.get(order_id)