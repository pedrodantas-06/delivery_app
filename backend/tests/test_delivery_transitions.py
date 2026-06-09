from uuid import uuid4

from fastapi.testclient import TestClient

from main import app
from modulos.delivery.wires import reset_delivery_state


def test_pickup_and_deliver_flow():
    reset_delivery_state()
    client = TestClient(app)

    created = client.post('/api/v1/deliverers/', json={'name': 'Carlos', 'phone': '11977777777', 'region': 'Zona Sul'})
    assert created.status_code == 201
    deliverer_id = created.json()['id']

    order_id = str(uuid4())
    assigned = client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': 'Zona Sul'})
    assert assigned.status_code == 200
    assert assigned.json()['assigned_deliverer_id'] == deliverer_id

    # accept
    accepted = client.post(f'/api/v1/orders/{order_id}/accept/', json={'deliverer_id': deliverer_id})
    assert accepted.status_code == 200
    assert accepted.json()['status'] == 'IN_DELIVERY'

    # pickup
    pickup = client.patch(f'/api/v1/orders/{order_id}/pickup/', json={'deliverer_id': deliverer_id})
    assert pickup.status_code == 200
    assert pickup.json()['status'] == 'PICKED_UP'

    # deliver
    deliver = client.patch(f'/api/v1/orders/{order_id}/deliver/', json={'deliverer_id': deliverer_id})
    assert deliver.status_code == 200
    assert deliver.json()['status'] == 'DELIVERED'
