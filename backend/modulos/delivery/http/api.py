from uuid import UUID

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
    order_id: UUID
    region: str
    deliverer_id: UUID | None = None


class ReassignOrderRequest(BaseModel):
    reason: str = 'timeout'


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
        order = deliverer_service.assign_deliverer(payload.order_id, payload.region, payload.deliverer_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'assigned_deliverer_id': str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None,
    }


@router.post('/orders/{order_id}/reassign/')
def reassign_order(order_id: UUID, payload: ReassignOrderRequest):
    try:
        order = deliverer_service.reassign_deliverer(order_id, reason=payload.reason)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        'order_id': str(order.id),
        'status': order.status.value,
        'assigned_deliverer_id': str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None,
    }