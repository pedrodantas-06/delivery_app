# import json
# from uuid import uuid4

# import pytest
# from django.test import Client
# from pytest_bdd import given, parsers, scenarios, then, when

# from modulos.delivery.domain.enums import DelivererStatus, OrderStatus
# from modulos.delivery.infrastructure.models.deliverers_model import DelivererModel, OrderModel

# scenarios('../deliverers/deliverers.feature')
# pytestmark = pytest.mark.django_db


# @pytest.fixture
# def context() -> dict:
#     return {
#         'deliverers_by_name': {},
#     }


# @given('nenhum entregador existe')
# def no_deliverers():
#     DelivererModel.objects.all().delete()


# @given(parsers.parse('um entregador existente com nome "{name}" e regiao "{region}"'))
# def existing_deliverer(client: Client, context: dict, name: str, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': name, 'phone': '11999999999', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     payload = response.json()
#     context['deliverer'] = payload
#     context['deliverers_by_name'][name] = payload


# @given('entregadores com status diferentes cadastrados')
# def deliverers_with_different_statuses(client: Client):
#     DelivererModel.objects.all().delete()

#     first = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': 'Ana', 'phone': '11111111111', 'region': 'Zona Sul'}),
#         content_type='application/json',
#     )
#     second = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': 'Bruno', 'phone': '22222222222', 'region': 'Zona Sul'}),
#         content_type='application/json',
#     )
#     assert first.status_code == 201
#     assert second.status_code == 201

#     bruno_id = second.json()['id']
#     DelivererModel.objects.filter(id=bruno_id).update(
#         status=DelivererStatus.OCCUPIED.value)


# @given(parsers.parse('uma ordem pendente na regiao "{region}"'))
# def pending_order(context: dict, region: str):
#     order = OrderModel.objects.create(
#         region=region, status=OrderStatus.PENDING.value)
#     context['order'] = {'id': str(order.id), 'region': order.region}


# @given(parsers.parse('um entregador disponivel na regiao "{region}"'))
# def available_deliverer(client: Client, context: dict, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': 'Carlos', 'phone': '11988888888', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     payload = response.json()
#     context['deliverer'] = payload
#     context['deliverers_by_name']['Carlos'] = payload


# @given(parsers.parse('um entregador com nome "{name}" disponivel na regiao "{region}"'))
# def available_named_deliverer(client: Client, context: dict, name: str, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': name, 'phone': '11977777777', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     payload = response.json()
#     context['deliverers_by_name'][name] = payload


# @given(parsers.parse('nao existe entregador disponivel na regiao "{region}"'))
# def no_available_deliverer_in_region(region: str):
#     DelivererModel.objects.filter(
#         region=region, status=DelivererStatus.AVAILABLE.value).delete()


# @given(parsers.parse('um entregador com nome "{name}" ocupado na regiao "{region}"'))
# def occupied_named_deliverer(client: Client, context: dict, name: str, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': name, 'phone': '11966666666', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     payload = response.json()
#     DelivererModel.objects.filter(id=payload['id']).update(
#         status=DelivererStatus.OCCUPIED.value)
#     context['deliverers_by_name'][name] = payload


# @given(parsers.parse('uma ordem em entrega na regiao "{region}" atribuida ao entregador "{name}"'))
# def in_delivery_order(client: Client, context: dict, region: str, name: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': name, 'phone': '11955555555', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     deliverer = response.json()
#     DelivererModel.objects.filter(id=deliverer['id']).update(
#         status=DelivererStatus.OCCUPIED.value)

#     order = OrderModel.objects.create(
#         id=uuid4(),
#         region=region,
#         status=OrderStatus.IN_DELIVERY.value,
#         assigned_deliverer_id=deliverer['id'],
#     )
#     context['order'] = {
#         'id': str(order.id),
#         'region': order.region,
#         'assigned_deliverer_id': deliverer['id'],
#     }
#     context['deliverers_by_name'][name] = deliverer


# @given(parsers.parse('outro entregador disponivel na regiao "{region}"'))
# def second_available_deliverer(client: Client, context: dict, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps(
#             {'name': 'Mario', 'phone': '11944444444', 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     payload = response.json()
#     context['deliverers_by_name']['Mario'] = payload


# @when(parsers.parse('o cliente registra um entregador com nome "{name}" telefone "{phone}" regiao "{region}"'))
# def register_deliverer(client: Client, context: dict, name: str, phone: str, region: str):
#     response = client.post(
#         '/api/deliverers/',
#         data=json.dumps({'name': name, 'phone': phone, 'region': region}),
#         content_type='application/json',
#     )
#     assert response.status_code == 201
#     context['response'] = response.json()


