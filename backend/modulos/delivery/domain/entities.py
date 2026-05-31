from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

from .enums import DelivererStatus, DeliveryStatus


@dataclass(frozen=True)
class Deliverer:
    id: UUID
    name: str
    phone: str
    region: str
    status: DelivererStatus
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class Delivery:
    id: UUID
    order_id: UUID
    region: str
    status: DeliveryStatus
    restaurant_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    deliverer_id: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    picked_up_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    metadata: Optional[dict] = None


# Compatibility alias for existing code paths.
Order = Delivery
