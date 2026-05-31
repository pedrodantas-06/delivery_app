from uuid import uuid4

from fastapi.testclient import TestClient

from main import app
from modulos.delivery.wires import reset_delivery_state


def test_api_assignment_marks_order_and_deliverer():
    reset_delivery_state()
    client = TestClient(app)

    created = client.post(
        '/api/v1/deliverers/', json={'name': 'Ana', 'phone': '11999999999', 'region': 'Zona Sul'})
    assert created.status_code == 201

    assigned = client.post(
        '/api/v1/orders/assign/', json={'order_id': str(uuid4()), 'region': 'Zona Sul'})
    assert assigned.status_code == 200
    assert assigned.json()['status'] in ('ASSIGNED', 'IN_DELIVERY')
    assert assigned.json()['deliverer_id'] == created.json()['id'] or assigned.json()['assigned_deliverer_id'] == created.json()['id']


def test_api_reassignment_uses_other_available_deliverer():
    reset_delivery_state()
    client = TestClient(app)

    first = client.post(
        '/api/v1/deliverers/', json={'name': 'Ana', 'phone': '11999999999', 'region': 'Zona Sul'})
    second = client.post(
        '/api/v1/deliverers/', json={'name': 'Bruno', 'phone': '11988888888', 'region': 'Zona Sul'})
    order_id = str(uuid4())

    assigned = client.post('/api/v1/orders/assign/', json={
                           'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': first.json()['id']})
    assert assigned.status_code == 200

    reassigned = client.post(
        f'/api/v1/orders/{order_id}/reassign/', json={'reason': 'refused'})
    assert reassigned.status_code == 200
    assert reassigned.json()['status'] in ('ASSIGNED', 'IN_DELIVERY')
    assert reassigned.json()['deliverer_id'] == second.json()['id'] or reassigned.json()['assigned_deliverer_id'] == second.json()['id']