# @when(parsers.parse('o entregador for atualizado para status "{status}"'))
# def update_deliverer_status(client: Client, context: dict, status: str):
#     deliverer_id = context['deliverer']['id']
#     response = client.patch(
#         f'/api/deliverers/{deliverer_id}/status/',
#         data=json.dumps({'status': status}),
#         content_type='application/json',
#     )
#     assert response.status_code == 200
#     context['response'] = response.json()


# @when(parsers.parse('a listagem de entregadores for solicitada com filtro de status "{status}"'))
# def list_deliverers_by_status(client: Client, context: dict, status: str):
#     response = client.get(f'/api/deliverers/?status={status}')
#     assert response.status_code == 200
#     context['response'] = response.json()


# @when('a atribuicao automatica for solicitada para a ordem')
# def assign_order_automatically(client: Client, context: dict):
#     order = context['order']
#     response = client.post(
#         '/api/orders/assign/',
#         data=json.dumps({'order_id': order['id'], 'region': order['region']}),
#         content_type='application/json',
#     )
#     context['status_code'] = response.status_code
#     context['response'] = response.json()


# @when(parsers.parse('a atribuicao manual for solicitada para a ordem com o entregador "{name}"'))
# def assign_order_manually(client: Client, context: dict, name: str):
#     order = context['order']
#     deliverer_id = context['deliverers_by_name'][name]['id']
#     response = client.post(
#         '/api/orders/assign/',
#         data=json.dumps(
#             {'order_id': order['id'], 'region': order['region'], 'deliverer_id': deliverer_id}),
#         content_type='application/json',
#     )
#     context['status_code'] = response.status_code
#     context['response'] = response.json()


# @when(parsers.parse('a reatribuicao for solicitada para a ordem por motivo "{reason}"'))
# def reassign_order(client: Client, context: dict, reason: str):
#     order_id = context['order']['id']
#     response = client.post(
#         f'/api/orders/{order_id}/reassign/',
#         data=json.dumps({'reason': reason}),
#         content_type='application/json',
#     )
#     assert response.status_code == 200
#     context['response'] = response.json()


# @then(parsers.parse('o entregador "{name}" deve ser criado com status "{status}" na regiao "{region}"'))
# def assert_deliverer_created(context: dict, name: str, status: str, region: str):
#     payload = context['response']
#     assert payload['name'] == name
#     assert payload['status'] == status
#     assert payload['region'] == region


# @then(parsers.parse('o entregador deve ter status "{status}"'))
# def assert_deliverer_status(context: dict, status: str):
#     payload = context['response']
#     assert payload['status'] == status


# @then(parsers.parse('apenas entregadores com status "{status}" devem ser retornados'))
# def assert_list_filtered_by_status(context: dict, status: str):
#     items = context['response']['items']
#     assert len(items) > 0
#     assert all(item['status'] == status for item in items)


# @then(parsers.parse('a ordem deve ser marcada como "{status}"'))
# def assert_order_status(context: dict, status: str):
#     payload = context['response']
#     assert payload['status'] == status


# @then('o entregador deve ser marcado como "OCCUPIED"')
# def assert_deliverer_occupied(context: dict):
#     payload = context['response']
#     deliverer = DelivererModel.objects.get(id=payload['assigned_deliverer_id'])
#     assert deliverer.status == DelivererStatus.OCCUPIED.value


# @then(parsers.parse('a ordem deve ser atribuida ao entregador "{name}"'))
# def assert_order_assigned_to_named_deliverer(context: dict, name: str):
#     payload = context['response']
#     expected_id = context['deliverers_by_name'][name]['id']
#     assert payload['assigned_deliverer_id'] == expected_id


# @then(parsers.parse('o sistema deve retornar erro "{message}"'))
# def assert_assignment_error(context: dict, message: str):
#     assert context['status_code'] == 400
#     assert context['response']['error'] == message


# @then('a nova atribuicao deve escolher outro entregador disponivel')
# def assert_reassignment_changed_deliverer(context: dict):
#     original_id = context['order']['assigned_deliverer_id']
#     current_id = context['response']['assigned_deliverer_id']
#     assert current_id != original_id


# @then('a ordem deve continuar em "IN_DELIVERY"')
# def assert_order_stays_in_delivery(context: dict):
#     assert context['response']['status'] == OrderStatus.IN_DELIVERY.value
