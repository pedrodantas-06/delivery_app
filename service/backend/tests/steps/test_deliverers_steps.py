import json
from uuid import uuid4

import pytest
from django.test import Client
from pytest_bdd import scenarios, given, when, then, parsers

from delivery.domain.enums import DelivererStatus, OrderStatus
from delivery.infrastructure.models import DelivererModel, OrderModel

scenarios('../features/deliverers.feature')


@pytest.fixture
def context() -> dict:
    return {}


@given('nenhum entregador existe')
def no_deliverers():
    DelivererModel.objects.all().delete()


@given(parsers.parse('um entregador existente com nome "{name}" e região "{region}"'))
def existing_deliverer(client: Client, name: str, region: str, context: dict):
    response = client.post(
        '/api/deliverers/',
        data=json.dumps(
            {'name': name, 'phone': '11999999999', 'region': region}),
        content_type='application/json',
    )
    assert response.status_code == 201
    context['deliverer'] = response.json()
    return context


@given(parsers.parse('um entregador disponível na região "{region}"'))
def available_deliverer(client: Client, region: str, context: dict):
    response = client.post(
        '/api/deliverers/',
        data=json.dumps(
            {'name': 'Carlos', 'phone': '11988888888', 'region': region}),
        content_type='application/json',
    )
    assert response.status_code == 201
    context['deliverer'] = response.json()
    return context


@given(parsers.parse('uma ordem pendente na região "{region}"'))
def pending_order(region: str, context: dict):
    order = OrderModel.objects.create(
        region=region, status=OrderStatus.PENDING.value)
    context['order'] = {'id': str(order.id), 'region': order.region}
    return context


@given(parsers.parse('uma ordem em entrega na região "{region}" atribuída ao entregador "{name}"'))
def in_delivery_order(client: Client, region: str, name: str, context: dict):
    response = client.post(
        '/api/deliverers/',
        data=json.dumps(
            {'name': name, 'phone': '11977777777', 'region': region}),
        content_type='application/json',
    )
    assert response.status_code == 201
    deliverer = response.json()
    DelivererModel.objects.filter(id=deliverer['id']).update(
        status=DelivererStatus.OCCUPIED.value)
    order = OrderModel.objects.create(
        id=uuid4(),
        region=region,
        status=OrderStatus.IN_DELIVERY.value,
        assigned_deliverer_id=deliverer['id'],
    )
    context['order'] = {'id': str(
        order.id), 'region': order.region, 'assigned_deliverer_id': deliverer['id']}
    context['deliverer'] = deliverer
    return context


@when(parsers.parse('o cliente registra um entregador com nome "{name}" telefone "{phone}" região "{region}"'))
def register_deliverer(client: Client, name: str, phone: str, region: str, context: dict):
    response = client.post(
        '/api/deliverers/',
        data=json.dumps({'name': name, 'phone': phone, 'region': region}),
        content_type='application/json',
    )
    assert response.status_code == 201
    context['response'] = response.json()
    return context


@when(parsers.parse('o entregador for atualizado para status "{status}"'))
def update_status(client: Client, context: dict, status: str):
    deliverer_id = context['deliverer']['id']
    response = client.patch(
        f'/api/deliverers/{deliverer_id}/status/',
        data=json.dumps({'status': status}),
        content_type='application/json',
    )
    assert response.status_code == 200
    context['response'] = response.json()
    return context


@when('a atribuição automática for solicitada para a ordem')
def assign_order(client: Client, context: dict):
    order = context['order']
    response = client.post(
        '/api/orders/assign/',
        data=json.dumps({'order_id': order['id'], 'region': order['region']}),
        content_type='application/json',
    )
    assert response.status_code == 200
    context['response'] = response.json()
    return context


@when('a reatribuição for solicitada para a ordem')
def reassign_order(client: Client, context: dict):
    order_id = context['order']['id']
    response = client.post(f'/api/orders/{order_id}/reassign/')
    assert response.status_code == 200
    context['response'] = response.json()
    return context


@then(parsers.parse('o entregador "{name}" deve ser criado com status "{status}" na região "{region}"'))
def assert_deliverer_created(context: dict, name: str, status: str, region: str):
    payload = context['response']
    assert payload['name'] == name
    assert payload['status'] == status
    assert payload['region'] == region


@then(parsers.parse('o entregador deve ter status "{status}"'))
def assert_status_updated(context: dict, status: str):
    payload = context['response']
    assert payload['status'] == status


@then(parsers.parse('a ordem deve ser marcada como "{status}"'))
def assert_order_status(context: dict, status: str):
    payload = context['response']
    assert payload['status'] == status


@then('o entregador deve ser marcado como "OCCUPIED"')
def assert_deliverer_occupied(context: dict):
    order = context['response']
    assert order['assigned_deliverer_id'] is not None
    deliverer = DelivererModel.objects.get(id=order['assigned_deliverer_id'])
    assert deliverer.status == DelivererStatus.OCCUPIED.value


@then('a nova atribuição deve escolher outro entregador disponível')
def assert_reassigned_to_other(context: dict):
    original_id = context['order']['assigned_deliverer_id']
    response = context['response']
    assert response['assigned_deliverer_id'] != original_id


@then('a ordem deve continuar em "IN_DELIVERY"')
def assert_order_still_in_delivery(context: dict):
    payload = context['response']
    assert payload['status'] == OrderStatus.IN_DELIVERY.value
