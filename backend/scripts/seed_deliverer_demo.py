"""Seed demo deliverer in SQLite for E2E presentation."""
import os

DEMO_DELIVERER_ID = "del_demo_001"
DEMO_NAME = "Entregador Demo"
DEMO_PHONE = "11999990001"
DEMO_REGION = "Zona Sul"


def seed_demo_deliverer(database_url: str | None = None) -> str:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from modulos.delivery.domain.enums import DelivererStatus
    from modulos.delivery.infrastructure.models import Base as DeliveryBase
    from modulos.delivery.infrastructure.models import DelivererModel

    url = database_url or os.getenv("DATABASE_URL") or "sqlite:///./dev.db"
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=connect_args)
    DeliveryBase.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    with Session() as db:
        existing = db.get(DelivererModel, DEMO_DELIVERER_ID)
        if existing is not None:
            return existing.id

        model = DelivererModel(
            id=DEMO_DELIVERER_ID,
            name=DEMO_NAME,
            phone=DEMO_PHONE,
            region=DEMO_REGION,
            status=DelivererStatus.AVAILABLE.value,
        )
        db.add(model)
        db.commit()
        return model.id


if __name__ == "__main__":
    deliverer_id = seed_demo_deliverer()
    print(f"Demo deliverer ready: {deliverer_id}")
