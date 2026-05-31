from modulos.delivery.application.services.deliverers_service import DelivererService
from modulos.delivery.infrastructure.sqlalchemy_repositories import DelivererRepositorySQL, OrderRepositorySQL
from backend.core.database import init_db


# initialize database and repositories
init_db()

deliverer_repository = DelivererRepositorySQL()
order_repository = OrderRepositorySQL()

deliverer_service = DelivererService(
    deliverer_repo=deliverer_repository,
    order_repo=order_repository,
)


def reset_delivery_state() -> None:
    # For SQLAlchemy-backed repo, simply drop all rows from tables (development helper)
    from backend.core.database import engine
    from modulos.delivery.infrastructure.models import DelivererModel, DeliveryModel, DeliveryAssignmentModel
    conn = engine.connect()
    trans = conn.begin()
    try:
        conn.execute(DeliveryAssignmentModel.__table__.delete())
        conn.execute(DeliveryModel.__table__.delete())
        conn.execute(DelivererModel.__table__.delete())
        trans.commit()
    except Exception:
        trans.rollback()
    finally:
        conn.close()
