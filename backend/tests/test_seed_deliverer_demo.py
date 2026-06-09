from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modulos.delivery.domain.enums import DelivererStatus
from modulos.delivery.infrastructure.models import DelivererModel
from scripts.seed_deliverer_demo import DEMO_DELIVERER_ID, DEMO_REGION, seed_demo_deliverer


def test_seed_demo_deliverer_creates_fixed_id(tmp_path):
    db_path = tmp_path / "seed_test.db"
    database_url = f"sqlite:///{db_path}"

    deliverer_id = seed_demo_deliverer(database_url=database_url)
    assert deliverer_id == DEMO_DELIVERER_ID

    deliverer_id_again = seed_demo_deliverer(database_url=database_url)
    assert deliverer_id_again == DEMO_DELIVERER_ID

    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine)
    with Session() as db:
        row = db.get(DelivererModel, DEMO_DELIVERER_ID)
        assert row is not None
        assert row.name == "Entregador Demo"
        assert row.region == DEMO_REGION
        assert row.status == DelivererStatus.AVAILABLE.value
        assert db.query(DelivererModel).count() == 1
