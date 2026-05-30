from typing import Optional
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select

from modulos.delivery.domain.entities import Deliverer, Delivery
from modulos.delivery.domain.enums import DelivererStatus, DeliveryStatus
from modulos.delivery.domain.ports import DelivererRepository, OrderRepository
from modulos.delivery.infrastructure.models import DelivererModel, DeliveryModel, DeliveryAssignmentModel
from backend.core.database import SessionLocal


class DelivererRepositorySQL(DelivererRepository):
    def save(self, deliverer: Deliverer) -> Deliverer:
        db = SessionLocal()
        try:
            model = db.get(DelivererModel, str(deliverer.id))
            if model is None:
                model = DelivererModel(id=str(deliverer.id))
            model.name = deliverer.name
            model.phone = deliverer.phone
            model.region = deliverer.region
            model.status = deliverer.status.value
            db.add(model)
            db.commit()
            db.refresh(model)
            return Deliverer(id=model.id, name=model.name, phone=model.phone, region=model.region, status=DelivererStatus(model.status))
        finally:
            db.close()

    def get_by_id(self, deliverer_id: UUID) -> Optional[Deliverer]:
        db = SessionLocal()
        try:
            model = db.get(DelivererModel, str(deliverer_id))
            if model is None:
                return None
            return Deliverer(id=model.id, name=model.name, phone=model.phone, region=model.region, status=DelivererStatus(model.status))
        finally:
            db.close()

    def list_deliverers(self, status: Optional[str] = None, region: Optional[str] = None) -> list[Deliverer]:
        db = SessionLocal()
        try:
            q = db.query(DelivererModel)
            if status:
                q = q.filter(DelivererModel.status == status)
            if region:
                q = q.filter(DelivererModel.region == region)
            results = q.order_by(DelivererModel.name).all()
            return [Deliverer(id=r.id, name=r.name, phone=r.phone, region=r.region, status=DelivererStatus(r.status)) for r in results]
        finally:
            db.close()

    def find_available_by_region(self, region: str, exclude_id: Optional[UUID] = None) -> Optional[Deliverer]:
        db = SessionLocal()
        try:
            q = db.query(DelivererModel).filter(DelivererModel.region == region, DelivererModel.status == DelivererStatus.AVAILABLE.value)
            if exclude_id:
                q = q.filter(DelivererModel.id != str(exclude_id))
            model = q.order_by(DelivererModel.name).first()
            if model is None:
                return None
            return Deliverer(id=model.id, name=model.name, phone=model.phone, region=model.region, status=DelivererStatus(model.status))
        finally:
            db.close()

    def reserve_available_by_region(self, region: str, exclude_id: Optional[UUID] = None) -> Optional[Deliverer]:
        db = SessionLocal()
        try:
            query = select(DelivererModel).where(
                DelivererModel.region == region,
                DelivererModel.status == DelivererStatus.AVAILABLE.value,
            ).order_by(DelivererModel.name).with_for_update(skip_locked=True)
            if exclude_id is not None:
                query = query.where(DelivererModel.id != str(exclude_id))
            model = db.execute(query).scalars().first()
            if model is None:
                return None
            model.status = DelivererStatus.BUSY.value
            db.add(model)
            db.commit()
            db.refresh(model)
            return Deliverer(id=model.id, name=model.name, phone=model.phone, region=model.region, status=DelivererStatus(model.status))
        finally:
            db.close()

    def reserve_specific_deliverer(self, deliverer_id: UUID, region: str) -> Optional[Deliverer]:
        db = SessionLocal()
        try:
            query = select(DelivererModel).where(
                DelivererModel.id == str(deliverer_id),
                DelivererModel.region == region,
            ).with_for_update(skip_locked=True)
            model = db.execute(query).scalars().first()
            if model is None or model.status != DelivererStatus.AVAILABLE.value:
                return None
            model.status = DelivererStatus.BUSY.value
            db.add(model)
            db.commit()
            db.refresh(model)
            return Deliverer(id=model.id, name=model.name, phone=model.phone, region=model.region, status=DelivererStatus(model.status))
        finally:
            db.close()


