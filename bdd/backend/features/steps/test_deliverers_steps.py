from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from main import app
from modulos.delivery.domain.entities import Order
from modulos.delivery.domain.enums import DelivererStatus, OrderStatus
from modulos.delivery.wires import deliverer_service, reset_delivery_state

scenarios('../deliverers/deliverers.feature')


@pytest.fixture(autouse=True)
def reset_state():
    reset_delivery_state()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def context() -> dict:
    return {
        'deliverers_by_name': {},
    }


@given('nenhum entregador existe')
def no_deliverers():
    reset_delivery_state()


@given(parsers.parse('um entregador existente com nome "{name}" e regiao "{region}"'))
def existing_deliverer(client: TestClient, context: dict, name: str, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': name, 'phone': '11999999999', 'region': region},
    )
    assert response.status_code == 201
    payload = response.json()
    context['deliverer'] = payload
    context['deliverers_by_name'][name] = payload


@given('entregadores com status diferentes cadastrados')
def deliverers_with_different_statuses(client: TestClient, context: dict):
    first = client.post(
        '/api/deliverers/',
        json={'name': 'Ana', 'phone': '11111111111', 'region': 'Zona Sul'},
    )
    second = client.post(
        '/api/deliverers/',
        json={'name': 'Bruno', 'phone': '22222222222', 'region': 'Zona Sul'},
    )
    assert first.status_code == 201
    assert second.status_code == 201

    bruno_id = second.json()['id']
    patch_response = client.patch(
        f'/api/deliverers/{bruno_id}/status/',
        json={'status': DelivererStatus.OCCUPIED.value},
    )
    assert patch_response.status_code == 200
    context['deliverers_by_name']['Ana'] = first.json()
    context['deliverers_by_name']['Bruno'] = patch_response.json() | {'name': 'Bruno', 'region': 'Zona Sul'}


@given(parsers.parse('uma ordem pendente na regiao "{region}"'))
def pending_order(context: dict, region: str):
    order = Order(
        id=uuid4(),
        region=region,
        status=OrderStatus.PENDING,
    )
    deliverer_service.order_repo.save(order)
    context['order'] = {'id': str(order.id), 'region': order.region}


@given(parsers.parse('um entregador disponivel na regiao "{region}"'))
def available_deliverer(client: TestClient, context: dict, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': 'Carlos', 'phone': '11988888888', 'region': region},
    )
    assert response.status_code == 201
    payload = response.json()
    context['deliverer'] = payload
    context['deliverers_by_name']['Carlos'] = payload


@given(parsers.parse('um entregador com nome "{name}" disponivel na regiao "{region}"'))
def available_named_deliverer(client: TestClient, context: dict, name: str, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': name, 'phone': '11977777777', 'region': region},
    )
    assert response.status_code == 201
    payload = response.json()
    context['deliverers_by_name'][name] = payload


@given(parsers.parse('nao existe entregador disponivel na regiao "{region}"'))
def no_available_deliverer_in_region(region: str):
    available = [
        deliverer
        for deliverer in list(deliverer_service.deliverer_repo._deliverers.values())
        if deliverer.region == region and deliverer.status == DelivererStatus.AVAILABLE
    ]
    for deliverer in available:
        deliverer_service.deliverer_repo._deliverers.pop(deliverer.id, None)


@given(parsers.parse('um entregador com nome "{name}" ocupado na regiao "{region}"'))
def occupied_named_deliverer(client: TestClient, context: dict, name: str, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': name, 'phone': '11966666666', 'region': region},
    )
    assert response.status_code == 201
    payload = response.json()
    patch_response = client.patch(
        f"/api/deliverers/{payload['id']}/status/",
        json={'status': DelivererStatus.OCCUPIED.value},
    )
    assert patch_response.status_code == 200
    context['deliverers_by_name'][name] = payload


@given(parsers.parse('uma ordem em entrega na regiao "{region}" atribuida ao entregador "{name}"'))
def in_delivery_order(client: TestClient, context: dict, region: str, name: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': name, 'phone': '11955555555', 'region': region},
    )
    assert response.status_code == 201
    deliverer = response.json()
    assign_response = client.post(
        '/api/orders/assign/',
        json={'order_id': str(uuid4()), 'region': region, 'deliverer_id': deliverer['id']},
    )
    assert assign_response.status_code == 200
    order = assign_response.json()
    context['order'] = {
        'id': order['order_id'],
        'region': region,
        'assigned_deliverer_id': order['assigned_deliverer_id'],
    }
    context['deliverers_by_name'][name] = deliverer


