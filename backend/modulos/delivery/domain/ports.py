from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from .entities import Deliverer, Delivery


class DelivererRepository(ABC):
    @abstractmethod
    def save(self, deliverer: Deliverer) -> Deliverer:
        pass

    @abstractmethod
    def get_by_id(self, deliverer_id: UUID) -> Optional[Deliverer]:
        pass

    @abstractmethod
    def list_deliverers(self, status: Optional[str] = None, region: Optional[str] = None) -> list[Deliverer]:
        pass

    @abstractmethod
    def find_available_by_region(self, region: str, exclude_id: Optional[UUID] = None) -> Optional[Deliverer]:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Delivery) -> Delivery:
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Delivery]:
        pass
    
    # optional: record assignment/audit
    def record_assignment(self, delivery_id: str, deliverer_id: Optional[str], assigned_by: Optional[str], reason: Optional[str]):
        raise NotImplementedError()
    
    def list_orders(self, region: Optional[str] = None) -> list[Delivery]:
        raise NotImplementedError()