class OrderRepositorySQL(OrderRepository):
    def save(self, order: Delivery) -> Delivery:
        db = SessionLocal()
        try:
            model = db.get(DeliveryModel, str(order.id))
            if model is None:
                model = DeliveryModel(id=str(order.id), order_id=str(order.order_id))
            model.region = order.region
            model.status = order.status.value
            model.deliverer_id = str(order.deliverer_id) if order.deliverer_id else None
            # set timestamps if present
            if getattr(order, 'assigned_at', None):
                model.assigned_at = order.assigned_at
            if getattr(order, 'picked_up_at', None):
                model.picked_up_at = order.picked_up_at
            if getattr(order, 'delivered_at', None):
                model.delivered_at = order.delivered_at

            db.add(model)
            db.commit()
            db.refresh(model)
            return Delivery(
                id=model.id,
                order_id=model.order_id,
                region=model.region,
                status=DeliveryStatus(model.status),
                deliverer_id=model.deliverer_id,
                assigned_at=model.assigned_at,
                picked_up_at=model.picked_up_at,
                delivered_at=model.delivered_at,
                metadata=model.payload,
            )
        finally:
            db.close()

    def get_by_id(self, order_id: UUID) -> Optional[Delivery]:
        db = SessionLocal()
        try:
            model = db.get(DeliveryModel, str(order_id))
            if model is None:
                return None
            return Delivery(
                id=model.id,
                order_id=model.order_id,
                region=model.region,
                status=DeliveryStatus(model.status),
                deliverer_id=model.deliverer_id,
                assigned_at=model.assigned_at,
                picked_up_at=model.picked_up_at,
                delivered_at=model.delivered_at,
                metadata=model.payload,
            )
        finally:
            db.close()

    def record_assignment(self, delivery_id: str, deliverer_id: Optional[str], assigned_by: Optional[str], reason: Optional[str]):
        db = SessionLocal()
        try:
            am = DeliveryAssignmentModel(delivery_id=delivery_id, deliverer_id=deliverer_id, assigned_by=assigned_by, reason=reason)
            db.add(am)
            db.commit()
            db.refresh(am)
            return am
        finally:
            db.close()

    def list_orders(self, region: Optional[str] = None) -> list[Delivery]:
        db = SessionLocal()
        try:
            q = db.query(DeliveryModel)
            if region:
                q = q.filter(DeliveryModel.region == region)
            results = q.order_by(DeliveryModel.assigned_at.desc().nullslast()).all()
            out = []
            for m in results:
                out.append(Delivery(id=m.id, order_id=m.order_id, region=m.region, status=DeliveryStatus(m.status), deliverer_id=m.deliverer_id, assigned_at=m.assigned_at, picked_up_at=m.picked_up_at, delivered_at=m.delivered_at, metadata=m.payload))
            return out
        finally:
            db.close()

    def accept_delivery_atomic(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        db = SessionLocal()
        try:
            with db.begin():
                query = select(DeliveryModel).where(DeliveryModel.id == str(delivery_id)).with_for_update()
                model = db.execute(query).scalars().first()
                if model is None:
                    raise ValueError('Order not found')
                if model.deliverer_id is not None and model.deliverer_id != str(deliverer_id):
                    raise ValueError('Deliverer not assigned to this order')
                if model.status == DeliveryStatus.DELIVERED.value:
                    return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
                if model.status != DeliveryStatus.ASSIGNED.value:
                    raise ValueError('invalid_transition')
                model.status = DeliveryStatus.IN_DELIVERY.value
                if model.deliverer_id is None:
                    model.deliverer_id = str(deliverer_id)
                db.add(model)
            db.refresh(model)
            return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
        finally:
            db.close()

    def pickup_delivery_atomic(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        db = SessionLocal()
        try:
            with db.begin():
                query = select(DeliveryModel).where(DeliveryModel.id == str(delivery_id)).with_for_update()
                model = db.execute(query).scalars().first()
                if model is None:
                    raise ValueError('Order not found')
                if model.deliverer_id != str(deliverer_id):
                    raise ValueError('Deliverer not assigned to this order')
                if model.status == DeliveryStatus.PICKED_UP.value:
                    return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
                if model.status not in (DeliveryStatus.ASSIGNED.value, DeliveryStatus.IN_DELIVERY.value):
                    raise ValueError('invalid_transition')
                model.status = DeliveryStatus.PICKED_UP.value
                model.picked_up_at = datetime.now(timezone.utc)
                db.add(model)
            db.refresh(model)
            return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
        finally:
            db.close()

    def deliver_delivery_atomic(self, delivery_id: UUID, deliverer_id: UUID) -> Delivery:
        db = SessionLocal()
        try:
            with db.begin():
                query = select(DeliveryModel).where(DeliveryModel.id == str(delivery_id)).with_for_update()
                model = db.execute(query).scalars().first()
                if model is None:
                    raise ValueError('Order not found')
                if model.deliverer_id != str(deliverer_id):
                    raise ValueError('Deliverer not assigned to this order')
                if model.status == DeliveryStatus.DELIVERED.value:
                    return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
                if model.status != DeliveryStatus.PICKED_UP.value:
                    raise ValueError('invalid_transition')
                model.status = DeliveryStatus.DELIVERED.value
                model.delivered_at = datetime.now(timezone.utc)
                db.add(model)
            db.refresh(model)
            return Delivery(id=model.id, order_id=model.order_id, region=model.region, status=DeliveryStatus(model.status), deliverer_id=model.deliverer_id, assigned_at=model.assigned_at, picked_up_at=model.picked_up_at, delivered_at=model.delivered_at, metadata=model.payload)
        finally:
            db.close()
