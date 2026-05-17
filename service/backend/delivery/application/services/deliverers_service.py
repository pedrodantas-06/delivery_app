from uuid import UUID, uuid4
from typing import Optional

from delivery.domain.entities import Deliverer, Order
from delivery.domain.enums import DelivererStatus, OrderStatus
from delivery.domain.ports import DelivererRepository, OrderRepository


class DelivererService:
    def __init__(self, deliverer_repo: DelivererRepository, order_repo: OrderRepository):
        self.deliverer_repo = deliverer_repo
        self.order_repo = order_repo

    def register_deliverer(self, name: str, phone: str, region: str) -> Deliverer:
        deliverer = Deliverer(
            id=uuid4(),
            name=name,
            phone=phone,
            region=region,
            status=DelivererStatus.AVAILABLE,
        )
        return self.deliverer_repo.save(deliverer)

    def update_status(self, deliverer_id: UUID, status: DelivererStatus) -> Deliverer:
        deliverer = self.deliverer_repo.get_by_id(deliverer_id)
        if deliverer is None:
            raise ValueError('Deliverer not found')
        updated = Deliverer(
            id=deliverer.id,
            name=deliverer.name,
            phone=deliverer.phone,
            region=deliverer.region,
            status=status,
        )
        return self.deliverer_repo.save(updated)

    def list_deliverers(
        self,
        status: Optional[DelivererStatus] = None,
        region: Optional[str] = None,
    ) -> list[Deliverer]:
        return self.deliverer_repo.list_deliverers(
            status=status.value if status else None,
            region=region,
        )

    def assign_deliverer(self, order_id: UUID, region: str, deliverer_id: Optional[UUID] = None) -> Order:
        order = self.order_repo.get_by_id(order_id)
        if order is None:
            order = Order(id=order_id, region=region,
                          status=OrderStatus.PENDING)

        if order.assigned_deliverer_id is not None:
            return order

        if deliverer_id is not None:
            deliverer = self.deliverer_repo.get_by_id(deliverer_id)
            if deliverer is None:
                raise ValueError('Deliverer not found')
            if deliverer.region != region:
                raise ValueError(
                    'Deliverer region does not match order region')
            if deliverer.status != DelivererStatus.AVAILABLE:
                raise ValueError('Deliverer is not available')
        else:
            deliverer = self.deliverer_repo.find_available_by_region(region)

        if deliverer is None:
            raise ValueError('No available deliverer in region')

        occupied = Deliverer(
            id=deliverer.id,
            name=deliverer.name,
            phone=deliverer.phone,
            region=deliverer.region,
            status=DelivererStatus.OCCUPIED,
        )
        self.deliverer_repo.save(occupied)

        assigned = Order(
            id=order.id,
            region=order.region,
            status=OrderStatus.IN_DELIVERY,
            assigned_deliverer_id=deliverer.id,
        )
        return self.order_repo.save(assigned)

    def reassign_deliverer(self, order_id: UUID, reason: str = 'timeout') -> Order:
        if reason not in ('timeout', 'refused'):
            raise ValueError('Invalid reassign reason')

        order = self.order_repo.get_by_id(order_id)
        if order is None:
            raise ValueError('Order not found')

        current_deliverer_id = order.assigned_deliverer_id
        if current_deliverer_id:
            current_deliverer = self.deliverer_repo.get_by_id(
                current_deliverer_id)
            if current_deliverer:
                released = Deliverer(
                    id=current_deliverer.id,
                    name=current_deliverer.name,
                    phone=current_deliverer.phone,
                    region=current_deliverer.region,
                    status=DelivererStatus.AVAILABLE,
                )
                self.deliverer_repo.save(released)

        deliverer = self.deliverer_repo.find_available_by_region(
            order.region, exclude_id=current_deliverer_id)
        if deliverer is None:
            waiting = Order(
                id=order.id,
                region=order.region,
                status=OrderStatus.WAITING,
                assigned_deliverer_id=None,
            )
            return self.order_repo.save(waiting)

        occupied = Deliverer(
            id=deliverer.id,
            name=deliverer.name,
            phone=deliverer.phone,
            region=deliverer.region,
            status=DelivererStatus.OCCUPIED,
        )
        self.deliverer_repo.save(occupied)

        reassigned = Order(
            id=order.id,
            region=order.region,
            status=OrderStatus.IN_DELIVERY,
            assigned_deliverer_id=deliverer.id,
        )
        return self.order_repo.save(reassigned)
