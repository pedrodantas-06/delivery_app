from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from .enums import DelivererStatus, OrderStatus


@dataclass(frozen=True)
class Deliverer:
    id: UUID
    name: str
    phone: str
    region: str
    status: DelivererStatus


@dataclass(frozen=True)
class Order:
    id: UUID
    region: str
    status: OrderStatus
    assigned_deliverer_id: Optional[UUID] = None
