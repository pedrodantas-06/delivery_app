from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from main import app
from modulos.delivery.wires import reset_delivery_state

scenarios('../../.specs/delivers/deliverer-bdd.feature')


@pytest.fixture(autouse=True)
def shared_state():
    state = {}
    pytest.shared = state
    yield state
    pytest.shared = {}


@given(parsers.parse('que existem entregadores cadastrados na região "{region}"'))
def entregadores_existentes(region):
    reset_delivery_state()
    client = TestClient(app)
    client.post('/api/v1/deliverers/', json={'name': 'A', 'phone': '1191', 'region': region})
    client.post('/api/v1/deliverers/', json={'name': 'B', 'phone': '1192', 'region': region})


@when(parsers.parse('eu envio um pedido para criar um entregador com nome "{name}" e telefone "{phone}"'))
def cria_entregador(name, phone):
    client = TestClient(app)
    resp = client.post('/api/v1/deliverers/', json={'name': name, 'phone': phone, 'region': 'Zona Sul'})
    pytest.shared['created'] = resp


@then(parsers.parse('a API responde 201 e retorna o id do entregador'))
def verifica_criacao():
    resp = pytest.shared['created']
    assert resp.status_code == 201
    assert 'id' in resp.json()


@given(parsers.parse('um order criado na região "{region}" com id "{order_id}"'))
def order_pronto(region, order_id):
    pytest.shared['order_id'] = order_id
    pytest.shared['region'] = region


@given(parsers.parse('existem entregadores AVAILABLE na região "{region}"'))
def entregadores_disponiveis(region):
    client = TestClient(app)
    client.post('/api/v1/deliverers/', json={'name': 'Alpha', 'phone': '1191', 'region': region})
    client.post('/api/v1/deliverers/', json={'name': 'Beta', 'phone': '1192', 'region': region})


@when(parsers.parse('o sistema tenta atribuir o delivery para order "{order_id}"'))
def sistema_atribui(order_id):
    client = TestClient(app)
    region = pytest.shared.get('region', 'Zona Sul')
    resp = client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': region})
    pytest.shared['assign'] = resp


@then(parsers.parse('o delivery fica com status ASSIGNED e um deliverer_id é preenchido'))
def verifica_assign():
    resp = pytest.shared['assign']
    assert resp.status_code == 200
    payload = resp.json()
    assert payload['status'] == 'ASSIGNED'
    assert payload['deliverer_id'] is not None or payload['assigned_deliverer_id'] is not None


@given(parsers.parse('um delivery ASSIGNED para order "{order_id}"'))
def delivery_assigned(order_id):
    reset_delivery_state()
    client = TestClient(app)
    created = client.post('/api/v1/deliverers/', json={'name': 'X', 'phone': '119', 'region': 'Zona Sul'})
    deliverer_id = created.json()['id']
    client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': deliverer_id})
    pytest.shared['order_id'] = order_id
    pytest.shared['deliverer_id'] = deliverer_id


@when(parsers.parse('dois entregadores enviam accept simultâneo'))
def two_accept_simultaneous():
    client = TestClient(app)
    order_id = str(uuid4())
    first = client.post('/api/v1/deliverers/', json={'name': 'D1', 'phone': '11', 'region': 'Zona Sul'}).json()['id']
    second = client.post('/api/v1/deliverers/', json={'name': 'D2', 'phone': '12', 'region': 'Zona Sul'}).json()['id']
    client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': first})
    r1 = client.post(f'/api/v1/orders/{order_id}/accept/', json={'deliverer_id': first})
    r2 = client.post(f'/api/v1/orders/{order_id}/accept/', json={'deliverer_id': second})
    pytest.shared['r1'] = r1
    pytest.shared['r2'] = r2


@then(parsers.parse('apenas o primeiro acceptante tem a atribuição confirmada'))
def verifica_race():
    assert pytest.shared['r1'].status_code == 200
    assert pytest.shared['r2'].status_code != 200


@given(parsers.parse('um delivery ASSIGNED com deliverer_id "{did}"'))
def assigned_with_id(did):
    reset_delivery_state()
    client = TestClient(app)
    order_id = str(uuid4())
    deliverer_id = client.post('/api/v1/deliverers/', json={'name': 'Z', 'phone': '1', 'region': 'Zona Sul'}).json()['id']
    client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': deliverer_id})
    pytest.shared['order_id'] = order_id
    pytest.shared['deliverer_id'] = deliverer_id


@when('o entregador faz pickup')
def step_pickup():
    client = TestClient(app)
    order_id = pytest.shared['order_id']
    deliverer_id = pytest.shared['deliverer_id']
    resp = client.patch(f'/api/v1/orders/{order_id}/pickup/', json={'deliverer_id': deliverer_id})
    pytest.shared['pickup'] = resp


@then('delivery.status é PICKED_UP e picked_up_at é registrado')
def verify_pickup():
    resp = pytest.shared['pickup']
    assert resp.status_code == 200
    assert resp.json()['status'] == 'PICKED_UP'


@given('um delivery PICKED_UP com deliverer_id "d-1"')
def picked_up_state():
    reset_delivery_state()
    client = TestClient(app)
    deliverer_id = client.post('/api/v1/deliverers/', json={'name': 'Q', 'phone': '1', 'region': 'Zona Sul'}).json()['id']
    order_id = str(uuid4())
    client.post('/api/v1/orders/assign/', json={'order_id': order_id, 'region': 'Zona Sul', 'deliverer_id': deliverer_id})
    client.patch(f'/api/v1/orders/{order_id}/pickup/', json={'deliverer_id': deliverer_id})
    pytest.shared['order_id'] = order_id
    pytest.shared['deliverer_id'] = deliverer_id


@when('o entregador envia deliver')
def do_deliver():
    client = TestClient(app)
    resp = client.patch(
        f"/api/v1/orders/{pytest.shared['order_id']}/deliver/",
        json={'deliverer_id': pytest.shared['deliverer_id']},
    )
    pytest.shared['deliver'] = resp


@then('delivery.status é DELIVERED e delivered_at é registrado e evento DeliveryCompleted é publicado')
def verify_delivered():
    resp = pytest.shared['deliver']
    assert resp.status_code == 200
    assert resp.json()['status'] == 'DELIVERED'
