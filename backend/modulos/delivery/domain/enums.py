from enum import Enum


class DelivererStatus(str, Enum):
    AVAILABLE = 'AVAILABLE'
    BUSY = 'BUSY'
    OCCUPIED = 'BUSY'
    OFFLINE = 'OFFLINE'


class DeliveryStatus(str, Enum):
    ASSIGNED = 'ASSIGNED'
    PICKED_UP = 'PICKED_UP'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
    WAITING = 'WAITING'
    IN_DELIVERY = 'IN_DELIVERY'


# Compatibility aliases used by existing code paths and tests.
OrderStatus = DeliveryStatus
