import json
from uuid import UUID
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from delivery.domain.enums import DelivererStatus
from delivery.wires import deliverer_service


def parse_body(request: HttpRequest) -> dict:
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}


@require_http_methods(['POST'])
def create_deliverer(request: HttpRequest) -> JsonResponse:
    data = parse_body(request)
    name = data.get('name')
    phone = data.get('phone')
    region = data.get('region')
    if not name or not phone or not region:
        return JsonResponse({'error': 'name, phone and region are required'}, status=400)

    deliverer = deliverer_service.register_deliverer(
        name=name, phone=phone, region=region)
    return JsonResponse({
        'id': str(deliverer.id),
        'name': deliverer.name,
        'phone': deliverer.phone,
        'region': deliverer.region,
        'status': deliverer.status.value,
    }, status=201)


@require_http_methods(['PATCH'])
def update_deliverer_status(request: HttpRequest, deliverer_id: UUID) -> JsonResponse:
    data = parse_body(request)
    status_value = data.get('status')
    if not status_value:
        return JsonResponse({'error': 'status is required'}, status=400)

    try:
        status = DelivererStatus(status_value)
        deliverer = deliverer_service.update_status(deliverer_id, status)
        return JsonResponse({
            'id': str(deliverer.id),
            'status': deliverer.status.value,
        })
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)


@require_http_methods(['POST'])
def assign_order(request: HttpRequest) -> JsonResponse:
    data = parse_body(request)
    order_id = data.get('order_id')
    region = data.get('region')
    if not order_id or not region:
        return JsonResponse({'error': 'order_id and region are required'}, status=400)

    try:
        order = deliverer_service.assign_order(UUID(order_id), region)
        return JsonResponse({
            'order_id': str(order.id),
            'status': order.status.value,
            'assigned_deliverer_id': str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None,
        }, status=200)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)


@require_http_methods(['POST'])
def reassign_order(request: HttpRequest, order_id: UUID) -> JsonResponse:
    try:
        order = deliverer_service.reassign_order(order_id)
        return JsonResponse({
            'order_id': str(order.id),
            'status': order.status.value,
            'assigned_deliverer_id': str(order.assigned_deliverer_id) if order.assigned_deliverer_id else None,
        }, status=200)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)
