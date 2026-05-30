from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


def gen_uuid():
    return str(uuid.uuid4())


class DelivererModel(Base):
    __tablename__ = 'deliverers'
    id = Column(String(36), primary_key=True, default=gen_uuid)
    name = Column(String(120), nullable=False)
    phone = Column(String(30), nullable=False)
    region = Column(String(80), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DeliveryModel(Base):
    __tablename__ = 'deliveries'
    id = Column(String(36), primary_key=True, default=gen_uuid)
    order_id = Column(String(36), unique=True, nullable=False)
    region = Column(String(80), nullable=False)
    restaurant_id = Column(String(36), nullable=True)
    customer_id = Column(String(36), nullable=True)
    deliverer_id = Column(String(36), nullable=True)
    status = Column(String(20), nullable=False)
    assigned_at = Column(DateTime, nullable=True)
    picked_up_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    payload = Column('metadata', JSON, nullable=True)


class DeliveryAssignmentModel(Base):
    __tablename__ = 'delivery_assignments'
    id = Column(String(36), primary_key=True, default=gen_uuid)
    delivery_id = Column(String(36), nullable=False)
    deliverer_id = Column(String(36), nullable=True)
    assigned_by = Column(String(120), nullable=True)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
