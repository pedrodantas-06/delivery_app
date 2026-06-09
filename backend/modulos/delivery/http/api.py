from uuid import UUID, uuid5, NAMESPACE_URL

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from modulos.delivery.domain.enums import DelivererStatus
from modulos.delivery.wires import deliverer_service


router = APIRouter()


class DelivererCreate(BaseModel):
    name: str
    phone: str
    region: str


class DelivererStatusUpdate(BaseModel):
    status: DelivererStatus = Field(...)


class AssignOrderRequest(BaseModel):
    order_id: str
    region: str
    deliverer_id: str | None = None


class ReassignOrderRequest(BaseModel):
    reason: str = 'timeout'


class AcceptRequest(BaseModel):
    deliverer_id: str


class DeliverActionRequest(BaseModel):
    deliverer_id: str


def normalize_uuid(value: str) -> UUID:
    try:
        return UUID(str(value))
    except ValueError:
        return uuid5(NAMESPACE_URL, value)


@router.get('/deliverers/')
def list_deliverers(status: DelivererStatus | None = None, region: str | None = None):
    deliverers = deliverer_service.list_deliverers(status=status, region=region)
    return {
        'items': [
            {
                'id': str(deliverer.id),
                'name': deliverer.name,
                'phone': deliverer.phone,
                'region': deliverer.region,
                'status': deliverer.status.value,
            }
            for deliverer in deliverers
        ]
    }


@router.post('/deliverers/', status_code=201)
def register_deliverer(payload: DelivererCreate):
    deliverer = deliverer_service.register_deliverer(payload.name, payload.phone, payload.region)
    return {
        'id': str(deliverer.id),
        'name': deliverer.name,
        'phone': deliverer.phone,
        'region': deliverer.region,
        'status': deliverer.status.value,
    }


@router.patch('/deliverers/{deliverer_id}/status/')
def update_deliverer_status(deliverer_id: UUID, payload: DelivererStatusUpdate):
    try:
        deliverer = deliverer_service.update_status(deliverer_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {'id': str(deliverer.id), 'status': deliverer.status.value}


@router.post('/orders/assign/')
def assign_order(payload: AssignOrderRequest):
    try:
        order = deliverer_service.assign_deliverer(
            normalize_uuid(payload.order_id),
            payload.region,
            normalize_uuid(payload.deliverer_id) if payload.deliverer_id else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
        'assigned_deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
    }


@router.get('/orders/')
def list_orders(region: str | None = None):
    orders = deliverer_service.order_repo.list_orders(region=region) if hasattr(deliverer_service.order_repo, 'list_orders') else []
    return {
        'items': [
            {
                'order_id': str(o.id),
                'region': o.region,
                'status': o.status.value,
                'assigned_deliverer_id': str(o.deliverer_id) if o.deliverer_id else None,
            }
            for o in orders
        ]
    }


@router.post('/orders/{order_id}/reassign/')
def reassign_order(order_id: str, payload: ReassignOrderRequest):
    try:
        order = deliverer_service.reassign_deliverer(normalize_uuid(order_id), reason=payload.reason)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
        'assigned_deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
    }


@router.post('/orders/{order_id}/accept/')
def accept_order(order_id: str, payload: AcceptRequest):
    try:
        order = deliverer_service.accept_delivery(normalize_uuid(order_id), normalize_uuid(payload.deliverer_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
        'assigned_deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
    }


@router.patch('/orders/{order_id}/pickup/')
def pickup_order(order_id: str, payload: DeliverActionRequest):
    try:
        order = deliverer_service.pickup_delivery(normalize_uuid(order_id), normalize_uuid(payload.deliverer_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'picked_up_at': getattr(order, 'picked_up_at', None),
        'deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
    }


@router.patch('/orders/{order_id}/deliver/')
def deliver_order(order_id: str, payload: DeliverActionRequest):
    try:
        order = deliverer_service.deliver_delivery(normalize_uuid(order_id), normalize_uuid(payload.deliverer_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'delivered_at': getattr(order, 'delivered_at', None),
        'deliverer_id': str(order.deliverer_id) if order.deliverer_id else None,
    }