@given(parsers.parse('outro entregador disponivel na regiao "{region}"'))
def second_available_deliverer(client: TestClient, context: dict, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': 'Mario', 'phone': '11944444444', 'region': region},
    )
    assert response.status_code == 201
    payload = response.json()
    context['deliverers_by_name']['Mario'] = payload


@when(parsers.parse('o cliente registra um entregador com nome "{name}" telefone "{phone}" regiao "{region}"'))
def register_deliverer(client: TestClient, context: dict, name: str, phone: str, region: str):
    response = client.post(
        '/api/deliverers/',
        json={'name': name, 'phone': phone, 'region': region},
    )
    assert response.status_code == 201
    context['response'] = response.json()


@when(parsers.parse('o entregador for atualizado para status "{status}"'))
def update_deliverer_status(client: TestClient, context: dict, status: str):
    deliverer_id = context['deliverer']['id']
    response = client.patch(
        f'/api/deliverers/{deliverer_id}/status/',
        json={'status': status},
    )
    assert response.status_code == 200
    context['response'] = response.json()


@when(parsers.parse('a listagem de entregadores for solicitada com filtro de status "{status}"'))
def list_deliverers_by_status(client: TestClient, context: dict, status: str):
    response = client.get(f'/api/deliverers/?status={status}')
    assert response.status_code == 200
    context['response'] = response.json()


@when('a atribuicao automatica for solicitada para a ordem')
def assign_order_automatically(client: TestClient, context: dict):
    order = context['order']
    response = client.post(
        '/api/orders/assign/',
        json={'order_id': order['id'], 'region': order['region']},
    )
    context['status_code'] = response.status_code
    context['response'] = response.json()


@when(parsers.parse('a atribuicao manual for solicitada para a ordem com o entregador "{name}"'))
def assign_order_manually(client: TestClient, context: dict, name: str):
    order = context['order']
    deliverer_id = context['deliverers_by_name'][name]['id']
    response = client.post(
        '/api/orders/assign/',
        json={'order_id': order['id'], 'region': order['region'], 'deliverer_id': deliverer_id},
    )
    context['status_code'] = response.status_code
    context['response'] = response.json()


@when(parsers.parse('a reatribuicao for solicitada para a ordem por motivo "{reason}"'))
def reassign_order(client: TestClient, context: dict, reason: str):
    order_id = context['order']['id']
    response = client.post(
        f'/api/orders/{order_id}/reassign/',
        json={'reason': reason},
    )
    assert response.status_code == 200
    context['response'] = response.json()


@then(parsers.parse('o entregador "{name}" deve ser criado com status "{status}" na regiao "{region}"'))
def assert_deliverer_created(context: dict, name: str, status: str, region: str):
    payload = context['response']
    assert payload['name'] == name
    assert payload['status'] == status
    assert payload['region'] == region


@then(parsers.parse('o entregador deve ter status "{status}"'))
def assert_deliverer_status(context: dict, status: str):
    payload = context['response']
    assert payload['status'] == status


@then(parsers.parse('apenas entregadores com status "{status}" devem ser retornados'))
def assert_list_filtered_by_status(context: dict, status: str):
    items = context['response']['items']
    assert len(items) > 0
    assert all(item['status'] == status for item in items)


@then(parsers.parse('a ordem deve ser marcada como "{status}"'))
def assert_order_status(context: dict, status: str):
    payload = context['response']
    assert payload['status'] == status


@then('o entregador deve ser marcado como "OCCUPIED"')
def assert_deliverer_occupied(context: dict):
    payload = context['response']
    deliverer = deliverer_service.deliverer_repo.get_by_id(UUID(payload['assigned_deliverer_id']))
    assert deliverer.status == DelivererStatus.OCCUPIED


@then(parsers.parse('a ordem deve ser atribuida ao entregador "{name}"'))
def assert_order_assigned_to_named_deliverer(context: dict, name: str):
    payload = context['response']
    expected_id = context['deliverers_by_name'][name]['id']
    assert payload['assigned_deliverer_id'] == expected_id


@then(parsers.parse('o sistema deve retornar erro "{message}"'))
def assert_assignment_error(context: dict, message: str):
    assert context['status_code'] == 400
    assert context['response']['detail'] == message


@then('a nova atribuicao deve escolher outro entregador disponivel')
def assert_reassignment_changed_deliverer(context: dict):
    original_id = context['order']['assigned_deliverer_id']
    current_id = context['response']['assigned_deliverer_id']
    assert current_id != original_id


@then('a ordem deve continuar em "IN_DELIVERY"')
def assert_order_stays_in_delivery(context: dict):
    assert context['response']['status'] == OrderStatus.IN_DELIVERY.value
