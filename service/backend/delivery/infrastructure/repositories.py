from uuid import UUID
from typing import Optional

from delivery.domain.entities import Deliverer, Order
from delivery.domain.enums import DelivererStatus, OrderStatus
from delivery.domain.ports import DelivererRepository, OrderRepository
from delivery.infrastructure.models import DelivererModel, OrderModel


class DelivererRepositoryImpl(DelivererRepository):
    def save(self, deliverer: Deliverer) -> Deliverer:
        model, _ = DelivererModel.objects.update_or_create(
            id=deliverer.id,
            defaults={
                'name': deliverer.name,
                'phone': deliverer.phone,
                'region': deliverer.region,
                'status': deliverer.status.value,
            },
        )
        return Deliverer(
            id=model.id,
            name=model.name,
            phone=model.phone,
            region=model.region,
            status=DelivererStatus(model.status),
        )

    def get_by_id(self, deliverer_id: UUID) -> Optional[Deliverer]:
        try:
            model = DelivererModel.objects.get(id=deliverer_id)
        except DelivererModel.DoesNotExist:
            return None
        return Deliverer(
            id=model.id,
            name=model.name,
            phone=model.phone,
            region=model.region,
            status=DelivererStatus(model.status),
        )

    def find_available_by_region(self, region: str, exclude_id: Optional[UUID] = None) -> Optional[Deliverer]:
        query = DelivererModel.objects.filter(
            region=region, status=DelivererStatus.AVAILABLE.value)
        if exclude_id:
            query = query.exclude(id=exclude_id)
        model = query.order_by('name').first()
        if model is None:
            return None
        return Deliverer(
            id=model.id,
            name=model.name,
            phone=model.phone,
            region=model.region,
            status=DelivererStatus(model.status),
        )


class OrderRepositoryImpl(OrderRepository):
    def save(self, order: Order) -> Order:
        model, _ = OrderModel.objects.update_or_create(
            id=order.id,
            defaults={
                'region': order.region,
                'status': order.status.value,
                'assigned_deliverer_id': order.assigned_deliverer_id,
            },
        )
        return Order(
            id=model.id,
            region=model.region,
            status=OrderStatus(model.status),
            assigned_deliverer_id=model.assigned_deliverer_id,
        )

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        try:
            model = OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return None
        return Order(
            id=model.id,
            region=model.region,
            status=OrderStatus(model.status),
            assigned_deliverer_id=model.assigned_deliverer_id,
        )
