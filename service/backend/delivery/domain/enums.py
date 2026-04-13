from enum import Enum


class DelivererStatus(str, Enum):
    AVAILABLE = 'AVAILABLE'
    OCCUPIED = 'OCCUPIED'
    OFFLINE = 'OFFLINE'


class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    IN_DELIVERY = 'IN_DELIVERY'
    WAITING = 'WAITING'
