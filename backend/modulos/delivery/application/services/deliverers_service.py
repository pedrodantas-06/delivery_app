from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from modulos.delivery.domain.entities import Deliverer, Delivery
from modulos.delivery.domain.enums import DelivererStatus, DeliveryStatus
from modulos.delivery.domain.ports import DelivererRepository, OrderRepository


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

    def assign_deliverer(self, order_id: UUID, region: str, deliverer_id: Optional[UUID] = None) -> Delivery:
        delivery = self.order_repo.get_by_id(order_id)
        if delivery is None:
            delivery = Delivery(
                id=order_id,
                order_id=order_id,
                region=region,
                status=DeliveryStatus.WAITING,
            )

        if delivery.deliverer_id is not None and delivery.status not in (DeliveryStatus.WAITING, DeliveryStatus.CANCELLED):
            return delivery

        if deliverer_id is not None and hasattr(self.deliverer_repo, 'reserve_specific_deliverer'):
            deliverer = self.deliverer_repo.reserve_specific_deliverer(deliverer_id, region)
            if deliverer is None:
                raise ValueError('Deliverer is not available')
        elif deliverer_id is not None:
            deliverer = self.deliverer_repo.get_by_id(deliverer_id)
            if deliverer is None:
                raise ValueError('Deliverer not found')
            if deliverer.region != region:
                raise ValueError('Deliverer region does not match order region')
            if deliverer.status != DelivererStatus.AVAILABLE:
                raise ValueError('Deliverer is not available')
        elif hasattr(self.deliverer_repo, 'reserve_available_by_region'):
            deliverer = self.deliverer_repo.reserve_available_by_region(region)
        else:
            deliverer = self.deliverer_repo.find_available_by_region(region)

        if deliverer is None:
            raise ValueError('No available deliverer in region')

        if not hasattr(self.deliverer_repo, 'reserve_available_by_region') and not hasattr(self.deliverer_repo, 'reserve_specific_deliverer'):
            occupied = Deliverer(
                id=deliverer.id,
                name=deliverer.name,
                phone=deliverer.phone,
                region=deliverer.region,
                status=DelivererStatus.BUSY,
            )
            self.deliverer_repo.save(occupied)

        assigned = Delivery(
            id=delivery.id,
            order_id=delivery.order_id,
            region=delivery.region,
            status=DeliveryStatus.ASSIGNED,
            deliverer_id=deliverer.id,
            assigned_at=datetime.now(timezone.utc),
        )
        saved = self.order_repo.save(assigned)
        if hasattr(self.order_repo, 'record_assignment'):
            try:
                self.order_repo.record_assignment(str(saved.id), str(deliverer.id), 'system', 'assign')
            except Exception:
                pass
        return saved

    def reassign_deliverer(self, order_id: UUID, reason: str = 'timeout') -> Delivery:
        if reason not in ('timeout', 'refused'):
            raise ValueError('Invalid reassign reason')

        delivery = self.order_repo.get_by_id(order_id)
        if delivery is None:
            raise ValueError('Order not found')

        current_deliverer_id = delivery.deliverer_id
        if current_deliverer_id:
            current_deliverer = self.deliverer_repo.get_by_id(current_deliverer_id)
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
            delivery.region, exclude_id=current_deliverer_id)
        if deliverer is None:
            waiting = Delivery(
                id=delivery.id,
                order_id=delivery.order_id,
                region=delivery.region,
                status=DeliveryStatus.WAITING,
                deliverer_id=None,
            )
            return self.order_repo.save(waiting)

        if not hasattr(self.deliverer_repo, 'reserve_available_by_region'):
            occupied = Deliverer(
                id=deliverer.id,
                name=deliverer.name,
                phone=deliverer.phone,
                region=deliverer.region,
                status=DelivererStatus.BUSY,
            )
            self.deliverer_repo.save(occupied)

        reassigned = Delivery(
            id=delivery.id,
            order_id=delivery.order_id,
            region=delivery.region,
            status=DeliveryStatus.ASSIGNED,
            deliverer_id=deliverer.id,
            assigned_at=datetime.now(timezone.utc),
        )
        saved = self.order_repo.save(reassigned)
        if hasattr(self.order_repo, 'record_assignment'):
            try:
                self.order_repo.record_assignment(str(saved.id), str(deliverer.id), 'system', reason)
            except Exception:
                pass
        return saved

    def accept_delivery(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        if hasattr(self.order_repo, 'accept_delivery_atomic'):
            return self.order_repo.accept_delivery_atomic(delivery_id, deliverer_id)

        delivery = self.order_repo.get_by_id(delivery_id)
        if delivery is None:
            raise ValueError('Order not found')
        if delivery.deliverer_id is not None and delivery.deliverer_id != deliverer_id:
            raise ValueError('Deliverer not assigned to this order')
        if delivery.status == DeliveryStatus.IN_DELIVERY:
            return delivery
        if delivery.status != DeliveryStatus.ASSIGNED:
            raise ValueError('invalid_transition')

        delivery = Delivery(
            id=delivery.id,
            order_id=delivery.order_id,
            region=delivery.region,
            status=DeliveryStatus.IN_DELIVERY,
            deliverer_id=delivery.deliverer_id,
            assigned_at=delivery.assigned_at,
        )
        return self.order_repo.save(delivery)

    def pickup_delivery(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        if hasattr(self.order_repo, 'pickup_delivery_atomic'):
            return self.order_repo.pickup_delivery_atomic(delivery_id, deliverer_id)

        delivery = self.order_repo.get_by_id(delivery_id)
        if delivery is None:
            raise ValueError('Order not found')
        if delivery.deliverer_id != deliverer_id:
            raise ValueError('Deliverer not assigned to this order')
        if delivery.status == DeliveryStatus.PICKED_UP:
            return delivery
        if delivery.status not in (DeliveryStatus.ASSIGNED, DeliveryStatus.IN_DELIVERY):
            raise ValueError('invalid_transition')

        delivery = Delivery(
            id=delivery.id,
            order_id=delivery.order_id,
            region=delivery.region,
            status=DeliveryStatus.PICKED_UP,
            deliverer_id=delivery.deliverer_id,
            assigned_at=delivery.assigned_at,
            picked_up_at=datetime.now(timezone.utc),
        )
        return self.order_repo.save(delivery)

    def deliver_delivery(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        if hasattr(self.order_repo, 'deliver_delivery_atomic'):
            saved = self.order_repo.deliver_delivery_atomic(delivery_id, deliverer_id)
        else:
            delivery = self.order_repo.get_by_id(delivery_id)
            if delivery is None:
                raise ValueError('Order not found')
            if delivery.deliverer_id != deliverer_id:
                raise ValueError('Deliverer not assigned to this order')
            if delivery.status == DeliveryStatus.DELIVERED:
                return delivery
            if delivery.status != DeliveryStatus.PICKED_UP:
                raise ValueError('invalid_transition')

            delivery = Delivery(
                id=delivery.id,
                order_id=delivery.order_id,
                region=delivery.region,
                status=DeliveryStatus.DELIVERED,
                deliverer_id=delivery.deliverer_id,
                assigned_at=delivery.assigned_at,
                picked_up_at=delivery.picked_up_at,
                delivered_at=datetime.now(timezone.utc),
            )
            saved = self.order_repo.save(delivery)

        if hasattr(self.order_repo, 'record_assignment'):
            try:
                self.order_repo.record_assignment(str(saved.id), str(deliverer_id), 'system', 'delivered')
            except Exception:
                pass
        return saved
