from uuid import uuid4

from fastapi.testclient import TestClient

from main import app
from modulos.delivery.wires import reset_delivery_state


def test_list_orders_returns_assigned_deliverer_id():
    reset_delivery_state()
    client = TestClient(app)

    created = client.post(
        '/api/v1/deliverers/',
        json={'name': 'Ana', 'phone': '11999999999', 'region': 'Zona Sul'},
    )
    assert created.status_code == 201
    deliverer_id = created.json()['id']

    order_id = str(uuid4())
    assigned = client.post(
        '/api/v1/orders/assign/',
        json={'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': deliverer_id},
    )
    assert assigned.status_code == 200

    listed = client.get('/api/v1/orders/')
    assert listed.status_code == 200

    items = listed.json()['items']
    assert len(items) >= 1
    match = next(item for item in items if item['order_id'] == order_id)
    assert match['assigned_deliverer_id'] == deliverer_id
